# Architecture & Persistent Memory (`HANDOVER.md`)

## Zero-Dependency Design
`src/cli.py` uses only Python 3 built-in `urllib.request` and `json` modules—keeping total storage under **~70MB** on Android devices.

## Cross-Model Memory (`HANDOVER.md`)
1. Start coding with any model (e.g., `gpt-6-astra`).
2. Run `/handover` before switching models or closing Termux.
3. Launch another model (`coarena gemini-4-carbon`) in the same folder—`HANDOVER.md` is automatically loaded.
