# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Utility Module
# This script is a component of the GremlinGPT system, under Alpha expansion.
# Purpose:
#   - Git automation helpers for system-wide autocommit and file archiving
#   - Shared by FSM, Planner, and other modules
#   - Must remain side-effect free unless explicitly invoked

import os
import shutil
from datetime import datetime
from pathlib import Path
from backend.globals import logger

DEFAULT_ARCHIVE_DIR = "docs/"


def archive_json_log(source_path: str, prefix: str = "log") -> str:
    """
    Archive a JSONL or log file with timestamp into docs/ directory.
    Returns the new archive path, or empty string on failure.
    """
    try:
        src = Path(source_path).expanduser().resolve()
        if not src.exists():
            logger.warning(f"[git_ops] Source file not found: {source_path}")
            return ""

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        dest_name = f"{prefix}_{timestamp}.jsonl"
        dest_path = Path(DEFAULT_ARCHIVE_DIR).resolve() / dest_name

        shutil.copyfile(src, dest_path)
        logger.info(f"[git_ops] Archived {src} → {dest_path}")
        return str(dest_path)

    except Exception as e:
        logger.error(f"[git_ops] Archive failed: {e}")
        return ""


def auto_commit(file_path: str, message: str = "[autocommit] Update via git_ops"):
    """
    Stage and commit a file into the current Git repo.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            logger.warning(f"[git_ops] File not found: {file_path}")
            return

        os.system(f"git add \"{path}\"")
        os.system(f'git commit -m "{message}"')
        logger.success(f"[git_ops] Git commit successful for: {path.name}")

    except Exception as e:
        logger.warning(f"[git_ops] Git commit failed: {e}")
