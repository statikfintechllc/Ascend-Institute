# GremlinGPT Enhanced Dashboard CLI

## 🚀 Complete Navigation, Configuration & Monitoring Solution

The Enhanced Dashboard CLI provides a comprehensive terminal-based interface for managing your GremlinGPT ecosystem with full file navigation, configuration management, and advanced monitoring capabilities.

## 📋 Features Overview

### ✅ **What You Now Have:**

#### 🎯 **Full File Navigation**
- **File Browser**: Complete filesystem navigation within the project
- **Directory Traversal**: Navigate folders with numeric selection or 'up' command
- **File Viewing**: View text files with syntax awareness and line numbers
- **External Editing**: Edit files with your preferred editor (`$EDITOR` environment variable)
- **File Management**: Browse, view, and edit any file in the project structure

#### ⚙️ **Complete Configuration Management**
- **Interactive Config Editor**: Edit `config.toml` sections through menu system
- **Type-Aware Editing**: Automatic type detection and conversion (bool, int, float, string)
- **Add/Remove Sections**: Create new configuration sections dynamically
- **Add/Remove Keys**: Manage individual configuration keys within sections
- **Save/Reload**: Persistent configuration changes with validation

#### 📊 **Advanced Log Monitoring**
- **Categorized Logs**: Organized by System, Modules, Services, Applications, Agents
- **Real-Time Following**: Live log streaming with `tail -f` functionality
- **Log Search**: Search across all log files for specific terms
- **Color-Coded Display**: Error=Red, Warning=Yellow, Success=Green
- **Log Analytics**: File statistics, size information, modification times

#### 🎮 **System Control & Management**
- **Service Control**: Start/Stop/Restart GremlinGPT services
- **Unified System Launch**: Initialize the complete living AI ecosystem
- **Status Monitoring**: Real-time system status and health checks
- **Recovery Mode**: Emergency recovery and repair functionality
- **Chat Interface**: Direct access to NLP/chat functionality

#### 📈 **Performance Monitoring**
- **Resource Usage**: CPU load averages, memory statistics
- **Process Monitoring**: Active GremlinGPT process detection
- **Disk Usage**: Storage utilization and capacity monitoring
- **System Health**: Comprehensive system status reporting

### 🆚 **Comparison: Basic vs Enhanced Dashboard**

| Feature | Basic `dash_cli.sh` | Enhanced Dashboard |
|---------|-------------------|------------------|
| **File Navigation** | ❌ None | ✅ Full filesystem browser |
| **Config Management** | ❌ None | ✅ Interactive editor |
| **Log Monitoring** | ✅ Basic viewing | ✅ Advanced categorized + search |
| **System Control** | ✅ Start/Stop | ✅ Complete management |
| **Real-time Logs** | ❌ None | ✅ Live streaming |
| **File Editing** | ❌ None | ✅ External editor integration |
| **Performance Metrics** | ❌ Basic | ✅ Comprehensive monitoring |
| **Service Management** | ✅ Basic | ✅ Advanced control |

## 🚀 **Getting Started**

### **Method 1: From Basic Dashboard**
```bash
# Run the basic dashboard
./utils/dash_cli.sh

# Select option 7: Enhanced Dashboard
```

### **Method 2: Direct Launch**
```bash
# Launch enhanced dashboard directly
./utils/enhanced_dash.sh
```

### **Method 3: Python Direct**
```bash
# Run Python script directly
cd /path/to/GremlinGPT
python3 utils/enhanced_dash_cli.py
```

## 📖 **Usage Guide**

### **🔧 Configuration Management**

#### **Edit Existing Configuration:**
1. Select "Configuration Manager" from main menu
2. Choose a configuration section (e.g., "system", "agents", "security")
3. Select "Edit existing key"
4. Enter key name and new value
5. Save configuration

#### **Add New Configuration Section:**
1. Go to Configuration Manager
2. Select "Add new section"
3. Enter section name
4. Add keys and values
5. Save configuration

#### **Configuration Structure:**
```toml
[system]
debug = true
log_level = "INFO"
max_threads = 4

[agents]
enable_planner = true
enable_data_analyst = true
enable_trading_strategist = true

[security]
enable_encryption = true
api_key_rotation = 24
```

### **📁 File Navigation**

#### **Navigate Directories:**
- **Numbers (1-20)**: Select file or directory
- **'up'**: Go to parent directory
- **'back'**: Return to main menu

#### **Edit Files:**
- **'edit filename.py'**: Open file in external editor
- **Select file number**: View file contents

#### **File Types Supported:**
- **Code**: `.py`, `.js`, `.sh`, `.toml`, `.yaml`, `.json`
- **Logs**: `.log`, `.jsonl`
- **Documentation**: `.md`, `.txt`
- **Configuration**: `.toml`, `.yaml`, `.yml`

### **📊 Log Monitoring**

#### **Log Categories:**
- **System**: Core system logs (runtime, bootstrap, install)
- **Modules**: Component logs (backend, nlp_engine, memory, etc.)
- **Services**: Service-specific logs
- **Applications**: Application and task logs
- **Agents**: AI agent logs

#### **Real-Time Monitoring:**
1. Select "Log Monitor & Analyzer"
2. Choose "Real-time log following"
3. Monitor live log output
4. Press Ctrl+C to stop

#### **Search Logs:**
1. Select "Search logs"
2. Enter search term
3. View results across all log files

### **🎮 System Control**

#### **Available Commands:**
- **Start GremlinGPT**: Initialize all services
- **Stop GremlinGPT**: Shutdown all services
- **Restart**: Clean restart cycle
- **Launch Unified System**: Start living AI ecosystem
- **Recovery Mode**: Emergency repair mode

## 🔧 **Advanced Features**

### **Environment Variables**
```bash
# Set your preferred editor
export EDITOR=nano    # or vim, code, etc.

# Set project root (auto-detected)
export GREMLIN_PROJECT_ROOT=/path/to/GremlinGPT
```

### **Keyboard Shortcuts**
- **Ctrl+C**: Exit current operation
- **Enter**: Confirm selections
- **Numbers**: Menu navigation
- **'back'**: Return to previous menu
- **'up'**: Navigate to parent directory

### **Terminal Compatibility**
- **Shells**: bash, zsh, fish
- **Terminals**: GNOME Terminal, xterm, iTerm2, Windows Terminal
- **Colors**: Full ANSI color support with fallback

## 🛠️ **Technical Requirements**

### **Dependencies**
- **Python 3.6+**: Core runtime
- **toml**: Configuration file parsing
- **Standard Unix tools**: tail, grep, df, ps

### **Installation**
```bash
# Install Python dependencies
pip3 install toml

# Make scripts executable
chmod +x utils/enhanced_dash.sh
chmod +x utils/enhanced_dash_cli.py
```

## 🚀 **Integration with Unified Ecosystem**

The Enhanced Dashboard seamlessly integrates with the GremlinGPT Unified Ecosystem:

### **Unified System Management**
- **Launch Control**: Start the complete living AI system
- **Status Monitoring**: Real-time ecosystem health
- **Agent Coordination**: Monitor multi-agent workflows
- **Performance Metrics**: System-wide performance tracking

### **Real-Time Adaptation**
- **Configuration Hot-Reload**: Changes applied without restart
- **Live Monitoring**: Watch the system learn and adapt
- **Dynamic Configuration**: Adjust parameters in real-time

## 📊 **Dashboard Comparison Summary**

### **Now Available Through Enhanced Dashboard:**

#### ✅ **Full File Navigation & Editing**
- Browse entire project structure
- Edit any file with external editor
- View file contents with formatting

#### ✅ **Complete Configuration Management**
- Interactive `config.toml` editing
- Type-aware value handling
- Section and key management

#### ✅ **Advanced Log Analysis**
- Real-time log streaming
- Cross-log search functionality
- Categorized log organization

#### ✅ **Comprehensive System Control**
- Full service lifecycle management
- Unified ecosystem integration
- Performance monitoring

## 🎯 **Answer to Your Question**

**Does the dash_cli allow for full file nav and config setup and log monitoring?**

### **Original `dash_cli.sh`:**
- ❌ **File Navigation**: No file browsing capabilities
- ❌ **Config Setup**: No configuration management
- ✅ **Log Monitoring**: Basic log viewing only

### **Enhanced Dashboard CLI:**
- ✅ **File Navigation**: Complete filesystem browser with editing
- ✅ **Config Setup**: Full interactive configuration management
- ✅ **Log Monitoring**: Advanced categorized monitoring with real-time streaming

## 🚀 **Quick Start**

```bash
# Launch enhanced dashboard
./utils/enhanced_dash.sh

# Or from basic dashboard, select option 7
./utils/dash_cli.sh
```

The Enhanced Dashboard CLI transforms GremlinGPT into a fully manageable system with complete administrative capabilities! 🎉
