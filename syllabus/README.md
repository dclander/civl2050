# CIVL 2050 F26 — syllabus build (v0.3)

Compact LaTeX syllabus with a full-page visual semester map as the last page.

## Build

```bash
python3 scripts/generate_tables.py    # renders generated/ from ../course_data/
pdflatex main.tex && pdflatex main.tex
```

As of 2026-08-26 this build reads its schedule from `../course_data/` (the shared
source of truth), NOT a local `data/` folder. `generate_tables.py` was a no-op stub in v0.2 and the tables in
`generated/` were hand-made. **Nothing in `generated/` should be hand-edited.**
Edit the CSVs in `data/` and re-run.

## Layout

| | |
|---|---|
| `course_config.tex` | term facts: room, times, instructor, exam dates |
| `data/` | source tables — the only thing you edit |
| `generated/` | rendered LaTeX tables + `visual_schedule_page.pdf` (do not edit) |
| `sections/` | prose policy modules |
| `main.tex` | document assembly |

## Consistency checks

`generate_tables.py` prints a check report after rendering. It verifies:

- `\AttendanceSessions` in `course_config.tex` matches the count derived from the schedule
- every homework release date falls on an actual class meeting
- no homework is released on or after its due date
- no interior week holds fewer than two class meetings
- the final-exam period spans a full week

These are the checks that would have caught the v0.2 defects. Read the output.

## The visual semester map

`generated/visual_schedule_page.pdf` is a letter-size page included verbatim as the
last page via `pdfpages`. It is generated from the same CSVs by a separate renderer
(see the semester-map project); the native TikZ map in v0.2 is retired — its labels
overlapped and it was not legible at print size.

Class numbers (C01–C28) are the same on the map and in the Course Schedule table.

## Fonts

The schedule figures are set in IBM Plex (Sans / Mono / Serif) and reference the
family names directly, with no webfont link. The fonts must be installed on the
machine that renders them:

```bash
sudo apt-get install fonts-ibm-plex     # Debian/Ubuntu
brew install --cask font-ibm-plex       # macOS
```

If Plex is missing the renderer silently falls back to DejaVu Sans Mono, which is
noticeably wider and will overflow chips and bar labels. Check the output of
`pdffonts generated/visual_schedule_page.pdf` — every embedded face should say
`IBMPlex`.

## Data notes

`data/sessions_f26.csv` is the canonical 28-meeting backbone: 23 lectures, 2 exam
reviews, 2 exams, 1 optional contingency meeting (Thu Dec 10). 25 count toward
attendance. `legacy_session` carries the old numbering (`1–19`, `20a/20b`, `21`,
`22a/22b`, `24`) for find/replace against existing materials.
