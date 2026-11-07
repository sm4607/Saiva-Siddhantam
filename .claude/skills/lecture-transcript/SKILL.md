---
name: lecture-transcript
description: Turn a recorded class or lecture's speech-to-text output into a citable transcript, and correct its technical terms against a master word list. Use whenever the user has a class JSON or TXT from a transcription tool, wants to add class N, asks to fix, cleanse or review a transcript, mentions misheard words or ASR errors, or wants learned corrections applied to other classes, even if they only say "do class 17".
---

# Lecture transcript

Other pages will cite this transcript by line, so its shape is a contract. Its words are machine
output, so every change has to be justified and reversible.

In this repository use `tools/class_terms.py`, and see
`docs/agent-skills/transcript-and-3in1/procedures.md`. For any other text, start with
`scripts/asr_to_transcript.py`, which makes the transcript alone.

## Building the transcript

The JSON is the clock; the TXT has no timings, so a transcript cannot be built from it.

- One segment becomes one paragraph, stamped with the segment's end time (`resultEndTime`).
- Skip empty segments. Some have no `alternatives` or no `transcript`, and some words have no
  `startTime`, so read fields defensively.
- Add nothing: no punctuation repair, no merging of short segments.
- Paragraph 1 sits on line 10, and each later one moves by two. Pages link to `#L<line>`.

```
python3 tools/class_terms.py new-class 17
```

It refuses to overwrite a class or skip a number, because the new page copies the previous one.

## Correcting it

1. `propose N` lists known misheard forms. `auto` rows are decided; the rest wait.
2. `review N` lists near matches, absent terms and low-confidence words.
3. Search for new forms: compare words not found in the book or pages against the master list, then
   read each candidate in its sentence.
4. Add rows to `corrections.tsv`. Use `book` when the book or a page confirms the word, and `listen`
   when only the audio can settle it.
5. Bring the user the doubtful rows, grouped, with the sentence and your reason. Recommend which to
   approve together, and list the unsure ones one by one.
6. `apply N`, then `review N` and `check`.

## Why the rules are what they are

- **A sound-alike can be a different word.** அருந்ததி is a real name and also a mishearing of
  அருணந்தி. So only `yes` and `auto` rows change text, and context decides.
- **Auto needs evidence.** A form becomes `auto` only if the row is book-backed and at least one of
  its words is not a real word. Real words stay `ask`, including everyday words the book lacks.
- **Learn nothing from an everyday word.** Fixing அதிகம் to இதிகம் on one line is right there, wrong
  elsewhere. Leave `term` empty so the fix stays on that line.
- **Check what the teacher is reading.** If a passage follows the book closely, the book settles the
  word, and it may not be the word you expect.
- **Saying no teaches too.** Refusing or undoing a fix moves that form back to `ask`.
- **Line numbers never move.** Replace words inside their line. `apply` stops if a line or timestamp
  would change.
- **Pages are not edited automatically.** `apply` warns if a page has the wrong form; the user decides.

## Honesty about the result

Correction covers key terms only. Say "term-corrected", never "clean" or "verified", and keep the
banner accurate. The audio stays the authority.

## Mapping

Which class teaches which song comes from the user's class map. Do not guess a song number from a
transcript. If a class needs a row, ask, or mark how you derived it.

## Done when

No row has an empty decision, the class is in the map, and `check` reports all clean.
