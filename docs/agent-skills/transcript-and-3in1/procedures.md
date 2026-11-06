# Build procedures — class transcripts and the 3-in-1 song view

Two jobs that go together: turn one uploaded class into a readable, citable transcript, then build
one page per verse that puts the verse, the commentary and the class side by side.

Written from the work on verses 1–13 and classes 1–16. Follow it literally where it is specific.

---

# Part 1 — Class transcript from a JSON + TXT pair

## 1.1 What arrives

Each class is uploaded as two files with the same number:

| File | What it is |
|---|---|
| `சித்தியார்_வகுப்பு_<N>.txt` | The ASR text, one paragraph per line. **No timings at all.** |
| `சித்தியார்_வகுப்பு_<N>.json` | The raw ASR result, with a timing against every word. |

**The TXT alone is not enough.** Without the JSON there are no timestamps, and a transcript without
timestamps cannot be cited — the song pages link to `#L<line>` in a transcript whose paragraphs carry
times. The TXT is the readable text; the JSON is the clock. Use both, always.

Do not assume the two files have the same number of paragraphs. They usually differ by a few.

## 1.2 What the JSON looks like

```json
{"results": [
  {"alternatives": [{"transcript": "…", "words": [{"word": "…", "startTime": "1.100s", "endTime": "2s"}, …]}],
   "resultEndTime": "218.430s"},
  …
]}
```

Two things to know before writing code:

- **Some segments are empty.** A segment can arrive as `{"alternatives": [{}], "resultEndTime": "…s"}`
  with no `transcript` key at all. `alt["transcript"]` raises `KeyError`. Use `alt.get("transcript")`
  and skip blanks.
- **`resultEndTime` is the paragraph's clock**, not the last word's `endTime`. Prefer it, and fall
  back to the last word only when it is missing.

## 1.3 The merge rule

One JSON segment becomes one paragraph. The paragraph is stamped with the segment's **end** time,
formatted `HH:MM:SS`, and prefixed in the repository's existing style:

```
**[00:12:34] பேச்சாளர் 0:** <segment text>
```

Blank line between paragraphs. Nothing else is added — no punctuation repair, no merging of short
segments, no reflowing. The text is a draft and says so in the header.

## 1.4 The generator

Save as `gen_md.py`; run `python3 gen_md.py <N> <out.md>`.

```python
# -*- coding: utf-8 -*-
import json, io, sys

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
    print(build(int(sys.argv[1]), sys.argv[2]), "segments")
```

## 1.5 The output, and why its line numbers matter

```
---
title: siddhiyar-class-13 — class transcript
recorded_on: unknown
songs: []
status: draft
---

> இது ஒரு வகுப்பின் எழுத்துவடிவம். …

**[00:00:25] பேச்சாளர் 0:** …
                                             ← blank line
**[00:00:37] பேச்சாளர் 0:** …
```

Because of the header, blank lines and the seven-line front matter, **paragraph 1 sits on line 10 and
each paragraph after it moves by two.** The song pages link to these line numbers
(`transcript.md#L388`), so the format is a contract:

- Never insert or remove a line without re-checking every anchor into that file.
- Never regenerate a transcript that pages already cite without re-verifying the anchors afterwards.
  Check by printing the timestamp at the cited line: `sed -n '388p' <file>` must show the time the
  page claims.

## 1.6 The keyterm review — `review.md`

A QA sheet over **fifty fixed keyterms**, run against the transcript. Same list for every class —
the union of the five original reports is fifty and so is the intersection, so there is nothing
per-class to recover.

Four sections:

| Section | Rule |
|---|---|
| சிதைந்திருக்கலாம் | the term does not appear verbatim, but a near-match does at similarity **≥ 0.82** — report the correct term, what the ASR wrote, and the score |
| வரவே இல்லை | no near-match either |
| சரியாக வந்தவை | appears verbatim |
| குறைந்த நம்பிக்கை | every word with confidence **< 0.55**, with its timestamp |

Generate with `references/gen_review.py <N> <out.md>`. The similarity cut of 0.82 is calibrated
against the original reports, whose lowest listed score is 0.82; the confidence cut of 0.55 puts
roughly 8% of words in the listening table, which matches the originals.

Then set `"keyterms_used": 50` in `meta.json`. A zero is the fingerprint of a skipped pass.

## 1.7 `meta.json`

Same shape as the existing classes. Fill `duration_seconds` from the JSON, not by guessing:

```python
dur = max(float(s["resultEndTime"][:-1]) for s in results if s.get("resultEndTime","").endswith("s"))
```

```json
{
  "slug": "siddhiyar-class-13", "date": "unknown", "songs": [], "status": "draft",
  "source_file": "சித்தியார்_வகுப்பு_13.txt", "audio_file": "சித்தியார் வகுப்பு 13.mp3",
  "audio_committed": false, "source_channel": "https://www.youtube.com/@KarkaUyarValluvam",
  "source_url": "", "model": "platform upload (json segments re-timed)", "mode": "codemix",
  "language": "ta-IN", "diarization": true, "keyterms_used": 0,
  "duration_seconds": 3463, "generated_at": "…"
}
```

## 1.8 The class page

One page per class at `recordings/siddhiyar-class-<NN>/index.html`, built to the same shell as the
existing five: site header, hero with the class number, pager to the previous and next class, a
ledger row showing paragraph and word counts, the draft note, then the transcript as
`<p><span class="ts">HH:MM:SS</span>text</p>`.

Word and paragraph counts go in `recordings/index.html` too, so compute them once:

```python
paras = len(re.findall(r"\*\*\[([\d:]+)\] பேச்சாளர் 0:\*\*\s*(.+)", md))
words = sum(len(t.split()) for _, t in re.findall(r"\*\*\[([\d:]+)\] பேச்சாளர் 0:\*\*\s*(.+)", md))
```

## 1.9 Register the class

Append a row to the ledger in `recordings/index.html` and bump its count:

```html
<a class="row" href="siddhiyar-class-13/index.html">
  <div class="num">13</div>
  <div class="t">சித்தியார் வகுப்பு 13<small>291 பத்திகள் · 3,425 சொற்கள்</small></div>
  <div class="go">திறக்க →</div>
</a>
```

## 1.10 Checks before it is called done

- [ ] Paragraph count and first/last timestamp look right for the class length
- [ ] No empty paragraphs, no `KeyError` survivors, no `None` in the text
- [ ] `duration_seconds` roughly matches the last timestamp
- [ ] `sed -n '<L>p' transcript.md` returns the paragraph the song page cites
- [ ] `review.md` written and `keyterms_used` set to 50 in `meta.json`
- [ ] Ledger row added and the count bumped

---

# Part 2 — The 3-in-1 view, one page per song

## 2.1 What it is

One self-contained HTML page per verse, at
`Gnanam Maragam/Book3-Sivagnana-Siddhiyar-Supakkam/three-voices/padal-<NN>-<slug>.html`.

It carries three voices and a fourth block that is the maker's:

| Voice | Whose | Source |
|---|---|---|
| 1 — மூலம் | அருணந்தி சிவாச்சாரியார் | the verse as printed in the 1971 edition |
| 2 — உரை | திரு. மு. திருவிளங்கம் | the commentary, drawn as a tree |
| 3 — வகுப்பு | கம்பவாரிதி இலங்கை திரு. ஜெயராஜ் அய்யா | the class transcript |
| — என் புரிதல் | the maker | the repository's own note, marked as such |

## 2.2 Page anatomy, in order

1. **Header nav** — the same nav on every page (see 2.5)
2. **Hero** — crumbs, title, standfirst, chips (verse, section, key counts, page range, link to the source page)
3. **Legend** — three voice cards, colour-coded terracotta / gold / teal
4. **Caveat** — the ASR warning, at the top and not only in the footer
5. **Verse block** — the lines, then a short prose gloss
6. **Voice 2** — the commentary as a branch tree: three branches, 3–6 cards each
7. **Voice 3** — cards, each headed by a **live link** to its transcript line
8. **Meet / more** — two columns: where the commentary and the class agree, and what the class adds
9. **என் புரிதல்** — marked as the maker's reading
10. **Seeds** — two, `B` business and `S` science, each with a break statement
11. **English block** — the same two seeds in English, collapsed
12. **Sources table** — every part, its source, and its confidence
13. **Footer** — verse, book, and "a companion, not a replacement"

## 2.3 The linking rule

**Every claim in the third voice must link to the line it came from.**

```html
<a class="gmeta" href="https://github.com/sm4607/Saiva-Siddhantam/blob/main/
Gnanam%20Maragam/Book3-Sivagnana-Siddhiyar-Supakkam/recordings/siddhiyar-class-13/transcript.md#L388"
   target="_blank" rel="noopener">வகுப்பு 13 · 00:34:44</a>
```

So the order of work is: **transcript first, page second.** A card cannot be written until its line
number is known. Find the line by grepping the generated `transcript.md` for the timestamp, then
confirm `sed -n '<L>p'` shows that timestamp.

## 2.4 The seeds rule

Two per page, one business and one science. They exist so a reader can see the verse's shape
recurring elsewhere — not to claim the book is business advice.

- **One idea per seed.** A paragraph or two, not a framework.
- **Always state where the analogy breaks.** A seed without a break statement is a claim, and these
  are not claims. Put it in a block of its own at the end of the seed.
- **Mark the seed as a seed**, in a standing note above them: a structural echo, not the book's
  claim, not a recommendation.
- **The English block repeats both seeds and both breaks.** A non-Tamil reader needs the break most
  of all.
- If a verse has no honest transferable structure, say so and skip the seed. A thin seed is worse
  than none.

## 2.5 The nav rule

Every page carries the identical nav — all twelve verse links, then the map, then seeds, sources and
the repository — with `class="here"` on the current one. Navs built page by page drift, and a reader
arriving at verse twelve then cannot reach verse one. Write the nav once and inject it into every
file; do not hand-write it per page.

## 2.6 Build method

Data plus a renderer, not hand-written HTML. One dict per verse (verse lines, gloss, tree, cards with
their `(timestamp, line)` pairs, meet/more, mine, seeds, English, sources). Reuse the stylesheet from
the existing pages so all thirteen stay in one visual system.

Validate after building, every time:

```python
s = open(path, encoding="utf-8").read()
assert s.count("<div") == s.count("</div>")
assert "[cite:" not in s            # markers are for chat only, never for files
assert 'class="sd-back"' in s or True
```

## 2.7 Checks before it is called done

- [ ] Three voices present and distinguishable; the caveat is at the top
- [ ] Every voice-3 card links to a real line, and that line carries the stated timestamp
- [ ] Every seed has a break statement, and the English block repeats it
- [ ] `என் புரிதல்` is marked as the maker's reading, not the book's
- [ ] Sources table names the commentary edition and page range
- [ ] Nav identical to the other pages; current page marked
- [ ] No `[cite:` strings; div counts equal; no placeholder text left

---

# Shared rules

## File names

| Artefact | Path |
|---|---|
| Class transcript | `recordings/siddhiyar-class-<NN>/transcript.md` |
| Class page | `recordings/siddhiyar-class-<NN>/index.html` |
| Song page | `three-voices/padal-<NN>-<slug>.html` |
| Mind-map page | `<NN>-<slug>/index.html` |

Slugs: lowercase, hyphens, transliterated Tamil, short — `muvakai-alavai`, `paakupaadu`,
`indiriya-maanatha`.

## Never do these

- **Never put words in the Guru's mouth.** Paraphrase his points; quote only lines you can point at
  in the transcript, and say they are draft ASR.
- **Never present a draft transcript as verified.** Every page and every transcript says the audio
  has not been checked.
- **Never let the artefact read as a replacement for the class.** It is a companion; say so on the
  page and in the commit message.
- **Never resolve a doubtful word into the more familiar reading.** Crop the scan instead.
- **Never write to the repository without permission.** Show the file, the exact content, the branch
  and the PR title first; then commit to a branch, never to `main`.
