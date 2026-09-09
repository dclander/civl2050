# coursemap kit — portable, works in Claude or ChatGPT

This folder is the durable, self-contained set. Drop it into any new thread —
Claude or GPT — and you can resume without the original conversation.

## What's here
- `coursemap-tool.tar.gz` — the renderer. Unpack, `python -m coursemap ...`.
- `SCHEMA.md` — the four-file data contract. This is the whole interface.

## The data lives next door
The tool is generic; a course's data is not. This course's four source files are
in `../course_data/` (course.toml, meetings.csv, items.csv, calendar.csv). A new
course is a new `course_data` folder — nothing in the tool changes.

## Resuming in ChatGPT (or any assistant)
1. Upload `SCHEMA.md` and paste: "produce the four coursemap files for my course
   per this schema, verifying dates against the registrar calendar."
2. Bring the four files back here, drop them in a `course_data/` folder.
3. Run the tool locally (needs Python 3.9+ and, for rendering, the browser step
   in the tool's own README).

## Resuming in a fresh Claude thread
Upload `coursemap-tool.tar.gz` and `SCHEMA.md`, point at the course_data folder,
and ask for the view you want (`wallmap`, `now`, or `instructor`).

## The three views
- wallmap — 17x11 colour, printed once in August, never changes.
- now — a browser page that reads today's date itself; publish once, bookmark.
- instructor — the two combined into one dated snapshot.

Full workflow is in WORKFLOW.md inside the tarball.
