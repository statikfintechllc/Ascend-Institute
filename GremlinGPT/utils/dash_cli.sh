#!/usr/bin/env zsh

# Get the actual GremlinGPT directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
APPLOC="$(cd "$SCRIPT_DIR/.." && pwd)"
LOGDIR="$APPLOC/data/logs"

# Dash CLI for GremlinGPT
LOGFILE="$LOGDIR/dash_cli.log"
mkdir -p "$(dirname "$LOGFILE")"
exec > >(tee -a "$LOGFILE") 2>&1
set -e

# Guarantee login+interactive shell for environment, if not already started
if [[ -z "$LOGIN_SHELL_STARTED" && "$0" != "-bash" ]]; then
    export LOGIN_SHELL_STARTED=1
    exec "$SHELL" -l -i "$0" "$@"
    exit 1
fi

APP_TITLE="AscendAI: GremlinGPT v1.0.3"
SUB_TITLE="From: SFTi"

# Resolve script dir, fallback to detected apploc
APPDIR="$HOME/.local/share/applications"
START_SCRIPT="$APPLOC/run/start_all.sh"
STOP_SCRIPT="$APPLOC/run/stop_all.sh"
CHAT_SCRIPT="$APPLOC/run/cli.py"
REBOOT_SCRIPT="$APPLOC/run/reboot_recover.sh"

# Detect preferred shell (get user's shell from /etc/passwd or $SHELL), fallback to /bin/bash
USER_SHELL="$(getent passwd "$USER" | cut -d: -f7 2>/dev/null || echo "${SHELL:-/bin/bash}")"

# List of popular emulators, in order of preference
# If none found, will prompt user to install one
# If multiple found, will use the first available one
# This list can be extended with more terminal emulators as needed
# Note: This list is not exhaustive and may vary by distribution.
# It includes common terminal emulators found in most Linux distributions.
EMULATORS=(x-terminal-emulator gnome-terminal konsole xfce4-terminal lxterminal tilix mate-terminal)

function relaunch_in_terminal() {
    for TERM_APP in "${EMULATORS[@]}"; do
        if command -v "$TERM_APP" &>/dev/null; then
            if [[ "$USER_SHELL" =~ (bash|zsh) ]]; then
                exec "$TERM_APP" -- "$USER_SHELL" -ilc "$0"
            else
                exec "$TERM_APP" -- "$USER_SHELL" -ic "$0"
            fi
            exit 0
        fi
    done
    echo "[ERROR] No graphical terminal emulator found. Exiting."
    exit 1
}

# Check if we're in a terminal, if not relaunch in a graphical one, if available
if ! [ -t 0 ]; then
    relaunch_in_terminal
fi

while true; do
    clear
    UPTIME=$(uptime -p | sed 's/^up //')
    echo -e "\033[1;36m$APP_TITLE\033[0m"
    echo -e "\033[0;32m$SUB_TITLE\033[0m"
    echo -e "Up-Time: \033[1;33m$UPTIME\033[0m"
    echo ""
    echo "Choose an action:"
    echo "1) ✅ Start GremlinGPT ✅"
    echo "2) 🚫 Stop GremlinGPT 🚫"
    echo "3) 🗣️ Chat Only 🗣️"
    echo "4) ⚠️ View GremlinGPT Logs ⚠️"
    echo "5) ✌️ Exit GremlinGPT ✌️"
    echo "6) ♻️ Reboot & Recover GremlinGPT ♻️"
    echo "7) 🚀 Enhanced Dashboard (Full Navigation & Config) 🚀"
    echo -n "Select> "
    read -r CHOICE
#    echo ""  # For better readability, can be uncommented if needed
    case $CHOICE in
        1)
            bash -l "$START_SCRIPT"
            echo -e "\nGremlinGPT Launched. Press enter to continue..."
            read -r
            ;;
        2)
            bash -l "$STOP_SCRIPT"
            echo -e "\nGremlinGPT has Stopped. Press enter to continue..."
            read -r
            ;;
        3)
            echo -e "\nLaunching CLI Chat (type 'Exit' in chat to return)...\n"
            python3 "$CHAT_SCRIPT"
            echo -e "\nExited Chat. Press enter to return to menu."
            read -r
            ;;
        4)
            while true; do
                clear
                echo -e "\033[1;34m[Log Menu]\033[0m"
                echo "Select a log category to view:"
                echo ""
                echo "1) System Logs (runtime, bootstrap, install)"
                echo "2) Service Logs (component outputs)"  
                echo "3) Module Logs (individual module logs)"
                echo "4) Application Logs (task errors, data)"
                echo "5) Return to main menu"
                echo -n "Select category> "
                read -r LOG_CAT_CHOICE
                
                case $LOG_CAT_CHOICE in
                    1)
                        # System Logs
                        LOG_NAMES=(
                            "system/runtime.log"
                            "system/bootstrap.log"
                            "system/install.log"
                        )
                        LOG_CATEGORY="System"
                        ;;
                    2)
                        # Service Logs  
                        LOG_NAMES=(
                            "services/backend.out"
                            "services/frontend.out"
                            "services/nlp.out"
                            "services/memory.out"
                            "services/fsm.out"
                            "services/scraper.out"
                            "services/trainer.out"
                            "services/ngrok.out"
                        )
                        LOG_CATEGORY="Service"
                        ;;
                    3)
                        # Module Logs
                        LOG_NAMES=(
                            "backend/backend.log"
                            "core/core.log"
                            "nlp_engine/nlp_engine.log"
                            "memory/memory.log"
                            "scraper/scraper.log"
                            "trading_core/trading_core.log"
                            "agents/agents.log"
                            "executors/executors.log"
                            "tools/tools.log"
                            "utils/utils.log"
                            "self_mutation_watcher/self_mutation_watcher.log"
                            "self_training/self_training.log"
                        )
                        LOG_CATEGORY="Module"
                        ;;
                    4)
                        # Application Logs
                        LOG_NAMES=(
                            "applications/task_errors.jsonl"
                            "tests/tests.log"
                        )
                        LOG_CATEGORY="Application"
                        ;;
                    5)
                        break
                        ;;
                    *)
                        echo "[!] Invalid input. Maybe choose a real Option."
                        read -r
                        continue
                        ;;
                esac
                
                if [[ $LOG_CAT_CHOICE != 5 ]]; then
                    clear
                    echo -e "\033[1;36m[$LOG_CATEGORY Logs]\033[0m"
                    echo "Select a log to view (last 40 lines):"
                    for i in "${!LOG_NAMES[@]}"; do
                        echo "$((i+1))) $(basename "${LOG_NAMES[$i]}")"
                    done
                    echo "$(( ${#LOG_NAMES[@]} + 1 ))) Back to categories"
                    echo -n "Select log> "
                    read -r LOG_CHOICE
                    if (( LOG_CHOICE > 0 && LOG_CHOICE <= ${#LOG_NAMES[@]} )); then
                        LOG_FILE="$LOGDIR/${LOG_NAMES[$((LOG_CHOICE - 1))]}"
                        clear
                        echo -e "\n\033[1;36m[Viewing: ${LOG_NAMES[$((LOG_CHOICE - 1))]}]\033[0m"
                        echo -e "Press Enter to return to log menu...\n"
                        if [[ -f "$LOG_FILE" ]]; then
                            tail -n 40 "$LOG_FILE"
                        else
                            echo "[Info] Log file not yet created: $LOG_FILE"
                        fi
                        read -r
                    elif (( LOG_CHOICE == ${#LOG_NAMES[@]} + 1 )); then
                        continue
                    else
                        echo "[!] Invalid input. Maybe choose a real Option."
                        read -r
                    fi
                fi
            done
            ;;
        5)
            echo "Goodbye, MeatSpace operator."
            exit 0
            ;;
        6)
            bash -l "$REBOOT_SCRIPT"
            echo -e "\nGremlinGPT reboot & recovery triggered. Press enter to continue..."
            read -r
            ;;
        7)
            echo -e "\n${CYAN}🚀 Launching Enhanced Dashboard CLI...${NC}"
            echo "This provides full file navigation, config management, and advanced monitoring."
            ENHANCED_CLI="$SCRIPT_DIR/enhanced_dash.sh"
            if [ -f "$ENHANCED_CLI" ]; then
                bash "$ENHANCED_CLI"
            else
                echo -e "${RED}❌ Enhanced dashboard not found${NC}"
                echo "Please ensure enhanced_dash.sh exists in utils/"
                read -r
            fi
            ;;
        *)
            echo "[!] Invalid input. Maybe choose a real Option."
            read -r
            ;;
    esac
done
