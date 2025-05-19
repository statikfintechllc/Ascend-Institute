# code_linter.py

import ast
import subprocess


def score_code_quality(code: str):
    try:
        ast.parse(code)
    except SyntaxError as e:
        return 0.0, f"Syntax error: {e}"

    with open("temp_check.py", "w") as f:
        f.write(code)

    result = subprocess.run(["flake8", "temp_check.py"], capture_output=True, text=True)
    if result.returncode != 0:
        return 0.5, result.stdout.strip()

    return 1.0, "Lint passed."
