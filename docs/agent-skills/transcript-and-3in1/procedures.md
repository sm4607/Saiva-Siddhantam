# Build procedures — class transcripts and the 3-in-1 song view

Two jobs that go together: turn one uploaded class into a readable, citable transcript, then build
one page per verse that puts the verse, the commentary and the class side by side.

Written from the work on verses 1–13 and classes 1–16. Follow it literally where it is specific.

---

# Part 1 — Class transcript from the ASR JSON

## 1.1 What arrives

The external tool produces two files per class, in `~/Downloads/Sivagana-Siddhiyar-mp3-transcript`:

| File | What it is |
|---|---|
| `சித்தியார் வகுப்பு <N>.txt` | The ASR text. **No timings at all.** |
| `சித்தியார் வகுப்பு <N>.json` | The raw ASR result, with text and a timing for every segment. |

`new-class` reads the JSON, because a transcript without timestamps cannot be cited.

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

## 1.4 Building the class

```
python3 tools/class_terms.py new-class 17
```

This writes `transcript.md`, `index.html` and `meta.json`, adds the next-class link to the previous
class page, and adds a row to `recordings/index.html` and the Book 3 `index.html`. It uses the
previous class page as the shell, so that class must exist. It stops if the class already exists.

## 1.5 The output, and why its line numbers matter

```
---
title: siddhiyar-class-13 — class transcript
recorded_on: unknown
songs: unassigned
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

## 1.6 Correcting a class

The master list is `terms-master.tsv`. Each word carries its misheard forms, labelled `auto` or `ask`.

```
python3 tools/class_terms.py propose 17
python3 tools/class_terms.py apply 17
python3 tools/class_terms.py review 17
```

- `propose` writes `corrections.tsv`. `auto` rows are already decided; the rest wait for a yes or no.
- To find new forms, read the near matches in `review.md`, then add rows to `corrections.tsv` by hand.
  Check each one in its sentence. Mark it `book` if the book or a song page confirms the word, and
  `listen` if only the audio can settle it.
- `apply` changes only `yes` and `auto` rows. A form is learned as `auto` only if the row is
  book-backed and at least one of its words is not a real word. Everything else stays `ask`.
- A row with an empty `term` fixes that line only and teaches the list nothing. Use it for everyday
  words, such as அதிகம் for இதிகம் in class 9.
- `apply` warns if a song or three-in-one page still has the wrong form. It never edits those pages.
- Correcting covers key terms only. Other recognition errors stay, and the banner says so.

`review.md` has four useful parts: known errors, near matches, absent words, and every word the
recogniser scored below 0.55 confidence, with its time, so the audio is played only at those seconds.

## 1.7 Mapping the class to its songs

Do this after listening. Add a row to `three-voices/class-verse-map.html`, then set `songs` in
`meta.json` and `transcript.md`. `check` reports a page that cites a class not mapped to its song.

## 1.8 Checks before it is called done

- [ ] Paragraph count and first and last timestamp look right for the class length
- [ ] No rows left with an empty decision in `corrections.tsv`
- [ ] `review.md` written from the master list
- [ ] Class added to the map, and `songs` set
- [ ] `python3 tools/class_terms.py check` reports all clean

---

# Part 2 — The 3-in-1 view, one page per song

## 2.1 What it is

This is Step 3. Build a page only when the classes that teach the song are in the repository and
corrected, and use the map to find them. One self-contained HTML page per verse, never per class, at
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
4. **Caveat** — the ASR warning, at the top and not only in the footer. Say which classes the page
   uses, and if the teaching continues in a class not yet in the repository, say that too
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

Every page carries the identical nav — one link per three-in-one page, then the map, then seeds, sources and
the repository — with `class="here"` on the current one. Navs built page by page drift, and a reader
arriving at verse twelve then cannot reach verse one. Write the nav once and inject it into every
file; do not hand-write it per page.

## 2.6 Build method

Data plus a renderer, not hand-written HTML. One dict per verse (verse lines, gloss, tree, cards with
their `(timestamp, line)` pairs, meet/more, mine, seeds, English, sources). Reuse the stylesheet from
the existing pages so all the pages stay in one visual system.

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

- **Never put words in the Guru's mouth.** Paraphrase the points; quote only lines you can point at
  in the transcript, and say they are ASR with only key terms corrected.
- **Never present a transcript as verified.** Every page and every transcript says the audio
  has not been checked.
- **Never let the artefact read as a replacement for the class.** It is a companion; say so on the
  page and in the commit message.
- **Never resolve a doubtful word into the more familiar reading.** Crop the scan instead.
- **Never write to the repository without permission.** Show the file, the exact content and the
  branch first; then commit to a branch, and merge to `main` only when told to.
