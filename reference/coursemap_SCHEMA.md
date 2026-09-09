# coursemap data contract

Four files describe a course. Nothing else. Any tool that can write CSV can feed
the renderer — this file is the whole interface, and it is deliberately short
enough to paste into a chat window.

---

## 1. `course.toml`

```toml
[course]
code  = "CIVL 2050"
title = "Fluid Mechanics"
term  = "Fall 2026"
room  = "Carnegie Building 113"

[term]
window_start = "2026-08-24"   # left edge of every timeline; a Monday
window_end   = "2026-12-22"   # right edge; must cover the final-exam period
first_class  = "2026-08-27"
last_class   = "2026-12-11"

[instructor]
enrollment              = 85  # heads, for grading-load estimates
grading_turnaround_days = 7   # how fast you promise work back

[[kinds]]                     # repeat this block per assessment type
id     = "homework"
label  = "Homework"
color  = "hue:60"             # 0-360; or a literal "#9d5300"
lane   = "homework"           # homework | labs | exams  (which timeline row)
marker = "caret"              # dot | triangle | diamond | square | caret | none
order  = 30                   # tie-break when several land on one day (low = first)
effort = 4.0                  # grading MINUTES PER STUDENT; 0 = not graded
deadline = true               # false for things that are not a student deadline
fill   = "tint"               # tint | solid | outline
```

**`window_start` must be on or before the earliest item start.** A span opening
before the window is clipped, and `check` will say so.

Suggested hues, so unrelated courses still look like one system:
`60` amber (problem sets) · `165` green (labs, projects) · `28` brick (exams) ·
`250` blue (readings, responses) · `310` violet (presentations).

---

## 2. `meetings.csv` — one row per class meeting

```csv
no,date,type,label,short,topic,reading,note
1,2026-08-27,lecture,Class 01,C01,Introduction; units; fluid properties,1.1-1.10,First class of the term
8,2026-09-24,review,Class 08,C08,Exam 1 review,course notes,No new exam content
9,2026-09-28,exam,Class 09,C09,Exam 1,,
28,2026-12-10,contingency,Class 28,C28,Optional contingency,,Not counted by default
```

| column | meaning |
|---|---|
| `no` | chronological index over **every** meeting, 1..N. This is the anchor. |
| `type` | `lecture` \| `review` \| `exam` \| `contingency`. Only the first two count toward attendance. |
| `label` / `short` | student-facing name and its compact form for figures |
| `topic` / `reading` / `note` | free text; `note` renders in its own column |

Number every meeting including exams. Two numbering systems is how the CIVL data
drifted — one index, no exceptions.

---

## 3. `items.csv` — one row per thing that happens or is due

Everything a course assesses is a **point** (one date) or a **span** (opens → due).

```csv
id,group,kind,shape,label,start,end,anchor,note
HW1,hw1,homework,span,HW1,2026-08-27,2026-09-09,C01-C02,default Wednesday due date
PL1-01,lab1,prelab,point,PL1 01,2026-10-05,,,night before the Tue lab
LAB1-01,lab1,session,point,Lab1 01,2026-10-06,,,Flow meters
R1,lab1,report,span,Lab 1 report,2026-10-07,2026-10-18,,Flow meters
Exam1,exam1,exam,point,Exam 1,2026-09-28,,C01-C08,
Exam1-COV,exam1,coverage,span,Exam 1 coverage,2026-08-27,2026-09-24,,
```

| column | meaning |
|---|---|
| `id` | unique |
| `group` | ties related rows together (a lab's pre-labs, session and report) |
| `kind` | must match a `[[kinds]]` id in `course.toml` |
| `shape` | `point` or `span` |
| `start` | the date, or the open date |
| `end` | due date for spans; blank for points |
| `anchor` | which meetings it draws on, e.g. `C01-C02`; free text |

A lab is not a row — it is five rows sharing a `group`. That is what makes a
course with quizzes and a project need no code changes.

---

## 4. `calendar.csv` — non-teaching days

```csv
date,status,label
2026-09-07,no_class,Labor Day
2026-09-10,makeup,Follows a Monday schedule
2026-11-23,break,Thanksgiving Break
2026-12-14,study,Study period
2026-12-16,finals,Final exam period
```

`status` ∈ `no_class` `makeup` `break` `study` `finals`. Everything except
`makeup` renders as hatched dead time.

Watch the makeup logic: a cancelled Monday whose make-up lands on a day the class
already meets does **not** restore the meeting. `check` flags any interior week
holding fewer than two meetings.

---

## Producing this from somewhere else

Ask any assistant for exactly these four files, pasting this document as the spec.
Then:

```bash
python -m coursemap check  --course path/to/course
python -m coursemap render --course path/to/course --view instructor --today 2026-10-20
```

`check` runs before anything is drawn: items outside the window, spans ending
before they start, two meetings on one date, kinds declared but unused, weeks with
one meeting, grading weights that do not sum to 100. Run it on anything you did
not write by hand.

---

## Optional enrichment columns (used by the syllabus build, ignored by coursemap)

The coursemap renderer reads only the columns it names, so extra columns are safe.
The CIVL 2050 syllabus build stores its extra needs in the same files:

- `items.csv` may carry `topics` and `drop` columns. On homework rows these hold
  the topic text and drop-eligibility (`yes`/`no`) the syllabus homework table
  shows. Blank on non-homework rows. coursemap never reads them.
- `course.toml` may carry a `[sections]` block with lab meeting times
  (`sec01 = "10:00-11:50 AM"`, etc.). The syllabus derives each lab run time from
  the lab's date plus these; coursemap ignores the block.
- Three policy tables may sit beside the four core files: `grading_weights.csv`,
  `letter_grades.csv`, `resources.csv`. Syllabus-only; coursemap ignores them.

## Round-trip caveat (important when regenerating files elsewhere)

If you have another assistant (e.g. GPT) rewrite these files, it must PRESERVE:
- the `topics` and `drop` columns in items.csv,
- the exam `coverage` / `emphasis` span rows in items.csv,
- the `[sections]` block and the three policy CSVs.

`coursemap check` validates dates and structure but does NOT check for dropped
enrichment columns — a regenerated items.csv missing `topics` passes check yet
produces a syllabus with blank homework topics. After any external regeneration,
rebuild the syllabus and eyeball the homework and lab tables before relying on it.
