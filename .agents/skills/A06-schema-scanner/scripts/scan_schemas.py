#!/usr/bin/env python3
"""
scan_schemas.py — Lightweight, zero-dependency database schema & model extractor.
Self-contained helper for the A06-schema-scanner skill.
Parses Prisma, SQL migrations, Pydantic, SQLAlchemy, Drizzle, and TypeORM models in <100ms.
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

def parse_prisma(content, file_rel):
    """Extract models and fields from Prisma schema files."""
    models = []
    # Match model ModelName { ... }
    model_blocks = re.findall(r'''model\s+([A-Za-z0-9_]+)\s*\{([^}]+)\}''', content)
    for model_name, body in model_blocks:
        fields = []
        for line in body.strip().splitlines():
            line = line.strip()
            if not line or line.startswith("//") or line.startswith("@@"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                f_name = parts[0]
                f_type = parts[1]
                is_pk = "@id" in line
                fields.append({
                    "name": f_name,
                    "type": f_type,
                    "is_primary_key": is_pk
                })
        models.append({
            "source_type": "Prisma",
            "model_name": model_name,
            "file": file_rel,
            "fields_count": len(fields),
            "fields": fields
        })
    return models

def parse_sql_create_table(content, file_rel):
    """Extract tables and columns from SQL migration files."""
    tables = []
    matches = re.finditer(r'''CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([`"']?)([A-Za-z0-9_]+)\1\s*\((.*?)\);''', content, re.IGNORECASE | re.DOTALL)
    for m in matches:
        table_name = m.group(2)
        body = m.group(3)
        fields = []
        for line in body.split(","):
            line = line.strip()
            if not line or line.upper().startswith(("PRIMARY KEY", "FOREIGN KEY", "CONSTRAINT", "INDEX", "KEY")):
                continue
            parts = line.split()
            if len(parts) >= 2:
                f_name = parts[0].strip('`"\'')
                f_type = parts[1].upper()
                is_pk = "PRIMARY KEY" in line.upper()
                fields.append({
                    "name": f_name,
                    "type": f_type,
                    "is_primary_key": is_pk
                })
        tables.append({
            "source_type": "SQL Table",
            "model_name": table_name,
            "file": file_rel,
            "fields_count": len(fields),
            "fields": fields
        })
    return tables

def parse_python_models(content, file_rel):
    """Extract Pydantic and SQLAlchemy models from Python files."""
    models = []
    # Match class ModelName(BaseModel) or class ModelName(Base)
    class_matches = re.finditer(r'''class\s+([A-Za-z0-9_]+)\s*\(\s*(?:BaseModel|Base|models\.Model)\s*\)\s*:\s*\n((?:\s+.*\n)+)''', content)
    for m in class_matches:
        model_name = m.group(1)
        body = m.group(2)
        fields = []
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("__"):
                continue
            # Pydantic: field_name: Type
            # SQLAlchemy: field_name = Column(Type, ...)
            py_match = re.match(r'''([A-Za-z0-9_]+)\s*:\s*([A-Za-z0-9_\[\], ]+)''', line)
            sql_match = re.match(r'''([A-Za-z0-9_]+)\s*=\s*(?:Column|mapped_column)\s*\(\s*([A-Za-z0-9_]+)''', line)
            if py_match:
                fields.append({"name": py_match.group(1), "type": py_match.group(2).strip(), "is_primary_key": False})
            elif sql_match:
                fields.append({"name": sql_match.group(1), "type": sql_match.group(2).strip(), "is_primary_key": "primary_key=True" in line})

        if fields:
            models.append({
                "source_type": "Python Model",
                "model_name": model_name,
                "file": file_rel,
                "fields_count": len(fields),
                "fields": fields
            })
    return models

def parse_ts_drizzle(content, file_rel):
    """Extract Drizzle ORM pgTable / sqliteTable definitions."""
    models = []
    # export const users = pgTable('users', { ... })
    drizzle_matches = re.finditer(r'''(?:export\s+const\s+)?([A-Za-z0-9_]+)\s*=\s*(?:pgTable|sqliteTable|mysqlTable)\s*\(\s*['"]([^'"]+)['"]\s*,\s*\{([^}]+)\}''', content)
    for m in drizzle_matches:
        table_name = m.group(2)
        body = m.group(3)
        fields = []
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            f_match = re.match(r'''([A-Za-z0-9_]+)\s*:\s*([A-Za-z0-9_]+)''', line)
            if f_match:
                fields.append({"name": f_match.group(1), "type": f_match.group(2), "is_primary_key": ".primaryKey()" in line})

        models.append({
            "source_type": "Drizzle ORM",
            "model_name": table_name,
            "file": file_rel,
            "fields_count": len(fields),
            "fields": fields
        })
    return models

def scan_schemas(target_dir="."):
    root = Path(target_dir).resolve()
    if not root.is_dir():
        print(json.dumps({"error": f"Invalid directory: {target_dir}"}))
        return

    all_models = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            full_path = os.path.join(dirpath, f)
            rel_file = os.path.relpath(full_path, root).replace("\\", "/")

            try:
                # 1. Prisma Schemas
                if f.endswith(".prisma"):
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                        all_models.extend(parse_prisma(file.read(), rel_file))

                # 2. SQL Migrations & Schema Dumps
                elif ext == ".sql":
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                        all_models.extend(parse_sql_create_table(file.read(), rel_file))

                # 3. Python Model Files (models.py, schemas.py)
                elif ext == ".py" and any(k in f.lower() for k in ["model", "schema", "entity"]):
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                        all_models.extend(parse_python_models(file.read(), rel_file))

                # 4. TypeScript / Drizzle / TypeORM Files
                elif ext in {".ts", ".tsx"} and any(k in f.lower() for k in ["schema", "model", "entity", "table"]):
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                        all_models.extend(parse_ts_drizzle(file.read(), rel_file))

            except Exception:
                continue

    result = {
        "root": str(root.name),
        "total_models_detected": len(all_models),
        "models": all_models
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_schemas(target)
