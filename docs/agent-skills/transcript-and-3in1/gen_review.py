# -*- coding: utf-8 -*-
"""Generate review.md — keyterm QA for one class — from its ASR json."""
import json, io, re, sys, difflib

LOWCONF = 0.55        # words below this are listed for listening
SIM_CUT = 0.82        # fuzzy match at or above this is reported as distorted

def hhmmss(x):
    x = int(float(str(x).rstrip("s")))
    return "%02d:%02d:%02d" % (x//3600, (x%3600)//60, x%60)

def load(n):
    d = json.load(open(f"/scratch/input/சித்தியார்_வகுப்பு_{n}.json", encoding="utf-8"))["results"]
    words, text = [], []
    for seg in d:
        for a in seg["alternatives"]:
            t = (a.get("transcript") or "").strip()
            if t: text.append(t)
            for w in (a.get("words") or []):
                if w.get("word"): words.append(w)
    return words, " ".join(text)

def keyterms():
    s = io.open("/scratch/repos/Saiva-Siddhantam/Gnanam Maragam/Book3-Sivagnana-Siddhiyar-Supakkam/"
                "recordings/siddhiyar-class-05/review.md", encoding="utf-8").read()
    dis = set(m.strip() for m in re.findall(r"^\| ([^|]+?) \|", s.split("## சிதைந்திருக்கலாம்")[1]
                                             .split("## வரவே இல்லை")[0], re.M)) - {"சரியான சொல்"}
    miss = set(m.strip() for m in re.findall(r"^- (.+)$", s, re.M))
    g = re.search(r"## சரியாக வந்தவை\n\n(.+?)\n", s)
    good = set(x.strip() for x in g.group(1).split(",")) if g else set()
    return sorted(dis | miss | good)

def candidates(words):
    toks = [w["word"].strip() for w in words if w.get("word")]
    out = set()
    for n in (1, 2, 3):
        for i in range(len(toks) - n + 1):
            out.add(" ".join(toks[i:i+n]))
    return sorted(out)

def build(n, out):
    words, text = load(n)
    terms = keyterms()
    cand = candidates(words)
    correct, doubtful, missing = [], [], []
    for t in terms:
        if t in text:
            correct.append(t); continue
        hit = difflib.get_close_matches(t, cand, n=1, cutoff=SIM_CUT)
        if hit:
            doubtful.append((t, hit[0], difflib.SequenceMatcher(None, t, hit[0]).ratio()))
        else:
            missing.append(t)
    doubtful.sort(key=lambda x: -x[2])
    low = [(w["startTime"], w["word"].strip(), w.get("confidence", 0))
           for w in words if w.get("confidence", 1) < LOWCONF]

    L = []
    L.append("# சொற்கள் — பரிசீலனை\n")
    L.append(f"மொத்தச் சொற்கள்: {len(terms)} · சரியாக வந்தவை: {len(correct)} · "
             f"சந்தேகம்: {len(doubtful)} · காணவில்லை: {len(missing)}\n")
    L.append("## சிதைந்திருக்கலாம் — ஒலியைக் கேட்டு உறுதி செய்யுங்கள்\n")
    if doubtful:
        L.append("| சரியான சொல் | ASR எழுதியது | ஒற்றுமை |")
        L.append("|---|---|---|")
        for t, h, r in doubtful:
            L.append(f"| {t} | {h} | {r:.2f} |")
    else:
        L.append("இந்தப் பதிவில் சிதைந்த சொற்கள் எதுவும் கண்டறியப்படவில்லை.")
    L.append("")
    L.append("## வரவே இல்லை\n")
    L.append("இந்தச் சொற்கள் இந்தப் பதிவில் வரவில்லை. வகுப்பில் பேசப்படவில்லை என்பதாகவோ, "
             "ASR தவறவிட்டதாகவோ இருக்கலாம்.\n")
    L.extend(f"- {m}" for m in missing)
    L.append("")
    L.append("## சரியாக வந்தவை\n")
    L.append(", ".join(correct) if correct else "—")
    L.append("")
    L.append("## குறைந்த நம்பிக்கை — இந்த இடங்களை மட்டும் கேளுங்கள்\n")
    L.append(f"ஒலிபெயர்ப்புக் கருவியே இந்த {len(low)} சொற்களில் உறுதியாக இல்லை "
             f"({LOWCONF} என்னும் நம்பிக்கை அளவுக்குக் கீழே). ஒவ்வொன்றும் நேரத்துடன் உள்ளது — "
             "ஒலியை அந்த நொடிக்குக் கொண்டு போய் ஒருமுறை கேட்டால் போதும்.\n")
    L.append("| நேரம் | சொல் | நம்பிக்கை |")
    L.append("|---|---|---|")
    for t, w, c in low:
        L.append(f"| {hhmmss(t)} | {w} | {c:.2f} |")
    L.append("")
    io.open(out, "w", encoding="utf-8").write("\n".join(L))
    return len(correct), len(doubtful), len(missing), len(low)

if __name__ == "__main__":
    n = int(sys.argv[1])
    print(n, build(n, sys.argv[2]))
