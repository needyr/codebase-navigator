#!/usr/bin/env python3
"""Heuristic scanner utilities for the codebase-navigator skill.

The scanner intentionally uses only the Python standard library. It is not a
compiler or language server; its output is a draft for human confirmation.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

IGNORE_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode", ".agent", "node_modules",
    "target", "build", "dist", "out", ".gradle", ".mvn", "coverage",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".next", ".nuxt",
    "vendor", "tmp", "temp", "logs", ".venv", "venv", "env",
}
SOURCE_EXTS = {".java", ".kt", ".kts", ".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".cs"}
TEXT_EXTS = SOURCE_EXTS | {".xml", ".yml", ".yaml", ".json", ".properties", ".toml", ".gradle", ".md", ".sql"}
LAYER_KEYS = {
    "controller": ["controller", "handler", "resource", "endpoint", "api"],
    "service": ["service", "manager", "facade", "biz"],
    "repository": ["repository", "mapper", "dao", "repo", "store"],
    "model": ["dto", "vo", "entity", "model", "domain", "po", "bo", "request", "response"],
    "client": ["client", "adapter", "gateway", "integration"],
    "converter": ["converter", "assembler", "mapperstruct", "translator"],
    "validator": ["validator", "validation", "checker", "check"],
    "config": ["config", "configuration", "properties"],
    "util": ["util", "utils", "helper", "common", "constant", "constants", "support"],
    "test": ["test", "tests", "spec"],
}
PUBLIC_VISIBILITY = {"public", "export", "func"}
JAVA_ROUTE_ANNOTATIONS = ("GetMapping", "PostMapping", "PutMapping", "DeleteMapping", "PatchMapping", "RequestMapping")
TS_ROUTE_DECORATORS = ("Get", "Post", "Put", "Delete", "Patch", "Controller")
HTTP_BY_ANNOTATION = {
    "GetMapping": "GET", "PostMapping": "POST", "PutMapping": "PUT",
    "DeleteMapping": "DELETE", "PatchMapping": "PATCH",
    "Get": "GET", "Post": "POST", "Put": "PUT", "Delete": "DELETE", "Patch": "PATCH",
}

@dataclass
class ClassInfo:
    name: str
    kind: str
    path: str
    module: str
    layer: str
    line: int

@dataclass
class MethodInfo:
    name: str
    class_name: str
    path: str
    module: str
    layer: str
    line: int
    signature: str
    visibility: str
    language: str
    annotations: List[str]
    category: str

@dataclass
class ApiInfo:
    method: str
    route: str
    handler: str
    path: str
    module: str
    line: int
    evidence: str


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def is_ignored(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def read_text(path: Path, max_bytes: int = 1_500_000) -> str:
    try:
        if path.stat().st_size > max_bytes:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def collect_files(root: Path, exts: Optional[set[str]] = None) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        dirnames[:] = [x for x in dirnames if x not in IGNORE_DIRS]
        if is_ignored(d):
            continue
        for name in filenames:
            p = d / name
            if exts is None or p.suffix in exts or name in {"Dockerfile", "Makefile"}:
                files.append(p)
    return sorted(files)


def detect_build_tools(root: Path) -> List[str]:
    checks = {
        "maven": ["pom.xml"],
        "gradle": ["build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts", "gradlew"],
        "node/npm": ["package.json", "package-lock.json"],
        "pnpm": ["pnpm-lock.yaml"],
        "yarn": ["yarn.lock"],
        "go modules": ["go.mod"],
        "python/pyproject": ["pyproject.toml"],
        "python/requirements": ["requirements.txt"],
        "python/pipenv": ["Pipfile"],
        "dotnet": ["*.csproj", "*.sln"],
        "docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
    }
    found: List[str] = []
    for tool, names in checks.items():
        for pattern in names:
            if "*" in pattern:
                if list(root.rglob(pattern)):
                    found.append(tool); break
            elif (root / pattern).exists():
                found.append(tool); break
    return sorted(set(found))


def grep_project(root: Path, patterns: List[str], max_files: int = 500) -> bool:
    regexes = [re.compile(p) for p in patterns]
    count = 0
    for p in collect_files(root, TEXT_EXTS):
        count += 1
        if count > max_files:
            break
        text = read_text(p, 300_000)
        if any(r.search(text) for r in regexes):
            return True
    return False


def detect_frameworks(root: Path) -> List[str]:
    frameworks = []
    package_json = read_text(root / "package.json") if (root / "package.json").exists() else ""
    pom = "\n".join(read_text(p, 500_000) for p in root.glob("**/pom.xml") if not is_ignored(p))[:2_000_000]
    gradle = "\n".join(read_text(p, 300_000) for p in list(root.glob("**/build.gradle")) + list(root.glob("**/build.gradle.kts")) if not is_ignored(p))[:2_000_000]
    meta = package_json + "\n" + pom + "\n" + gradle
    checks = [
        ("spring boot", [r"spring-boot", r"@SpringBootApplication", r"@RestController"]),
        ("spring cloud", [r"spring-cloud", r"@FeignClient"]),
        ("mybatis", [r"mybatis", r"@Mapper", r"<mapper"]),
        ("jpa/hibernate", [r"spring-boot-starter-data-jpa", r"@Entity", r"JpaRepository"]),
        ("nestjs", [r"@nestjs/", r"@Controller\(", r"@Injectable\("]),
        ("express", [r"express", r"app\.get\(", r"router\.post\("]),
        ("fastapi", [r"fastapi", r"FastAPI\(", r"@router\.(get|post|put|delete|patch)\("]),
        ("flask", [r"flask", r"Flask\(", r"@app\.route\("]),
        ("django", [r"django", r"manage.py", r"django\.conf"]),
        ("gin", [r"github.com/gin-gonic/gin", r"gin\.Default\(", r"\.GET\("]),
        ("grpc", [r"grpc", r"\.proto"]),
    ]
    for name, pats in checks:
        if any(re.search(p, meta, re.I) for p in pats) or grep_project(root, pats, max_files=250):
            frameworks.append(name)
    return sorted(set(frameworks))


def detect_test_tools(root: Path) -> List[str]:
    tools = []
    text = "\n".join(read_text(p, 300_000) for p in collect_files(root, {".xml", ".gradle", ".json", ".toml", ".py", ".ts", ".js"})[:200])
    checks = [
        ("junit", r"junit|org.junit"),
        ("mockito", r"mockito"),
        ("pytest", r"pytest"),
        ("unittest", r"import unittest"),
        ("jest", r"jest"),
        ("vitest", r"vitest"),
        ("go test", r"_test\.go|go test"),
        ("dotnet test", r"xunit|nunit|MSTest"),
    ]
    for name, pat in checks:
        if re.search(pat, text, re.I):
            tools.append(name)
    return sorted(set(tools))


def detect_source_roots(root: Path) -> List[str]:
    candidates = [
        "src/main/java", "src/main/kotlin", "src/main/scala", "src", "app",
        "server", "backend", "internal", "pkg", "cmd", "lib", "services",
    ]
    roots = [c for c in candidates if (root / c).exists()]
    if not roots:
        roots = sorted({rel(p.parent, root).split("/")[0] for p in collect_files(root, SOURCE_EXTS)[:200] if len(rel(p, root).split("/")) > 1})[:10]
    return roots


def classify_layer(path: Path, class_name: str = "") -> str:
    hay = (path.as_posix() + "/" + class_name).lower()
    for layer, keys in LAYER_KEYS.items():
        if any(k in hay for k in keys):
            return layer
    return "unknown"


def infer_module(path: Path, root: Path, layer: str = "unknown") -> str:
    parts = list(Path(rel(path, root)).parts)
    # Strip common source roots.
    strips = [
        ["src", "main", "java"], ["src", "main", "kotlin"], ["src", "test", "java"],
        ["src", "test", "kotlin"], ["src"], ["app"], ["server"], ["backend"],
        ["internal"], ["pkg"], ["cmd"], ["lib"], ["services"],
    ]
    for s in strips:
        if parts[:len(s)] == s:
            parts = parts[len(s):]
            break
    # Remove filename.
    if parts:
        parts = parts[:-1]
    layer_words = {x for values in LAYER_KEYS.values() for x in values}
    if layer == "util" and "common" in [x.lower() for x in parts]:
        return "common"
    candidates = [p for p in parts if p.lower() not in layer_words and not re.fullmatch(r"com|org|net|io|cn|java|main|test", p.lower())]
    if not candidates:
        return "root"
    # Prefer directory immediately before layer marker, otherwise last meaningful segment.
    for i, p in enumerate(parts):
        if p.lower() in layer_words and i > 0:
            prev = parts[i-1]
            if prev.lower() not in {"com", "org", "net", "io", "cn"}:
                return prev
    return candidates[-1]


def language_for(path: Path) -> str:
    return {
        ".java": "java", ".kt": "kotlin", ".kts": "kotlin", ".ts": "typescript",
        ".tsx": "typescript", ".js": "javascript", ".jsx": "javascript",
        ".py": "python", ".go": "go", ".cs": "csharp",
    }.get(path.suffix, "unknown")


def clean_route_arg(arg: str) -> str:
    m = re.search(r'"([^"]*)"|\'([^\']*)\'', arg)
    if m:
        return (m.group(1) or m.group(2) or "").strip()
    value_match = re.search(r"(?:value|path)\s*=\s*\{?\s*\"([^\"]*)\"", arg)
    if value_match:
        return value_match.group(1).strip()
    return ""


def method_category(visibility: str, layer: str, name: str, path: Path) -> str:
    lname = name.lower()
    p = path.as_posix().lower()
    if visibility in {"private", "protected"} or lname.startswith("_"):
        return "internal"
    if layer in {"controller", "service", "repository", "client", "converter", "validator", "util"}:
        return "public-core"
    if any(k in p for k in ["common", "util", "helper", "shared", "support"]):
        return "public-core"
    return "internal" if visibility in {"", "package"} else "public-core"


def extract_from_file(path: Path, root: Path) -> Tuple[List[ClassInfo], List[MethodInfo], List[ApiInfo]]:
    text = read_text(path)
    if not text:
        return [], [], []
    lang = language_for(path)
    lines = text.splitlines()
    classes: List[ClassInfo] = []
    methods: List[MethodInfo] = []
    apis: List[ApiInfo] = []
    relpath = rel(path, root)
    current_class = path.stem
    class_line = 1
    class_patterns = [
        re.compile(r"\b(class|interface|enum|record)\s+([A-Za-z_][A-Za-z0-9_]*)"),
        re.compile(r"\btype\s+([A-Za-z_][A-Za-z0-9_]*)\s+(struct|interface)\b"),
    ]
    for i, line in enumerate(lines, start=1):
        for pat in class_patterns:
            m = pat.search(line)
            if m:
                if pat.pattern.startswith("\\btype"):
                    name, kind = m.group(1), m.group(2)
                else:
                    kind, name = m.group(1), m.group(2)
                layer = classify_layer(path, name)
                module = infer_module(path, root, layer)
                classes.append(ClassInfo(name=name, kind=kind, path=relpath, module=module, layer=layer, line=i))
                current_class = name
                class_line = i
                break
    if not classes:
        layer = classify_layer(path, current_class)
        classes.append(ClassInfo(name=current_class, kind="file", path=relpath, module=infer_module(path, root, layer), layer=layer, line=1))
    base_routes: List[str] = []
    pending_annotations: List[Tuple[int, str]] = []
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        # Track route annotations/decorators.
        if stripped.startswith("@"):
            pending_annotations.append((i, stripped))
            if "@RequestMapping" in stripped or "@Controller" in stripped:
                route = clean_route_arg(stripped)
                if route:
                    base_routes.append(route)
            continue
        if re.search(r"\b(class|interface|enum|record)\s+[A-Za-z_]", stripped) or re.search(r"\btype\s+[A-Za-z_][A-Za-z0-9_]*\s+(struct|interface)\b", stripped):
            pending_annotations = []
        # Python decorators.
        if re.match(r"@(app|router)\.(get|post|put|delete|patch)\(", stripped):
            pending_annotations.append((i, stripped))
            continue
        method_match = None
        visibility = ""
        name = ""
        signature = stripped
        if lang in {"java", "kotlin", "csharp"}:
            if lang == "kotlin":
                method_match = re.search(r"\bfun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", stripped)
                visibility = "public" if not stripped.startswith("private") else "private"
                if method_match: name = method_match.group(1)
            else:
                method_match = re.search(r"\b(public|private|protected)?\s*(?:static\s+)?(?:final\s+)?[A-Za-z0-9_<>,?\[\]\s]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^;{}]*)\)\s*(?:\{|;)?", stripped)
                if method_match:
                    visibility = method_match.group(1) or "package"
                    name = method_match.group(2)
        elif lang in {"typescript", "javascript"}:
            method_match = re.search(r"\b(?:export\s+)?(?:async\s+)?(?:function\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", stripped)
            if method_match and not re.match(r"(if|for|while|switch|catch)\b", stripped):
                name = method_match.group(1)
                visibility = "export" if "export" in stripped or any("@" in a for _, a in pending_annotations) else "package"
        elif lang == "python":
            method_match = re.search(r"\bdef\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", stripped)
            if method_match:
                name = method_match.group(1)
                visibility = "private" if name.startswith("_") else "public"
        elif lang == "go":
            method_match = re.search(r"\bfunc\s+(?:\([^)]*\)\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", stripped)
            if method_match:
                name = method_match.group(1)
                visibility = "public" if name[:1].isupper() else "package"
        if method_match and name not in {"if", "for", "while", "switch", "catch", "return", "new"}:
            cls = current_class
            # Pick most recent class above the method.
            prior = [c for c in classes if c.line <= i]
            if prior:
                cls = prior[-1].name
            layer = classify_layer(path, cls)
            module = infer_module(path, root, layer)
            annotations = [a for _, a in pending_annotations[-8:]]
            cat = method_category(visibility, layer, name, path)
            methods.append(MethodInfo(
                name=name, class_name=cls, path=relpath, module=module, layer=layer,
                line=i, signature=signature[:240], visibility=visibility, language=lang,
                annotations=annotations, category=cat,
            ))
            route_annotations = annotations
            for ann in route_annotations:
                route = ""
                http = ""
                if lang in {"java", "kotlin", "csharp"}:
                    for ann_name in JAVA_ROUTE_ANNOTATIONS:
                        if f"@{ann_name}" in ann:
                            http = HTTP_BY_ANNOTATION.get(ann_name, "ANY")
                            if ann_name == "RequestMapping":
                                mm = re.search(r"method\s*=\s*RequestMethod\.([A-Z]+)", ann)
                                if mm: http = mm.group(1)
                            route = clean_route_arg(ann)
                            break
                elif lang in {"typescript", "javascript"}:
                    for dec in TS_ROUTE_DECORATORS:
                        if re.search(rf"@{dec}\(", ann):
                            if dec == "Controller":
                                continue
                            http = HTTP_BY_ANNOTATION.get(dec, "ANY")
                            route = clean_route_arg(ann)
                            break
                elif lang == "python":
                    m = re.match(r"@(app|router)\.(get|post|put|delete|patch)\((.*)\)", ann)
                    if m:
                        http = m.group(2).upper()
                        route = clean_route_arg(m.group(3))
                if route or http:
                    base = base_routes[-1] if base_routes else ""
                    full = normalize_route(base, route)
                    apis.append(ApiInfo(method=http or "ANY", route=full, handler=f"{cls}.{name}", path=relpath, module=module, line=i, evidence=ann))
            pending_annotations = []
        elif stripped and not stripped.startswith("@") and not stripped.startswith("//") and not stripped.startswith("#"):
            # Keep annotations only if the next meaningful line is a declaration.
            if len(pending_annotations) > 12:
                pending_annotations = []
        # Gin/Express-style inline routes.
        for rm in re.finditer(r"\b(?:app|router|r|engine)\.(GET|POST|PUT|DELETE|PATCH|get|post|put|delete|patch)\s*\(\s*['\"]([^'\"]+)", stripped):
            layer = classify_layer(path, current_class)
            module = infer_module(path, root, layer)
            apis.append(ApiInfo(method=rm.group(1).upper(), route=rm.group(2), handler=current_class, path=relpath, module=module, line=i, evidence=stripped[:200]))
    return classes, methods, apis


def normalize_route(base: str, route: str) -> str:
    if not base and not route:
        return "unknown"
    b = (base or "").strip("/")
    r = (route or "").strip("/")
    if not b: return "/" + r if r else "/"
    if not r: return "/" + b
    return "/" + b + "/" + r


def scan(root: Path) -> Dict[str, object]:
    root = root.resolve()
    files = collect_files(root, SOURCE_EXTS)
    classes: List[ClassInfo] = []
    methods: List[MethodInfo] = []
    apis: List[ApiInfo] = []
    for p in files:
        c, m, a = extract_from_file(p, root)
        classes.extend(c); methods.extend(m); apis.extend(a)
    profile = detect_project(root)
    return {
        "root": str(root),
        "scanned_at": utc_now(),
        "profile": profile,
        "files": [rel(p, root) for p in files],
        "classes": [asdict(x) for x in classes],
        "methods": [asdict(x) for x in methods],
        "apis": [asdict(x) for x in apis],
    }


def detect_project(root: Path) -> Dict[str, object]:
    source_files = collect_files(root, SOURCE_EXTS)
    ext_counts = Counter(p.suffix for p in source_files)
    languages = []
    for ext, lang in [(".java", "java"), (".kt", "kotlin"), (".ts", "typescript"), (".js", "javascript"), (".py", "python"), (".go", "go"), (".cs", "csharp")]:
        if ext_counts.get(ext, 0):
            languages.append(lang)
    return {
        "project_root": str(root.resolve()),
        "scanned_at": utc_now(),
        "build_tools": detect_build_tools(root),
        "frameworks": detect_frameworks(root),
        "test_tools": detect_test_tools(root),
        "languages": languages,
        "source_roots": detect_source_roots(root),
        "source_file_count": len(source_files),
        "source_extension_counts": dict(ext_counts),
    }


def md_table(headers: List[str], rows: Iterable[List[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(x).replace("\n", " ").replace("|", "\\|") for x in row) + " |")
    return "\n".join(out) + "\n"


def render_project_profile(data: Dict[str, object]) -> str:
    p = data["profile"]
    return f"""# Project Profile Draft

## Confirmation Status
- Status: draft
- Generated at: {data['scanned_at']}
- Project root: `{data['root']}`

## Inferred Technology Stack
- Languages: {', '.join(p.get('languages') or ['unknown'])}
- Frameworks: {', '.join(p.get('frameworks') or ['unknown'])}
- Build tools: {', '.join(p.get('build_tools') or ['unknown'])}
- Test tools: {', '.join(p.get('test_tools') or ['unknown'])}
- Source roots: {', '.join(p.get('source_roots') or ['unknown'])}
- Source files scanned: {p.get('source_file_count')}

## Architecture and Layering
This section is a draft inferred from paths, class names, and annotations. Confirm before treating it as project truth.

## Directory Conventions
See `module-index.md` and `class-interface-index.md` drafts for inferred structure.

## API Conventions
See `api-index.md` draft.

## Data Access Conventions
See repository/mapper entries in `class-interface-index.md` and `method-index-public.md`.

## Reusable Method Placement Rules
See `reusable-method-index.md` draft. Confirm whether shared logic should live in module-specific helpers or shared common utilities.

## Open Questions
- Are the inferred frameworks and build/test tools correct?
- Are the inferred layers aligned with the team's intended architecture?
- Which modules should be treated as stable or high-risk?
- Which directories are the preferred home for reusable methods?
"""


def render_module_index(data: Dict[str, object]) -> str:
    modules = defaultdict(lambda: {"files": set(), "layers": Counter(), "classes": 0, "methods": 0, "apis": 0})
    for c in data["classes"]:
        m = modules[c["module"]]; m["files"].add(c["path"]); m["layers"][c["layer"]] += 1; m["classes"] += 1
    for meth in data["methods"]:
        modules[meth["module"]]["methods"] += 1
    for api in data["apis"]:
        modules[api["module"]]["apis"] += 1
    rows = []
    for name, info in sorted(modules.items()):
        sample_paths = ", ".join(sorted(info["files"]))[:160]
        layers = ", ".join(f"{k}:{v}" for k, v in info["layers"].most_common())
        rows.append([name, sample_paths, layers, str(info["classes"]), str(info["methods"]), str(info["apis"]), "draft"])
    return "# Module Index Draft\n\n" + md_table(["Module", "Sample paths", "Layers", "Classes", "Methods", "APIs", "Status"], rows)


def render_class_index(data: Dict[str, object]) -> str:
    rows = [[c["name"], c["kind"], c["path"], c["module"], c["layer"], str(c["line"]), "draft"] for c in data["classes"]]
    return "# Class and Interface Index Draft\n\n" + md_table(["Name", "Kind", "Path", "Module", "Layer", "Line", "Status"], rows)


def render_method_index(data: Dict[str, object], category: str) -> str:
    if category == "public":
        selected = [m for m in data["methods"] if m["category"] == "public-core"]
        title = "# Public and Core Method Index Draft"
    else:
        selected = [m for m in data["methods"] if m["category"] != "public-core"]
        title = "# Internal Method Index Draft"
    rows = [[f"{m['class_name']}.{m['name']}", m["path"], m["module"], m["layer"], m["visibility"], str(m["line"]), m["signature"], "draft"] for m in selected]
    return title + "\n\n" + md_table(["Method", "Path", "Module", "Layer", "Visibility", "Line", "Signature", "Status"], rows)


def render_api_index(data: Dict[str, object]) -> str:
    rows = [[a["method"], a["route"], a["handler"], a["path"], a["module"], str(a["line"]), a["evidence"], "draft"] for a in data["apis"]]
    return "# API Index Draft\n\n" + md_table(["HTTP", "Route", "Handler", "Path", "Module", "Line", "Evidence", "Status"], rows)


def render_reusable_index(data: Dict[str, object]) -> str:
    reusable_layers = {"service", "repository", "client", "converter", "validator", "util"}
    selected = [m for m in data["methods"] if m["layer"] in reusable_layers or any(x in m["path"].lower() for x in ["common", "util", "helper", "shared", "support"])]
    rows = [[f"{m['class_name']}.{m['name']}", m["path"], m["module"], m["layer"], m["signature"], "confirm recommended reuse before using", "draft"] for m in selected]
    return "# Reusable Method Index Draft\n\n" + md_table(["Method", "Path", "Module", "Layer", "Signature", "Reuse note", "Status"], rows)


def render_dependency_index(data: Dict[str, object], root: Path) -> str:
    source_files = [Path(root) / f for f in data["files"]]
    interesting = [m for m in data["methods"] if m["category"] == "public-core"][:300]
    rows = []
    # Simple reference count only; impact_scan.py provides detailed context.
    texts: List[Tuple[str, str]] = []
    for p in source_files[:2000]:
        texts.append((rel(p, root), read_text(p, 400_000)))
    for m in interesting:
        name = m["name"]
        refs = []
        pattern = re.compile(rf"\b{re.escape(name)}\s*\(")
        for path_str, text in texts:
            if path_str == m["path"]:
                continue
            if pattern.search(text):
                refs.append(path_str)
            if len(refs) >= 8:
                break
        rows.append([f"{m['class_name']}.{name}", m["path"], ", ".join(refs) if refs else "not found by heuristic", "draft"])
    return "# Dependency Index Draft\n\n" + md_table(["Symbol", "Defined in", "Reference samples", "Status"], rows)


def render_task_playbooks() -> str:
    return """# Task Playbooks

Status: draft

## New API
1. Locate module.
2. Find similar APIs.
3. Find reusable methods.
4. Analyze impact.
5. Ask confirmation questions.
6. After answers, output adjustment plan.
7. After plan confirmation, execute changes, tests, and docs.

## Change Existing API
1. Locate existing API.
2. Trace controller/service/repository chain.
3. Analyze compatibility.
4. Find reusable methods.
5. Ask confirmation questions.
6. Produce plan only after answers.

## Explain Module
1. Use module index.
2. Use class/interface index.
3. Use method index only when method-level detail is requested.

## Refactor Duplicated Logic
1. Locate duplicates.
2. Search reusable methods.
3. Analyze call sites.
4. Ask confirmation questions before plan.

## Debugging
1. Extract symbols and keywords.
2. Locate modules/classes/methods.
3. Trace dependencies.
4. If fixing code, ask confirmation questions before plan.

## Code Review
1. Check reuse.
2. Check layering.
3. Check impact.
4. Check tests/docs.
5. Check exceptions/logging/permissions/compatibility.
"""


def render_confirmation_rules() -> str:
    return """# Confirmation Rules

Status: draft

Use this heading before adjustment plans:

```text
下面是需要确认的问题，在完成这些问题之后，我会为你输出调整方案：
```

Use this heading before project knowledge updates:

```text
下面是需要确认的问题，在完成这些问题之后，我会更新项目认知文档：
```

## New API Must Confirm
- Business semantics.
- Data scope.
- Permission boundary.
- Request parameters.
- Response shape.
- Pagination and sorting.
- Error handling.
- DTO/VO reuse.
- Tests and API docs.

## Change Existing API Must Confirm
- Whether behavior may change.
- Compatibility with old clients.
- Request and response changes.
- Caller impact.
- Whether old fields or old behavior must remain.
- Tests.

## Refactor Must Confirm
- Whether behavior may change.
- Where shared logic should live.
- Whether old methods must remain.
- Regression test scope.

## Debug Fix Must Confirm
- Whether to only diagnose or also change code.
- Whether risky fixes need fallback or feature flags.

## Direct Execution Exception
Only skip confirmation when the user explicitly says to execute directly or not wait for confirmation.
"""


def write_drafts(root: Path, data: Dict[str, object], mode: str, module: Optional[str] = None) -> Path:
    draft_root = root / ".agent" / "codebase-navigator" / "_drafts" / "latest"
    if draft_root.exists():
        shutil.rmtree(draft_root)
    draft_root.mkdir(parents=True, exist_ok=True)
    outputs = {
        "project-profile.md": render_project_profile(data),
        "module-index.md": render_module_index(data),
        "class-interface-index.md": render_class_index(data),
        "method-index-public.md": render_method_index(data, "public"),
        "method-index-internal.md": render_method_index(data, "internal"),
        "api-index.md": render_api_index(data),
        "reusable-method-index.md": render_reusable_index(data),
        "dependency-index.md": render_dependency_index(data, root),
        "task-playbooks.md": render_task_playbooks(),
        "confirmation-rules.md": render_confirmation_rules(),
        "scan-data.json": json.dumps(data, ensure_ascii=False, indent=2),
    }
    for name, content in outputs.items():
        (draft_root / name).write_text(content, encoding="utf-8")
    summary = {
        "generated_at": utc_now(), "mode": mode, "module": module, "draft_root": str(draft_root),
        "counts": {"classes": len(data["classes"]), "methods": len(data["methods"]), "apis": len(data["apis"]), "files": len(data["files"])}
    }
    (draft_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (draft_root / "README.md").write_text(render_draft_readme(summary), encoding="utf-8")
    return draft_root


def render_draft_readme(summary: Dict[str, object]) -> str:
    c = summary["counts"]
    return f"""# Codebase Navigator Drafts

Generated at: {summary['generated_at']}
Mode: {summary['mode']}
Module filter: {summary.get('module') or 'none'}

## Counts
- Files: {c['files']}
- Classes/interfaces: {c['classes']}
- Methods/functions: {c['methods']}
- APIs: {c['apis']}

These files are drafts. Review them with the user before promoting them into official project knowledge.
"""
