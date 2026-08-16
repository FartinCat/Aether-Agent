#!/usr/bin/env python3
"""
scan_routes.py — Lightweight, zero-dependency route & endpoint crawler.
Self-contained helper for the A05-route-scanner skill.
Discovers file-based routes (Next.js, SvelteKit, Remix) and code-based routes
(Express, FastAPI, Flask, Django, Gin, React Router) in <100ms.
"""

import os
import sys
import re
import json
from pathlib import Path

IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "target", "dist", "build", ".next", ".turbo", ".idea", ".vscode"
}

# Regex patterns for code-based routing
CODE_ROUTE_PATTERNS = [
    # Express / Node: app.get('/api/users', ...), router.post(...)
    (re.compile(r'''(?:\bapp|\brouter|\bserver)\.(get|post|put|delete|patch|all)\s*\(\s*['"]([^'"]+)['"]''', re.IGNORECASE), "Express/Node"),
    
    # FastAPI / Flask: @app.get("/items"), @router.post("/auth")
    (re.compile(r'''@(?:app|router|bp|api)\.(get|post|put|delete|patch|route)\s*\(\s*['"]([^'"]+)['"]''', re.IGNORECASE), "FastAPI/Flask"),
    
    # Django: path('api/users/', ...), re_path(...)
    (re.compile(r'''\b(?:path|re_path)\s*\(\s*['"]([^'"]+)['"]'''), "Django"),
    
    # React Router: <Route path="/dashboard" ... />
    (re.compile(r'''<Route\s+[^>]*\bpath=['"]([^'"]+)['"]'''), "React Router"),
    
    # Vue Router / Route definitions: path: '/settings'
    (re.compile(r'''\bpath\s*:\s*['"](/[^'"]*)['"]'''), "Route Config")
]

def scan_file_based_routes(root_path):
    """Scan Next.js, SvelteKit, and Remix file-based routing structures."""
    routes = []
    root = Path(root_path).resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")

        for f in filenames:
            rel_file = os.path.join(rel_dir, f).replace("\\", "/")
            if rel_file.startswith("./"):
                rel_file = rel_file[2:]

            # Next.js App Router (app/**/page.tsx or app/**/route.ts)
            if "/app/" in f"/{rel_file}" or rel_file.startswith("app/"):
                # Clean prefix to find route path
                idx = rel_file.find("app/")
                subpath = rel_file[idx + 4:]
                
                if f.startswith("page."):
                    route_path = os.path.dirname(subpath)
                    route_path = "/" + route_path if route_path else "/"
                    # Strip Next.js route groups: (group) -> ignored
                    clean_path = re.sub(r'/\([^)]+\)', '', route_path) or "/"
                    clean_path = re.sub(r'/+', '/', clean_path)
                    routes.append({
                        "type": "UI Page",
                        "route": clean_path,
                        "method": "GET",
                        "framework": "Next.js App Router",
                        "file": rel_file,
                        "line": 1
                    })
                elif f.startswith("route."):
                    route_path = "/" + os.path.dirname(subpath)
                    clean_path = re.sub(r'/\([^)]+\)', '', route_path) or "/"
                    clean_path = re.sub(r'/+', '/', clean_path)
                    routes.append({
                        "type": "API Route",
                        "route": clean_path,
                        "method": "ANY",
                        "framework": "Next.js Route Handler",
                        "file": rel_file,
                        "line": 1
                    })

            # Next.js Pages Router (pages/**/*.tsx or pages/api/**/*.ts)
            elif "/pages/" in f"/{rel_file}" or rel_file.startswith("pages/"):
                idx = rel_file.find("pages/")
                subpath = rel_file[idx + 6:]
                name, _ = os.path.splitext(subpath)
                
                # Exclude internal pages (_app, _document, _error)
                if not any(f.startswith(x) for x in ["_app", "_document", "_error"]):
                    if name.endswith("/index") or name == "index":
                        route_path = "/" + name[:-6] if name.endswith("/index") else "/"
                    else:
                        route_path = "/" + name
                    
                    is_api = route_path.startswith("/api/") or route_path == "/api"
                    routes.append({
                        "type": "API Route" if is_api else "UI Page",
                        "route": route_path,
                        "method": "ANY" if is_api else "GET",
                        "framework": "Next.js Pages Router",
                        "file": rel_file,
                        "line": 1
                    })

            # SvelteKit (+page.svelte or +server.ts)
            elif f.startswith("+page."):
                subpath = rel_dir.split("routes/")[-1] if "routes/" in rel_dir else rel_dir
                route_path = "/" + subpath if subpath != rel_dir else "/"
                routes.append({
                    "type": "UI Page",
                    "route": route_path,
                    "method": "GET",
                    "framework": "SvelteKit",
                    "file": rel_file,
                    "line": 1
                })
            elif f.startswith("+server."):
                subpath = rel_dir.split("routes/")[-1] if "routes/" in rel_dir else rel_dir
                route_path = "/" + subpath if subpath != rel_dir else "/"
                routes.append({
                    "type": "API Route",
                    "route": route_path,
                    "method": "ANY",
                    "framework": "SvelteKit Server",
                    "file": rel_file,
                    "line": 1
                })

    return routes

def scan_code_based_routes(root_path):
    """Scan regex patterns for Express, FastAPI, Django, and React Router."""
    routes = []
    root = Path(root_path).resolve()
    scannable_exts = {".ts", ".tsx", ".js", ".jsx", ".py", ".go"}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in scannable_exts:
                full_path = os.path.join(dirpath, f)
                rel_file = os.path.relpath(full_path, root).replace("\\", "/")

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                        for line_no, line in enumerate(file, start=1):
                            line_str = line.strip()
                            if not line_str or line_str.startswith("//") or line_str.startswith("#"):
                                continue

                            for pattern, framework in CODE_ROUTE_PATTERNS:
                                match = pattern.search(line_str)
                                if match:
                                    groups = match.groups()
                                    if len(groups) == 2:
                                        method, route = groups
                                        method = method.upper()
                                    else:
                                        method = "GET"
                                        route = groups[0]

                                    if not route.startswith("/"):
                                        route = "/" + route

                                    is_api = "/api" in route or method in {"POST", "PUT", "DELETE", "PATCH"}
                                    routes.append({
                                        "type": "API Route" if is_api else "UI Page",
                                        "route": route,
                                        "method": method,
                                        "framework": framework,
                                        "file": rel_file,
                                        "line": line_no
                                    })
                except Exception:
                    continue

    return routes

def scan_routes(target_dir="."):
    root = Path(target_dir).resolve()
    if not root.is_dir():
        print(json.dumps({"error": f"Invalid directory: {target_dir}"}))
        return

    file_routes = scan_file_based_routes(root)
    code_routes = scan_code_based_routes(root)
    all_routes = file_routes + code_routes

    # Deduplicate by (route, method, file)
    seen = set()
    unique_routes = []
    for r in all_routes:
        key = (r["route"], r["method"], r["file"])
        if key not in seen:
            seen.add(key)
            unique_routes.append(r)

    # Sort routes by route path
    unique_routes.sort(key=lambda x: (x["type"] != "UI Page", x["route"]))

    ui_pages = [r for r in unique_routes if r["type"] == "UI Page"]
    api_routes = [r for r in unique_routes if r["type"] == "API Route"]

    result = {
        "root": str(root.name),
        "total_routes_detected": len(unique_routes),
        "ui_pages_count": len(ui_pages),
        "api_routes_count": len(api_routes),
        "ui_pages": ui_pages,
        "api_routes": api_routes
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_routes(target)
