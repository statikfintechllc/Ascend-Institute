#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Centralized Logging Migration Script

import os
import re
from pathlib import Path

def update_logging_imports():
    """
    Update all Python files to use the centralized logging system
    """
    project_root = Path.cwd()
    
    # Modules mapping for proper logger initialization
    module_mapping = {
        'backend/': 'backend',
        'nlp_engine/': 'nlp_engine', 
        'memory/': 'memory',
        'scraper/': 'scraper',
        'agents/': 'agents',
        'trading_core/': 'trading_core',
        'tools/': 'tools',
        'core/': 'core',
        'executors/': 'executors',
        'self_training/': 'self_training',
        'self_mutation_watcher/': 'self_mutation_watcher',
        'utils/': 'utils',
        'tests/': 'tests',
        'run/': 'utils',
        'frontend/': 'frontend'
    }
    
    files_updated = []
    
    # Find all Python files
    for py_file in project_root.rglob("*.py"):
        if 'utils/logging_config.py' in str(py_file):
            continue  # Skip the logging config itself
            
        relative_path = py_file.relative_to(project_root)
        
        # Determine module category
        module_name = 'utils'  # default
        for path_prefix, module in module_mapping.items():
            if str(relative_path).startswith(path_prefix):
                module_name = module
                break
        
        # Read file content
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Could not read {py_file}: {e}")
            continue
        
        # Check if file uses loguru logger
        if 'from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("utils")' in content or 'from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("utils")' in content:
            # Replace loguru import
            new_content = content.replace(
                'from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("utils")',
                f'from utils.logging_config import get_module_logger\n\n# Initialize module-specific logger\nlogger = get_module_logger("{module_name}")'
            )
            
            # Replace backend.globals logger import
            new_content = new_content.replace(
                'from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("utils")',
                f'from utils.logging_config import get_module_logger\n\n# Initialize module-specific logger\nlogger = get_module_logger("{module_name}")'
            )
            
            # Write updated content
            try:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_updated.append((str(py_file), module_name))
                print(f"✓ Updated {relative_path} -> {module_name} logger")
            except Exception as e:
                print(f"⚠️  Could not write {py_file}: {e}")
    
    return files_updated

def fix_specific_issues():
    """
    Fix specific logging issues in problematic files
    """
    # Fix self_training/trainer.py - ensure logger is properly initialized
    trainer_file = Path("self_training/trainer.py")
    if trainer_file.exists():
        with open(trainer_file, 'r') as f:
            content = f.read()
        
        # Ensure logger is initialized after imports
        if 'logger = get_module_logger("self_training")' not in content:
            # Find the imports section and add logger initialization
            lines = content.split('\n')
            new_lines = []
            added_logger = False
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                # Add logger after the logging import
                if 'from utils.logging_config import get_module_logger' in line and not added_logger:
                    new_lines.extend([
                        '',
                        '# Initialize self_training module logger',
                        'logger = get_module_logger("self_training")',
                        ''
                    ])
                    added_logger = True
            
            if added_logger:
                with open(trainer_file, 'w') as f:
                    f.write('\n'.join(new_lines))
                print(f"✓ Fixed logger initialization in {trainer_file}")

if __name__ == "__main__":
    print("🔧 Starting centralized logging migration...")
    
    # Update logging imports
    updated_files = update_logging_imports()
    
    # Fix specific issues
    fix_specific_issues()
    
    print(f"\n✅ Migration complete! Updated {len(updated_files)} files")
    print("\nFiles updated:")
    for file_path, module_name in updated_files:
        print(f"  • {file_path} -> {module_name}")
