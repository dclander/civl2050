#!/usr/bin/env python3
"""Render every LaTeX table in generated/ from the CSVs in data/.

Source tables are authoritative. Do not hand-edit anything in generated/.
Run:  python3 scripts/generate_tables.py   (from the project root)
"""
from __future__ import annotations
import csv
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, GEN = ROOT / "data", ROOT / "generated"
GEN.mkdir(exist_ok=True)

read = lambda n: list(csv.DictReader((DATA / n).open()))
pd = lambda s: datetime.strptime(s, "%Y-%m-%d").date()
DOWFULL = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}

def esc(s: str) -> str:
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}")]:
        s = s.replace(a, b)
    return s.replace("--", "--")

def fmt(d: date, dow=True) -> str:
    return ("%s %s %d" % (DOWFULL[d.weekday()], d.strftime("%b"), d.day)) if dow else d.strftime("%b %-d")

def linkcell(labels: str, urls: str) -> str:
    """One cell may hold several labelled links, pipe-separated in both columns."""
    L, U = labels.split("|"), (urls or "").split("|")
    out = []
    for i, lab in enumerate(L):
        u = U[i].strip() if i < len(U) else ""
        out.append((r"\href{%s}{%s}" % (u, esc(lab.strip()))) if u else esc(lab.strip()))
    return " / ".join(out)

def write(name: str, body: str):
    (GEN / name).write_text(body.rstrip() + "\n")
    print("  wrote generated/%s" % name)

# ---------------------------------------------------------------- sources
# Read the SCHEDULE from the canonical coursemap folder (course_data/), the single
# source of truth shared with the renderer. Only syllabus-specific policy tables
# (grading, letters, resources) and the enrichment columns coursemap ignores
# (homework topics/drop, lab section times) also live there. There is no second
# copy of any schedule date.
import os
CD = Path(os.environ.get("COURSE_DATA", ROOT.parent / "course_data"))
cd = lambda n: list(csv.DictReader((CD / n).open()))

def _toml_section(name):
    out, cur = {}, False
    for line in (CD / "course.toml").read_text().splitlines():
        t = line.split("#", 1)[0].strip()
        if t.startswith("["):
            cur = (t.strip("[]").strip() == name); continue
        if cur and "=" in t:
            k, v = t.split("=", 1); out[k.strip()] = v.strip().strip('"\'')
    return out
SEC = _toml_section("sections")

_meet = cd("meetings.csv")
SESS = [{"session_no": r["no"], "date": r["date"], "type": r["type"],
         "class_label": r["label"], "short_label": r["short"],
         "topic": r["topic"], "reading": r["reading"], "note": r["note"]} for r in _meet]

_items = cd("items.csv")
_byid = {r["id"]: r for r in _items}
_grp = {}
for r in _items:
    _grp.setdefault(r["group"], []).append(r)

HW = [{"id": r["id"], "available_date": r["start"], "due_date": r["end"],
       "covers_classes": r["anchor"], "topics": r.get("topics", ""),
       "drop_eligible": r.get("drop", "") or "yes", "rule_note": r["note"]}
      for r in _items if r["kind"] == "homework"]

def _run(dt_iso, slot):
    d = datetime.strptime(dt_iso, "%Y-%m-%d").date()
    return "%s %s %d, %s" % (DOWFULL[d.weekday()], d.strftime("%b"), d.day, slot)

LABS = []
for g, rows in _grp.items():
    sess = [x for x in rows if x["kind"] == "session"]
    rep  = [x for x in rows if x["kind"] == "report"]
    if not (sess and rep):
        continue
    s01 = next(x for x in sess if x["id"].endswith("-01"))
    s23 = next(x for x in sess if x["id"].endswith("-0203"))
    rp = rep[0]
    d = datetime.strptime(rp["end"], "%Y-%m-%d").date()
    LABS.append({
        "lab_id": "Lab " + g[-1], "lab_title": s01["note"],
        "section_01": _run(s01["start"], SEC["sec01"]),
        "section_02": _run(s23["start"], SEC["sec02"]),
        "section_03": _run(s23["start"], SEC["sec03"]),
        "report_due": "%s %s %d" % (DOWFULL[d.weekday()], d.strftime("%b"), d.day)})
LABS.sort(key=lambda l: l["lab_id"])

EXAMS = []
for g in ("exam1", "exam2", "final"):
    rows = _grp.get(g, [])
    pt  = next((x for x in rows if x["kind"] == "exam"), None)
    cov = next((x for x in rows if x["kind"] == "coverage"), None)
    emp = next((x for x in rows if x["kind"] == "emphasis"), None)
    if not cov:
        continue
    EXAMS.append({
        "id": g, "label": (pt or cov)["label"].replace(" coverage", ""),
        "date": pt["start"] if pt else "TBA",
        "covers_classes": cov["anchor"], "scope_note": cov["note"],
        "coverage_start": cov["start"], "coverage_end": cov["end"],
        "emphasis_start": emp["start"] if emp else "",
        "emphasis_end": emp["end"] if emp else ""})

CAL   = cd("calendar.csv")
GRADE = cd("grading_weights.csv")
LETT  = cd("letter_grades.csv")
RES   = cd("resources.csv")

N_MEET    = len(SESS)
N_COUNTED = sum(1 for r in SESS if r["type"] in ("lecture", "review"))
N_LECT    = sum(1 for r in SESS if r["type"] == "lecture")
N_REVIEW  = sum(1 for r in SESS if r["type"] == "review")

# --------------------------------------------------- course calendar table
TINT = {"lecture": "", "review": r"\rowcolor{rpilight}", "exam": r"\rowcolor{rpiexam}",
        "contingency": r"\rowcolor{rpilight}"}
DROP_NOTE = ("runs this week",)          # repeated on both meetings of a lab week -- the lab table owns this
NICE = {"No class": "Labor Day", "TG": "Thanksgiving Break"}
_nc = sorted((pd(r["date"]), r["label"]) for r in CAL if r["status"] in ("no_class", "break"))
runs, i = [], 0
while i < len(_nc):
    j = i
    while j + 1 < len(_nc) and (_nc[j + 1][0] - _nc[j][0]).days == 1 and _nc[j + 1][1] == _nc[i][1]:
        j += 1
    runs.append((_nc[i][0], _nc[j][0], NICE.get(_nc[i][1], _nc[i][1])))
    i = j + 1
CAL_LABEL = {pd(r["date"]): r["label"] for r in CAL}
for d in (date(2026, 9, 7),):
    pass
allrows = sorted([(pd(r["date"]), r) for r in SESS] +
                 [(a, {"type": "noclass", "label": lab, "span": (a, b)}) for a, b, lab in runs])
rows, seen_week = [], None
for d, r in allrows:
    wk = ((d - date(2026, 8, 24)).days // 7) + 1
    newweek = wk != seen_week
    if newweek and rows:
        rows.append(r"\arrayrulecolor{weekrule}\midrule\arrayrulecolor{black}")
    wcell = str(wk) if newweek else ""
    seen_week = wk
    if r["type"] == "noclass":
        a, b = r["span"]
        when = fmt(a) if a == b else "%s -- %s" % (fmt(a), fmt(b))
        rows.append(r"\rowcolor{rpilight} %s & %s & -- & No class --- %s & -- & \\" %
                    (wcell, when, esc(r["label"])))
        continue
    topic = esc(r["topic"])
    note = esc(r["note"])
    if any(k in r["note"] for k in DROP_NOTE):
        note = ""
    if r["type"] == "exam":
        cov = next((e for e in EXAMS if e["label"] == r["topic"]), None)
        topic = r"\textbf{%s}" % topic
        note = ("covers %s" % esc(cov["covers_classes"])) if cov else note
    rows.append("%s %s & %s & %s & %s & %s & {\\footnotesize %s} \\\\" %
                (TINT[r["type"]], wcell, fmt(d), r["short_label"] or "--", topic,
                 esc(r["reading"]) or "--", note))
write("course_calendar_table.tex", "\n".join([
    r"\begin{longtable}{@{}C{0.027\textwidth} L{0.125\textwidth} C{0.040\textwidth} L{0.360\textwidth} L{0.150\textwidth} L{0.230\textwidth}@{}}",
    r"\toprule", r"Wk & Date & Class & Topic / activity & Reading & Notes \\", r"\midrule", r"\endfirsthead",
    r"\toprule", r"Wk & Date & Class & Topic / activity & Reading & Notes \\", r"\midrule", r"\endhead",
    r"\bottomrule", r"\endfoot", *rows, r"\end{longtable}"]))

# ----------------------------------------------- assessment calendar table
items = []
BOILERPLATE = ("Default Wednesday due date",)
for h in HW:
    n = h["rule_note"]
    for b in BOILERPLATE:
        n = n.replace(b, "").strip(" ;")
    if h["drop_eligible"] != "yes":
        n = (n + "; not drop-eligible").strip(" ;") if n else "not drop-eligible"
    items.append((pd(h["due_date"]), "%s due" % h["id"].replace("HW", "HW "), "Homework", n))
for l in LABS:
    n = l["lab_id"].split()[-1]
    items.append((pd(l["report_due"].split(",")[0].strip()[4:].strip() if False else
                  datetime.strptime(l["report_due"].split(",")[0].strip(), "%a %b %d").replace(year=2026).strftime("%Y-%m-%d")),
                  "%s report due" % l["lab_id"], "Lab report", l["lab_title"]))
    for sec, key in (("01", "section_01"), ("02/03", "section_02")):
        run = datetime.strptime(l[key].split(",")[0].strip(), "%a %b %d").replace(year=2026).date()
        items.append((run - timedelta(days=1), "%s pre-lab due (%s)" % (l["lab_id"], sec), "Pre-lab",
                      "night before the %s lab" % DOWFULL[run.weekday()]))
for e in EXAMS:
    if e["date"] != "TBA":
        items.append((pd(e["date"]), e["label"], "Exam", "covers %s" % e["covers_classes"]))
tg = [pd(r["date"]) for r in CAL if r["status"] == "break"]
items.append((min(tg), "Thanksgiving Break", "No class",
              "Nov %d--%d; protected grading / catch-up buffer" % (min(tg).day, max(tg).day)))
arow = []
for d, item, kind, note in sorted(items):
    tint = r"\rowcolor{rpiexam}" if kind == "Exam" else (r"\rowcolor{rpilight}" if kind == "No class" else "")
    when = fmt(d) + ("" if kind in ("Exam", "No class") else r", 11:59\,PM")
    if kind == "Exam": when += ", class time"
    arow.append("%s %s & %s & %s & {\\footnotesize %s} \\\\" % (tint, when, esc(item), kind, esc(note)))
fe = next(e for e in EXAMS if e["date"] == "TBA")
arow.append(r"\rowcolor{rpiexam} \textbf{TBA} (Dec 16--22) & \textbf{Final exam} & Exam & {\footnotesize %s} \\" % esc(fe["scope_note"]))
write("assessment_calendar_table.tex", "\n".join([
    r"\begin{longtable}{@{}L{0.190\textwidth} L{0.270\textwidth} L{0.110\textwidth} L{0.360\textwidth}@{}}",
    r"\toprule", r"Date / time & Item & Type & Notes \\", r"\midrule", r"\endfirsthead",
    r"\toprule", r"Date / time & Item & Type & Notes \\", r"\midrule", r"\endhead",
    r"\bottomrule", r"\endfoot", *arow, r"\end{longtable}"]))

# ------------------------------------------------------------ homework table
hrow = ["%s & %s & %s & %s & %s & %s \\\\" % (
        h["id"].replace("HW", ""), fmt(pd(h["available_date"])), fmt(pd(h["due_date"])),
        esc(h["covers_classes"]), esc(h["topics"]), "yes" if h["drop_eligible"] == "yes" else r"\textbf{no}")
        for h in HW]
write("homework_table.tex", "\n".join([
    r"\begin{tabularx}{\textwidth}{@{}C{0.040\textwidth} L{0.120\textwidth} L{0.120\textwidth} L{0.110\textwidth} X C{0.060\textwidth}@{}}",
    r"\toprule", r"HW & Posted & Due (11:59\,PM) & Anchor classes & Topics & Drop? \\", r"\midrule",
    *hrow, r"\bottomrule", r"\end{tabularx}",
    ]))

# --------------------------------------------------------- lab schedule table
lrow = []
for l in LABS:
    section_rows = []
    for sec, key in (("01", "section_01"), ("02", "section_02"), ("03", "section_03")):
        run = l[key]
        day = datetime.strptime(run.split(",")[0].strip(), "%a %b %d").replace(year=2026).date()
        hour1, hour2 = (("10:00--11:00 AM", "11:00--11:50 AM")
                        if sec in ("01", "02") else ("2:00--3:00 PM", "3:00--3:50 PM"))
        label = r"\textbf{%s} \newline %s" % (l["lab_id"], esc(l["lab_title"])) if sec == "01" else ""
        section_rows.append("%s & %s & %s & %s & %s & %s & %s \\\\" % (
            label, r"\textbf{%s}" % sec, fmt(day), hour1, hour2, fmt(day - timedelta(days=1)),
            esc(l["report_due"].split(",")[0])))
    lrow.extend(section_rows)
    lrow.append(r"\addlinespace[3pt]")
write("lab_schedule_table.tex", "\n".join([
    r"{\setlength{\tabcolsep}{2.5pt}\begin{tabularx}{\textwidth}{@{}X C{0.045\textwidth} L{0.105\textwidth} C{0.115\textwidth} C{0.115\textwidth} L{0.095\textwidth} L{0.095\textwidth}@{}}",
    r"\toprule", r"Experiment & Sec. & Date & Hour 1 (A/B) & Hour 2 (C/D) & Pre-lab & Report \\", r"\midrule",
    *lrow[:-1], r"\bottomrule", r"\end{tabularx}}", r"\par\vspace{0.15em}",
    r"{\footnotesize Each section meets only on the three dates shown. Pre-lab and report submissions are due at 11:59\,PM.}"]))

# ------------------------------------------------------------- grading table
def pct(v):
    f = float(v)
    return ("%g" % f)
tot1 = sum(float(g["option1_pct"]) for g in GRADE)
tot2 = sum(float(g["option2_pct"]) for g in GRADE)
mark = {}
notes = []
for g in GRADE:
    if g["note"]:
        if g["note"] not in notes: notes.append(g["note"])
        mark[g["component"]] = notes.index(g["note"]) + 1
grows = []
for g in GRADE:
    sup = (r"\,$^{%d}$" % mark[g["component"]]) if g["component"] in mark else ""
    grows.append(r"%s%s & %s\%% & %s\%% \\" % (esc(g["component"]), sup,
                 pct(g["option1_pct"]), pct(g["option2_pct"])))
totrow = r"\midrule \textbf{Total} & \textbf{%s\%%} & \textbf{%s\%%} \\" % (pct(tot1), pct(tot2))
fn = " ".join(r"$^{%d}$ %s." % (i + 1, esc(n)) for i, n in enumerate(notes))
write("grading_table.tex", "\n".join([
    r"\begin{tabularx}{\textwidth}{@{}X C{0.22\textwidth} C{0.22\textwidth}@{}}", r"\toprule",
    r"Component & Option 1 (with final) & Option 2 (no final) \\", r"\midrule",
    *grows, totrow, r"\bottomrule", r"\end{tabularx}", r"\vspace{-0.25em}",
    r"{\footnotesize %s}" % fn]))
if abs(tot1 - 100) > 0.001 or abs(tot2 - 100) > 0.001:
    problems_pre = "  * grading weights: Option 1 totals %s%%, Option 2 totals %s%% (each must be 100%%)" % (pct(tot1), pct(tot2))
else:
    problems_pre = None

# --------------------------------------------------------- letter grade table
col = [LETT[i::4] for i in range(4)]
col = [LETT[0:4], LETT[4:8], LETT[8:12]]
lg = ["%s & %s--%s & %s & %s--%s & %s & %s--%s \\\\" % (
        col[0][i]["letter"], col[0][i]["low"], col[0][i]["high"],
        col[1][i]["letter"], col[1][i]["low"], col[1][i]["high"],
        col[2][i]["letter"], col[2][i]["low"], col[2][i]["high"]) for i in range(4)]
write("letter_grade_table.tex", "\n".join([
    r"\begin{tabularx}{\textwidth}{@{}C{0.07\textwidth}X C{0.07\textwidth}X C{0.07\textwidth}X@{}}",
    r"\toprule", r"Letter & Range & Letter & Range & Letter & Range \\", r"\midrule",
    *lg, r"\bottomrule", r"\end{tabularx}"]))

# ------------------------------------------------------------ resources table
write("resources_table.tex", "\n".join([
    r"\begin{tabularx}{\textwidth}{@{}L{0.28\textwidth}L{0.38\textwidth}X@{}}", r"\toprule",
    r"Resource & Location / link & Contact \\", r"\midrule",
    *["%s & %s & %s \\\\" % (esc(r["resource"]), linkcell(r["location"], r.get("url", "")),
        esc(r["contact"])) for r in RES],
    r"\bottomrule", r"\end{tabularx}"]))

# ------------------------------------------------- derived counts for prose
write("course_counts.tex", "\n".join([
    r"\newcommand{\NumClassMeetings}{%d}" % N_MEET,
    r"\newcommand{\NumCountedSessions}{%d}" % N_COUNTED,
    r"\newcommand{\NumLectures}{%d}" % N_LECT,
    r"\newcommand{\NumReviews}{%d}" % N_REVIEW,
    r"\newcommand{\NumHomework}{%d}" % len(HW),
    r"\newcommand{\NumLabs}{%d}" % len(LABS)]))

# ------------------------------------------------- consistency checks
problems = []
if problems_pre: problems.append(problems_pre.strip('* ').strip())
cfg = (ROOT / "course_config.tex").read_text()
import re as _re
m = _re.search(r"\\newcommand\{\\AttendanceSessions\}\{(\d+)\}", cfg)
if m and int(m.group(1)) != N_COUNTED:
    problems.append("course_config.tex \\AttendanceSessions = %s but the schedule yields %d"
                    % (m.group(1), N_COUNTED))
for h in HW:
    if pd(h["available_date"]) >= pd(h["due_date"]):
        problems.append("%s is released on or after its due date" % h["id"])
byweek = {}
for r in SESS:
    byweek.setdefault((pd(r["date"]) - date(2026, 8, 24)).days // 7, []).append(r["short_label"])
first, last = min(byweek), max(byweek)
for w in sorted(byweek):
    if len(byweek[w]) < 2 and w not in (first, last):
        problems.append("week %d holds only one class meeting (%s) -- a cancelled day whose "
                        "make-up landed on a day the course already meets"
                        % (w + 1, ", ".join(byweek[w])))
fin = [pd(r["date"]) for r in CAL if r["status"] == "finals"]
if fin and (max(fin) - min(fin)).days + 1 < 7:
    problems.append("final-exam period spans only %d days" % ((max(fin) - min(fin)).days + 1))

print("\n  %d class meetings | %d counted for attendance (%d lectures + %d reviews)"
      % (N_MEET, N_COUNTED, N_LECT, N_REVIEW))
if problems:
    print("\n  CHECKS -- %d item(s) to review:" % len(problems))
    for x in problems:
        print("    * " + x)
else:
    print("  checks: all clear")
