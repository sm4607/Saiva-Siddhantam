#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turn one ASR result file into a citable transcript.

    python3 asr_to_transcript.py class.json transcript.md --title "class-17" \
        --banner "Machine transcript, not checked against the audio." --speaker "Speaker 0"

One JSON segment becomes one paragraph, stamped with the segment's end time. Paragraph 1
sits on line 10 and each later one moves by two, so pages can link to a line and trust it.
The text is left as the recogniser wrote it, apart from collapsing whitespace.
"""
import argparse
import json
import sys


def hhmmss(seconds):
    x = int(float(str(seconds).rstrip("s")))
    return f"{x // 3600:02d}:{x % 3600 // 60:02d}:{x % 60:02d}"


def segments(path):
    """[(time, text)] and the length in seconds. Empty segments are skipped."""
    with open(path, encoding="utf-8") as f:
        results = json.load(f)["results"]
    out, length = [], 0.0
    for seg in results:
        alt = (seg.get("alternatives") or [{}])[0]
        end = seg.get("resultEndTime") or (alt["words"][-1]["endTime"] if alt.get("words") else "0s")
        length = max(length, float(str(end).rstrip("s")))
        text = " ".join((alt.get("transcript") or "").split())
        if text:
            out.append((hhmmss(end), text))
    return out, int(length)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("json_file")
    ap.add_argument("out_file")
    ap.add_argument("--title", default="class transcript")
    ap.add_argument("--banner", default="Machine transcript, not checked against the audio.")
    ap.add_argument("--speaker", default="Speaker 0")
    a = ap.parse_args()
    paras, length = segments(a.json_file)
    if not paras:
        sys.exit("The file has no text. Nothing written.")
    head = (f"---\ntitle: {a.title}\nrecorded_on: unknown\nsongs: unassigned\nstatus: draft\n---\n\n"
            f"> {a.banner}\n\n")
    with open(a.out_file, "w", encoding="utf-8") as f:
        f.write(head + "\n\n".join(f"**[{t}] {a.speaker}:** {x}" for t, x in paras) + "\n")
    print(f"{len(paras)} paragraphs · {sum(len(x.split()) for _, x in paras):,} words · {hhmmss(length)}")


if __name__ == "__main__":
    main()
