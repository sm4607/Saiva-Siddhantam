# Agent skills

Operating instructions for the assistant that works on this repository. Each folder is a skill:
`SKILL.md` is what the agent reads first, and the rest are its references and scripts.

These are kept here so the method survives outside the agent — a future session, a different agent,
or a person can read them and produce the same artefacts.

| Skill | Does | Trigger |
|---|---|---|
| [`song-mindmap/`](song-mindmap/) | One mind-map page per verse, read from the 1971 commentary | "song mind map", "mind map for song N" |
| [`transcript-and-3in1/`](transcript-and-3in1/) | Merges a class JSON + TXT into a citable transcript, then builds the three-voice page for a verse | "class transcript", "3-in-1 page for song N" |

## Two rules that run through both

**The transcript comes first.** A three-voice page links every class claim to a line in the class
transcript, so the transcript must exist — with its line numbers settled — before the page is built.

**Nothing goes to `main` unshown.** A change is proposed with the file, the exact content, the branch
and the pull-request title, and waits for a yes.
