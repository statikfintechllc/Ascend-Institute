# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

# GremlinGPT v5 :: Utility Module
# Purpose:
#   - Git automation helpers for system-wide autocommit and file archiving
#   - Shared by FSM, Planner, and other modules
#   - Must remain side-effect free unless explicitly invoked

import os
import shutil
from datetime import datetime
from backend.globals import logger

DEFAULT_ARCHIVE_DIR = "docs/"


def archive_json_log(source_path: str, prefix: str = "log") -> str:
    """
    Archive a JSONL or log file with timestamp into docs/ directory.
    Returns the new archive path.
    """
    if not os.path.exists(source_path):
        logger.warning(f"[git_ops] Source file not found: {source_path}")
        return ""

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    filename = f"{prefix}_{timestamp}.jsonl"
    archive_path = os.path.join(DEFAULT_ARCHIVE_DIR, filename)

    try:
        shutil.copyfile(source_path, archive_path)
        logger.info(f"[git_ops] Archived {source_path} → {archive_path}")
        return archive_path
    except Exception as e:
        logger.error(f"[git_ops] Archive failed: {e}")
        return ""


def auto_commit(file_path: str, message: str = "[autocommit] Update via git_ops"):
    """
    Stage and commit the given file with a consistent message.
    """
    try:
        os.system(f"git add {file_path}")
        os.system(f'git commit -m "{message}"')
        logger.success(f"[git_ops] Git commit successful.")
    except Exception as e:
        logger.warning(f"{git_ops} Git commit failed: {e}")
