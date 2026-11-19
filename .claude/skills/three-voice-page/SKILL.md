---
name: three-voice-page
description: Build a three-in-one page for one verse or song that puts the original text, the commentary and the teacher's class side by side, with every class claim linked to its transcript line and business and science seeds. Use whenever the user asks for a 3-in-1, three voices or மூன்று குரல் page, or wants a verse compared with what the class taught. First check that the classes for that song are corrected.
---

# Three-voice page

The page shows three people on one verse without blurring them, and lets a reader check every class
claim at its source.

In this repository, read `docs/agent-skills/transcript-and-3in1/procedures.md`, Part 2.

## Before you start

**Use the classes processed so far.** A song's page needs its mind map and the corrected
transcripts of the classes that teach it. You cannot know when a song is finished, because the
teacher may return to it later, so build from what is in and update the page if a later class adds
something. Say on the page which classes it uses.

**One page per song, never per class.** Use the class map to find every class that teaches the song.
That map is the user's source, so follow it and do not rewrite its rows. Classes can switch between
parts of the book, so one song's classes may be far apart.

**Keep students out of the teacher's voice.** Students sometimes share their understanding of earlier classes, usually for one or two songs, while the teacher speaks for most of the class. The transcript gives everyone the same speaker label, so read the lines around a passage for signs that a student is speaking, such as the teacher inviting a summary. Leave out anything doubtful rather than credit a student's words to the teacher.

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
