# பாடல் மனவரைபடம் — Song mind-map authoring

One page per verse of சிவஞான சித்தியார் சுபக்கம், built from the printed commentary.

Use this whenever Selva asks for a "song mind map", a "mind map for song N", or a page for a
verse that is not yet in the repository. The full original guide is in
`authoring-guide.md` — **read it before starting a new verse**; this file is the
operating summary, not a replacement.

---

## 1. The artefact

One self-contained HTML page per verse, in this order:

1. **Eyebrow** — book · section · verse number
2. **Title** — the verse's section name
3. **Standfirst** — two or three sentences on what the verse *does*, not what it says
4. **Chips** — verse N of total · section · key counts · page range
5. **Verse card** — the printed lines, then a prose gloss (பொருள்)
6. **Branch tree** — one root, **exactly three branches**, 3–6 cards each
7. **Flow strip** — three cells showing how the verse moves across its own lines
8. **Two panels** — the commentator's குறிப்புகள் summary, and a term/grammar table
9. **என் புரிதல்** — two or three paragraphs, marked as the maker's reading
10. **Footer** — edition, commentator, page range

No external JS, no build step, inline CSS, Google Fonts only.

## 2. Source of truth

**Book:** சிவஞான சித்தியார் சுபக்கம். உரை: திரு. மு. திருவிளங்கம். யாழ்ப்பாணம் கூட்டுறவுத்
தமிழ் நூற்பதிப்பு விற்பனைக் கழகம், 1971 (second edition).

Both files are on archive.org, item `acc.no.25598SivagnanaSiddhiyarSubakkam`.

| File | Use |
|---|---|
| `Acc.No.1635-SivagananaSiddhiyaaarSupakkam-1971.pdf` — 718 pages, ~254 dpi | **Read from this.** One book page per PDF page |
| `Acc.No.25598-...-1971_djvu.txt` — OCR | Grep to locate passages fast |

**Page mapping:** PDF page = book page + 34. Verify against the printed folio the first time you
touch a page, and re-verify if you switch scans.

**Never use** `சிவஞான_சித்தியார்_சுபக்கம்_திருவிளங்கம்.pdf` — the 361-page spread scan. About
100 dpi; anything read from it is partly guessed.

**Section → verse → page.** The bracketed number in the contents list is the **verse** number,
not a page number. Verses 1–6 are the பாயிரம்; from verse 7 the ஞானபாதம் begins:

| Verse | Sub-section | Pages |
|---|---|---|
| 7 | மூவகை அளவை | 14–17 |
| 8 | மூவகையளவையின் இலக்கணம் | 17–19 |
| 9 | நிருவிகற்பம் முதலிய நால்வகைக் காட்சிகள் | 19–21 |
| 10 | பாகுபாடும் பிரமேயப் பாகுபாடும் | 21–22 |
| 11 | சிறப்பியல்பு பொதுவியல்புகளின் இலக்கணம் | 22–24 |
| 12 | இந்திரியக்காட்சி மானதக்காட்சிகளின் இலக்கணம் | 24–27 |
| 13 | தன்வேதனைக் காட்சி யோகக்காட்சியின் இலக்கணம் | 27–29 |
| 14 | தன்பொருட்டு / பிறர்பொருட்டு அனுமானங்கள் | 29– |

## 3. Reading procedure

1. **Locate** — grep the OCR text for the sub-section heading; it is one blob with no page
   markers, so byte offsets are the only handle.
2. **Bound** — a verse's commentary runs from its heading to the next numbered heading. Read the
   whole slice before writing anything.
3. **Verify** — every term you intend to quote is confirmed against the 254 dpi scan, rendered at
   400 dpi and cropped. Not optional.
4. **Note the shape** — (a) the verse's clause structure, (b) the numbered குறிப்புகள்,
   (c) every enumeration of four or more, (d) every worked example. These four decide the layout.

**Known OCR traps:** `பரஞானபஇ`→**பரஞானபதி**; `தாலுதல்`→**நாலுதல்**; a gloss truncated at
`நீக்கும்` when the text continues `நீக்கிச் சிவத்தைத் தரும்`; `நூலின்வழி` misread as `நாலின்வழி`.

**Rule:** if a word is doubtful, crop the scan. If it is still doubtful, use the form the
commentary itself glosses and say so in the footer. **Never resolve a doubtful word into the more
familiar reading** — that is how `பரஞானபதி` became `பரஞானம்`, the one error that changes doctrine
rather than spelling.

## 4. Turning a verse into a tree

1. **Let the verse draw its own branches.** Verses here announce their structure ("ஆறு என்பர் …
   மூன்றில் அடங்கிடுமே"). Find the announcement; do not impose a schema.
2. **Follow the movement, not the commentary's order.** The commentator explains word by word; the
   tree must follow the verse's argument.
3. **Three branches. Default to three.** Four only if the verse genuinely has four co-equal parts —
   and then reconsider, because a four-column Tamil layout is too narrow. A real but smaller fourth
   part goes in the flow strip or a panel.
4. **Cards, 3–6 per branch.** One term, a one-line gloss, one to three sentences, and an optional
   `n-x` line for an example, caveat or cross-reference.
5. **Enumerations of four or more are tables, never cards.** Cards for concepts, tables for
   inventories.
6. **The flow strip is the verse's own progression** — three cells labelled by line ("அடி 1 – 2").
   If the three cells are not a progression, the split is wrong.
7. **Panels are the commentator's apparatus** — left: the commentator's குறிப்புகள் in order; right: a term table,
   or a comparison against a neighbouring verse when two form a pair (verses 5/6).
8. **The insight is your reading** — open with what the verse is *doing*, close with why it matters
   for the book. `<strong>` on three or four load-bearing phrases only.

## 5. Editorial rules

- **Never invent.** No dates, no cross-references to chapters not read, no "as the tradition holds".
- **Separate the three voices.** Verse and gloss are the book. Panels are the commentator. The
  insight block is the maker, labelled என் புரிதல்.
- **Keep the commentator's silences.** If the verse has a term and the commentary says nothing,
  say nothing.
- **Quote surprising verdicts** — where the commentator rejects a view or explains why a scheme is given
  only to present others, put it in.
- **Verse lines:** four-line layout, rebuilt from the printed half-lines; do not reproduce the
  print's mid-word breaks. Keep the printed spelling even where it looks odd.

## 6. Build

Data plus renderer, never hand-written HTML. `build_lib.py` holds `CSS`, `HEAD` and
`render(song)`. One dict per verse; the schema is in the authoring guide §5.

- Never call `str.format()` on a string containing CSS — use `.replace("{title}", …)`.
- Branch colour is positional: `b1` terracotta, `b2` sage, `b3` teal — dict order is visual order.
- Validate after building: `<div>` open/close counts equal, and zero `[cite:` strings.

## 7. Repository conventions

Pages live at `Gnanam Maragam/Book3-Sivagnana-Siddhiyar-Supakkam/<NN>-<slug>/index.html`.
Slug: lowercase, hyphens, transliterated Tamil, short.

Every published page also carries, and the standalone build does not:

- a `.sd-back` style block before `</head>`, and `<a class="sd-back" href="../index.html">← பாடல்களின் பட்டியல்</a>` as the first child of `.wrap`.

Four registration edits, all mandatory:

1. **Book ledger** — append a row inside `<div class="ledger">` in the Book 3 `index.html`.
2. **README** — add the table row and bump the count line.
3. **Progress chips** — every mind-map page's `பாடல் N / TOTAL` must be bumped when TOTAL changes.
   Do it as a regex over `<NN>-<slug>/index.html`, never by hand. Three-in-one pages count their own
   total, so leave them alone.
4. **Words** — run `python3 tools/class_terms.py song N`. It writes candidates to
   `song-words/song-NN.tsv`. Fill in each meaning from the book, write yes or no, and write no in the
   glossary column to keep a word out of the glossary. Then show the user, and run `learn N`.

## 8. Pre-publish checklist

- [ ] Verse text verified word by word against the 254 dpi scan
- [ ] Every quoted term verified; doubtful ones flagged in the footer
- [ ] Exactly three branches, each 3–6 cards
- [ ] Every enumeration of 4+ is a table
- [ ] Flow strip is a progression, not a list
- [ ] Insight marked என் புரிதல் and reads as interpretation
- [ ] Footer cites edition, commentator, page range
- [ ] `div` counts equal; no `[cite:` strings
- [ ] `sd-back` present
- [ ] Ledger row, README row, README count, all chips updated
- [ ] Song words proposed, approved and learned; `check` reports all clean

## 9. Publishing

Commit to a branch with `git`, and merge to `main` and push only when told to. A push to `main`
publishes the site. Show the file, the exact content and the branch first, and get permission
before writing.

## References

- `authoring-guide.md` — the full original guide, including the OCR trap log, the
  stylesheet and the renderer. Read it before a new verse.
- `build_lib.py` — `CSS`, `HEAD`, `render(song)`.
