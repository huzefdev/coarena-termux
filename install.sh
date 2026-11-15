#!/data/data/com.termux/files/usr/bin/bash
C="\033[1;36m"
G="\033[1;32m"
Y="\033[1;33m"
R="\033[1;31m"
W="\033[1;37m"
X="\033[0m"

clear
echo -e "${C}╔══════════════════════════════════════════════════╗${X}"
echo -e "${C}║${X}   ${W}FUSON // COARENA AI ENGINE (TERMUX EDITION)${X}    ${C}║${X}"
echo -e "${C}╚══════════════════════════════════════════════════╝${X}"

if ! command -v python3 &> /dev/null; then
    echo -e "${Y}[*] Installing lightweight Python runtime...${X}"
    pkg update -y && pkg install -y python
else
    echo -e "${G}[✓] Python runtime verified.${X}"
fi

mkdir -p "$HOME/bin"
echo -e "${Y}[*] Fetching Coarena HUD CLI...${X}"
curl -sL "https://raw.githubusercontent.com/huzefdev/coarena-termux/main/src/cli.py" -o echo -e "\n\033[1;32m[✓] Ready! Run: coarena\033[0m"
chmod +x echo -e "\n\033[1;32m[✓] Ready! Run: coarena\033[0m"

echo ""
echo -e "${C}┌── API KEY CONFIGURATION ─────────────────────────┐${X}"
echo -e "${C}│${X} 1. Create a free account: ${W}coarena.ai/account/api${X} ${C}│${X}"
echo -e "${C}│${X} 2. Generate & copy your API key (${W}coa_...${X})         ${C}│${X}"
echo -e "${C}└──────────────────────────────────────────────────┘${X}"
echo ""
read -p "❯ Paste your Coarena API Key: " USER_KEY </dev/tty

if [[ -z "$USER_KEY" ]]; then
    echo -e "${R}[✗] No API key provided. Installation aborted.${X}"
    exit 1
fi

sed -i "/COARENA_/d" "$HOME/.bashrc"
sed -i "/HOME\/bin/d" "$HOME/.bashrc"

cat << EOB >> "$HOME/.bashrc"
export COARENA_API_KEY="$USER_KEY"
export COARENA_BASE_URL="https://coarena.ai/api/v1"
export PATH="\$HOME/bin:\$PATH"
EOB

export COARENA_API_KEY="$USER_KEY"
export COARENA_BASE_URL="https://coarena.ai/api/v1"
export PATH="$HOME/bin:$PATH"

echo ""
echo -e "${G}[✓] Installation complete! Launching Coarena HUD...${X}"
sleep 1
echo -e "\n\033[1;32m[✓] Ready! Run: coarena\033[0m"
