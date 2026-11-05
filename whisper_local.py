#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
whisper_local.py — transcribe a class recording on your own machine, free.

It runs faster-whisper locally and writes a JSON in the same shape the
Sarvam API returns, so the rest of the pipeline is unchanged:

    python whisper_local.py class-14.mp3 --model large-v3 --out class-14.json
    python stt_to_git.py --from-json class-14.json --date 2026-11-05 \
        --slug class-14 --songs 10,11 --keyterms terms.txt

Setup (once):

    pip install faster-whisper "av==12.3.0"

The av pin matters. A plain `pip install faster-whisper` pulls a much newer
av that breaks audio decoding with
    TypeError: open() got an unexpected keyword argument 'metadata_errors'

Models are downloaded on first use:
    tiny 75MB · base 145MB · small 480MB · medium 1.5GB · large-v3 3.1GB

For Tamil with Sanskrit technical words, only large-v3 is worth using.
No speaker labels: Whisper cannot tell your guru from you.
"""

import argparse
import json
import os
import sys
import time


def main():
    ap = argparse.ArgumentParser(description="Local transcription with faster-whisper")
    ap.add_argument("audio")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--language", default="ta")
    ap.add_argument("--compute-type", default="int8",
                    help="int8 (CPU, default) · float16 (GPU) · int8_float16")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--beam-size", type=int, default=5)
    ap.add_argument("--prompt-file", default="",
                    help="terms.txt — seeds the decoder with your vocabulary")
    ap.add_argument("--prompt-terms", type=int, default=30,
                    help="how many glossary terms to seed with (Whisper's prompt is ~224 tokens)")
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    if not os.path.exists(a.audio):
        sys.exit(f"No such file: {a.audio}")

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit('faster-whisper is not installed. Run:\n'
                 '  pip install faster-whisper "av==12.3.0"')

    prompt = ""
    if a.prompt_file and os.path.exists(a.prompt_file):
        terms = [l.strip() for l in open(a.prompt_file, encoding="utf-8")
                 if l.strip() and not l.startswith("#")]
        prompt = ", ".join(terms[:a.prompt_terms])
        print(f"Seeding the decoder with {min(len(terms), a.prompt_terms)} terms", flush=True)

    print(f"Loading {a.model} ({a.device}/{a.compute_type}) — first run downloads it …", flush=True)
    t0 = time.time()
    model = WhisperModel(a.model, device=a.device, compute_type=a.compute_type)
    print(f"  ready in {time.time()-t0:.0f}s", flush=True)

    print(f"Transcribing {a.audio} … this runs at roughly 1–6× the audio length on a CPU.", flush=True)
    t0 = time.time()
    segments, info = model.transcribe(
        a.audio,
        language=a.language or None,
        beam_size=a.beam_size,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        initial_prompt=prompt or None,
        condition_on_previous_text=False,
    )

    entries, last = [], 0.0
    for s in segments:
        text = s.text.strip()
        if text:
            entries.append({
                "transcript": text,
                "start_time_seconds": round(s.start, 2),
                "end_time_seconds": round(s.end, 2),
                "speaker_id": "0",
            })
        if s.end - last > 120:
            last = s.end
            print(f"  {int(s.end//60)} min …", flush=True)

    out = a.out or os.path.splitext(a.audio)[0] + ".json"
    payload = {
        "language_code": getattr(info, "language", a.language),
        "language_probability": round(getattr(info, "language_probability", 0) or 0, 3),
        "engine": f"faster-whisper/{a.model}",
        "diarized_transcript": {"entries": entries},
        "transcript": " ".join(e["transcript"] for e in entries),
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    mins = time.time() - t0
    print(f"\n{len(entries)} segments · audio {info.duration/60:.1f} min · took {mins/60:.1f} min "
          f"({info.duration/max(mins,1):.2f}× realtime)")
    print(f"Wrote {out}")
    if not entries:
        print("Nothing was recognised. Check that the file has speech and the language is right.")
    print("\nNext:\n  python stt_to_git.py --from-json "
          f"{out} --date YYYY-MM-DD --slug class-NN --songs 10,11 --keyterms terms.txt")


if __name__ == "__main__":
    main()
