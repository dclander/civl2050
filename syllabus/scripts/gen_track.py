# -*- coding: utf-8 -*-
from sched import *
from datetime import timedelta

C = dict(hw="#9d5300",hwd="#713500",hwt="#fde9d9",hwm="#e2b38d",
         lab="#007f56",labd="#005938",labt="#dbf4e8",labm="#90ceb2",
         ex="#a7463c",exd="#782a24",ext="#ffe6e2",exm="#eaaca3",
         lec="#3e66b3",lecd="#254582",lect_="#e2edff",lecm="#a4beef",
         ink="#191610",ink2="#504d47",ink3="#83807b",
         paper="#fcfaf6",paper2="#f5f1ec",rule="#d8d5d1",rule2="#c0bdb9")
MONO="'IBM Plex Mono', ui-monospace, Menlo, monospace"
SANS="'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif"
HATCH="repeating-linear-gradient(45deg, #efeae3 0 4px, #e5dfd7 4px 8px)"

NDAYS=(END-START).days+1
idx=lambda d:(d-START).days
GC=lambda a,b:"grid-column:%d / %d;"%(idx(a)+1, idx(b)+2)
TRACK="display:grid;grid-template-columns:repeat(%d, minmax(0, 1fr));"%NDAYS
LBLW=104

def lane(label, sub, content, h, bg="transparent", bord=True):
    return ('<div style="display:flex;border-top:%s;">'
            '<div style="width:%dpx;flex:0 0 %dpx;padding:5px 10px 0 0;text-align:right;">'
            '<div style="font-family:%s;font-size:9.5px;font-weight:600;letter-spacing:0.07em;text-transform:uppercase;color:%s;line-height:12px;">%s</div>'
            '<div style="font-family:%s;font-size:8px;color:%s;line-height:10px;">%s</div></div>'
            '<div style="flex:1 1 auto;position:relative;height:%dpx;background:%s;%s">%s</div></div>'
            % ("0.75px solid "+C["rule"] if bord else "none", LBLW, LBLW, SANS, C["ink2"], label, MONO, C["ink3"], sub, h, bg, TRACK, content))

# ---------- background overlays (breaks + exam rules) ----------
def exam_rules(h):
    o=[]
    for e in EX:
        if not e["date"]: continue
        o.append('<div style="%sgrid-row:1;height:%dpx;border-left:1.25px solid %s;opacity:0.55;"></div>'%(GC(e["date"],e["date"]),h,C["ex"]))
    return "".join(o)

def overlays(h):
    out=[exam_rules(h)]
    runs=[]; cur=None
    for i in range(NDAYS):
        d=START+timedelta(days=i); st,_=status(d)
        k = st if st in ("no_class","break","study","finals") else ""
        if k!=cur: 
            if cur: runs[-1]["e"]=d-timedelta(days=1)
            if k: runs.append({"s":d,"e":d,"k":k})
            cur=k
        elif k: runs[-1]["e"]=d
    for r in runs:
        out.append('<div style="%sgrid-row:1;background:%s;height:%dpx;"></div>'%(GC(r["s"],r["e"]),HATCH,h))
    return "".join(out)

# ---------- ruler ----------
def ruler():
    mo=[]
    for m,(nm,y) in enumerate([("AUGUST",2026),("SEPTEMBER",2026),("OCTOBER",2026),("NOVEMBER",2026),("DECEMBER",2026)]):
        mn=m+8
        ds=[START+timedelta(days=i) for i in range(NDAYS) if (START+timedelta(days=i)).month==mn]
        mo.append('<div style="%sgrid-row:1;border-left:1.25px solid %s;padding-left:5px;font-family:%s;font-size:10px;'
                  'font-weight:600;letter-spacing:0.12em;color:%s;line-height:16px;">%s</div>'%(GC(ds[0],ds[-1]),C["ink"],MONO,C["ink"],nm))
    wk=[]
    for w in WEEKS:
        s=max(w["start"],START); e=min(w["end"],END)
        nd=len(TOTAL_DUE[w["n"]])
        heavy = nd>=3
        wk.append('<div style="%sgrid-row:1;border-left:0.75px solid %s;padding-left:4px;font-family:%s;font-size:8.5px;'
                  'color:%s;font-weight:%s;line-height:15px;background:%s;">W%d</div>'
                  %(GC(s,e),C["rule2"],MONO,C["ink"] if heavy else C["ink3"],"600" if heavy else "400",
                    C["paper2"] if heavy else "transparent",w["n"]))
    return ('<div style="display:flex;"><div style="width:%dpx;flex:0 0 %dpx;"></div>'
            '<div style="flex:1 1 auto;"><div style="%s">%s</div><div style="%s">%s</div></div></div>'
            %(LBLW,LBLW,TRACK,"".join(mo),TRACK,"".join(wk)))

# ---------- lectures ----------
def lectures(h=62):
    o=[overlays(h)]
    prev=None
    for dt,s in sorted(SESS.items()):
        off = 16 if (prev and (dt-prev).days<=1) else 0
        prev=dt
        ty = s["type"]
        if ty=="review":
            mark='<div style="width:0;height:0;border-left:3.5px solid transparent;border-right:3.5px solid transparent;border-bottom:6px solid %s;"></div>'%C["lec"]
        elif ty=="contingency":
            mark='<div style="width:6px;height:6px;border-radius:50%%;border:1px dashed %s;"></div>'%C["ink3"]
        else:
            mark='<div style="width:6px;height:6px;border-radius:50%%;background:%s;"></div>'%C["lec"]
        rev = ty=="review"
        o.append('<div style="%sgrid-row:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;height:%dpx;gap:2px;padding-top:%dpx;">'
                 '%s<span style="font-family:%s;font-size:8px;font-weight:%s;color:%s;letter-spacing:-0.02em;white-space:nowrap;">%s</span></div>'
                 %(GC(dt,dt),h,off+6,mark,MONO,"600" if rev else "500",C["ink3"] if ty=="contingency" else C["lecd"],s["short_label"]))
    return "".join(o)

# ---------- exams ----------
def exams(h=76):
    o=[overlays(h)]
    lanes={"Exam 1":4,"Exam 2":4,"Final Exam":44}
    for e in EX:
        y=lanes[e["label"]]
        isfin = e["date"] is None
        o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:14px;background:%s;border:0.75px solid %s;border-radius:2px;'
                 'display:flex;align-items:center;justify-content:%s;padding:0 5px;position:relative;">'
                 '<span style="font-family:%s;font-size:8.5px;font-weight:600;color:%s;letter-spacing:0.05em;white-space:nowrap;%s">%s</span></div>'
                 %(GC(e["cs"],e["ce"]),y,C["ext"],C["exm"],"flex-start",MONO,C["exd"],
                   "",
                   "FINAL EXAM &middot; CUMULATIVE &middot; DATE TBA" if isfin else e["label"].upper()+" COVERAGE"))
        if e["es"] and e["ee"]:
            o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:14px;background:%s;border:0.75px solid %s;'
                     'border-radius:2px;display:flex;align-items:center;justify-content:center;position:relative;z-index:2;">'
                     '<span style="font-family:%s;font-size:7px;font-weight:600;color:%s;letter-spacing:0.04em;'
                     'white-space:nowrap;">EMPHASIS</span></div>'%(GC(e["es"],e["ee"]),y,C["exm"],C["ex"],MONO,C["exd"]))
        if e["date"]:
            o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:16px;display:flex;align-items:center;justify-content:center;">'
                     '<div style="background:%s;color:#fff;font-family:%s;font-size:8.5px;font-weight:600;padding:1.5px 5px;border-radius:2px;'
                     'white-space:nowrap;transform:translateX(2px);line-height:12px;position:relative;z-index:3;">%s</div></div>'%(GC(e["date"],e["date"]),y+18,C["ex"],MONO,e["label"].upper()))
    return "".join(o)

# ---------- homework ----------
def homework(h=88):
    o=[overlays(h)]
    for s in SPANS:
        if s["role"]!="hw": continue
        y = 8 + s["lane"]*26
        o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:17px;background:%s;border-radius:2px 8px 8px 2px;border-left:2.5px solid %s;'
                 'display:flex;align-items:center;justify-content:space-between;padding:0 2px 0 4px;position:relative;z-index:1;">'
                 '<span style="font-family:%s;font-size:8.5px;font-weight:600;color:%s;letter-spacing:0.02em;">%s</span>'
                 '<span style="width:0;height:0;border-top:4px solid transparent;border-bottom:4px solid transparent;border-left:6px solid %s;"></span></div>'
                 %(GC(s["s"],s["e"]),y,C["hwm"],C["hw"],MONO,C["hwd"],s["id"],C["hw"]))
    return "".join(o)

# ---------- labs ----------
def labs_lane(h=122):
    o=[overlays(h)]
    for i,l in enumerate(LABS):
        y=8+i*38
        o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:16px;background:%s;border-radius:2px 8px 8px 2px;border-left:2.5px solid %s;'
                 'display:flex;align-items:center;padding-left:7px;overflow:hidden;">'
                 '<span style="font-family:%s;font-size:8.5px;font-weight:600;color:%s;white-space:nowrap;overflow:hidden;'
                 'text-overflow:ellipsis;">Lab %s &middot; %s</span></div>'
                 %(GC(l["s23"],l["due"]),y+1,C["labm"],C["lab"],MONO,C["labd"],l["num"],l["title"]))
        for d,txt in ((l["s01"]-timedelta(days=1),"PL"),(l["s23"]-timedelta(days=1),"PL")):
            o.append('<div style="%sgrid-row:1;margin-top:%dpx;display:flex;justify-content:center;">'
                     '<span style="width:7px;height:7px;flex:0 0 7px;border:1px dashed %s;background:%s;"></span></div>'%(GC(d,d),y+5,C["lab"],C["paper"]))
        o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:14px;display:flex;align-items:center;justify-content:center;gap:1px;">'
                 '<span style="width:7px;height:7px;flex:0 0 7px;border-radius:50%%;background:%s;"></span></div>'%(GC(l["s01"],l["s01"]),y+5,C["lab"]))
        o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:14px;display:flex;align-items:center;justify-content:center;">'
                 '<span style="width:7px;height:7px;flex:0 0 7px;border-radius:50%%;background:%s;"></span></div>'%(GC(l["s23"],l["s23"]),y+5,C["lab"]))
        o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:14px;display:flex;align-items:center;justify-content:flex-start;">'
                 '<span style="background:%s;color:#fff;font-family:%s;font-size:8px;font-weight:600;padding:1px 4px;border-radius:2px;'
                 'white-space:nowrap;transform:translateX(6px);line-height:11px;">R%s due</span></div>'%(GC(l["due"],l["due"]),y+2,C["lab"],MONO,l["num"]))
    return "".join(o)

# ---------- load ribbon ----------
def ribbon(h=106):
    o=[]
    KC={"due":C["hw"],"prelab":C["labm"],"report":C["lab"],"exam":C["ex"]}
    for w in WEEKS:
        s=max(w["start"],START); e=min(w["end"],END)
        items=TOTAL_DUE[w["n"]]
        blocks="".join('<div style="height:8px;background:%s;border-radius:1px;"></div>'%KC[c["kind"]] for c in items)
        n=len(items)
        o.append('<div style="%sgrid-row:1;height:%dpx;border-left:0.75px solid %s;display:flex;flex-direction:column;'
                 'justify-content:flex-end;padding:0 3px 3px;gap:2px;background:%s;">%s'
                 '<div style="font-family:%s;font-size:8px;font-weight:%s;color:%s;text-align:center;line-height:11px;">%s</div></div>'
                 %(GC(s,e),h,C["rule2"],C["paper2"] if n>=3 else "transparent",blocks,MONO,
                   "600" if n>=3 else "400",C["ink"] if n>=3 else C["ink3"],n if n else "&middot;"))
    return "".join(o)

def legend():
    it=[('<span style="width:7px;height:7px;border-radius:50%%;background:%s;display:block;"></span>'%C["lec"],"lecture"),
        ('<span style="width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-bottom:7px solid %s;display:block;"></span>'%C["lec"],"exam review"),
        ('<span style="width:7px;height:7px;border-radius:50%%;border:1px dashed %s;display:block;"></span>'%C["ink3"],"optional / contingency"),
        ('<span style="width:22px;height:10px;background:%s;border:0.75px solid %s;display:block;"></span>'%(C["ext"],C["exm"]),"exam coverage"),
        ('<span style="width:1.5px;height:12px;background:%s;display:block;"></span>'%C["ex"],"exam date"),
        ('<span style="width:24px;height:10px;background:%s;border-left:2.5px solid %s;border-radius:1px 5px 5px 1px;display:block;"></span>'%(C["hwm"],C["hw"]),"HW open → due"),
        ('<span style="width:7px;height:7px;flex:0 0 7px;border:1px dashed %s;display:block;"></span>'%C["lab"],"pre-lab due"),
        ('<span style="width:7px;height:7px;border-radius:50%%;background:%s;display:block;"></span>'%C["lab"],"lab session"),
        ('<span style="width:24px;height:10px;background:%s;border-left:2.5px solid %s;border-radius:1px 5px 5px 1px;display:block;"></span>'%(C["labm"],C["lab"]),"report writing → due"),
        ('<span style="width:16px;height:11px;background:%s;display:block;border:0.75px solid %s;"></span>'%(HATCH,C["rule"]),"no class / break / finals")]
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
<div style="width:1440px;height:706px;background:{paper};padding:34px 40px 28px;display:flex;flex-direction:column;color:{ink};">
  <div style="display:flex;align-items:baseline;justify-content:space-between;padding-bottom:12px;">
    <div>
      <div style="font-family:'IBM Plex Serif',Georgia,serif;font-size:26px;font-weight:600;letter-spacing:-0.01em;line-height:28px;">CIVL 2050 &middot; Fluid Mechanics</div>
      <div style="font-size:12px;color:{ink2};line-height:16px;padding-top:3px;">One continuous timeline &mdash; what is open, what is due, and what each exam covers.</div>
    </div>
    <div style="text-align:right;">
      <div style="font-family:{MONO};font-size:13px;font-weight:600;letter-spacing:0.08em;">FALL 2026</div>
      <div style="font-family:{MONO};font-size:9.5px;color:{ink3};letter-spacing:0.04em;">AUG 27 &ndash; DEC 22 &middot; 28 CLASS MEETINGS</div>
    </div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:7px 18px;align-items:center;padding:8px 0 10px;border-top:1.5px solid {ink};border-bottom:0.75px solid {rule};">{legend}</div>
  <div style="padding-top:8px;">{ruler}</div>
  {lect}
  {exam}
  {hwl}
  {labs}
  {rib}
  <div style="border-top:1.5px solid {ink};display:flex;justify-content:space-between;align-items:baseline;padding-top:7px;margin-top:auto;">
    <div style="font-family:{MONO};font-size:8.5px;color:{ink3};letter-spacing:0.04em;">GENERATED FROM SOURCE TABLES &middot; DO NOT HAND-EDIT</div>
    <div style="font-family:{MONO};font-size:8.5px;color:{ink3};letter-spacing:0.04em;">VERTICAL RULE = EXAM DATE &middot; EVERYTHING LEFT OF IT IS IN SCOPE</div>
  </div>
</div>
</x-dc>
</body>
</html>
""".format(SANS=SANS,MONO=MONO,legend=legend(),ruler=ruler(),
           lect=lane("Lectures","28 meetings",lectures(),62),
           exam=lane("Exams","coverage → date",exams(),76),
           hwl=lane("Homework","10 sets",homework(),88),
           labs=lane("Labs","3 + reports",labs_lane(),122),
           rib=lane("Weekly load","items due",ribbon(),106),
           **C)
open("TrackView.dc.html","w").write(HTML)
print("bytes",len(HTML))
