# civl2050-web — static site for GitHub Pages

Blackboard holds links only; this tree is the content. See the project doc
`CIVL2050_coursemap_hosting_handoff.md` for the full rationale and requirements.

## What's here
- `index.html` — student schedule view (week-at-a-glance). THE Blackboard link.
  Rebuilt from `course_data/`, do not hand-edit. To refresh:
  `python -m coursemap render --course <course_data> --view student --out .`
  then copy/rename the output to `index.html`.
- `aids/<slug>/index.html` — one lecture aid per folder (self-contained; no data dep).

## Deploy (once the GitHub account is ready)
Push this folder to a repo, enable Pages on the default branch. The schedule is then
at `https://<user>.github.io/<repo>/` and each aid at `/aids/<slug>/`. Updating is a
file replace; the URLs stay stable, so the Monday-announcement link never changes.

## Requirements that must stay true (from the hosting handoff)
One self-contained file each · all date logic client-side · degrades offline ·
relative links only · index.html is the stable URL · course_data stays the source
of truth (index.html embeds a build-time snapshot).
