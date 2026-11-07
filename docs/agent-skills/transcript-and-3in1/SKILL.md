# எழுத்துவடிவமும் மூன்று குரல் பக்கமும் — Transcript & 3-in-1 builder

Two recurring jobs on Selva's Saiva Siddhanta repository. Load `procedures.md` before
starting either one — it is the full runbook, with the generator and the page anatomy.

**Triggers:** "class transcript", "merge the json and txt", "make the transcript for class N",
"3-in-1 page for song N", "three voices page", "build the page for verse N".

---

## The two jobs

| Job | In | Out |
|---|---|---|
| **A. Class transcript** | `சித்தியார் வகுப்பு <N>.json` | `recordings/siddhiyar-class-<NN>/transcript.md`, `meta.json`, `corrections.tsv`, `review.md`, `index.html` |
| **B. 3-in-1 page** | verse text + commentary + class transcript | `three-voices/padal-<NN>-<slug>.html` |

**A comes before B. Always.** This is Step 2 before Step 3: a song gets its page only when the classes
that teach it are in the repository and corrected. A page's third voice links to `#L<line>` in the
transcript, so a card cannot be written until its line number exists. One page per song, never per
class. `three-voices/class-verse-map.html` says which classes teach which song.

---

## Job A — in short

Run everything from the repository root. `tools/class_terms.py` does the work.

```
python3 tools/class_terms.py new-class 17   # build the class from its ASR json
python3 tools/class_terms.py propose 17     # known misheard forms -> corrections.tsv
(write yes or no on rows with an empty decision)
python3 tools/class_terms.py apply 17       # fix the text, learn the new forms
python3 tools/class_terms.py review 17      # write review.md from the master list
python3 tools/class_terms.py check          # confirm everything still agrees
```

- `new-class` reads `சித்தியார் வகுப்பு <N>.json` from `~/Downloads/Sivagana-Siddhiyar-mp3-transcript`.
  It writes the transcript, class page and `meta.json`, links the previous class, and adds the
  recordings and Book 3 list rows.
- `review` and `propose` work from `terms-master.tsv`, the one master word list. Never use a fixed
  list. Every approved word goes to the list; a yes or no decides whether it also goes in the
  glossary, defaulting to yes.
- Only rows marked `yes` or `auto` change text. Doubtful rows go to the user. A sound-alike can be a
  different word, so check the context, and use the book scan where the word is doubtful.
- After listening, add the class to `three-voices/class-verse-map.html`, and set `songs` in
  `meta.json` and `transcript.md`.

**The line numbers are a contract.** Paragraph 1 sits on line 10 and each one after moves by two.
Pages cite `#L388`. `apply` refuses any change that moves a line or timestamp, and `check` confirms
every cited line is still a paragraph.

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
  they are ASR with only key terms corrected.
- **Never present a transcript as verified.** The audio has not been checked; every page and
  transcript says so.
- **Never let the artefact read as a replacement for the class.** It is a companion.
- **Never write to the repository without permission.** Show the file, the exact content and the
  branch; commit to a branch, and merge to `main` only when told to.

## References

- `procedures.md` — the full runbook: output format, page anatomy, and the traps that cost time.
- `tools/class_terms.py` — the class and word list tool. Its opening comment lists every rule.
