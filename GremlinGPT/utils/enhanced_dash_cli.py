#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Enhanced Dashboard CLI - Full Navigation & Management

import os
import sys
import json
import toml
import subprocess
import time
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import threading
import queue
import select
import termios
import tty
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from utils.logging_config import setup_module_logger
    from backend.globals import CFG
    logger = setup_module_logger("utils", "enhanced_dash_cli")
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("enhanced_dash_cli")
    CFG = {}

# Terminal color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        return f"{color}{text}{Colors.END}"


@dataclass
class FileItem:
    """Represents a file or directory in the file browser"""
    name: str
    path: Path
    is_dir: bool
    size: int
    modified: datetime
    permissions: str


class EnhancedDashboardCLI:
    """
    Enhanced Dashboard CLI for GremlinGPT
    
    Features:
    - Full file system navigation
    - Configuration management
    - Real-time log monitoring
    - System control and status
    - Service management
    - Interactive editing
    """
    
    def __init__(self):
        self.project_root = project_root
        self.current_path = self.project_root
        self.config_path = self.project_root / "config" / "config.toml"
        self.logs_path = self.project_root / "data" / "logs"
        
        # Terminal state
        self.running = True
        self.current_mode = "main"
        self.log_follow_active = False
        self.log_follow_thread = None
        self.log_queue = queue.Queue()
        
        # File browser state
        self.selected_index = 0
        self.items_per_page = 20
        self.current_page = 0
        
        # Load configuration
        self.load_config()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.running = False
        if self.log_follow_thread and self.log_follow_thread.is_alive():
            self.log_follow_active = False
            self.log_follow_thread.join(timeout=1)
    
    def load_config(self):
        """Load configuration from config.toml"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = toml.load(f)
            else:
                self.config = {}
        except Exception as e:
            self.config = {}
            logger.error(f"Failed to load config: {e}")
    
    def save_config(self):
        """Save configuration to config.toml"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                toml.dump(self.config, f)
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def get_terminal_size(self):
        """Get terminal dimensions"""
        try:
            return os.get_terminal_size()
        except:
            return os.terminal_size((80, 24))
    
    def print_header(self, title: str):
        """Print dashboard header"""
        term_size = self.get_terminal_size()
        width = term_size.columns
        
        self.clear_screen()
        print("=" * width)
        print(Colors.colorize(f"🧠 GremlinGPT Enhanced Dashboard - {title}", Colors.BOLD + Colors.CYAN))
        print(Colors.colorize(f"Path: {self.current_path}", Colors.BLUE))
        print(Colors.colorize(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Colors.GREEN))
        print("=" * width)
        print()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status information"""
        try:
            # Check if unified system is available
            unified_status = {"available": False}
            try:
                from core.integration import get_unified_system
                import asyncio
                
                async def get_status():
                    unified_system = get_unified_system()
                    return await unified_system.get_system_status()
                
                # Try to get status (simplified for CLI)
                unified_status = {"available": True, "status": "checking..."}
            except:
                unified_status = {"available": False, "error": "Unified system not initialized"}
            
            # Basic system info
            uptime = subprocess.check_output(['uptime'], text=True).strip()
            disk_usage = subprocess.check_output(['df', '-h', str(self.project_root)], text=True).strip().split('\n')[1]
            
            return {
                "uptime": uptime,
                "disk_usage": disk_usage,
                "unified_system": unified_status,
                "config_loaded": bool(self.config),
                "logs_available": self.logs_path.exists()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def display_main_menu(self):
        """Display main dashboard menu"""
        self.print_header("Main Menu")
        
        status = self.get_system_status()
        
        # System status display
        print(Colors.colorize("📊 System Status:", Colors.BOLD + Colors.YELLOW))
        if "error" not in status:
            print(f"⏱️  {status.get('uptime', 'Unknown')}")
            print(f"💾 {status.get('disk_usage', 'Unknown')}")
            print(f"⚙️  Config: {Colors.colorize('Loaded' if status.get('config_loaded') else 'Not Found', Colors.GREEN if status.get('config_loaded') else Colors.RED)}")
            print(f"📝 Logs: {Colors.colorize('Available' if status.get('logs_available') else 'Not Found', Colors.GREEN if status.get('logs_available') else Colors.RED)}")
            
            unified = status.get('unified_system', {})
            if unified.get('available'):
                print(f"🧠 Unified System: {Colors.colorize('Active', Colors.GREEN)}")
            else:
                print(f"🧠 Unified System: {Colors.colorize('Inactive', Colors.YELLOW)}")
        else:
            print(Colors.colorize(f"❌ Error: {status['error']}", Colors.RED))
        
        print()
        
        # Main menu options
        print(Colors.colorize("🎛️ Main Menu Options:", Colors.BOLD + Colors.CYAN))
        print("1. 📁 File Navigator & Editor")
        print("2. ⚙️  Configuration Manager")
        print("3. 📊 Log Monitor & Analyzer")
        print("4. 🎮 System Control")
        print("5. 🧠 Unified System Manager")
        print("6. 📈 Performance Monitor")
        print("7. 🔧 Service Manager")
        print("8. ❓ Help & Documentation")
        print("9. 🚪 Exit")
        print()
        
        choice = input(Colors.colorize("Select option (1-9): ", Colors.BOLD))
        return choice.strip()
    
    def file_navigator(self):
        """Interactive file navigator and editor"""
        while True:
            self.print_header(f"File Navigator - {self.current_path.name}")
            
            try:
                items = self.get_directory_items(self.current_path)
                self.display_file_list(items)
                
                print("\nNavigation:")
                print("Enter number to select | 'up' for parent | 'edit <file>' to edit | 'back' to return")
                
                choice = input(Colors.colorize("Navigator> ", Colors.BOLD)).strip()
                
                if choice.lower() == 'back':
                    break
                elif choice.lower() == 'up':
                    if self.current_path != self.project_root:
                        self.current_path = self.current_path.parent
                elif choice.startswith('edit '):
                    filename = choice[5:].strip()
                    file_path = self.current_path / filename
                    if file_path.exists() and file_path.is_file():
                        self.edit_file(file_path)
                    else:
                        print(Colors.colorize(f"File not found: {filename}", Colors.RED))
                        input("Press Enter to continue...")
                elif choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(items):
                        selected = items[index]
                        if selected.is_dir:
                            self.current_path = selected.path
                        else:
                            self.view_file(selected.path)
                else:
                    print(Colors.colorize("Invalid choice", Colors.RED))
                    time.sleep(1)
                    
            except Exception as e:
                print(Colors.colorize(f"Error: {e}", Colors.RED))
                input("Press Enter to continue...")
    
    def get_directory_items(self, path: Path) -> List[FileItem]:
        """Get list of files and directories"""
        items = []
        
        try:
            for item in sorted(path.iterdir()):
                if item.name.startswith('.') and item.name not in ['.', '..']:
                    continue  # Skip hidden files except . and ..
                
                try:
                    stat = item.stat()
                    items.append(FileItem(
                        name=item.name,
                        path=item,
                        is_dir=item.is_dir(),
                        size=stat.st_size,
                        modified=datetime.fromtimestamp(stat.st_mtime),
                        permissions=oct(stat.st_mode)[-3:]
                    ))
                except:
                    # Handle permission errors
                    items.append(FileItem(
                        name=item.name,
                        path=item,
                        is_dir=item.is_dir(),
                        size=0,
                        modified=datetime.now(),
                        permissions="???"
                    ))
        except PermissionError:
            print(Colors.colorize("Permission denied", Colors.RED))
        
        return items
    
    def display_file_list(self, items: List[FileItem]):
        """Display file list with formatting"""
        if not items:
            print(Colors.colorize("Directory is empty", Colors.YELLOW))
            return
        
        print(f"{'#':<3} {'Name':<30} {'Type':<6} {'Size':<10} {'Modified':<20} {'Perm'}")
        print("-" * 75)
        
        for i, item in enumerate(items[:self.items_per_page], 1):
            icon = "📁" if item.is_dir else "📄"
            type_str = "DIR" if item.is_dir else "FILE"
            size_str = self.format_size(item.size) if not item.is_dir else "-"
            modified_str = item.modified.strftime("%Y-%m-%d %H:%M")
            
            color = Colors.BLUE if item.is_dir else Colors.WHITE
            print(Colors.colorize(
                f"{i:<3} {icon} {item.name:<28} {type_str:<6} {size_str:<10} {modified_str:<20} {item.permissions}",
                color
            ))
    
    def format_size(self, size: int) -> str:
        """Format file size in human readable format"""
        size_float = float(size)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_float < 1024:
                return f"{size_float:.1f}{unit}"
            size_float /= 1024
        return f"{size_float:.1f}TB"
    
    def view_file(self, file_path: Path):
        """View file contents"""
        self.print_header(f"File Viewer - {file_path.name}")
        
        try:
            if file_path.suffix.lower() in ['.log', '.txt', '.md', '.py', '.js', '.json', '.toml', '.yaml', '.yml']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                lines = content.split('\n')
                if len(lines) > 50:
                    print(f"File has {len(lines)} lines. Showing first 50 lines:")
                    print("-" * 60)
                    for i, line in enumerate(lines[:50], 1):
                        print(f"{i:3}: {line}")
                    print("-" * 60)
                    print(f"... and {len(lines) - 50} more lines")
                else:
                    for i, line in enumerate(lines, 1):
                        print(f"{i:3}: {line}")
            else:
                print(Colors.colorize("Binary file - cannot display content", Colors.YELLOW))
                
        except Exception as e:
            print(Colors.colorize(f"Error reading file: {e}", Colors.RED))
        
        input("\nPress Enter to continue...")
    
    def edit_file(self, file_path: Path):
        """Edit file with external editor"""
        try:
            editor = os.environ.get('EDITOR', 'nano')
            subprocess.call([editor, str(file_path)])
        except Exception as e:
            print(Colors.colorize(f"Error opening editor: {e}", Colors.RED))
            input("Press Enter to continue...")
    
    def configuration_manager(self):
        """Configuration management interface"""
        while True:
            self.print_header("Configuration Manager")
            
            print(Colors.colorize("📋 Configuration Sections:", Colors.BOLD + Colors.CYAN))
            
            sections = list(self.config.keys()) if self.config else []
            for i, section in enumerate(sections, 1):
                print(f"{i}. {section}")
            
            print(f"{len(sections) + 1}. Add new section")
            print(f"{len(sections) + 2}. Save configuration")
            print(f"{len(sections) + 3}. Reload configuration")
            print(f"{len(sections) + 4}. Back to main menu")
            
            choice = input(Colors.colorize("\nSelect option: ", Colors.BOLD)).strip()
            
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(sections):
                    self.edit_config_section(sections[index])
                elif index == len(sections):
                    self.add_config_section()
                elif index == len(sections) + 1:
                    if self.save_config():
                        print(Colors.colorize("✅ Configuration saved", Colors.GREEN))
                    else:
                        print(Colors.colorize("❌ Failed to save configuration", Colors.RED))
                    input("Press Enter to continue...")
                elif index == len(sections) + 2:
                    self.load_config()
                    print(Colors.colorize("✅ Configuration reloaded", Colors.GREEN))
                    input("Press Enter to continue...")
                elif index == len(sections) + 3:
                    break
    
    def edit_config_section(self, section_name: str):
        """Edit a configuration section"""
        self.print_header(f"Edit Section: {section_name}")
        
        section = self.config.get(section_name, {})
        
        print(Colors.colorize(f"Current values in [{section_name}]:", Colors.CYAN))
        for key, value in section.items():
            print(f"  {key} = {value}")
        
        print("\nOptions:")
        print("1. Edit existing key")
        print("2. Add new key")
        print("3. Delete key")
        print("4. Back")
        
        choice = input(Colors.colorize("Select: ", Colors.BOLD)).strip()
        
        if choice == "1":
            key = input("Enter key name: ").strip()
            if key in section:
                current_value = section[key]
                print(f"Current value: {current_value}")
                new_value = input("Enter new value: ").strip()
                
                # Try to maintain type
                if isinstance(current_value, bool):
                    section[key] = new_value.lower() in ['true', '1', 'yes', 'on']
                elif isinstance(current_value, int):
                    try:
                        section[key] = int(new_value)
                    except ValueError:
                        section[key] = new_value
                elif isinstance(current_value, float):
                    try:
                        section[key] = float(new_value)
                    except ValueError:
                        section[key] = new_value
                else:
                    section[key] = new_value
                
                print(Colors.colorize("✅ Key updated", Colors.GREEN))
            else:
                print(Colors.colorize("❌ Key not found", Colors.RED))
            input("Press Enter to continue...")
            
        elif choice == "2":
            key = input("Enter key name: ").strip()
            value = input("Enter value: ").strip()
            
            # Try to detect type
            if value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            elif '.' in value:
                try:
                    value = float(value)
                except ValueError:
                    pass
            
            section[key] = value
            self.config[section_name] = section
            print(Colors.colorize("✅ Key added", Colors.GREEN))
            input("Press Enter to continue...")
            
        elif choice == "3":
            key = input("Enter key name to delete: ").strip()
            if key in section:
                del section[key]
                print(Colors.colorize("✅ Key deleted", Colors.GREEN))
            else:
                print(Colors.colorize("❌ Key not found", Colors.RED))
            input("Press Enter to continue...")
    
    def add_config_section(self):
        """Add a new configuration section"""
        section_name = input("Enter section name: ").strip()
        if section_name:
            self.config[section_name] = {}
            print(Colors.colorize(f"✅ Section '{section_name}' added", Colors.GREEN))
        else:
            print(Colors.colorize("❌ Invalid section name", Colors.RED))
        input("Press Enter to continue...")
    
    def log_monitor(self):
        """Log monitoring and analysis interface"""
        while True:
            self.print_header("Log Monitor & Analyzer")
            
            log_files = self.get_log_files()
            
            print(Colors.colorize("📊 Available Logs:", Colors.BOLD + Colors.CYAN))
            for i, (category, files) in enumerate(log_files.items(), 1):
                print(f"{i}. {Colors.colorize(category, Colors.YELLOW)} ({len(files)} files)")
                for file in files[:3]:  # Show first 3 files
                    print(f"   • {file.name}")
                if len(files) > 3:
                    print(f"   • ... and {len(files) - 3} more")
            
            print(f"{len(log_files) + 1}. Real-time log following")
            print(f"{len(log_files) + 2}. Search logs")
            print(f"{len(log_files) + 3}. Back to main menu")
            
            choice = input(Colors.colorize("\nSelect option: ", Colors.BOLD)).strip()
            
            if choice.isdigit():
                index = int(choice) - 1
                categories = list(log_files.keys())
                
                if 0 <= index < len(categories):
                    category = categories[index]
                    self.browse_log_category(category, log_files[category])
                elif index == len(categories):
                    self.follow_logs()
                elif index == len(categories) + 1:
                    self.search_logs()
                elif index == len(categories) + 2:
                    break
    
    def get_log_files(self) -> Dict[str, List[Path]]:
        """Get categorized log files"""
        log_files = {
            "System": [],
            "Modules": [],
            "Services": [],
            "Applications": [],
            "Agents": []
        }
        
        if not self.logs_path.exists():
            return log_files
        
        try:
            for log_file in self.logs_path.rglob("*.log"):
                relative_path = log_file.relative_to(self.logs_path)
                parent = relative_path.parts[0] if relative_path.parts else "root"
                
                if parent in ["system", "core"]:
                    log_files["System"].append(log_file)
                elif parent in ["backend", "nlp_engine", "memory", "scraper", "trading_core"]:
                    log_files["Modules"].append(log_file)
                elif parent in ["services"]:
                    log_files["Services"].append(log_file)
                elif parent in ["agents"]:
                    log_files["Agents"].append(log_file)
                else:
                    log_files["Applications"].append(log_file)
            
            # Also include .jsonl files for application logs
            for jsonl_file in self.logs_path.rglob("*.jsonl"):
                log_files["Applications"].append(jsonl_file)
                
        except Exception as e:
            logger.error(f"Error scanning log files: {e}")
        
        return log_files
    
    def browse_log_category(self, category: str, files: List[Path]):
        """Browse logs in a specific category"""
        while True:
            self.print_header(f"Log Browser - {category}")
            
            print(Colors.colorize(f"📄 {category} Log Files:", Colors.CYAN))
            for i, file in enumerate(files, 1):
                size = self.format_size(file.stat().st_size) if file.exists() else "0B"
                modified = datetime.fromtimestamp(file.stat().st_mtime).strftime("%m-%d %H:%M") if file.exists() else "N/A"
                print(f"{i:2}. {file.name:<30} {size:>8} {modified}")
            
            print(f"{len(files) + 1}. Back to log categories")
            
            choice = input(Colors.colorize("\nSelect log file: ", Colors.BOLD)).strip()
            
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(files):
                    self.view_log_file(files[index])
                elif index == len(files):
                    break
    
    def view_log_file(self, log_file: Path):
        """View and analyze a log file"""
        self.print_header(f"Log Viewer - {log_file.name}")
        
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            print(f"📊 Log Statistics:")
            print(f"   Lines: {len(lines)}")
            print(f"   Size: {self.format_size(log_file.stat().st_size)}")
            print(f"   Modified: {datetime.fromtimestamp(log_file.stat().st_mtime)}")
            print()
            
            # Show recent lines
            recent_lines = lines[-50:] if len(lines) > 50 else lines
            print(Colors.colorize("📄 Recent Log Entries (last 50 lines):", Colors.CYAN))
            print("-" * 80)
            
            for line in recent_lines:
                line = line.rstrip()
                if "ERROR" in line.upper():
                    print(Colors.colorize(line, Colors.RED))
                elif "WARNING" in line.upper() or "WARN" in line.upper():
                    print(Colors.colorize(line, Colors.YELLOW))
                elif "SUCCESS" in line.upper() or "INFO" in line.upper():
                    print(Colors.colorize(line, Colors.GREEN))
                else:
                    print(line)
            
            print("-" * 80)
            
        except Exception as e:
            print(Colors.colorize(f"Error reading log file: {e}", Colors.RED))
        
        input("\nPress Enter to continue...")
    
    def follow_logs(self):
        """Real-time log following"""
        self.print_header("Real-time Log Following")
        
        print(Colors.colorize("🔄 Starting real-time log monitoring...", Colors.CYAN))
        print(Colors.colorize("Press Ctrl+C to stop", Colors.YELLOW))
        print("-" * 80)
        
        # Simple tail -f implementation
        log_files = []
        for category, files in self.get_log_files().items():
            log_files.extend(files)
        
        if not log_files:
            print(Colors.colorize("No log files found", Colors.RED))
            input("Press Enter to continue...")
            return
        
        try:
            # Use tail -f on the most recent log file
            recent_log = max(log_files, key=lambda f: f.stat().st_mtime if f.exists() else 0)
            
            process = subprocess.Popen(
                ['tail', '-f', str(recent_log)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"Following: {recent_log.name}")
            print("-" * 40)
            
            while True:
                if process.stdout:
                    line = process.stdout.readline()
                    if line:
                        line = line.rstrip()
                        if "ERROR" in line.upper():
                            print(Colors.colorize(line, Colors.RED))
                        elif "WARNING" in line.upper():
                            print(Colors.colorize(line, Colors.YELLOW))
                        elif "SUCCESS" in line.upper():
                            print(Colors.colorize(line, Colors.GREEN))
                        else:
                            print(line)
                else:
                    break
                
        except KeyboardInterrupt:
            if 'process' in locals():
                process.terminate()
            print(Colors.colorize("\n📴 Log following stopped", Colors.YELLOW))
            input("Press Enter to continue...")
    
    def search_logs(self):
        """Search through log files"""
        self.print_header("Log Search")
        
        search_term = input("Enter search term: ").strip()
        if not search_term:
            return
        
        print(f"\n🔍 Searching for: '{search_term}'")
        print("-" * 50)
        
        found_results = False
        for category, files in self.get_log_files().items():
            for log_file in files:
                try:
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if search_term.lower() in line.lower():
                                if not found_results:
                                    found_results = True
                                
                                print(f"{Colors.colorize(log_file.name, Colors.CYAN)}:{line_num}: {line.strip()}")
                
                except Exception as e:
                    continue
        
        if not found_results:
            print(Colors.colorize("No results found", Colors.YELLOW))
        
        input("\nPress Enter to continue...")
    
    def system_control(self):
        """System control interface"""
        while True:
            self.print_header("System Control")
            
            print(Colors.colorize("🎮 System Control Options:", Colors.BOLD + Colors.CYAN))
            print("1. 🚀 Start GremlinGPT")
            print("2. 🛑 Stop GremlinGPT")
            print("3. 🔄 Restart GremlinGPT")
            print("4. 📊 System Status")
            print("5. 🧠 Launch Unified System")
            print("6. 💬 Chat Interface")
            print("7. 🔧 Recovery Mode")
            print("8. 🏠 Back to main menu")
            
            choice = input(Colors.colorize("\nSelect option: ", Colors.BOLD)).strip()
            
            if choice == "1":
                self.execute_system_command("start")
            elif choice == "2":
                self.execute_system_command("stop")
            elif choice == "3":
                self.execute_system_command("restart")
            elif choice == "4":
                self.show_system_status()
            elif choice == "5":
                self.launch_unified_system()
            elif choice == "6":
                self.launch_chat_interface()
            elif choice == "7":
                self.execute_system_command("recovery")
            elif choice == "8":
                break
    
    def execute_system_command(self, command: str):
        """Execute system control commands"""
        self.print_header(f"System Control - {command.upper()}")
        
        scripts = {
            "start": self.project_root / "run" / "start_all.sh",
            "stop": self.project_root / "run" / "stop_all.sh",
            "restart": [
                self.project_root / "run" / "stop_all.sh",
                self.project_root / "run" / "start_all.sh"
            ],
            "recovery": self.project_root / "run" / "reboot_recover.sh"
        }
        
        if command in scripts:
            try:
                script_paths = scripts[command]
                if not isinstance(script_paths, list):
                    script_paths = [script_paths]
                
                for script_path in script_paths:
                    if script_path.exists():
                        print(f"🔄 Executing: {script_path.name}")
                        result = subprocess.run(['bash', str(script_path)], 
                                              capture_output=True, text=True, timeout=30)
                        
                        if result.returncode == 0:
                            print(Colors.colorize("✅ Command executed successfully", Colors.GREEN))
                            if result.stdout:
                                print("Output:", result.stdout)
                        else:
                            print(Colors.colorize(f"❌ Command failed with code {result.returncode}", Colors.RED))
                            if result.stderr:
                                print("Error:", result.stderr)
                    else:
                        print(Colors.colorize(f"❌ Script not found: {script_path}", Colors.RED))
                
            except subprocess.TimeoutExpired:
                print(Colors.colorize("⏰ Command timed out", Colors.YELLOW))
            except Exception as e:
                print(Colors.colorize(f"❌ Error executing command: {e}", Colors.RED))
        else:
            print(Colors.colorize(f"❌ Unknown command: {command}", Colors.RED))
        
        input("\nPress Enter to continue...")
    
    def show_system_status(self):
        """Show detailed system status"""
        self.print_header("System Status")
        
        status = self.get_system_status()
        
        print(Colors.colorize("📊 Detailed System Status:", Colors.BOLD + Colors.CYAN))
        print()
        
        for key, value in status.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"{key}: {value}")
        
        print()
        
        # Check process status
        print(Colors.colorize("🔍 Process Status:", Colors.CYAN))
        try:
            # Check for Python processes
            result = subprocess.run(['pgrep', '-f', 'gremlin'], capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                print(f"  GremlinGPT processes: {len(pids)} running")
                for pid in pids:
                    print(f"    PID: {pid}")
            else:
                print("  No GremlinGPT processes found")
        except:
            print("  Could not check process status")
        
        input("\nPress Enter to continue...")
    
    def launch_unified_system(self):
        """Launch the unified system"""
        self.print_header("Launch Unified System")
        
        unified_script = self.project_root / "run" / "unified_startup.py"
        
        if unified_script.exists():
            print("🚀 Launching unified GremlinGPT ecosystem...")
            print("This will start the complete living AI system.")
            
            confirm = input("Continue? (y/N): ").strip().lower()
            if confirm == 'y':
                try:
                    # Launch in background
                    subprocess.Popen([sys.executable, str(unified_script)])
                    print(Colors.colorize("✅ Unified system launched", Colors.GREEN))
                except Exception as e:
                    print(Colors.colorize(f"❌ Failed to launch: {e}", Colors.RED))
            else:
                print("Cancelled")
        else:
            print(Colors.colorize("❌ Unified startup script not found", Colors.RED))
        
        input("\nPress Enter to continue...")
    
    def launch_chat_interface(self):
        """Launch chat interface"""
        chat_script = self.project_root / "run" / "cli.py"
        
        if chat_script.exists():
            print("💬 Launching chat interface...")
            try:
                subprocess.call([sys.executable, str(chat_script)])
            except Exception as e:
                print(Colors.colorize(f"❌ Failed to launch chat: {e}", Colors.RED))
        else:
            print(Colors.colorize("❌ Chat script not found", Colors.RED))
        
        input("\nPress Enter to continue...")
    
    def unified_system_manager(self):
        """Unified system management interface"""
        self.print_header("Unified System Manager")
        
        print(Colors.colorize("🧠 This feature requires the unified system to be active.", Colors.YELLOW))
        print("The unified system provides advanced multi-agent coordination,")
        print("real-time learning, and autonomous operation capabilities.")
        print()
        print("To activate the unified system, use 'System Control > Launch Unified System'")
        
        input("\nPress Enter to continue...")
    
    def performance_monitor(self):
        """Performance monitoring interface"""
        self.print_header("Performance Monitor")
        
        print(Colors.colorize("📈 System Performance Metrics:", Colors.BOLD + Colors.CYAN))
        
        try:
            # CPU and Memory info
            with open('/proc/loadavg', 'r') as f:
                load_avg = f.read().strip()
            print(f"Load Average: {load_avg}")
            
            # Memory info
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            for line in meminfo.split('\n'):
                if 'MemTotal' in line or 'MemAvailable' in line:
                    print(line.strip())
            
            # Disk usage
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            print("\nDisk Usage:")
            print(result.stdout)
            
        except Exception as e:
            print(Colors.colorize(f"Error getting performance data: {e}", Colors.RED))
        
        input("\nPress Enter to continue...")
    
    def service_manager(self):
        """Service management interface"""
        self.print_header("Service Manager")
        
        print(Colors.colorize("🔧 GremlinGPT Service Management:", Colors.BOLD + Colors.CYAN))
        print()
        print("This feature allows management of GremlinGPT system services.")
        print("Services include: FSM, Memory, NLP Engine, Trading Core, Scrapers")
        print()
        print(Colors.colorize("⚠️ Service management is handled by the main system scripts.", Colors.YELLOW))
        print("Use 'System Control' for starting/stopping services.")
        
        input("\nPress Enter to continue...")
    
    def show_help(self):
        """Show help and documentation"""
        self.print_header("Help & Documentation")
        
        help_text = """
🆘 GremlinGPT Enhanced Dashboard CLI Help

📁 FILE NAVIGATOR:
   • Browse project files and directories
   • Edit files with your default editor ($EDITOR)
   • View file contents with syntax awareness
   • Navigate with numbers, 'up' for parent, 'edit <file>' to edit

⚙️ CONFIGURATION MANAGER:
   • Edit config.toml sections interactively
   • Add/remove configuration keys
   • Type-aware value editing (bool, int, float, string)
   • Save and reload configuration

📊 LOG MONITOR:
   • Browse logs by category (System, Modules, Services, etc.)
   • Real-time log following (tail -f)
   • Search across all log files
   • Color-coded log levels (Error=Red, Warning=Yellow, Info=Green)

🎮 SYSTEM CONTROL:
   • Start/Stop/Restart GremlinGPT
   • Launch unified ecosystem
   • System status monitoring
   • Recovery mode access

🧠 UNIFIED SYSTEM:
   • Advanced multi-agent coordination
   • Real-time learning and adaptation
   • Autonomous operation capabilities
   • Performance optimization

📈 PERFORMANCE MONITOR:
   • System resource usage
   • Load averages and memory
   • Disk usage statistics

KEYBOARD SHORTCUTS:
   • Ctrl+C: Exit current operation
   • 'back': Return to previous menu
   • 'up': Navigate to parent directory
   • Numbers: Select menu items

ENVIRONMENT VARIABLES:
   • $EDITOR: Default text editor (defaults to nano)
   • $SHELL: User shell (auto-detected)

For more information, see: UNIFIED_ECOSYSTEM.md
        """
        
        print(help_text)
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main dashboard loop"""
        try:
            while self.running:
                choice = self.display_main_menu()
                
                if choice == "1":
                    self.file_navigator()
                elif choice == "2":
                    self.configuration_manager()
                elif choice == "3":
                    self.log_monitor()
                elif choice == "4":
                    self.system_control()
                elif choice == "5":
                    self.unified_system_manager()
                elif choice == "6":
                    self.performance_monitor()
                elif choice == "7":
                    self.service_manager()
                elif choice == "8":
                    self.show_help()
                elif choice == "9":
                    self.running = False
                else:
                    print(Colors.colorize("Invalid choice. Please select 1-9.", Colors.RED))
                    time.sleep(1)
        
        except KeyboardInterrupt:
            print(Colors.colorize("\n👋 Goodbye! Dashboard terminated by user.", Colors.CYAN))
        except Exception as e:
            print(Colors.colorize(f"\n❌ Unexpected error: {e}", Colors.RED))
        finally:
            self._signal_handler(None, None)


def main():
    """Main entry point"""
    try:
        dashboard = EnhancedDashboardCLI()
        dashboard.run()
    except Exception as e:
        print(f"Failed to start dashboard: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
