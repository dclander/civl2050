# CIVL 2050 — _AI_automation

Cleaned up 2026-08-26. Superseded generations are in `_archive/` (nothing deleted).

## Durable set — what to keep and return to

| Folder / file | What it is | Thread it belongs to |
|---|---|---|
| `course_data/` | The four canonical source files. **Single source of truth** for schedule + assessments. | both |
| `coursemap_kit/` | Portable renderer + schema. Works in Claude or GPT. | coursemap tool |
| `CIVL2050_F26_syllabus_v0_3/` | Complete LaTeX syllabus build (source, tables, scripts, main.pdf). | CIVL 2050 syllabus |
| `CIVL2050_wallmap.pdf` | Current printed wall map. | CIVL 2050 syllabus |
| `CHANGELOG.md` | Source changes, rebuild results, and release status. | both |

The renderer itself is installed one level up, at `_Teaching/_tools/coursemap`
(shared across all courses). `coursemap_kit/` holds the uploadable copy for other
threads and tools.

## Suggested durable threads
1. **coursemap tool** — owns the engine. Portable, cross-course, cross-tool.
   Seed a new thread with `coursemap_kit/`.
2. **CIVL 2050 F26 syllabus + schedule** — owns this course. The syllabus build,
   `course_data`, and the rendered wall map / now page.

The live "now" page is already published as a Claude artifact — bookmark its URL;
it needs no files to keep working.

## Single source of truth (done 2026-08-26)
`course_data/` is now the ONLY place schedule facts live. The syllabus build reads
it directly — `generate_tables.py` was rewired to load from `../course_data/`, and
the syllabus's old `data/` folder is archived. The regenerated tables are
byte-identical to before, so nothing about the syllabus changed except where its
data comes from. Homework release dates (the field that drifted) now exist in
exactly one file.

`course_data/` holds the four coursemap files plus three syllabus policy tables
(grading_weights, letter_grades, resources) and a few enrichment columns the
renderer ignores (homework topics/drop in items.csv; lab section times in
course.toml [sections]). coursemap reads only the columns it names; the syllabus
reads the rest.

## _archive/ contents
- `matplotlib_prep_v0_3/` — the original matplotlib visual-schedule system (v0.3).
- `latex_template_v0_2/` — the earlier syllabus template with the broken TikZ map.
- `syllabus_previous_build/` — prior build snapshots of the current syllabus.
- `old_renders/` — early instructor/wall-map PDFs (font-fallback and pre-fix).
- `CIVL2050_F26_syllabus_v0_3.tar.gz` — redundant snapshot of the live folder.
- `coursemap_SCHEMA.md` — duplicate of the copy now in `coursemap_kit/`.
- `syllabus_old_data_csvs/` — the syllabus build's former 10-CSV data folder,
  replaced by `course_data/`.
