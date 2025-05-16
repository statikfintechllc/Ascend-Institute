# tools/self_edit.py

import os
import shutil
from pathlib import Path
from core.model_interface import ask_model
from memory.sqlite_memory import log_memory

def self_edit(input_data):
    """
    input_data: dict with {
        'file_path': str,
        'instruction': str
    }

    Example:
    {
        'file_path': 'tools/buy_crypto.py',
        'instruction': 'Add error handling and improve logging'
    }
    """
    file_path = input_data.get("file_path")
    instruction = input_data.get("instruction")

    if not file_path or not instruction:
        return "[self_edit] Missing 'file_path' or 'instruction'."

    file_path = Path(file_path)
    if not file_path.exists():
        return f"[self_edit] File does not exist: {file_path}"

    # Backup the file
    backup_path = file_path.with_suffix(file_path.suffix + ".bak")
    shutil.copy(file_path, backup_path)

    with open(file_path, "r") as f:
        original_code = f.read()

    # Build the prompt
    prompt = (
        f"You're an expert Python engineer. Here is the file content:\n\n"
        f"{original_code}\n\n"
        f"Now apply this instruction to the file above:\n'{instruction}'\n\n"
        f"Return the full updated code. Do not explain it. Just code."
    )

    new_code = ask_model(prompt)

    # Save new code
    with open(file_path, "w") as f:
        f.write(new_code)

    log_memory(
        input_text=f"Self-edit on {file_path.name}: {instruction}",
        output_text="Edit complete. Backup saved.",
        tag="self_edit"
    )

    return f"[self_edit] Updated {file_path.name}. Backup created: {backup_path.name}"
