<div align="center">

# ⚡ FUSON // Coarena AI Termux CLI

**Run Frontier AI Models Natively on Android — Zero Root, Zero Heavy SDKs, $5–$10/Day Free**

[![Platform](https://img.shields.io/badge/Platform-Android%20(Termux)-00E5FF?style=for-the-badge&logo=android&logoColor=black)](https://termux.dev)
[![Python](https://img.shields.io/badge/Dependencies-Zero%20(Stdlib%20Only)-00C853?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

<br>

<img src="Screenshot_2026-11-15-11-38-28-43_84d3000e3f4017145260f7618db1d683.jpg" alt="FUSON HUD Banner" width="460" />

</div>

---

### 🚀 Overview

**Coarena Termux CLI** turns any Android phone into a lightweight (~70MB) AI coding terminal powered by **Coarena AI Gateway**. Switch live between frontier models (`gpt-6-1-sol`, `gpt-6-astra`, `gemini-4-carbon`, `deepseek-v4-1-flash-1017`, `grok-4-7`, `kimi-k3-1-pro`) with **$5/day free credits** (upgradeable to **$10/day**) and persistent cross-model memory via `HANDOVER.md`.

---

### 📸 Live Terminal Preview

<div align="center">
  <img src="Screenshot_2026-11-15-11-37-21-53_84d3000e3f4017145260f7618db1d683.jpg" alt="Live Model Switching & Quota Telemetry" width="360" />
</div>

---

### ⚡ Quick Start (Works on Fresh Termux)

1. Create a free account and copy your API key (`coa_...`) from **[coarena.ai/account/api/keys](https://coarena.ai/account/api/keys)** (no credit card required).
2. Open **Termux**, tap the **Copy** icon below (auto-installs `curl` & `python` if missing), and press **Enter**:

```bash
pkg update -y && pkg install -y curl python && curl -sL https://raw.githubusercontent.com/huzefdev/coarena-termux/main/install.sh | bash
```

3. Paste your `coa_...` API key when prompted, then run:

```bash
coarena
```

---

### 🛠️ Interactive CLI Commands

| Command | Description |
| :--- | :--- |
| `/models` | Fetch and switch between live active models on Coarena |
| `/model <id>` | Switch directly to a specific model (e.g., `/model gemini-4-carbon`) |
| `/limits` | View daily `$5/day` allowance, used balance, and remaining quota |
| `/upgrade` | Submit an API request to double your daily limit (`$5` → `$10/day`) |
| `/handover` | Export current session state into `HANDOVER.md` for persistent memory |
| `/clear` | Wipe active conversation history to save context tokens |
| `/exit` | Exit the CLI cleanly |

---

### 📂 Repository Structure

```text
coarena-termux/
├── install.sh              # One-line interactive Termux installer
├── src/
│   └── cli.py              # Zero-dependency Neon-Cyan HUD Python CLI
├── scripts/
│   └── uninstall.sh        # Clean removal utility
├── docs/
│   └── WORKFLOW.md         # Architecture & HANDOVER.md memory guide
├── LICENSE                 # MIT License
└── README.md               # Documentation
```

---

### 🔒 Security Notice

Third-party API gateways route inference traffic through external servers. **Never send passwords, private keys, or sensitive personal credentials** inside prompts.

---

<div align="center">
Built by <b>Huzef Dev</b> • Engineered for Low-Resource Android Workflows
</div>
