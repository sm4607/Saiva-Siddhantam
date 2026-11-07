---
name: text-mindmap
description: Build a one-page mind map of a verse, sutra or passage from its printed commentary, with a branch tree, flow strip, commentary panels and a marked personal reading. Use whenever the user asks for a mind map, song or verse page, a new song such as song 14, or wants a commentary laid out in the same format as existing pages, even if they only say "do the next song".
---

# Text mind map

One page per verse, drawn from the printed source. The page is only useful if a reader can trust that
the text is the book's and can see which voice is speaking.

In this repository, read `docs/agent-skills/song-mindmap/SKILL.md` and `authoring-guide.md` first. They
hold the book's page mapping, OCR traps and registration steps. This skill is the method for any text.

## Page order

Title and standfirst · chips · verse with a prose gloss · branch tree · flow strip · commentary panels ·
a personal reading, marked as such · footer with edition and page range.

## Reading the source

1. **Locate** the passage with the searchable text. OCR is for finding, not for quoting.
2. **Bound** it: from its heading to the next heading. Read all of it before writing.
3. **Verify** every word you quote against the scan. Check the printed page number the first time.
4. **Note the shape:** clause structure, numbered notes, lists of four or more, worked examples.

If a word stays doubtful, use the form the commentary itself glosses and say so in the footer. Do not
resolve it to the more familiar reading; that is how one wrong word changes the doctrine.

## Turning a verse into a tree

- Let the verse draw its own branches. Verses often announce their structure, so find that first.
- Follow the verse's argument, not the commentary's word-by-word order.
- Use three branches by default, with 3–6 cards each. Four columns are too narrow for Tamil. If a
  verse truly has two halves, the third branch can come from a commentator's note, and say so.
- Lists of four or more go in tables. Cards are for concepts, tables for inventories.
- The flow strip is the verse's own progression, labelled by line. If its three cells are not a
  progression, the split is wrong.

## Keeping the voices apart

- Verse and gloss are the book. Panels are the commentator. The reading is the maker's, and it is
  labelled so.
- Never invent dates, cross-references or "as the tradition holds".
- Keep the commentator's silences. If the commentary says nothing on a term, say nothing.
- Keep printed spellings, even odd ones. Rebuild verse lines but keep the words.

## Building it

Use data plus a renderer, not hand-written HTML, so every page stays in one design. Fill one dict per
verse and call `render()` from `scripts/build_lib.py`.

- `source_label` and `insight_label` set the two fixed labels for another text.
- Do not call `str.format()` on a string containing CSS. Use `.replace("{title}", ...)`.
- Branch colour follows position, so dict order is visual order.
- After building, check that `<div` and `</div>` counts match.

## After the page

Add it to the index and README, and update the progress chips on every mind-map page with a regex. Then
use the `term-list-builder` skill to add its words. A new mind map does not mean its three-voice page
is due; that waits for the classes.

## Done when

The text is verified against the scan, doubtful words are flagged, and the page and its words are
registered.
