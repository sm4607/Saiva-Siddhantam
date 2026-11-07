# Book 3 workflow: Steps 1 to 4

What has to happen for each song and class of சிவஞான சித்தியார் சுபக்கம், in order. This file lists the
steps. The detailed method is in the guides linked from each step.

Paths below start from `Gnanam Maragam/Book3-Sivagnana-Siddhiyar-Supakkam/`, except `tools/` and
`docs/`, which start from the repository root.

| Step | Input | Output | Guide |
|---|---|---|---|
| 1 | Source PDF | 1.1 mind map per song · 1.2 review words · 1.3 glossary | [song-mindmap](song-mindmap/SKILL.md) |
| 2 | The Guru's class, as an mp3 converted to a transcript | 2.1 corrected transcript · 2.2 approved words added to 1.2 and 1.3 | [transcript-and-3in1, Job A](transcript-and-3in1/SKILL.md) |
| 3 | 1.1 + 2.1 | 3.1 three-in-one page per song, with business and science seeds | [transcript-and-3in1, Job B](transcript-and-3in1/SKILL.md) |
| 4 | Seeds you pick from 3.1 | A specific business proposal | No guide yet |

## Rules for every step

- A song gets its three-in-one page only after Step 2 is complete for the classes that teach it.
- There is one three-in-one page per song, never one per class.
- `three-voices/class-verse-map.html` is the source for which class teaches which song.
- Classes are added one at a time, as you listen to each class.
- Nothing is merged to `main` until you say so. A push to `main` publishes the site.

## Step 1: From the book to a song

Do this once per song. It does not depend on any class.

1. Read the verse and its commentary in the 1971 PDF. The PDF page is the book page plus 34.
2. Check the verse text and every quoted word against the scan.
3. Build the mind map at `<NN>-<slug>/index.html`, in the same format as the other songs.
4. Add the song to the Book 3 `index.html` and `README.md`, and update the `பாடல் N / TOTAL` chips on the mind-map pages.
5. Run `python3 tools/class_terms.py song N` to list candidate words in `song-words/song-NN.tsv`.
6. Fill in each meaning from the book, and write yes or no against each word.
7. Decide which words go in the glossary. The default is yes for philosophical terms and names.
8. Run `python3 tools/class_terms.py learn N`, which adds the words to `terms-master.tsv` and rebuilds `terms.txt` and `kalaisol-agarathi.md`.

**Done when:** the page is checked against the book, the words are learned, and `check` reports all clean.

## Step 2: From the class to a corrected transcript

Do this once per class, as you listen to it.

1. Convert the mp3 with the external tool. Save the JSON and TXT in `~/Downloads/Sivagana-Siddhiyar-mp3-transcript/`.
2. Run `python3 tools/class_terms.py new-class N` to build the transcript, class page and list rows.
3. Run `python3 tools/class_terms.py propose N` to list known misheard words in `corrections.tsv`.
4. Run `python3 tools/class_terms.py review N`, then add any new misheard words from `review.md` to `corrections.tsv`.
5. Decide the doubtful rows: write yes or no. Rows marked `auto` need no decision.
6. Run `python3 tools/class_terms.py apply N`. This fixes the text and learns the new forms.
7. Give any new word a meaning in `terms-master.tsv`, then run `sync`.
8. Run `review N` again so the sheet reflects the fixes.
9. Add the class to `three-voices/class-verse-map.html`, and set `songs` in `meta.json` and `transcript.md`.

**Done when:** no row in `corrections.tsv` has an empty decision, the class is in the map, and `check` reports all clean.

Correction covers key terms only. Other recognition errors stay in the transcript, and the audio remains the authority.

## Step 3: From song and classes to the three-in-one page

Do this once per song, after Steps 1 and 2 are complete for that song.

1. Use the map to find every class that teaches the song.
2. Read those classes and pick the points worth citing.
3. Build `three-voices/padal-<NN>-<slug>.html` in the same format as the other pages: verse, commentary tree, class cards, where they meet, என் புரிதல், seeds and sources.
4. Link every class card to its transcript line, and check that line shows the same timestamp.
5. Write one business seed and one science seed. Each must say where the analogy breaks.
6. Add the page to the navigation on every three-in-one page and the map, and to the Book 3 `index.html`.

**Done when:** every card links to the right line, each seed states its break, and `check` reports all clean.

## Step 4: From seeds to a business proposal

There is no guide for this step yet. These are the steps as agreed so far.

1. Pick the seeds you want to take further from the three-in-one pages.
2. Record which seeds you picked and why.
3. Write a specific business proposal from them.
4. Add it to `vanika-inai/` and list it in the Book 3 `index.html`.

**Done when:** you have approved the proposal. The format is still to be decided.

## Where things stand (2026-11-07)

| Step | Done | Next |
|---|---|---|
| 1 | Mind maps for songs 1–13 · 119 words in the master list, 118 confirmed · glossary built from it | Song 14 |
| 2 | Classes 1–16 corrected for key terms | Class 17, then on to class 25 as you listen. Source files for all 25 are ready |
| 3 | Pages for songs 1–12 | Song 13, once its classes from 17 onward are corrected |
| 4 | 24 seeds available · two வணிக இணை documents | Pick seeds, and agree the proposal format |

Open items:

- **Step 1:** விட்டுணு is still only proposed, so it is not in the glossary.
- **Step 2:** the song numbers for classes 1–5 in the map come from what the pages cite, not from reading those classes.
- **Step 3:** the pages for songs 1–12 were built before Step 2 finished. None of the corrected wrong forms remain in them, apart from மெய்கண்டதேவர் written without a space on the song 3 pages, but the pages have not been reread against the corrected transcripts.
- **Step 3:** the map gives class 9 to songs 7 and 8, and class 16 to song 12, but those pages do not yet use either class.
