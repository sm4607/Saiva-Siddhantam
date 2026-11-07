#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
class_terms.py — keep one master word list, and use it to correct class transcripts.

The master list is Book 3's terms-master.tsv. terms.txt and kalaisol-agarathi.md are
generated from it, so edit meanings in the master list.
A newly learned word appears in the glossary by itself, under பொருள் சேர்க்க வேண்டியவை,
until someone writes its meaning in the master list and runs sync.
The loop for each class:

    python3 tools/class_terms.py propose 7     # known misheard forms -> corrections.tsv
    (open corrections.tsv, write yes or no on rows with an empty decision)
    python3 tools/class_terms.py apply 7 --dry-run
    python3 tools/class_terms.py apply 7       # fix the transcript, learn the new forms
    python3 tools/class_terms.py review 7      # rewrite review.md from the master list
    python3 tools/class_terms.py check         # confirm everything still agrees
    python3 tools/class_terms.py undo 7 182 ஐதீகத்தோடு    # reverse one fix

The loop for each new song page:

    python3 tools/class_terms.py song 14       # candidate words -> song-words/song-14.tsv
    (fill in meaning, write yes or no in decision, no in glossary to keep a word out of it)
    python3 tools/class_terms.py learn 14      # add the yes rows to the master list

Rules the tool enforces:
  * Only rows marked yes or auto change anything. A sound-alike can be a different word.
  * propose marks a row auto only if its form sits in the auto column of the master list.
    Everything else waits for you. Change auto to no on any row to stop that fix.
  * A form you approve is learned as auto only if the row is book-backed and at least one
    of its words is not a real word. A word is real if the book or verified pages have it
    exactly, or it starts with an entry in real-words.txt (நாள், பசுமை). Add everyday words
    to that file whenever one is wrongly fixed. Rows marked listen always stay in ask.
  * No book text file means every new form stays in ask.
  * Answering no to an auto row, or undoing a fix, moves that form back to ask.
  * apply warns when a song or three-voices page contains the wrong form. It never edits
    those pages, because their text was written and checked by hand.
  * Words are replaced inside their line. The song pages link to transcript.md by line
    number, so apply stops if the line count or any timestamp would change.
  * A row with an empty term column fixes that line only and teaches the list nothing.
    Use that for words that are real words elsewhere (கொல்லப்படும் / கொள்ளப்படும்).

Columns of terms-master.tsv:
  term        the correct spelling
  auto        misheard forms fixed without asking, separated by " ; ". "wrong=right"
              gives the inflected fix; a bare "wrong" means use the term itself.
  ask         misheard forms that always come to you. Same format. Move a form between
              these two columns to change its label.
  kind        term or name. Names go in the பெயர்கள் section of the glossary.
  section     glossary section, usually the song where the word belongs
  meaning     glossary meaning. Blank means it is listed as needing one.
  source      where the spelling was verified
  status      confirmed, or proposed until a class fix is approved
  glossary    yes or no. no keeps the word on the review list but out of the glossary.
              New words default to yes. Set it in corrections.tsv or the song words file.
  first_class first class where a fix was approved
"""

import argparse
import csv
import difflib
import html
import io
import json
import os
import re
import sys

BOOK3 = "Gnanam Maragam/Book3-Sivagnana-Siddhiyar-Supakkam"
MASTER_COLS = ["term", "auto", "ask", "kind", "section", "meaning", "source", "status", "glossary", "first_class"]
FIX_COLS = ["line", "time", "wrong", "right", "term", "evidence", "certainty", "decision", "glossary"]
SONG_COLS = ["term", "kind", "section", "meaning", "source", "glossary", "decision"]
PARA = re.compile(r"^\*\*\[([\d:]+)\] பேச்சாளர் 0:\*\*\s*(.*)$")
HTML_PARA = re.compile(r'<p><span class="ts">([\d:]+)</span>(.*?)</p>')
COUNTS = r"\d[\d,]* பத்திகள் · \d[\d,]* சொற்கள்"
TAMIL = "஀-௿"
LOW_CONFIDENCE = 0.55
NEAR_MATCH = 0.82
GLOSSARY_SECTIONS = ["விநாயக வணக்கம்", "பரசிவ வணக்கம்", "நூலின்வழி", "நுதலிய பொருள்",
                     "அவையடக்கம் 1", "அவையடக்கம் 2", "மூவகை அளவை", "அளவையின் இலக்கணம்",
                     "நால்வகைக் காட்சிகள்", "பிரமாணப் பாகுபாடு", "இயல்பு வகைகள்",
                     "இந்திரிய/மானதக் காட்சி", "தன்வேதனை, யோகக் காட்சி"]
NAMES_SECTION = "பெயர்கள்"
PENDING_SECTION = "பொருள் சேர்க்க வேண்டியவை"
GLOSSARY_HEAD = """# கலைச்சொல் அகராதி — சிவஞான சித்தியார் சுபக்கம்

> வளரும் பட்டியல். புதிய பாடம் வரும்போது இதில் சேரும். ஒவ்வொரு சொல்லும்
> எந்தப் பாடலில் வந்தது என்பதுடன் இருக்கிறது, அதனால் பின்னர் தேடலாம்.

இந்தப் பட்டியல் இரண்டு வேலை செய்கிறது: படிக்கும்போது சொற்பொருள் தேட, மற்றும்
வகுப்பு எழுத்துவடிவங்களில் கலைச்சொற்களைத் திருத்த.

மொத்தச் சொற்கள்: **{total}**
"""
GLOSSARY_FOOT = """---

## பராமரிப்பு

- இந்தக் கோப்பை நேரடியாகத் திருத்த வேண்டாம். இது `terms-master.tsv` இலிருந்து தானாக உருவாக்கப்படுகிறது.
- சொல்லையோ பொருளையோ மாற்ற `terms-master.tsv` ஐத் திருத்தி, `python3 tools/class_terms.py sync` ஓட்டவும்.
- வகுப்பிலிருந்தோ புதிய பாடலிலிருந்தோ உறுதியான சொல், பொருள் எழுதப்படும்வரை "பொருள் சேர்க்க வேண்டியவை" பகுதியில் இருக்கும்.
- ஒரு சொல்லுக்கு உரை மரபில் வேறு பொருள் இருந்தால், இரண்டையும் கொடுக்கவும் — ஒன்றை மட்டும் தேர்ந்தெடுக்க வேண்டாம்.
- `terms.txt` உம் அதே மூலப் பட்டியலிலிருந்து உருவாகிறது.
"""
CITING_PAGES_SKIP = ("recordings", "vanika-inai")
BANNER_NOW = "கலைச்சொற்கள் மட்டும் பகுதியாகத் திருத்தப்பட்டுள்ளன"
BANNER_OLD = ("சொற்கள் திருத்தப்படவில்லை", "சொற்கள் திருத்தப்பட்டுள்ளன")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def read_tsv(path, cols):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE, quotechar=None))
    return [{c: (r.get(c) or "").strip() for c in cols} for r in rows]


def write_tsv(path, cols, rows):
    buffer = io.StringIO(newline="")
    w = csv.DictWriter(buffer, cols, delimiter="\t", quoting=csv.QUOTE_NONE, quotechar=None,
                       lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    write(path, buffer.getvalue())


def word_re(form):
    """Match a form only as whole words, so இறம் never matches inside நிறம்."""
    return re.compile(rf"(?<![{TAMIL}]){re.escape(form)}(?![{TAMIL}])")


class Repo:
    def __init__(self, root):
        self.root = root
        self.book3 = os.path.join(root, BOOK3)
        self.master_path = os.path.join(self.book3, "terms-master.tsv")

    def class_dir(self, n):
        return os.path.join(self.book3, "recordings", f"siddhiyar-class-{n:02d}")

    def path(self, n, name):
        return os.path.join(self.class_dir(n), name)

    def song_path(self, n):
        return os.path.join(self.book3, "song-words", f"song-{n:02d}.tsv")

    def classes(self):
        found = re.findall(r"siddhiyar-class-(\d+)$", "\n".join(
            sorted(os.listdir(os.path.join(self.book3, "recordings")))), re.M)
        return [int(x) for x in found]

    def master(self):
        rows = read_tsv(self.master_path, MASTER_COLS)
        if not rows:
            sys.exit(f"No master list at {self.master_path}")
        return rows

    def generated(self, rows):
        """The files built from the master list, as {path: text}."""
        confirmed = sorted(r["term"] for r in rows if r["status"] == "confirmed")
        terms = "\n".join(confirmed) + "\n"
        return {
            os.path.join(self.root, "terms.txt"): terms,
            os.path.join(self.book3, "terms.txt"): terms,
            os.path.join(self.book3, "kalaisol-agarathi.md"): render_glossary(rows),
        }


def render_glossary(rows):
    confirmed = sorted((r for r in rows if r["status"] == "confirmed" and r["glossary"] != "no"),
                       key=lambda r: r["term"])
    groups = {}
    pending = []
    for r in confirmed:
        if not r["meaning"]:
            pending.append(r)
            continue
        section = NAMES_SECTION if r["kind"] == "name" else r["section"] or PENDING_SECTION
        groups.setdefault(section, []).append(r)
    extra = sorted(set(groups) - set(GLOSSARY_SECTIONS) - {NAMES_SECTION})
    out = [GLOSSARY_HEAD.format(total=len(confirmed))]
    for section in GLOSSARY_SECTIONS + extra + [NAMES_SECTION]:
        if section in groups:
            out += [f"## {section}\n", "| சொல் | பொருள் |", "|---|---|"]
            out += [f"| **{r['term']}** | {r['meaning']} |" for r in groups[section]]
            out.append("")
    if pending:
        out += [f"## {PENDING_SECTION}\n", "| சொல் | முதல் வகுப்பு | மூலம் |", "|---|---|---|"]
        out += [f"| **{r['term']}** | {r['first_class'] or '—'} | {r['source'] or '—'} |"
                for r in pending]
        out.append("")
    return "\n".join(out) + GLOSSARY_FOOT


def forms(cell):
    return [x.strip() for x in cell.split(";") if x.strip()]


def misheard_pairs(rows):
    """Every known (wrong, right, term, label) from the master list."""
    pairs = []
    for r in rows:
        for label in ("auto", "ask"):
            for item in forms(r[label]):
                wrong, _, right = item.partition("=")
                pairs.append((wrong.strip(), right.strip() or r["term"], r["term"], label))
    return pairs


def site_pages(repo):
    """Song and three-voices pages as {relative path: plain text}."""
    pages = {}
    for base, _, files in os.walk(repo.book3):
        if any(skip in base for skip in CITING_PAGES_SKIP):
            continue
        for name in files:
            if name.endswith(".html"):
                path = os.path.join(base, name)
                text = re.sub(r"<style.*?</style>|<[^>]+>", " ", read(path), flags=re.S)
                pages[os.path.relpath(path, repo.book3)] = html.unescape(text)
    return pages


def known_words(repo, book_text):
    """Words from the book and verified pages, or None without the book text."""
    if not os.path.exists(book_text):
        return None
    words = set(re.findall(rf"[{TAMIL}]+", read(book_text)))
    for text in site_pages(repo).values():
        words |= set(re.findall(rf"[{TAMIL}]+", text))
    stems = tuple(x.strip() for x in read(os.path.join(repo.book3, "real-words.txt")).split("\n")
                  if x.strip())
    return words, stems


def looks_real(word, known):
    """True if the book or pages have this exact word, or it starts with a real-words.txt entry.

    The book is philosophy, so everyday words like நாள் and பசுமை are missing from it.
    real-words.txt holds those, and matches with any ending: பசுமையானதால் starts with பசுமை.
    """
    words, stems = known
    return word in words or word.startswith(stems)


def label_for(row, known):
    """auto only for a book-backed form with at least one word that is not real."""
    if known is None or row["certainty"] != "book":
        return "ask"
    return "ask" if all(looks_real(w, known) for w in row["wrong"].split()) else "auto"


def move_to_ask(rows, wrong):
    for r in rows:
        keep = []
        for item in forms(r["auto"]):
            if item.partition("=")[0].strip() == wrong:
                r["ask"] = " ; ".join(forms(r["ask"]) + [item])
            else:
                keep.append(item)
        r["auto"] = " ; ".join(keep)


def paragraphs(md):
    """Return [(line_number, time, text)] for the transcript."""
    out = []
    for i, line in enumerate(md.split("\n"), 1):
        m = PARA.match(line)
        if m:
            out.append((i, m[1], m[2]))
    return out


def cmd_sync(repo, _):
    for path, text in repo.generated(repo.master()).items():
        write(path, text)
        print(f"wrote {os.path.relpath(path, repo.root)}")


def cmd_propose(repo, a):
    md = read(repo.path(a.n, "transcript.md"))
    fix_path = repo.path(a.n, "corrections.tsv")
    fixes = read_tsv(fix_path, FIX_COLS)
    seen = {(r["line"], r["wrong"]) for r in fixes}
    added = {"auto": 0, "ask": 0}
    pairs = misheard_pairs(repo.master())
    rights = {}
    for wrong, right, *_ in pairs:
        rights.setdefault(wrong, set()).add(right)
    for line, time, text in paragraphs(md):
        for wrong, right, term, label in pairs:
            if word_re(wrong).search(text) and (str(line), wrong) not in seen:
                seen.add((str(line), wrong))
                if len(rights[wrong]) > 1:
                    label = "ask"
                fixes.append({"line": line, "time": time, "wrong": wrong, "right": right,
                              "term": term, "evidence": "master list",
                              "certainty": label,
                              "decision": "auto" if label == "auto" else ""})
                added[label] += 1
    fixes.sort(key=lambda r: int(r["line"]))
    write_tsv(fix_path, FIX_COLS, fixes)
    print(f"class {a.n}: {added['auto']} auto, {added['ask']} for you to decide, "
          f"{len(fixes)} rows in corrections.tsv")


def asr_words(a, n):
    path = os.path.join(a.sources, f"சித்தியார் வகுப்பு {n}.json")
    if not os.path.exists(path):
        return None
    data = json.loads(read(path))["results"]
    return [w for seg in data for alt in seg["alternatives"] for w in alt.get("words") or []
            if w.get("word")]


def hhmmss(seconds):
    x = int(float(str(seconds).rstrip("s")))
    return f"{x // 3600:02d}:{x % 3600 // 60:02d}:{x % 60:02d}"


def cmd_review(repo, a):
    rows = repo.master()
    md = read(repo.path(a.n, "transcript.md"))
    paras = paragraphs(md)
    text = " ".join(t for _, _, t in paras)
    tokens = text.split()
    grams = sorted({" ".join(tokens[i:i + k]) for k in (1, 2, 3)
                    for i in range(len(tokens) - k + 1)})

    correct, doubtful, missing = [], [], []
    for term in (r["term"] for r in rows):
        if term in text:
            correct.append(term)
            continue
        hit = difflib.get_close_matches(term, grams, n=1, cutoff=NEAR_MATCH)
        if hit:
            doubtful.append((term, hit[0], difflib.SequenceMatcher(None, term, hit[0]).ratio()))
        else:
            missing.append(term)
    doubtful.sort(key=lambda x: -x[2])

    known = []
    for line, time, para in paras:
        for wrong, right, _, label in misheard_pairs(rows):
            if word_re(wrong).search(para):
                known.append((line, time, wrong, right, label))

    out = ["# சொற்கள் — பரிசீலனை\n",
           f"மூலப் பட்டியல்: `terms-master.tsv` · மொத்தச் சொற்கள்: {len(rows)} · "
           f"சரியாக வந்தவை: {len(correct)} · சந்தேகம்: {len(doubtful)} · "
           f"காணவில்லை: {len(missing)} · அறிந்த தவறுகள்: {len(known)}\n",
           "## அறிந்த தவறுகள் — முன்பே உறுதியான தவற்று வடிவங்கள்\n"]
    if known:
        out += ["| வரி | நேரம் | இருப்பது | சரியான வடிவம் | வகை |", "|---|---|---|---|---|"]
        out += [f"| {l} | {t} | {w} | {r} | {b} |" for l, t, w, r, b in known]
    else:
        out.append("இந்தப் பதிவில் அறிந்த தவறுகள் எதுவும் இல்லை.")
    out += ["", "## சிதைந்திருக்கலாம் — ஒலியைக் கேட்டு உறுதி செய்யுங்கள்\n"]
    if doubtful:
        out += ["| சரியான சொல் | ASR எழுதியது | ஒற்றுமை |", "|---|---|---|"]
        out += [f"| {t} | {h} | {s:.2f} |" for t, h, s in doubtful]
    else:
        out.append("இந்தப் பதிவில் சிதைந்த சொற்கள் எதுவும் கண்டறியப்படவில்லை.")
    out += ["", "## வரவே இல்லை\n",
            "இந்தச் சொற்கள் இந்தப் பதிவில் வரவில்லை. வகுப்பில் பேசப்படவில்லை என்பதாகவோ, "
            "ASR தவறவிட்டதாகவோ, வேற்றுமை உருபுடன் வந்ததாகவோ இருக்கலாம்.\n"]
    out += [f"- {m}" for m in missing]
    out += ["", "## சரியாக வந்தவை\n", ", ".join(correct) or "—", ""]

    words = asr_words(a, a.n)
    if words is None:
        print(f"class {a.n}: no ASR json in {a.sources}, low-confidence table left out")
    else:
        low = [w for w in words if w.get("confidence", 1) < LOW_CONFIDENCE]
        out += ["## குறைந்த நம்பிக்கை — இந்த இடங்களை மட்டும் கேளுங்கள்\n",
                f"ஒலிபெயர்ப்புக் கருவியே இந்த {len(low)} சொற்களில் உறுதியாக இல்லை "
                f"({LOW_CONFIDENCE} என்னும் நம்பிக்கை அளவுக்குக் கீழே). இவை கருவி முதலில் "
                "எழுதிய சொற்கள் — திருத்தத்துக்கு முந்தையவை.\n",
                "| நேரம் | சொல் | நம்பிக்கை |", "|---|---|---|"]
        out += [f"| {hhmmss(w['startTime'])} | {w['word'].strip()} | {w.get('confidence', 0):.2f} |"
                for w in low]
        out.append("")
    write(repo.path(a.n, "review.md"), "\n".join(out))

    meta_path = repo.path(a.n, "meta.json")
    meta = json.loads(read(meta_path))
    meta["keyterms_used"] = len(rows)
    write(meta_path, json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    print(f"class {a.n}: {len(rows)} terms · correct {len(correct)} · doubtful {len(doubtful)} "
          f"· absent {len(missing)} · known errors {len(known)}")


def update_counts(repo, n, md):
    paras = paragraphs(md)
    count_p = len(paras)
    count_w = sum(len(t.split()) for _, _, t in paras)
    listing = f"{count_p:,} பத்திகள் · {count_w:,} சொற்கள்"
    changed = {}
    for path in (os.path.join(repo.book3, "recordings", "index.html"),
                 os.path.join(repo.book3, "index.html")):
        page = read(path)
        changed[path] = re.sub(rf"(சித்தியார் வகுப்பு {n:02d}<small>[^\n]*?){COUNTS}",
                               lambda m: m[1] + listing, page)
    return changed, f"{count_w:,} சொற்கள் · {count_p:,} பத்திகள்"


def page_matches_transcript(md, page):
    return [(t, x) for _, t, x in paragraphs(md)] == \
        [(t, html.unescape(x)) for t, x in HTML_PARA.findall(page)]


def write_class(repo, n, new_md, page):
    """Write the transcript and rebuild everything that repeats its text or counts."""
    texts = iter(paragraphs(new_md))

    def rebuilt(_):
        _, time, text = next(texts)
        return f'<p><span class="ts">{time}</span>{html.escape(text, quote=False)}</p>'

    new_page = HTML_PARA.sub(rebuilt, page)
    listings, ledger = update_counts(repo, n, new_md)
    new_page = re.sub(r"\d[\d,]* சொற்கள் · \d[\d,]* பத்திகள்", ledger, new_page, count=1)
    for old in BANNER_OLD:
        new_md = new_md.replace(old, BANNER_NOW, 1)
        new_page = new_page.replace(old, BANNER_NOW, 1)
    new_md = re.sub(r"^status: .*$", "status: terms-corrected", new_md, count=1, flags=re.M)

    meta_path = repo.path(n, "meta.json")
    meta = json.loads(read(meta_path))
    meta["status"] = "terms-corrected"
    write(meta_path, json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    write(repo.path(n, "transcript.md"), new_md)
    write(repo.path(n, "index.html"), new_page)
    for path, text in listings.items():
        write(path, text)


def quote_warnings(repo, todo):
    pages = site_pages(repo)
    found = {}
    for r in todo:
        for name, text in pages.items():
            if word_re(r["wrong"]).search(text):
                found.setdefault(name, set()).add(r["wrong"])
    for name, wrongs in sorted(found.items()):
        print(f"WARNING {name} still contains: {', '.join(sorted(wrongs))}")


def cmd_apply(repo, a):
    md = read(repo.path(a.n, "transcript.md"))
    page = read(repo.path(a.n, "index.html"))
    fix_path = repo.path(a.n, "corrections.tsv")
    fixes = read_tsv(fix_path, FIX_COLS)
    todo = [r for r in fixes if r["decision"].lower() in ("yes", "auto")]
    refused = [r for r in fixes if r["decision"].lower() == "no"]
    if not todo:
        sys.exit(f"class {a.n}: no rows marked yes or auto in corrections.tsv")
    if not page_matches_transcript(md, page):
        sys.exit(f"class {a.n}: transcript.md and index.html differ. Nothing changed.")

    before = paragraphs(md)
    lines = md.split("\n")
    for r in todo:
        i = int(r["line"]) - 1
        new, hits = word_re(r["wrong"]).subn(r["right"], lines[i])
        if not hits or not PARA.match(lines[i]) or PARA.match(lines[i])[1] != r["time"]:
            sys.exit(f"class {a.n}: line {r['line']} has no '{r['wrong']}' at {r['time']}. "
                     "Nothing changed.")
        lines[i] = new

    new_md = "\n".join(lines)
    after = paragraphs(new_md)
    if len(lines) != len(md.split("\n")) or [(l, t) for l, t, _ in after] != [(l, t) for l, t, _ in before]:
        sys.exit(f"class {a.n}: line numbers or timestamps would move. Nothing changed.")
    automatic = sum(r["decision"].lower() == "auto" for r in todo)
    print(f"class {a.n}: {len(todo)} fixes ({automatic} auto) on "
          f"{sum(x != y for x, y in zip(before, after))} lines · "
          f"words {sum(len(t.split()) for *_, t in before):,} → "
          f"{sum(len(t.split()) for *_, t in after):,}")
    quote_warnings(repo, todo)
    if a.dry_run:
        print("dry run: nothing written")
        return

    write_class(repo, a.n, new_md, page)

    rows = repo.master()
    by_term = {r["term"]: r for r in rows}
    known = known_words(repo, a.book_text)
    if known is None:
        print(f"No book text at {a.book_text}: new forms stay in ask.")
    held = {p[0] for p in misheard_pairs(rows)}
    learned = {"auto": [], "ask": []}
    for r in todo:
        was_auto = r["decision"].lower() == "auto"
        r["decision"] = "auto-applied" if was_auto else "applied"
        if not r["term"] or was_auto:
            continue
        row = by_term.get(r["term"])
        if row is None:
            row = dict.fromkeys(MASTER_COLS, "")
            row.update(term=r["term"], kind="term", source=r["evidence"],
                       glossary=r["glossary"] or "yes")
            rows.append(row)
            by_term[r["term"]] = row
        row["status"] = "confirmed"
        row["first_class"] = row["first_class"] or str(a.n)
        if r["wrong"] not in held:
            held.add(r["wrong"])
            label = label_for(r, known)
            form = r["wrong"] if r["right"] == r["term"] else f"{r['wrong']}={r['right']}"
            row[label] = " ; ".join(forms(row[label]) + [form])
            learned[label].append(r["wrong"])
    for r in refused:
        move_to_ask(rows, r["wrong"])
    rows.sort(key=lambda r: r["term"])
    write_tsv(fix_path, FIX_COLS, fixes)
    write_tsv(repo.master_path, MASTER_COLS, rows)
    cmd_sync(repo, a)
    for label, found in learned.items():
        if found:
            print(f"learned as {label}: {', '.join(found)}")
    print("Next: run review for this class, propose for the others, then check.")


def cmd_undo(repo, a):
    md = read(repo.path(a.n, "transcript.md"))
    page = read(repo.path(a.n, "index.html"))
    fix_path = repo.path(a.n, "corrections.tsv")
    fixes = read_tsv(fix_path, FIX_COLS)
    row = next((r for r in fixes if r["line"] == str(a.line) and r["wrong"] == a.wrong
                and r["decision"] in ("applied", "auto-applied")), None)
    if row is None:
        sys.exit(f"class {a.n}: no applied fix for '{a.wrong}' on line {a.line}.")
    lines = md.split("\n")
    found = word_re(row["right"]).findall(lines[a.line - 1])
    if len(found) != 1:
        sys.exit(f"class {a.n}: '{row['right']}' appears {len(found)} times on line {a.line}. "
                 "Edit that line by hand. Nothing changed.")
    lines[a.line - 1] = word_re(row["right"]).sub(a.wrong, lines[a.line - 1])
    write_class(repo, a.n, "\n".join(lines), page)
    row["decision"] = "undone"
    write_tsv(fix_path, FIX_COLS, fixes)
    rows = repo.master()
    move_to_ask(rows, a.wrong)
    write_tsv(repo.master_path, MASTER_COLS, rows)
    print(f"class {a.n}: line {a.line} back to '{a.wrong}', and that form now stays in ask.")


def song_page(repo, n):
    for name in sorted(os.listdir(repo.book3)):
        if name.startswith(f"{n:02d}-"):
            return os.path.join(repo.book3, name, "index.html")
    sys.exit(f"No folder for song {n}. Use --page to name its index.html.")


def page_candidates(page):
    """Bold words and mind map titles: the page's own marking of what matters."""
    body = re.sub(r"<(style|script|footer).*?</\1>", " ", page, flags=re.S)
    marked = re.findall(r'<(?:b|strong)\b[^>]*>(.*?)</(?:b|strong)>|'
                        r'class="n-(?:t|s)[^"]*"[^>]*>(.*?)<', body, flags=re.S)
    found = []
    for pair in marked:
        text = html.unescape(re.sub(r"<[^>]+>", "", pair[0] or pair[1]))
        text = re.sub(rf"[^{TAMIL} ]", " ", text)
        text = " ".join(text.split())
        if text and len(text.split()) <= 3 and text not in found:
            found.append(text)
    return found


def cmd_song(repo, a):
    page = read(a.page or song_page(repo, a.n))
    path = repo.song_path(a.n)
    rows = read_tsv(path, SONG_COLS)
    seen = {r["term"] for r in rows} | {r["term"] for r in repo.master()}
    new = [t for t in page_candidates(page) if t not in seen]
    rows += [{"term": t, "kind": "term", "section": "", "meaning": "", "source": f"பாடல் {a.n} பக்கம்",
              "glossary": "yes", "decision": ""} for t in new]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_tsv(path, SONG_COLS, rows)
    print(f"song {a.n}: {len(new)} new candidates, {len(rows)} rows in "
          f"{os.path.relpath(path, repo.root)}")


def cmd_learn(repo, a):
    song = read_tsv(repo.song_path(a.n), SONG_COLS)
    if not song:
        sys.exit(f"song {a.n}: no song words file. Run song {a.n} first.")
    waiting = [r["term"] for r in song if r["decision"].lower() not in ("yes", "no", "added")]
    rows = repo.master()
    terms = {r["term"]: r for r in rows}
    added = []
    for r in song:
        if r["decision"].lower() != "yes":
            continue
        if r["term"] in terms:
            sys.exit(f"song {a.n}: {r['term']} is already in the master list. Nothing changed.")
        row = dict.fromkeys(MASTER_COLS, "")
        row.update({c: r[c] for c in ("term", "kind", "section", "meaning", "source")})
        row.update(status="confirmed", glossary=r["glossary"] or "yes")
        rows.append(row)
        terms[r["term"]] = row
        added.append(r["term"])
        r["decision"] = "added"
    rows.sort(key=lambda r: r["term"])
    write_tsv(repo.master_path, MASTER_COLS, rows)
    write_tsv(repo.song_path(a.n), SONG_COLS, song)
    cmd_sync(repo, a)
    print(f"song {a.n}: added {len(added)}: {', '.join(added) or 'none'}")
    if waiting:
        print(f"still needing yes or no: {', '.join(waiting)}")


def cmd_check(repo, _):
    rows = repo.master()
    problems = []
    terms = [r["term"] for r in rows]
    for t in {t for t in terms if terms.count(t) > 1}:
        problems.append(f"master list: duplicate term {t}")
    rights = {}
    for wrong, right, _, label in misheard_pairs(rows):
        rights.setdefault(wrong, set()).add((right, label))
    for wrong, seen in rights.items():
        if len(seen) > 1:
            problems.append(f"master list: '{wrong}' is listed more than once")
    for path, text in repo.generated(rows).items():
        if not os.path.exists(path) or read(path) != text:
            problems.append(f"out of date, run sync: {os.path.relpath(path, repo.root)}")

    confirmed = {r["term"] for r in rows if r["status"] == "confirmed"}
    no_meaning = [r["term"] for r in rows if r["status"] == "confirmed" and not r["meaning"]]
    if no_meaning:
        print(f"Words still needing a meaning: {', '.join(no_meaning)}")

    citations = set()
    for base, _, files in os.walk(repo.book3):
        if "recordings" in base:
            continue
        for name in files:
            if name.endswith(".html"):
                citations |= set(re.findall(r"siddhiyar-class-(\d+)/transcript\.md#L(\d+)",
                                            read(os.path.join(base, name))))

    for n in repo.classes():
        md = read(repo.path(n, "transcript.md"))
        paras = paragraphs(md)
        page = HTML_PARA.findall(read(repo.path(n, "index.html")))
        if [(t, x) for _, t, x in paras] != [(t, html.unescape(x)) for t, x in page]:
            problems.append(f"class {n}: transcript.md and index.html differ")
        para_lines = {l: x for l, _, x in paras}
        for c, line in citations:
            if int(c) == n and int(line) not in para_lines:
                problems.append(f"class {n}: a page cites line {line}, which is not a paragraph")
        for r in read_tsv(repo.path(n, "corrections.tsv"), FIX_COLS):
            if r["decision"].lower() in ("", "yes", "auto"):
                if not word_re(r["wrong"]).search(para_lines.get(int(r["line"]), "")):
                    problems.append(f"class {n}: corrections.tsv line {r['line']} "
                                    f"no longer has '{r['wrong']}'")
    print(f"{len(rows)} terms ({len(confirmed)} confirmed) · {len(citations)} line citations · "
          f"{len(repo.classes())} classes")
    print("\n".join(problems) if problems else "All clean.")
    return 1 if problems else 0


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description="Master word list and transcript corrections")
    ap.add_argument("--root", default=here, help="repository folder")
    ap.add_argument("--sources", default=os.path.expanduser(
        "~/Downloads/Sivagana-Siddhiyar-mp3-transcript"), help="folder of ASR json files")
    ap.add_argument("--book-text", default=os.path.expanduser(
        "~/Downloads/Sivagnana-Siddhiyar-mp3/book_text.txt"),
        help="searchable book text, used to tell real words from misheard ones")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sync", help="rebuild terms.txt and the glossary from the master list")
    sub.add_parser("check", help="report anything out of step")
    for name in ("propose", "review"):
        sub.add_parser(name).add_argument("n", type=int)
    p = sub.add_parser("song", help="list a song page's candidate words for review")
    p.add_argument("n", type=int)
    p.add_argument("--page", default="", help="the page, if it is not in its song folder yet")
    sub.add_parser("learn", help="add a song's yes rows to the master list").add_argument("n", type=int)
    p = sub.add_parser("apply", help="apply the rows marked yes")
    p.add_argument("n", type=int)
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("undo", help="reverse one applied fix")
    p.add_argument("n", type=int)
    p.add_argument("line", type=int)
    p.add_argument("wrong")
    a = ap.parse_args()
    run = {"sync": cmd_sync, "propose": cmd_propose, "review": cmd_review,
           "apply": cmd_apply, "undo": cmd_undo, "check": cmd_check,
           "song": cmd_song, "learn": cmd_learn}[a.cmd]
    sys.exit(run(Repo(a.root), a) or 0)


if __name__ == "__main__":
    main()
