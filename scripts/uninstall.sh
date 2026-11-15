#!/data/data/com.termux/files/usr/bin/bash
rm -f "$HOME/bin/coarena"
sed -i "/COARENA_/d" "$HOME/.bashrc"
echo "[✓] Coarena Termux CLI removed cleanly."
