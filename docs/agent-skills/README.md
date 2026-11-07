# Agent skills

Operating instructions for the assistant that works on this repository. Each folder is a skill:
`SKILL.md` is what the agent reads first, and the rest are its references and scripts.

These are kept here so the method survives outside the agent: a future session, a different agent,
or a person can read them and produce the same artefacts.

| Skill | Does | Trigger |
|---|---|---|
| [`song-mindmap/`](song-mindmap/) | One mind-map page per verse, read from the 1971 commentary, and its words for the master list | "song mind map", "mind map for song N" |
| [`transcript-and-3in1/`](transcript-and-3in1/) | Adds and corrects a class transcript, then builds the three-voice page for a verse | "class transcript", "3-in-1 page for song N" |

## The four steps

| Step | Input | Output |
|---|---|---|
| 1 | Source PDF | 1.1 mind map per song · 1.2 review words (`terms-master.tsv`) · 1.3 glossary (`kalaisol-agarathi.md`) |
| 2 | The Guru's class, converted to a transcript by an external tool | 2.1 corrected transcript · 2.2 approved words added to 1.2, and appropriate ones to 1.3 |
| 3 | 1.1 + 2.1 | 3.1 the three-in-one view, with business and science sightings |
| 4 | Seeds the user picks from 3.1 | A specific business proposal. The two வணிக இணை documents belong here |

## Rules that run through both

**Step 3 only after Step 2.** A song gets its three-in-one page only when the classes that teach it
are in the repository and corrected. Do not build one ahead of that.

**One three-in-one page per song, never per class.** Several classes can feed one page, and a class
need not be cited at all.

**The map is the source for mappings.** `three-voices/class-verse-map.html` says which class teaches
which song. Do not override its rows.

**Classes are done one at a time.** Classes 17 onward are added as the user listens to each class,
not as a batch.

**Nothing goes to `main` unshown.** A change is proposed with the file, the exact content and the
branch, and waits for a yes.
