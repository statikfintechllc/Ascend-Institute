#!/usr/bin/env python3

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# It must:
#   - Integrate seamlessly into the architecture defined in the full outline
#   - Operate autonomously and communicate cross-module via defined protocols
#   - Be production-grade, repair-capable, and state-of-the-art in logic
#   - Support learning, persistence, mutation, and traceability
#   - Not remove or weaken logic (stubs may be replaced, but never deleted)
#   - Leverage appropriate dependencies, imports, and interlinks to other systems
#   - Return enhanced — fully wired, no placeholders, no guesswork
# Objective:
#   Receive, reinforce, and return each script as a living part of the Gremlin:

# run/module_tracer.py

import os
import importlib.util
from rich import print
from rich.table import Table

BASE_DIR = "."


def is_importable(module_path):
    """Check if a module is importable using importlib."""
    try:
        spec = importlib.util.spec_from_file_location("temp_module", module_path)
        return spec is not None
    except Exception:
        return False


def trace_calls():
    table = Table(title="GremlinGPT Module Interconnectivity")
    table.add_column("Module", style="cyan", no_wrap=True)
    table.add_column("Imports", style="green")
    table.add_column("Importable", style="magenta")

    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                module_name = path.replace("/", ".").replace(".py", "")
                try:
                    with open(path, encoding="utf-8") as f:
                        lines = f.readlines()
                    imports = [
                        line.strip()
                        for line in lines
                        if line.strip().startswith("import")
                        or line.strip().startswith("from")
                    ]
                    importable = "Yes" if is_importable(path) else "No"
                    table.add_row(module_name, "\n".join(imports), importable)
                except Exception as e:
                    table.add_row(module_name, "[error] Could not read", "No")
                    print(f"[WARN] Skipped {module_name}: {e}")

    print(table)


if __name__ == "__main__":
    trace_calls()
