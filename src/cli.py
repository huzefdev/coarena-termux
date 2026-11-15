#!/usr/bin/env python3
import os, sys, json, urllib.request, urllib.error

if not sys.stdin.isatty() and os.path.exists("/dev/tty"):
    sys.stdin = open("/dev/tty", "r")

BASE_URL = os.environ.get("COARENA_BASE_URL", "https:" + "//coarena.ai/api/v1")
API_KEY = os.environ.get("COARENA_API_KEY")

B = "\033[38;5;240m"   # Muted Slate Border
A = "\033[38;5;179m"   # Warm Metallic Gold
W = "\033[1;37m"       # Crisp White
D = "\033[38;5;244m"   # Subtle Gray
E = "\033[38;5;203m"   # Soft Coral Error
X = "\033[0m"

if not API_KEY:
    print(f"{E}[error] COARENA_API_KEY missing. Run installer or check ~/.bashrc{X}")
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
        print(f"\n{E}[http {e.code}]{X} {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"\n{E}[network error]{X} {e}")
    return None

def get_live_models():
    res = req("/models")
    if res and "data" in res:
        return [m["id"] for m in res["data"] if m.get("id")]
    return ["gpt-6-1-sol", "gpt-6-astra", "gemini-4-carbon", "deepseek-v4-1-flash-1017"]

def banner(model, total_models, ctx_loaded):
    os.system("clear")
    mem = "HANDOVER.md active" if ctx_loaded else "clean session"
    print(f"{B}╭────────────────────────────────────────────╮{X}")
    print(f"{B}│{X} {A}FUSON{X} {W}coarena gateway{X}        {D}by huzef dev{X} {B}│{X}")
    print(f"{B}├────────────────────────────────────────────┤{X}")
    print(f"{B}│{X} {D}model  :{X} {W}{model:<33}{X} {B}│{X}")
    print(f"{B}│{X} {D}nodes  :{X} {A}{total_models} online{X}                         {B}│{X}")
    print(f"{B}│{X} {D}memory :{X} {W}{mem:<33}{X} {B}│{X}")
    print(f"{B}╰────────────────────────────────────────────╯{X}")
    print(f"{D}/models  /limits  /upgrade  /handover  /clear  /exit{X}\n")

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
            prompt = input(f"{D}[{X}{A}{model}{X}{D}]{X} {A}❯{X} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{D}session closed.{X}")
            break

        if not prompt:
            continue
        if prompt == "/exit":
            break
        if prompt == "/clear":
            msgs = []
            print(f"{D}[memory cleared]{X}\n")
            continue
        if prompt == "/models":
            models = get_live_models()
            print(f"\n{B}╭─ active models ────────────────────────────╮{X}")
            for i, m in enumerate(models, 1):
                mark = f"{A}●{X}" if m == model else f"{D}○{X}"
                print(f"{B}│{X} {mark} {D}{i:2d}.{X} {W}{m:<36}{X} {B}│{X}")
            print(f"{B}╰────────────────────────────────────────────╯{X}")
            s = input(f"{D}select #:{X} ").strip()
            if s.isdigit() and 1 <= int(s) <= len(models):
                model = models[int(s) - 1]
                print(f"{A}✓{X} {D}switched to{X} {W}{model}{X}\n")
            continue
        if prompt.startswith("/model "):
            model = prompt.split(" ", 1)[1].strip()
            print(f"{A}✓{X} {D}switched to{X} {W}{model}{X}\n")
            continue
        if prompt == "/limits":
            out = req("/limits")
            if out and "data" in out:
                d = out["data"]
                t = d.get("today", {})
                print(f"\n{B}╭─ daily quota ──────────────────────────────╮{X}")
                print(f"{B}│{X} {D}allowance :{X} {W}${d.get('usd_per_day', 5)}/day{X}                        {B}│{X}")
                print(f"{B}│{X} {D}used      :{X} {A}${t.get('used_usd', 0):.4f}{X}                       {B}│{X}")
                print(f"{B}│{X} {D}remaining :{X} {W}${t.get('left_usd', 5):.4f}{X}                       {B}│{X}")
                print(f"{B}╰────────────────────────────────────────────╯{X}\n")
            continue
        if prompt == "/upgrade":
            out = req("/limits/requests", {"usd_per_day": 10}, method="POST")
            if out:
                msg = out.get("data", {}).get("message", "upgrade request sent.")
                print(f"{A}✓{X} {W}{msg}{X}\n")
            continue
        if prompt == "/handover":
            if not msgs:
                print(f"{D}[nothing to export]{X}\n")
                continue
            print(f"{D}writing HANDOVER.md...{X}")
            p = "Generate a concise technical HANDOVER.md summarizing Objective, Completed State, Key Code/Decisions, and Next Steps."
            out = req("/chat/completions", {"model": model, "messages": msgs + [{"role": "user", "content": p}]})
            if out and "choices" in out:
                with open("HANDOVER.md", "w", encoding="utf-8") as f:
                    f.write(out["choices"][0]["message"]["content"])
                print(f"{A}✓{X} {D}saved to{X} {W}HANDOVER.md{X}\n")
            continue

        msgs.append({"role": "user", "content": prompt})
        print(f"{D}thinking...{X}", end="\r")
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
