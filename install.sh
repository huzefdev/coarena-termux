#!/data/data/com.termux/files/usr/bin/bash
B="\033[38;5;130m"
A="\033[1;38;5;214m"
M="\033[38;5;172m"
X="\033[0m"
clear
echo -e "${B}╭──────────────────────────────────────────╮${X}"
echo -e "${B}│${X} ${A}FUSON // COARENA INSTALLER${X}  ${M}by huzef dev${X} ${B}│${X}"
echo -e "${B}╰──────────────────────────────────────────╯${X}"
command -v python3 >/dev/null || (echo -e "${M}[*] installing python...${X}" && pkg update -y && pkg install -y python)
mkdir -p "$HOME/bin"
echo -e "${M}[*] fetching cli...${X}"
curl -sL "https://raw.githubusercontent.com/huzefdev/coarena-termux/main/src/cli.py" -o "$HOME/bin/coarena"
chmod +x "$HOME/bin/coarena"
echo -e "\n${B}╭─ api key setup ──────────────────────────╮${X}"
echo -e "${B}│${X} ${M}1. open coarena.ai/account/api/keys${X}      ${B}│${X}"
echo -e "${B}│${X} ${M}2. paste key (coa_...) below${X}             ${B}│${X}"
echo -e "${B}╰──────────────────────────────────────────╯${X}\n"
printf "${A}coarena :: key ❯ ${X}"
read -r K </dev/tty
[ -z "$K" ] && echo -e "\n${M}[✗] aborted.${X}" && exit 1
sed -i "/COARENA_/d;/HOME\/bin/d" "$HOME/.bashrc"
printf "export COARENA_API_KEY=\"%s\"\nexport COARENA_BASE_URL=\"https://coarena.ai/api/v1\"\nexport PATH=\"\$HOME/bin:\$PATH\"\n" "$K" >> "$HOME/.bashrc"
echo -e "\n${B}╭──────────────────────────────────────────╮${X}"
echo -e "${B}│${X} ${A}[✓] setup complete. run: coarena${X}         ${B}│${X}"
echo -e "${B}╰──────────────────────────────────────────╯${X}"
