---
name: term-list-builder
description: Build and maintain a master term list and glossary (kalaisol, கலைச்சொல் அகராதி) for a text studied through a book and recorded classes. Use whenever the user wants to create, update or check a glossary, kalaisol, word list, review words or technical terms, add words from a new song, verse or chapter, learn corrections from a class, or explain an unexplained technical term in a later passage, even if they only say "add this word" or "update the agarathi".
---

# Term list builder

A term list goes stale when it is frozen, and it drifts when the same words live in several files.
So keep one master list, generate everything else from it, and let every class and chapter teach it.

In this repository the list is `Gnanam Maragam/Book3-Sivagnana-Siddhiyar-Supakkam/terms-master.tsv`
and the tool is `tools/class_terms.py`. For another book, change `BOOK3`, `GLOSSARY_SECTIONS` and the
glossary header text at the top of the tool.

## What the master list holds

One row per term:

| Column | Holds |
|---|---|
| term | The correct spelling, as the book prints it |
| auto | Misheard forms that are safe to fix without asking |
| ask | Misheard forms that always go to the user |
| kind | term or name |
| section | The chapter or song where the word belongs |
| meaning | The glossary meaning |
| source | Where the spelling and meaning were verified |
| status | confirmed, or proposed |
| glossary | yes or no. No keeps it on the review list only |
| first_class | First class where a fix was approved |
| taught_first | Where the teacher first taught the term |
| expansion | The explanation given then, in full. Only for compressed terms |
| later_form | How the term comes back later |

Generated files, never edited by hand: the plain term list and the glossary. If someone edits the
glossary directly, `check` reports it and the next `sync` overwrites it.

## Where words come from

**From a new song or chapter** (Step 1):

1. Run `python3 tools/class_terms.py song N`. It takes bold words and mind map titles as candidates.
   They are rough, so expect to drop many.
2. Read the book, not the page. A page can paraphrase; the meaning and spelling come from the scan.
3. Fill in `meaning` and `source`, and write yes or no.
4. Keep technical terms, names, and verse words the commentary glosses. Leave out ordinary words
   and anything the book does not define here, rather than inventing a meaning.
5. Show the user the list, then run `learn N`.

**From a class** (Step 2): approved corrections teach the list. See the `lecture-transcript` skill.

**When a meaning is missing:** the word appears under a needs-a-meaning section. Add the meaning to
the master list and run `sync`.

## Rules that protect the list

- **Every approved word goes on the review list. A yes or no decides the glossary**, defaulting to
  yes for technical terms and names.
- **The book wins over a page.** If a page and the book disagree, follow the book and flag the page
  for the user. Do not silently fix either.
- **Book spelling over the familiar spelling.** ஐதிகம், not ஐதீகம், because the book prints it so.
  Crop the scan when OCR is doubtful, because OCR also misreads.
- **Keep two readings if tradition has two.** Give both, do not pick one.
- **Never guess a meaning.** Mark it as unconfirmed and say so. Say where it came from: the user's
  note, the class or the book. A note is not the same as checking the printed edition.
- **A correct meaning can still need a decision.** If a user's meaning looks factually wrong, say why
  and offer an alternative before writing it, then follow what they decide.

## Compressed terms

A teacher often explains a term at length once, then uses it later as a single word. It looks new or
thin, but it is a compressed reference, and a reader who misses that loses the thread.

When a later passage uses a term without explaining it:

1. Look it up in the list.
2. Give the full explanation again, not a summary.
3. Say where it was first taught.
4. Show where it sits in the book.
5. If it is not on the list, add it with its status.

For these terms, fill `taught_first`, `expansion` and `later_form` in the master list. A term with an
expansion appears in the glossary's compressed terms section. Cite the class and time or the book page.
Leave a field blank rather than guessing, and keep a term as `proposed` until its meaning is confirmed.

## Done when

`python3 tools/class_terms.py check` reports all clean, and any word still needing a meaning is listed
for the user.
