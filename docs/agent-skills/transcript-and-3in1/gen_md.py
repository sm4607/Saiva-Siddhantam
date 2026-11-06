# -*- coding: utf-8 -*-
import json, io, sys, re

def secs(s):
    return float(s.rstrip("s"))

def hhmmss(x):
    x = int(x)
    return "%02d:%02d:%02d" % (x//3600, (x%3600)//60, x%60)

def build(n, out):
    d = json.load(open(f"/scratch/input/சித்தியார்_வகுப்பு_{n}.json", encoding="utf-8"))["results"]
    head = (f"---\ntitle: siddhiyar-class-{n:02d} — class transcript\n"
            f"recorded_on: unknown\nsongs: []\nstatus: draft\n---\n\n"
            "> இது ஒரு வகுப்பின் எழுத்துவடிவம். தானியங்கியாக எடுக்கப்பட்டது, சொற்கள் திருத்தப்படவில்லை. "
            "தவறுகள் இருக்கலாம் — ஒலியே முதன்மை.\n\n")
    body = []
    for seg in d:
        alt = seg["alternatives"][0]
        t = (alt.get("transcript") or "").strip()
        if not t:
            continue
        end = seg.get("resultEndTime") or (alt["words"][-1]["endTime"] if alt.get("words") else "0s")
        body.append(f"**[{hhmmss(secs(end))}] பேச்சாளர் 0:** {t}")
    io.open(out, "w", encoding="utf-8").write(head + "\n\n".join(body) + "\n")
    return len(body)

if __name__ == "__main__":
    n = int(sys.argv[1]); out = sys.argv[2]
    print(n, "segments:", build(n, out))
