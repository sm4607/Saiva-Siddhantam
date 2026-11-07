---
name: three-voice-page
description: Build a three-in-one page for one verse or song that puts the original text, the commentary and the teacher's class side by side, with every class claim linked to its transcript line and business and science seeds. Use whenever the user asks for a 3-in-1, three voices or மூன்று குரல் page, or wants a verse compared with what the class taught. First check that the classes for that song are corrected.
---

# Three-voice page

The page shows three people on one verse without blurring them, and lets a reader check every class
claim at its source.

In this repository, read `docs/agent-skills/transcript-and-3in1/procedures.md`, Part 2.

## Before you start

**Check that the page is due.** A song gets its page only after the classes that teach it are in the
repository and corrected, and the mind map exists. If the classes are incomplete, stop and say so.
Do not build ahead on a partial overview, however much material one class has.

**One page per song, never per class.** Use the class map to find every class that teaches the song.
That map is the user's source, so follow it and do not rewrite its rows.

## Page order

Nav · hero with chips · three-voice legend · caveat · verse and gloss · commentary tree · class cards ·
where they meet and what the class adds · the maker's reading · seeds · English version of the seeds ·
sources table · footer.

Reuse the stylesheet and nav of the existing pages. Build from data, and inject one shared nav.

## Rules

- **Every class claim links to its line.** The card header is the link. Find the line from the
  timestamp and check the line shows that time.
- **Quote only what is there.** A pull quote must be an exact part of the cited line. Everything else
  is paraphrase, in your own words, and never put a made-up sentence in the teacher's mouth.
- **Show where the voices differ.** If commentary and class come at the point differently, say so.
- **Name the limits at the top.** State which classes the page uses, that the transcript is machine
  output with only terms corrected, and that the audio is not checked.
- **The maker's reading stays the maker's.** Label it, and never present it as the book's.
- **Two seeds, each with a break.** One business, one science, one idea each, ending with where the
  analogy breaks. A seed with no break is a claim. If a verse has no honest echo, say so and skip it.
- **The English block repeats both breaks.** Those readers need them most.

## Done when

Every card's line and timestamp match, each pull quote is found in its line, each seed has a break, the
nav is the same on every page, `<div` counts match, and no placeholder text remains.
