# -*- coding: utf-8 -*-
from sched import *
from datetime import timedelta

C = dict(hw="#9d5300",hwd="#713500",hwt="#fde9d9",hwm="#e2b38d",
         lab="#007f56",labd="#005938",labt="#dbf4e8",labm="#90ceb2",
         ex="#a7463c",exd="#782a24",ext="#ffe6e2",exm="#eaaca3",
         lec="#3e66b3",lecd="#254582",lecm="#a4beef",
         ink="#191610",ink2="#504d47",ink3="#83807b",
         paper="#fcfaf6",paper2="#f5f1ec",rule="#d8d5d1",rule2="#c0bdb9")
MONO="'IBM Plex Mono', ui-monospace, Menlo, monospace"
SANS="'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif"
HATCH="repeating-linear-gradient(45deg, #efeae3 0 4px, #e5dfd7 4px 8px)"

UNIT, BLOCK, TOP, BOT = 40, 34, 132, 148

def inflight(w):
    n=0
    for s in SPANS:
        if s["s"]<=w["end"] and s["e"]>=w["start"]: n+=1
    return n

def week_sessions(w):
    return [s for d,s in sorted(SESS.items()) if w["start"]<=d<=w["end"]]

KIND={"due":(C["hw"],C["hwt"],C["hwd"]),"prelab":(C["labm"],C["labt"],C["labd"]),
      "report":(C["lab"],C["labt"],C["labd"]),"exam":(C["ex"],C["ext"],C["exd"])}

def col(w):
    items=list(TOTAL_DUE[w["n"]])
    nf=inflight(w); nd=len(items)
    days=[w["start"]+timedelta(days=i) for i in range(7)]
    isbreak=all(status(d)[0] in ("break","study","finals") or d.weekday()>=5 for d in days)
    # above the line: open work
    above=('<div style="height:%dpx;display:flex;flex-direction:column;justify-content:flex-end;padding:0 3px;">'
           '<div style="height:%dpx;background:%s;border-top:2px solid %s;border-left:0.75px solid %s;border-right:0.75px solid %s;"></div></div>'
           %(TOP, nf*UNIT, C["paper2"], C["ink3"] if nf else "transparent", C["rule"], C["rule"]))
    # the axis band
    def _m(s):
        if s["type"]=="review":
            return ('<span style="width:0;height:0;border-left:3.5px solid transparent;border-right:3.5px solid transparent;'
                    'border-bottom:6px solid %s;display:block;"></span>'%C["lec"])
        if s["type"]=="contingency":
            return '<span style="width:5px;height:5px;border-radius:50%%;border:1px dashed %s;display:block;"></span>'%C["ink3"]
        return '<span style="width:5px;height:5px;border-radius:50%%;background:%s;display:block;"></span>'%C["lec"]
    ticks="".join(_m(s) for s in week_sessions(w))
    axis=('<div style="height:26px;border-top:1.5px solid %s;border-bottom:0.75px solid %s;display:flex;align-items:center;'
          'justify-content:center;gap:3px;background:%s;">%s</div>'%(C["ink"],C["rule"],HATCH if isbreak else "transparent",ticks))
    # below the line: due
    blocks=[]
    for c in items:
        fg,bg,tx = KIND[c["kind"]]
        strong = c["kind"] in ("exam","report")
        blocks.append('<div style="height:%dpx;background:%s;border-left:3px solid %s;display:flex;align-items:center;'
                      'padding-left:5px;"><span style="font-family:%s;font-size:9px;font-weight:%s;color:%s;white-space:nowrap;'
                      'overflow:hidden;text-overflow:ellipsis;">%s</span></div>'
                      %(BLOCK, fg if strong else bg, fg, MONO, "600", "#fff" if strong else tx, c["text"]))
    below=('<div style="height:%dpx;display:flex;flex-direction:column;gap:2px;padding:3px 3px 0;">%s</div>'%(BOT,"".join(blocks)))
    heavy = nd>=3
    label=('<div style="padding-top:6px;text-align:center;">'
           '<div style="font-family:%s;font-size:11px;font-weight:%s;color:%s;line-height:13px;">W%d</div>'
           '<div style="font-family:%s;font-size:7.5px;color:%s;line-height:10px;">%s</div></div>'
           %(MONO,"700" if heavy else "500",C["ink"] if heavy else C["ink2"],w["n"],MONO,C["ink3"],
             w["start"].strftime("%-m/%-d")))
    return ('<div style="border-left:0.75px solid %s;background:%s;">%s%s%s%s</div>'
            %(C["rule"], C["paper2"] if heavy else "transparent", above, axis, below, label))

def closing_col():
    return ('<div style="border-left:0.75px solid %s;">'
            '<div style="height:%dpx;"></div>'
            '<div style="height:26px;border-top:1.5px solid %s;border-bottom:0.75px solid %s;background:%s;"></div>'
            '<div style="height:%dpx;padding:3px 3px 0;">'
            '<div style="height:%dpx;background:%s;border-left:3px solid %s;display:flex;align-items:center;padding-left:5px;">'
            '<span style="font-family:%s;font-size:8px;font-weight:600;color:#fff;white-space:nowrap;letter-spacing:-0.02em;">FINAL TBA</span></div></div>'
            '<div style="padding-top:6px;text-align:center;">'
            '<div style="font-family:%s;font-size:11px;font-weight:500;color:%s;line-height:13px;">W17&ndash;18</div>'
            '<div style="font-family:%s;font-size:7.5px;color:%s;line-height:10px;">12/14</div></div></div>'
            %(C["rule"],TOP,C["ink"],C["rule"],HATCH,BOT,BLOCK,C["ex"],C["exd"],MONO,MONO,C["ink2"],MONO,C["ink3"]))
cols="".join(col(w) for w in WEEKS if w["n"]<=16) + closing_col()

def gridline(v,label):
    return ('<div style="position:absolute;left:0;right:0;bottom:%dpx;border-top:0.75px dashed %s;">'
            '<span style="position:absolute;left:-26px;top:-7px;font-family:%s;font-size:8.5px;color:%s;">%d</span></div>'
            %(v*UNIT, C["rule2"], MONO, C["ink3"], v))

def legend():
    it=[('<span style="width:22px;height:11px;background:%s;border-left:3px solid %s;display:block;"></span>'%(C["hwt"],C["hw"]),"homework due"),
        ('<span style="width:22px;height:11px;background:%s;border-left:3px solid %s;display:block;"></span>'%(C["labt"],C["labm"]),"pre-lab due"),
        ('<span style="width:22px;height:11px;background:%s;border-left:3px solid %s;display:block;"></span>'%(C["lab"],C["labd"]),"lab report due"),
        ('<span style="width:22px;height:11px;background:%s;border-left:3px solid %s;display:block;"></span>'%(C["ex"],C["exd"]),"exam"),
        ('<span style="width:22px;height:11px;background:%s;border-top:2px solid %s;display:block;"></span>'%(C["paper2"],C["ink3"]),"assignments open (in progress)"),
        ('<span style="width:7px;height:7px;border-radius:50%%;background:%s;display:block;"></span>'%C["lec"],"lecture"),
        ('<span style="width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-bottom:7px solid %s;display:block;"></span>'%C["lec"],"exam review"),
        ('<span style="width:16px;height:11px;background:%s;border:0.75px solid %s;display:block;"></span>'%(HATCH,C["rule"]),"no class / break / finals")]
    return "".join('<div style="display:flex;align-items:center;gap:6px;">%s<span style="font-size:10px;color:%s;">%s</span></div>'%(s,C["ink2"],t) for s,t in it)

HTML="""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  
  <style>
    body {{ margin:0; font-family:{SANS}; -webkit-font-smoothing:antialiased; }}
    a {{ color:{hw}; }} a:hover {{ color:{hwd}; }}
    * {{ box-sizing:border-box; }}
  </style>
</helmet>
<div style="width:1200px;height:548px;background:{paper};padding:34px 40px 26px;display:flex;flex-direction:column;color:{ink};">
  <div style="display:flex;align-items:baseline;justify-content:space-between;padding-bottom:12px;">
    <div>
      <div style="font-family:'IBM Plex Serif',Georgia,serif;font-size:26px;font-weight:600;letter-spacing:-0.01em;line-height:28px;">Where the pressure is</div>
      <div style="font-size:12px;color:{ink2};line-height:16px;padding-top:3px;">CIVL 2050 Fluid Mechanics &mdash; work in progress above the line, deadlines below it.</div>
    </div>
    <div style="text-align:right;">
      <div style="font-family:{MONO};font-size:13px;font-weight:600;letter-spacing:0.08em;">FALL 2026</div>
      <div style="font-family:{MONO};font-size:9.5px;color:{ink3};letter-spacing:0.04em;">{NS} CLASS MEETINGS &middot; {ND} DEADLINES</div>
    </div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:7px 18px;align-items:center;padding:8px 0 10px;border-top:1.5px solid {ink};border-bottom:0.75px solid {rule};">{legend}</div>

  <div style="display:flex;padding-top:14px;">
    <div style="width:78px;flex:0 0 78px;position:relative;">
      <div style="height:{TOP}px;position:relative;">
        {g3}{g2}{g1}
        <div style="position:absolute;right:0;bottom:0;transform:translateY(50%);font-family:{MONO};font-size:8.5px;
             letter-spacing:0.07em;text-transform:uppercase;color:{ink2};text-align:right;line-height:11px;padding-right:8px;">open<br>work</div>
      </div>
      <div style="height:26px;"></div>
      <div style="height:{BOT}px;padding-right:8px;text-align:right;font-family:{MONO};font-size:8.5px;letter-spacing:0.07em;
           text-transform:uppercase;color:{ink2};line-height:11px;padding-top:4px;">due<br>this<br>week</div>
    </div>
    <div style="flex:1 1 auto;display:grid;grid-template-columns:repeat(17, minmax(0, 1fr));border-right:0.75px solid {rule};">{cols}</div>
  </div>

  <div style="border-top:1.5px solid {ink};display:flex;justify-content:space-between;align-items:baseline;padding-top:7px;margin-top:auto;">
    <div style="font-family:{MONO};font-size:8.5px;color:{ink3};letter-spacing:0.04em;">GENERATED FROM SOURCE TABLES &middot; DO NOT HAND-EDIT</div>
    <div style="font-family:{MONO};font-size:8.5px;color:{ink3};letter-spacing:0.04em;">SHADED COLUMNS = 3 OR MORE DEADLINES</div>
  </div>
</div>
</x-dc>
</body>
</html>
""".format(SANS=SANS,MONO=MONO,legend=legend(),cols=cols,TOP=TOP,BOT=BOT,
           g1=gridline(1,"1"),g2=gridline(2,"2"),g3=gridline(3,"3"),ND=N_DEADLINES,NS=N_SESSIONS,**C)
open("LoadFirst.dc.html","w").write(HTML)
print("bytes",len(HTML))
