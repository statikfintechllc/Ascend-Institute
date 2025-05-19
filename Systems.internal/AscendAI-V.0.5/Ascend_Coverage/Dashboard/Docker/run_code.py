# Docker/run_code.py

import sys


def main():
    code = sys.stdin.read()
    try:
        exec(code, {}, {})
    except Exception as e:
        print(f"[run_code.py] Runtime Error:\n{e}")


if __name__ == "__main__":
    main()
