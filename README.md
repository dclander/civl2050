# CIVL 2050 — Fluid Mechanics

Course infrastructure: the schedule data, the syllabus source, the lecture aids,
and the static site students actually visit.

## Layout

    docs/         THE PUBLISHED SITE. GitHub Pages serves this folder.
      index.html    week-at-a-glance student schedule — the one Blackboard link
      aids/<slug>/index.html   one lecture aid per folder, self-contained
      figures/      static figures for notes and slides
    course_data/  SINGLE SOURCE OF TRUTH — schedule + policy tables
    syllabus/     LaTeX source for the syllabus PDF
    reference/    schema, changelog, inherited docs
    dist/         build outputs (wallmap PDF, SCORM package) — regenerable
    notes/        working notes, not published

`docs/` is named that because GitHub Pages only publishes from the repo root or a
folder called `docs/`. It is the website, not documentation. Documentation is in
`reference/`.

## The one rule

`course_data/` is the source of truth. Both the syllabus and the schedule views read
it. Change a date there and rebuild — never hand-edit `docs/index.html` or the
generated LaTeX tables.

## Publishing

Pages settings: deploy from branch `main`, folder `/docs`. Students get
`https://dclander.github.io/civl2050/`. That URL is stable forever — put it in
Blackboard once and never touch it again. Updating is a file replace and a push.

Blackboard cannot host interactive HTML: it serves uploaded `.html` as a download
and its content editor strips `<script>`. `dist/*_SCORM.zip` is the fallback for
anything that must live inside Blackboard.

## Semesters

Current offering lives at the top level. When F26 ends, move the semester-specific
material into `archive/f26/` and keep the URL. One repo across offerings — you get
the history of how the course changed.

## Naming

Lowercase, hyphens, no spaces, no version suffixes in folder names. Git holds the
versions; `_v0_3` in a directory name is what you do when it doesn't.
