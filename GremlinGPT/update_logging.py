#!/usr/bin/env python3
"""
Script to update all logging configurations to use the new structured logging pattern
"""

import os
import re
from pathlib import Path

def update_logging_imports(file_path):
    """Update a single file to use the new logging pattern"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already updated
    if 'setup_module_logger' in content:
        print(f"  Already updated: {file_path}")
        return False
    
    # Skip venv files
    if '.venv' in str(file_path):
        return False
        
    # Extract module name from path
    file_path_obj = Path(file_path)
    if file_path.startswith('./'):
        file_path_obj = Path(file_path[2:])  # Remove './'
    
    module_parts = file_path_obj.parts[:-1]  # Remove filename
    
    if not module_parts:
        module_name = 'root'
        file_name = file_path_obj.stem
    else:
        module_name = module_parts[0]
        file_name = file_path_obj.stem
    
    # Pattern to match the old logging setup
    old_pattern = r'from utils\.logging_config import get_module_logger\s*\n\s*#?\s*Initialize module-specific logger\s*\n\s*logger = get_module_logger\(["\'][^"\']*["\']\)'
    
    # New logging setup
    new_logging = f'''from utils.logging_config import setup_module_logger

# Initialize module-specific logger
logger = setup_module_logger("{module_name}", "{file_name}")'''
    
    # Replace the pattern
    new_content = re.sub(old_pattern, new_logging, content, flags=re.MULTILINE)
    
    # If no match found, try simpler pattern
    if new_content == content:
        old_simple = r'from utils\.logging_config import get_module_logger[^\n]*\n[^\n]*logger = get_module_logger\([^)]*\)'
        new_content = re.sub(old_simple, new_logging, content, flags=re.MULTILINE)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Updated: {file_path}")
        return True
    else:
        print(f"  No changes needed: {file_path}")
        return False

def main():
    print("Updating logging configurations...")
    
    # Get list of files to update
    files_to_update = [
        "./nlp_engine/parser.py",
        "./nlp_engine/diff_engine.py", 
        "./nlp_engine/pos_tagger.py",
        "./nlp_engine/semantic_score.py",
        "./tools/reward_model.py",
        "./trading_core/rules_engine.py",
        "./trading_core/portfolio_tracker.py",
        "./trading_core/signal_generator.py",
        "./trading_core/tax_estimator.py",
        "./trading_core/stock_scraper.py",
        "./scraper/page_simulator.py",
        "./scraper/web_knowledge_scraper.py",
        "./scraper/stt_scraper.py",
        "./scraper/ask_monday_handler.py",
        "./scraper/dom_navigator.py",
        "./scraper/source_router.py",
        "./scraper/tws_scraper.py",
        "./self_training/mutation_engine.py",
        "./self_training/trainer.py",
        "./self_training/feedback_loop.py",
        "./memory/vector_store/embedder.py",
        "./memory/log_history.py",
        "./backend/interface/commands.py",
        "./backend/api/scraping_api.py",
        "./backend/utils/git_ops.py",
        "./run/cli.py",
        "./self_mutation_watcher/watcher.py",
        "./self_mutation_watcher/mutation_daemon.py"
    ]
    
    updated_count = 0
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if update_logging_imports(file_path):
                updated_count += 1
    
    print(f"\nCompleted: Updated {updated_count} files")

if __name__ == "__main__":
    main()
