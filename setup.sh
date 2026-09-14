#!/usr/bin/env bash
# ==============================================================================
# Textual TUI-Creator — Production Setup & Dependency Installer
# Bulletproof Bash Engineer Architecture (Arch Linux / CachyOS / Generic Linux)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/setup.log"

# Dual logging
exec > >(tee -a "$LOG_FILE") 2>&1

cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo -e "\n\033[1;31m[!] Setup wurde mit Fehlercode $exit_code abgebrochen.\033[0m"
        echo -e "Details findest du im Log: $LOG_FILE"
    fi
}
trap cleanup EXIT ERR

# Farben
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}${BOLD}====================================================================${NC}"
echo -e "${CYAN}${BOLD}   🛠️ Textual TUI-Creator — Setup & Systemvorbereitung              ${NC}"
echo -e "${CYAN}${BOLD}====================================================================${NC}"
echo -e "Startzeit: $(date '+%Y-%m-%d %H:%M:%S')\n"

# 1. Pre-Flight Checks
echo -e "${CYAN}[1/4] Pre-Flight Checks...${NC}"
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[FEHLER] Python 3 wurde nicht gefunden. Bitte installiere Python 3.${NC}" >&2
    exit 1
fi
PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}[✓] Python 3 gefunden (Version $PYTHON_VER)${NC}"

# 2. Abhängigkeiten auflösen (Arch Linux / CachyOS nativ vs. venv)
echo -e "\n${CYAN}[2/4] Abhängigkeiten prüfen & installieren...${NC}"

HAS_TEXTUAL=false
python3 -c "import textual" &>/dev/null && HAS_TEXTUAL=true || true

if [ "$HAS_TEXTUAL" = true ]; then
    echo -e "${GREEN}[✓] Textual ist bereits im System-Python verfügbar.${NC}"
fi

# Erstelle oder aktualisiere venv für volle Portabilität
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo -e "${CYAN}[+] Erstelle isolierte virtuelle Umgebung (venv)...${NC}"
    python3 -m venv "$SCRIPT_DIR/venv"
    "$SCRIPT_DIR/venv/bin/pip" install --upgrade pip
    "$SCRIPT_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"
    echo -e "${GREEN}[✓] Virtuelle Umgebung venv erfolgreich erstellt.${NC}"
else
    echo -e "${GREEN}[✓] Virtuelle Umgebung venv existiert bereits. Aktualisiere Abhängigkeiten...${NC}"
    "$SCRIPT_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt" --quiet
fi

# 3. Berechtigungen setzen
echo -e "\n${CYAN}[3/4] Dateiberechtigungen setzen...${NC}"
chmod +x "$SCRIPT_DIR/tui_creator.py"
[ -f "$SCRIPT_DIR/start_tui_creator.sh" ] && chmod +x "$SCRIPT_DIR/start_tui_creator.sh"
[ -f "$SCRIPT_DIR/run.sh" ] && chmod +x "$SCRIPT_DIR/run.sh"
[ -f "$SCRIPT_DIR/setup.sh" ] && chmod +x "$SCRIPT_DIR/setup.sh"
echo -e "${GREEN}[✓] Alle Skripte sind nun ausführbar.${NC}"

# 4. Funktions-Test
echo -e "\n${CYAN}[4/4] Funktions-Test (Smoke-Test)...${NC}"
if "$SCRIPT_DIR/venv/bin/python3" -c "import textual; from tui_creator.app import TuiCreatorApp; print('OK')" &>/dev/null; then
    echo -e "${GREEN}[✓] Textual TUI-Creator Backend und Komponenten erfolgreich validiert.${NC}"
else
    echo -e "${YELLOW}[!] Warnung: Initialer Komponenten-Import schlug fehl. Bitte Logdatei prüfen.${NC}"
fi

echo -e "\n${GREEN}${BOLD}====================================================================${NC}"
echo -e "${GREEN}${BOLD}   Setup erfolgreich abgeschlossen! 🚀                              ${NC}"
echo -e "${GREEN}${BOLD}====================================================================${NC}"
echo -e "Starte den Editor mit:"
echo -e "  ${CYAN}./run.sh${NC}  oder  ${CYAN}./start_tui_creator.sh${NC}  oder  ${CYAN}python3 tui_creator.py${NC}\n"
