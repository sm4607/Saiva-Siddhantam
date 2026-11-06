# எழுத்துவடிவமும் மூன்று குரல் பக்கமும் — Transcript & 3-in-1 builder

Two recurring jobs on Selva's Saiva Siddhanta repository. Load `references/procedures.md` before
starting either one — it is the full runbook, with the generator and the page anatomy.

**Triggers:** "class transcript", "merge the json and txt", "make the transcript for class N",
"3-in-1 page for song N", "three voices page", "build the page for verse N".

---

## The two jobs

| Job | In | Out |
|---|---|---|
| **A. Transcript merge** | `சித்தியார்_வகுப்பு_<N>.txt` + `.json` | `recordings/siddhiyar-class-<NN>/transcript.md`, `meta.json`, `index.html` |
| **B. 3-in-1 page** | verse text + commentary + class transcript | `three-voices/padal-<NN>-<slug>.html` |

**A comes before B. Always.** A page's third voice links to `#L<line>` in the transcript, so a card
cannot be written until its line number exists. Do not build a page against a transcript you have not
generated.

---

## Job A — in short

- The **TXT has no timings at all**; the **JSON is the clock**. Both are needed; the JSON is not
  optional.
- One JSON segment → one paragraph, stamped with the segment's **`resultEndTime`** (not the last
  word's), formatted `HH:MM:SS`, in the form `**[00:12:34] பேச்சாளர் 0:** …`, blank line between.
- Some segments arrive as `{"alternatives": [{}]}` with no transcript — use `.get()` and skip.
- Run `references/gen_md.py <N> <out.md>`.
- `duration_seconds` = max `resultEndTime`, not a guess.
- Then the class page, then the ledger row in `recordings/index.html` with paragraph and word counts.

**The line numbers are a contract.** Paragraph 1 sits on line 10 and each one after moves by two.
Pages cite `#L388`. Never insert or remove a line from a transcript that pages already cite without
re-verifying every anchor: `sed -n '388p' file` must show the timestamp the page claims.

## Job B — in short

Page order: nav · hero + chips · three-voice legend · **ASR caveat at the top** · verse + gloss ·
voice 2 tree (three branches, 3–6 cards) · voice 3 cards · meet/more · என் புரிதல் · two seeds ·
collapsed English · sources table · footer.

Hard rules:

1. **Every voice-3 claim links to its transcript line.** Header of each card is the link:
   `…/recordings/siddhiyar-class-<NN>/transcript.md#L<line>`, labelled `வகுப்பு NN · HH:MM:SS`.
2. **Two seeds per page**, `B` business and `S` science, each short, each **ending with a statement
   of where the analogy breaks**. A seed without a break is a claim; these are not claims.
3. **The English block repeats both seeds and both breaks.**
4. **என் புரிதல் is the maker's reading**, marked as such — never as the book's.
5. **One nav for every page**, written once and injected, `class="here"` on the current one.
6. If a verse has no honest transferable structure, say so and ship no seed.

## File names

| Artefact | Path |
|---|---|
| Transcript | `recordings/siddhiyar-class-<NN>/transcript.md` |
| Class page | `recordings/siddhiyar-class-<NN>/index.html` |
| Song page | `three-voices/padal-<NN>-<slug>.html` |

Slugs: lowercase, hyphens, transliterated Tamil, short — `muvakai-alavai`, `paakupaadu`.

## Checks, both jobs

- [ ] `s.count("<div") == s.count("</div>")`
- [ ] `"[cite:" not in s` — markers are for chat, never for files
- [ ] Every `#L<line>` resolves, and that line carries the stated timestamp
- [ ] No placeholder text left in the output
- [ ] Transcript: paragraph count and first/last timestamp plausible for the class length

## Never

- **Never put words in the Guru's mouth.** Paraphrase; quote only lines you can point at, and say
  they are draft ASR.
- **Never present a draft transcript as verified.** The audio has not been checked; every page and
  transcript says so.
- **Never let the artefact read as a replacement for the class.** It is a companion.
- **Never write to the repository without permission.** Show the file, the exact content, the branch
  and the PR title; commit to a branch, never to `main`.

## References

- `references/procedures.md` — the full runbook: generator, output format, page anatomy, registration
  steps, and the traps that cost time.
- `references/gen_md.py` — the transcript generator, ready to run.
