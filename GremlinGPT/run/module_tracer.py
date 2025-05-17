import importlib
import os
from rich import print
from rich.table import Table

BASE_DIR = "."

def trace_calls():
    table = Table(title="GremlinGPT Module Interconnectivity")
    table.add_column("Module", style="cyan")
    table.add_column("Imports", style="green")

    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                module_name = path.replace("/", ".").replace(".py", "")
                with open(path) as f:
                    lines = f.readlines()
                imports = [line.strip() for line in lines if line.strip().startswith("import") or line.strip().startswith("from")]
                if imports:
                    table.add_row(module_name, "\n".join(imports))
    print(table)

if __name__ == "__main__":
    trace_calls()

