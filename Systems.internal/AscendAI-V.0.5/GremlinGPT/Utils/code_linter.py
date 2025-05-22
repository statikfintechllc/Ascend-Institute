# code_linter.py

import subprocess


def lint_code(file_path):
    subprocess.run(["flake8", file_path])
    subprocess.run(["black", file_path])
    subprocess.run(["mypy", file_path])
