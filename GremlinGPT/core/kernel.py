# core/kernel.py

from datetime import datetime
from pathlib import Path
from memory.vector_store.embedder import embed_text, package_embedding
from self_training.feedback_loop import inject_feedback
from nlp_engine.diff_engine import diff_texts
from backend.globals import logger

KERNEL_TAG = "kernel_writer"
SOURCE_ROOT = Path("GremlinGPT")

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[KERNEL] Failed to read {path}: {e}")
        return None

def write_file(path, content):
    try:
        with open(path, "w") as f:
            f.write(content)
        logger.success(f"[KERNEL] Overwrote: {path}")
        return True
    except Exception as e:
        logger.error(f"[KERNEL] Failed to write {path}: {e}")
        return False

def apply_patch(file_path, new_code, reason="mutation"):
    original = read_file(file_path)
    if original is None:
        return False

    if original == new_code:
        logger.info(f"[KERNEL] No changes in patch for {file_path}")
        return False

    diff = diff_texts(original, new_code)
    diff_text = "\n".join(diff["diff_lines"])
    vector = embed_text(diff_text)

    package_embedding(
        text=diff_text,
        vector=vector,
        meta={
            "origin": KERNEL_TAG,
            "file": file_path,
            "type": "code_patch",
            "reason": reason,
            "semantic_score": diff["semantic_score"],
            "embedding_delta": diff["embedding_delta"],
            "timestamp": datetime.utcnow().isoformat()
        }
    )

    success = write_file(file_path, new_code)
    if success:
        inject_feedback()

    return success

def patch_from_text(target_file, injected_code, reason="human"):
    path = SOURCE_ROOT / target_file
    return apply_patch(str(path), injected_code, reason)

def patch_from_file(target_file, patch_file):
    try:
        with open(patch_file, "r") as f:
            new_code = f.read()
        return patch_from_text(target_file, new_code, reason=f"patch:{patch_file}")
    except Exception as e:
        logger.error(f"[KERNEL] Failed patch from file: {e}")
        return False

if __name__ == "__main__":
    test_file = "agent_core/tool_executor.py"
    test_patch = """
def execute_tool(task):
    return f"Mocked execution of {task}"
"""
    patch_from_text(test_file, test_patch.strip(), reason="example_patch")
