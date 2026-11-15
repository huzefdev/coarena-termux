#!/usr/bin/env python3
import os, sys, json, urllib.request, urllib.error

if not sys.stdin.isatty() and os.path.exists("/dev/tty"):
    sys.stdin = open("/dev/tty", "r")

BASE_URL = os.environ.get("COARENA_BASE_URL", "https:" + "//coarena.ai/api/v1")
API_KEY = os.environ.get("COARENA_API_KEY")

C = "\033[1;36m"
G = "\033[1;32m"
Y = "\033[1;33m"
R = "\033[1;31m"
D = "\033[90m"
W = "\033[1;37m"
X = "\033[0m"

if not API_KEY:
    print(f"{R}[ERROR] COARENA_API_KEY missing. Run the one-line installer or check ~/.bashrc{X}")
    sys.exit(1)

def req(path, payload=None, method=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    m = method or ("POST" if payload is not None else "GET")
    r = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method=m,
    )
    try:
        with urllib.request.urlopen(r, timeout=90) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"\n{R}[HTTP {e.code}]{X} {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"\n{R}[NET ERROR]{X} {e}")
    return None

def get_live_models():
    res = req("/models")
    if res and "data" in res:
        return [m["id"] for m in res["data"] if m.get("id")]
    return ["gpt-6-1-sol", "gpt-6-astra", "gemini-4-carbon", "deepseek-v4-1-flash-1017"]

def banner(model, total_models, ctx_loaded):
    os.system("clear")
    print(f"{C}╔══════════════════════════════════════════════════╗{X}")
    print(f"{C}║{X}   {W}FUSON // COARENA AI GATEWAY{X} {D}(TERMUX CLI){X}      {C}│{X}" if False else f"{C}║{X}   {W}FUSON // COARENA AI GATEWAY{X} {D}(TERMUX CLI){X}      {C}║{X}")
    print(f"{C}╠══════════════════════════════════════════════════╣{X}")
    print(f"{C}║{X}  Active Model : {G}{model:<31}{X}  {C}║{X}")
    print(f"{C}║{X}  Live Models  : {W}{total_models} online{X}                        {C}║{X}")
    print(f"{C}║{X}  Context Sync : {Y}{'HANDOVER.md LOADED' if ctx_loaded else 'Clean Session':<31}{X}  {C}║{X}")
    print(f"{C}╚══════════════════════════════════════════════════╝{X}")
    print(f"{D}Commands: /models | /limits | /upgrade | /handover | /clear | /exit{X}\n")

def main():
    models = get_live_models()
    model = sys.argv[1] if len(sys.argv) > 1 else ("gpt-6-1-sol" if "gpt-6-1-sol" in models else models[0])
    msgs = []
    ctx_loaded = False

    if os.path.exists("HANDOVER.md"):
        with open("HANDOVER.md", "r", encoding="utf-8") as f:
            msgs.append({"role": "system", "content": f"Project Context:\n\n{f.read()}"})
        ctx_loaded = True

    banner(model, len(models), ctx_loaded)

    while True:
        try:
            prompt = input(f"{C}[{model}]{X} {W}❯{X} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{D}Session terminated.{X}")
            break

        if not prompt:
            continue
        if prompt == "/exit":
            break
        if prompt == "/clear":
            msgs = []
            print(f"{Y}[MEM] Conversation memory cleared.{X}\n")
            continue
        if prompt == "/models":
            models = get_live_models()
            print(f"\n{C}┌── LIVE ACTIVE MODELS ──────────────────────────┐{X}")
            for i, m in enumerate(models, 1):
                mark = f"{G}●{X}" if m == model else f"{D}○{X}"
                print(f"{C}│{X} {mark} {W}{i:2d}.{X} {m:<40} {C}│{X}")
            print(f"{C}└────────────────────────────────────────────────┘{X}")
            s = input(f"{Y}Select model #:{X} ").strip()
            if s.isdigit() and 1 <= int(s) <= len(models):
                model = models[int(s) - 1]
                print(f"{G}[✓] Switched to {model}{X}\n")
            continue
        if prompt.startswith("/model "):
            model = prompt.split(" ", 1)[1].strip()
            print(f"{G}[✓] Switched to {model}{X}\n")
            continue
        if prompt == "/limits":
            out = req("/limits")
            if out and "data" in out:
                d = out["data"]
                t = d.get("today", {})
                print(f"\n{C}┌── DAILY QUOTA TELEMETRY ───────────────────────┐{X}")
                print(f"{C}│{X} Daily Allowance : {G}${d.get('usd_per_day', 5)}/day{X}                       {C}│{X}")
                print(f"{C}│{X} Used Today      : {Y}${t.get('used_usd', 0):.4f}{X}                      {C}│{X}")
                print(f"{C}│{X} Remaining       : {G}${t.get('left_usd', 5):.4f}{X}                      {C}│{X}")
                print(f"{C}└────────────────────────────────────────────────┘{X}\n")
            continue
        if prompt == "/upgrade":
            out = req("/limits/requests", {"usd_per_day": 10}, method="POST")
            if out:
                msg = out.get("data", {}).get("message", "Upgrade request sent.")
                print(f"{G}[✓] {msg}{X}\n")
            continue
        if prompt == "/handover":
            if not msgs:
                print(f"{Y}[!] No conversation history to export.{X}\n")
                continue
            print(f"{D}Synthesizing HANDOVER.md...{X}")
            p = "Generate a concise technical HANDOVER.md summarizing Objective, Completed State, Key Code/Decisions, and Next Steps."
            out = req("/chat/completions", {"model": model, "messages": msgs + [{"role": "user", "content": p}]})
            if out and "choices" in out:
                with open("HANDOVER.md", "w", encoding="utf-8") as f:
                    f.write(out["choices"][0]["message"]["content"])
                print(f"{G}[✓] Exported session state to HANDOVER.md{X}\n")
            continue

        msgs.append({"role": "user", "content": prompt})
        print(f"{D}Processing...{X}", end="\r")
        out = req("/chat/completions", {"model": model, "messages": msgs})
        sys.stdout.write("\033[K")
        if out and "choices" in out:
            ans = out["choices"][0]["message"]["content"]
            msgs.append({"role": "assistant", "content": ans})
            print(f"\n{ans}\n")
        else:
            msgs.pop()

if __name__ == "__main__":
    main()
