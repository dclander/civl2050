# -*- coding: utf-8 -*-
from sched import *
from datetime import timedelta

C = dict(hw="#9d5300",hwd="#713500",hwt="#fde9d9",hwm="#e2b38d",
         lab="#007f56",labd="#005938",labt="#dbf4e8",labm="#90ceb2",
         ex="#a7463c",exd="#782a24",ext="#ffe6e2",
         lec="#3e66b3",lecd="#254582",lect_="#e2edff",
         ink="#191610",ink2="#504d47",ink3="#83807b",
         paper="#fcfaf6",paper2="#f5f1ec",rule="#d8d5d1",rule2="#c0bdb9")

# Fall 2026 administrative reconciliation: Class 28 is the final review, not a contingency.
CHIP[date(2026, 12, 10)] = [{"role":"lect", "kind":"review", "text":"C28"}]

ROWH, LANEH, DATEH, CHIPH = 51, 7, 11, 15
GRID = "56px repeat(5, minmax(0, 1fr)) 38px 58px"
INNER = "repeat(5, minmax(0, 1fr)) 38px 58px"
MONO = "'IBM Plex Mono', ui-monospace, Menlo, monospace"
SANS = "'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif"

def chip(c):
    k, t = c["kind"], c["text"]
    base = ("display:inline-flex;align-items:center;gap:2.5px;height:13px;padding:0 3.5px;"
            "font-family:%s;font-size:9.5px;letter-spacing:0.005em;white-space:nowrap;"%MONO)
    if k == "exam":
        return ('<span style="%sbackground:%s;color:#fff;font-weight:600;border-radius:1.5px;">'
                '<span style="width:5px;height:5px;background:#fff;transform:rotate(45deg);display:block;"></span>%s</span>'%(base,C["ex"],t))
    if k == "lecture":
        return ('<span style="%scolor:%s;font-weight:500;">'
                '<span style="width:5px;height:5px;border-radius:50%%;background:%s;display:block;"></span>%s</span>'%(base,C["lecd"],C["lec"],t))
    if k == "contingency":
        return ('<span style="%scolor:%s;border:0.75px dashed %s;border-radius:1.5px;font-style:italic;">'
                '<span style="width:5px;height:5px;border-radius:50%%;border:1px solid %s;display:block;"></span>%s</span>'%(base,C["ink3"],C["rule2"],C["ink3"],t))
    if k == "review":
        return ('<span style="%scolor:%s;font-weight:600;">'
                '<span style="width:0;height:0;border-left:3px solid transparent;border-right:3px solid transparent;border-bottom:5px solid %s;display:block;"></span>%s</span>'%(base,C["lecd"],C["lec"],t))
    if k == "due":
        return ('<span style="%sbackground:%s;color:%s;border:0.75px solid %s;border-radius:1.5px;font-weight:600;">%s'
                '<span style="width:0;height:0;border-left:3px solid transparent;border-right:3px solid transparent;border-top:4px solid %s;display:block;"></span></span>'%(base,C["hwt"],C["hwd"],C["hw"],t,C["hw"]))
    if k == "prelab":
        b2=base.replace("font-size:9.5px","font-size:8.5px").replace("padding:0 3px","padding:0 2.5px")
        return ('<span style="%scolor:%s;border:0.75px dashed %s;border-radius:1.5px;">%s</span>'%(b2,C["labd"],C["lab"],t))
    if k == "session":
        return ('<span style="%sbackground:%s;color:%s;border:0.75px solid %s;border-radius:1.5px;">'
                '<span style="width:5px;height:5px;border-radius:50%%;background:%s;display:block;"></span>%s</span>'%(base,C["labt"],C["labd"],C["lab"],C["lab"],t))
    if k == "report":
        return ('<span style="%sbackground:%s;color:#fff;font-weight:600;border-radius:1.5px;">'
                '<span style="width:5px;height:5px;background:#fff;display:block;"></span>%s</span>'%(base,C["lab"],t))
    return ""

HATCH = ("repeating-linear-gradient(45deg, %s 0 3px, %s 3px 6px)"%(C["paper2"],"#eae5de"))

def day_cell(dt, is_last_wk=False):
    st, lb = status(dt)
    wknd = dt.weekday() >= 5
    bg = "transparent"
    if wknd: bg = C["paper2"]
    if st in ("no_class","break","study","finals"): bg = HATCH
    chips = CHIP.get(dt, [])
    inner = "".join(chip(c) for c in chips)
    narrow = wknd
    num = ('<div style="font-family:%s;font-size:9px;font-weight:%s;color:%s;line-height:%spx;text-align:%s;padding:0 4px;">%d%s</div>'
           % (MONO, "600" if dt.weekday()==0 else "400", C["ink2"] if not wknd else C["ink3"], DATEH,
              "center" if narrow else "left", dt.day,
              ('<span style="float:right;color:%s;font-size:8px;font-weight:400;">%s</span>'%(C["ink3"], lb)) if (lb and not narrow) else ""))
    body = ('<div style="display:flex;gap:2px;align-items:center;height:%spx;padding:0 3px;overflow:hidden;">%s</div>'%(CHIPH, inner))
    return ('<div style="background:%s;border-left:0.75px solid %s;box-sizing:border-box;">%s%s</div>'
            % (bg, C["rule"], num, body))

def seg_bar(sg):
    col = C["hw"] if sg["role"]=="hw" else C["lab"]
    fill = C["hwm"] if sg["role"]=="hw" else C["labm"]
    r_l = "0" if sg["cl"] else "3px"
    r_r = "0" if sg["cr"] else "3px"
    cap_l = ('<span style="width:2px;align-self:stretch;background:%s;"></span>'%col) if not sg["cl"] else ""
    cap_r = ('<span style="width:2px;align-self:stretch;background:%s;"></span>'%col) if not sg["cr"] else ""
    arrow_r = ('<span style="width:0;height:0;border-top:3px solid transparent;border-bottom:3px solid transparent;border-left:4px solid %s;align-self:center;"></span>'%col) if sg["cr"] else ""
    arrow_l = ('<span style="width:0;height:0;border-top:3px solid transparent;border-bottom:3px solid transparent;border-right:4px solid %s;align-self:center;"></span>'%col) if sg["cl"] else ""
    label = ""
    if not sg["cl"] and (sg["c1"]-sg["c0"]) >= 2:
        label = ('<span style="font-family:%s;font-size:7.5px;font-weight:600;color:%s;line-height:6px;padding-left:2px;letter-spacing:0.02em;">%s</span>'
                 % (MONO, C["hwd"] if sg["role"]=="hw" else C["labd"], sg["id"].replace("Report ","R")))
    return ('<div style="grid-column:%d / %d;grid-row:%d;display:flex;align-items:center;'
            'background:%s;border-radius:%s %s %s %s;height:6px;overflow:hidden;">%s%s%s%s%s</div>'
            % (sg["c0"]+1, sg["c1"]+2, sg["lane"]+1, fill, r_l, r_r, r_r, r_l, arrow_l, cap_l, label, cap_r, arrow_r))

def week_row(w, compressed=False):
    days = [w["start"]+timedelta(days=i) for i in range(7)]
    segs = week_segments(w)
    ndue = len(TOTAL_DUE[w["n"]])
    barw = min(ndue,4)*8
    load = ('<div style="height:2.5px;width:%dpx;background:%s;border-radius:1px;margin-top:2px;"></div>'%(barw, C["ink"] if ndue>=3 else C["ink3"])) if ndue else ""
    lab = ('<div style="padding:2px 6px 0 0;text-align:right;">'
           '<div style="font-family:%s;font-size:11px;font-weight:600;color:%s;line-height:12px;">W%d</div>'
           '<div style="font-family:%s;font-size:7.5px;color:%s;line-height:9px;white-space:nowrap;">%s</div>'
           '<div style="display:flex;justify-content:flex-end;">%s</div></div>'
           % (MONO, C["ink"], w["n"], MONO, C["ink3"],
              "%s–%s" % (w["start"].strftime("%-m/%-d"), w["end"].strftime("%-m/%-d")), load))
    cells = "".join(day_cell(d) for d in days)
    if compressed:
        return ('<div style="display:grid;grid-template-columns:%s;border-top:0.75px solid %s;height:26px;align-items:center;">%s'
                '<div style="grid-column:2 / 9;background:%s;height:100%%;display:flex;align-items:center;padding-left:8px;'
                'font-family:%s;font-size:9.5px;color:%s;letter-spacing:0.06em;text-transform:uppercase;">%s</div></div>'
                % (GRID, C["rule2"], lab, HATCH, MONO, C["ink2"], "Study period · final exam period — Finals TBA"))
    band = ('<div style="grid-column:2 / 9;display:grid;grid-template-columns:%s;grid-template-rows:repeat(3,%dpx);'
            'padding-top:1px;">%s</div>' % (INNER, LANEH, "".join(seg_bar(s) for s in segs)))
    return ('<div style="display:grid;grid-template-columns:%s;grid-template-rows:%dpx %dpx;border-top:0.75px solid %s;height:%dpx;box-sizing:border-box;">'
            '<div style="grid-row:1 / 3;">%s</div>%s%s</div>'
            % (GRID, DATEH+CHIPH, LANEH*3+4, C["rule2"], ROWH, lab, cells, band))

# ---------- legend ----------
def legend():
    specs = [
        (chip({"kind":"lecture","text":"C12"}), "class meeting"),
        (chip({"kind":"review","text":"C08"}), "exam review"),
        (chip({"kind":"exam","text":"EXAM 1"}), "exam")
        ,(chip({"kind":"review","text":"C28"}), "final exam review"),
        (chip({"kind":"due","text":"HW6"}), "homework due"),
        (chip({"kind":"prelab","text":"PL2 01"}), "pre-lab due"),
        (chip({"kind":"session","text":"Lab2 01"}), "lab session"),
        (chip({"kind":"report","text":"R1"}), "lab report due"),
    ]
    items = "".join('<div style="display:flex;align-items:center;gap:5px;">%s<span style="font-size:9px;color:%s;">%s</span></div>'%(s,C["ink2"],t) for s,t in specs)
    bars = ('<div style="display:flex;align-items:center;gap:5px;">'
            '<span style="width:26px;height:6px;background:%s;border-radius:3px;display:block;"></span>'
            '<span style="font-size:9px;color:%s;">HW open → due</span></div>'
            '<div style="display:flex;align-items:center;gap:5px;">'
            '<span style="width:26px;height:6px;background:%s;border-radius:3px;display:block;"></span>'
            '<span style="font-size:9px;color:%s;">report writing period</span></div>'
            '<div style="display:flex;align-items:center;gap:5px;">'
            '<span style="width:14px;height:11px;background:%s;display:block;border:0.75px solid %s;"></span>'
            '<span style="font-size:9px;color:%s;">no class / break / finals</span></div>'
            % (C["hwm"],C["ink2"],C["labm"],C["ink2"],HATCH,C["rule"],C["ink2"]))
    return ('<div style="display:flex;flex-wrap:wrap;gap:5px 14px;align-items:center;height:41px;overflow:hidden;padding:6px 0 7px;border-top:1.5px solid %s;border-bottom:0.75px solid %s;">%s%s</div>'
            % (C["ink"], C["rule"], items, bars))

DOWS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
def colhead():
    cs = "".join('<div style="border-left:0.75px solid %s;text-align:%s;padding:0 4px;font-family:%s;font-size:8.5px;'
                 'letter-spacing:0.1em;text-transform:uppercase;color:%s;line-height:16px;">%s</div>'
                 % (C["rule"], "center" if i>=5 else "left", MONO, C["ink3"] if i>=5 else C["ink2"], d[:3] if i<5 else d[0])
                 for i,d in enumerate(DOWS))
    return '<div style="display:grid;grid-template-columns:%s;height:16px;">%s%s</div>'%(GRID,'<div></div>',cs)

def closing_band():
    lab=('<div style="padding:2px 6px 0 0;text-align:right;">'
         '<div style="font-family:%s;font-size:11px;font-weight:600;color:%s;line-height:12px;">W17&ndash;18</div>'
         '<div style="font-family:%s;font-size:7.5px;color:%s;line-height:9px;white-space:nowrap;">12/14&ndash;12/22</div></div>'
         %(MONO,C["ink"],MONO,C["ink3"]))
    return ('<div style="display:grid;grid-template-columns:%s;border-top:0.75px solid %s;height:26px;align-items:center;">%s'
            '<div style="grid-column:2 / 9;background:%s;height:100%%;display:flex;align-items:center;padding-left:8px;gap:14px;'
            'font-family:%s;font-size:9px;color:%s;letter-spacing:0.05em;text-transform:uppercase;">'
            '<span>Study period Dec 12&ndash;15</span><span style="color:%s;font-weight:600;">Final exam period Dec 16&ndash;22 &mdash; date TBA</span></div></div>'
            % (GRID, C["rule2"], lab, HATCH, MONO, C["ink2"], C["exd"]))
rows = "".join(week_row(w) for w in WEEKS if w["n"]<=16) + closing_band()

HTML = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  
  <style>
    body {{ margin: 0; font-family: {SANS}; -webkit-font-smoothing: antialiased; }}
    a {{ color: {hw}; }} a:hover {{ color: {hwd}; }}
    * {{ box-sizing: border-box; }}
  </style>
</helmet>
<div style="width:816px;height:1056px;background:{paper};padding:34px 36px 30px;display:flex;flex-direction:column;color:{ink};">

  <div style="display:flex;align-items:baseline;justify-content:space-between;padding-bottom:6px;">
    <div>
      <div style="font-family:'IBM Plex Serif',Georgia,serif;font-size:23px;font-weight:600;letter-spacing:-0.01em;line-height:26px;">CIVL 2050 &middot; Fluid Mechanics</div>
      <div style="font-size:11px;color:{ink2};line-height:15px;padding-top:2px;">Semester map &mdash; lectures, homework, labs, and exams, week by week.</div>
    </div>
    <div style="text-align:right;">
      <div style="font-family:{MONO};font-size:12px;font-weight:600;letter-spacing:0.08em;">FALL 2026</div>
      <div style="font-family:{MONO};font-size:9px;color:{ink3};letter-spacing:0.04em;">AUG 27 &ndash; DEC 22</div>
    </div>
  </div>

  {legend}
  {colhead}
  <div style="flex:1 1 auto;">{rows}</div>
  <div style="border-top:1.5px solid {ink};display:flex;justify-content:space-between;align-items:baseline;padding-top:6px;">
    <div style="font-family:{MONO};font-size:8px;color:{ink3};letter-spacing:0.04em;">GENERATED FROM SOURCE TABLES &middot; DO NOT HAND-EDIT</div>
    <div style="font-family:{MONO};font-size:8px;color:{ink3};letter-spacing:0.04em;">28 CLASS MEETINGS &middot; 26 COUNTED BY DEFAULT FOR ATTENDANCE</div>
  </div>
</div>
</x-dc>
</body>
</html>
""".format(SANS=SANS, MONO=MONO, legend=legend(), colhead=colhead(), rows=rows, **C)
open("Main.dc.html","w").write(HTML)
print("rows:", len(WEEKS), "bytes:", len(HTML))
print("height budget:", 34+30+ (26+15+2) + 41 + 16 + (16*ROWH+26) + 24, "of 1056")
