#!/data/data/com.termux/files/usr/bin/bash
B="\033[38;5;240m"
A="\033[38;5;179m"
W="\033[1;37m"
D="\033[38;5;244m"
X="\033[0m"
clear
echo -e "${B}╭────────────────────────────────────────────╮${X}"
echo -e "${B}│${X} ${A}FUSON${X} ${W}coarena installer${X}      ${D}by huzef dev${X}  ${B}│${X}"
echo -e "${B}╰────────────────────────────────────────────╯${X}"
command -v python3 >/dev/null || (echo -e "${D}[*] installing python...${X}" && pkg update -y && pkg install -y python)
mkdir -p "$HOME/bin"
echo -e "${D}[*] fetching cli...${X}"
curl -sL "https://raw.githubusercontent.com/huzefdev/coarena-termux/main/src/cli.py" -o "$HOME/bin/coarena"
chmod +x "$HOME/bin/coarena"
echo -e "\n${B}╭─ api key setup ────────────────────────────╮${X}"
echo -e "${B}│${X} ${D}1.${X} ${W}open coarena.ai/account/api/keys${X}        ${B}│${X}"
echo -e "${B}│${X} ${D}2.${X} ${W}paste key (coa_...) below${X}               ${B}│${X}"
echo -e "${B}╰────────────────────────────────────────────╯${X}\n"
printf "${D}[${X}${A}coarena${X}${D}]${X} ${A}❯${X} "
read -r K </dev/tty
[ -z "$K" ] && echo -e "\n${D}[aborted]${X}" && exit 1
sed -i "/COARENA_/d;/HOME\/bin/d" "$HOME/.bashrc"
printf "export COARENA_API_KEY=\"%s\"\nexport COARENA_BASE_URL=\"https://coarena.ai/api/v1\"\nexport PATH=\"\$HOME/bin:\$PATH\"\n" "$K" >> "$HOME/.bashrc"
echo -e "\n${B}╭────────────────────────────────────────────╮${X}"
echo -e "${B}│${X} ${A}✓${X} ${W}setup complete. run:${X} ${A}coarena${X}             ${B}│${X}"
echo -e "${B}╰────────────────────────────────────────────╯${X}"
