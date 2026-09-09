# -*- coding: utf-8 -*-
from sched import *
from datetime import timedelta
C = dict(lec="#3e66b3",lecd="#254582",hw="#9d5300",hwd="#713500",hwt="#fde9d9",hwm="#e2b38d",
         lab="#007f56",labd="#005938",labt="#dbf4e8",labm="#90ceb2",
         ex="#a7463c",exd="#782a24",ext="#ffe6e2",exm="#eaaca3",
         ink="#191610",ink2="#504d47",ink3="#83807b",
         paper="#fcfaf6",paper2="#f5f1ec",rule="#d8d5d1",rule2="#c0bdb9")
MONO="'IBM Plex Mono', ui-monospace, Menlo, monospace"
SANS="'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif"
HATCH="repeating-linear-gradient(45deg, #efeae3 0 4px, #e5dfd7 4px 8px)"
W, LBL = 816, 74
NDAYS=(END-START).days+1
idx=lambda d:(d-START).days
GC=lambda a,b:"grid-column:%d / %d;"%(idx(a)+1, idx(b)+2)
TRACK="display:grid;grid-template-columns:repeat(%d, minmax(0, 1fr));"%NDAYS

def breaks(h):
    o=[]; runs=[]; cur=None
    for i in range(NDAYS):
        d=START+timedelta(days=i); st,_=status(d)
        k=st if st in ("no_class","break","study","finals") else ""
        if k!=cur:
            if cur: runs[-1]["e"]=d-timedelta(days=1)
            if k: runs.append({"s":d,"e":d,"k":k})
            cur=k
        elif k: runs[-1]["e"]=d
    for r in runs: o.append('<div style="%sgrid-row:1;background:%s;height:%dpx;"></div>'%(GC(r["s"],r["e"]),HATCH,h))
    for e in EX:
        if e["date"]:
            o.append('<div style="%sgrid-row:1;height:%dpx;border-left:1.25px solid %s;opacity:0.6;"></div>'%(GC(e["date"],e["date"]),h,C["ex"]))
    return "".join(o)

def lane(label, content, h):
    return ('<div style="display:flex;border-top:0.75px solid %s;">'
            '<div style="width:%dpx;flex:0 0 %dpx;padding:5px 8px 0 0;text-align:right;'
            'font-family:%s;font-size:11px;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;color:%s;line-height:13px;">%s</div>'
            '<div style="flex:1 1 auto;position:relative;height:%dpx;%s">%s</div></div>'
            %(C["rule"],LBL,LBL,SANS,C["ink2"],label,h,TRACK,content))

def ruler():
    mo=[]
    for nm,mn in [("AUG",8),("SEPTEMBER",9),("OCTOBER",10),("NOVEMBER",11),("DECEMBER",12)]:
        ds=[START+timedelta(days=i) for i in range(NDAYS) if (START+timedelta(days=i)).month==mn]
        mo.append('<div style="%sgrid-row:1;border-left:1.25px solid %s;padding-left:4px;font-family:%s;font-size:10px;'
                  'font-weight:600;letter-spacing:0.1em;color:%s;line-height:15px;">%s</div>'%(GC(ds[0],ds[-1]),C["ink"],MONO,C["ink"],nm))
    wk=[]
    for w in WEEKS:
        s=max(w["start"],START); e=min(w["end"],END)
        heavy=len(TOTAL_DUE[w["n"]])>=3
        wk.append('<div style="%sgrid-row:1;border-left:0.75px solid %s;text-align:center;font-family:%s;font-size:9px;'
                  'color:%s;font-weight:%s;line-height:14px;background:%s;">%d</div>'
                  %(GC(s,e),C["rule2"],MONO,C["ink"] if heavy else C["ink3"],"700" if heavy else "400",
                    C["paper2"] if heavy else "transparent",w["n"]))
    return ('<div style="display:flex;"><div style="width:%dpx;flex:0 0 %dpx;padding-right:8px;text-align:right;'
            'font-family:%s;font-size:9px;color:%s;line-height:29px;">week</div>'
            '<div style="flex:1 1 auto;"><div style="%s">%s</div><div style="%s">%s</div></div></div>'
            %(LBL,LBL,MONO,C["ink3"],TRACK,"".join(mo),TRACK,"".join(wk)))

def exams(h=64):
    o=[breaks(h)]
    for e in EX:
        fin = e["date"] is None
        y = 42 if fin else 2
        o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:16px;background:%s;border:0.75px solid %s;border-radius:2px;'
                 'display:flex;align-items:center;padding:0 5px;position:relative;z-index:1;">'
                 '<span style="font-family:%s;font-size:10px;font-weight:600;color:%s;white-space:nowrap;">%s</span></div>'
                 %(GC(e["cs"],e["ce"]),y,C["ext"],C["exm"],MONO,C["exd"],
                   "FINAL &middot; cumulative &middot; TBA" if fin else e["label"].upper()+" coverage"))
        if e["es"]:
            o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:16px;background:%s;border:0.75px solid %s;border-radius:2px;'
                     'position:relative;z-index:2;"></div>'%(GC(e["es"],e["ee"]),y,C["exm"],C["ex"]))
        if e["date"]:
            o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:16px;display:flex;align-items:center;justify-content:center;'
                     'position:relative;z-index:3;"><span style="background:%s;color:#fff;font-family:%s;font-size:10px;font-weight:600;'
                     'padding:1px 4px;border-radius:2px;white-space:nowrap;line-height:13px;position:absolute;right:calc(100%% - 3px);">%s</span></div>'
                     %(GC(e["date"],e["date"]),y+20,C["ex"],MONO,e["label"].upper()))
    return "".join(o)

def localpack(role):
    items=[dict(x) for x in SPANS if x["role"]==role]
    ends=[]
    for it in sorted(items,key=lambda x:(x["s"],x["e"])):
        for ln in range(len(ends)):
            if ends[ln] < it["s"]: it["lane"]=ln; ends[ln]=it["e"]; break
        else: it["lane"]=len(ends); ends.append(it["e"])
    return items, len(ends)

def spans(role,h,pitch,tint,solid,dark):
    items,_=localpack(role)
    o=[breaks(h)]
    for s in items:
        y=2+s["lane"]*pitch
        o.append('<div style="%sgrid-row:1;margin-top:%dpx;height:%dpx;background:%s;border-radius:2px 7px 7px 2px;'
                 'border-left:2.5px solid %s;display:flex;align-items:center;padding-left:4px;overflow:hidden;'
                 'position:relative;z-index:1;"><span style="font-family:%s;font-size:10px;font-weight:600;color:%s;'
                 'white-space:nowrap;">%s</span></div>'
                 %(GC(s["s"],s["e"]),y,pitch-3,tint,solid,MONO,dark,s["id"].replace("Report ","Lab ")))
    return "".join(o)

def lectures(h=46):
    o=[breaks(h)]; prev=None; lastoff=0
    for dt,ss in sorted(SESS.items()):
        off = 14 if (prev and (dt-prev).days<=3 and lastoff==0) else 0
        prev=dt; lastoff=off; ty=ss["type"]
        if ty=="review":
            mark='<div style="width:0;height:0;border-left:3px solid transparent;border-right:3px solid transparent;border-bottom:5px solid %s;"></div>'%C["lec"]
        elif ty=="contingency":
            mark='<div style="width:5px;height:5px;border-radius:50%%;border:1px dashed %s;"></div>'%C["ink3"]
        else:
            mark='<div style="width:5px;height:5px;border-radius:50%%;background:%s;"></div>'%C["lec"]
        o.append('<div style="%sgrid-row:1;display:flex;flex-direction:column;align-items:center;height:%dpx;gap:1px;padding-top:%dpx;">'
                 '%s<span style="font-family:%s;font-size:9.5px;font-weight:%s;color:%s;white-space:nowrap;letter-spacing:-0.04em;">%s</span></div>'
                 %(GC(dt,dt),h,off+4,mark,MONO,"700" if ty=="review" else "500",
                   C["ink3"] if ty=="contingency" else C["lecd"],ss["short_label"]))
    return "".join(o)

def ribbon(h=52):
    KC={"due":C["hw"],"prelab":C["labm"],"report":C["lab"],"exam":C["ex"]}
    o=[]
    for w in WEEKS:
        a=max(w["start"],START); b=min(w["end"],END)
        items=TOTAL_DUE[w["n"]]; n=len(items)
        blocks="".join('<div style="height:6px;background:%s;border-radius:1px;"></div>'%KC[c["kind"]] for c in items)
        o.append('<div style="%sgrid-row:1;height:%dpx;border-left:0.75px solid %s;display:flex;flex-direction:column;'
                 'justify-content:flex-end;padding:0 2px 2px;gap:1.5px;background:%s;">%s'
                 '<div style="font-family:%s;font-size:8px;font-weight:%s;color:%s;text-align:center;line-height:10px;">%s</div></div>'
                 %(GC(a,b),h,C["rule2"],C["paper2"] if n>=3 else "transparent",blocks,MONO,
                   "700" if n>=3 else "400",C["ink"] if n>=3 else C["ink3"],n if n else "&middot;"))
    return "".join(o)

def legend():
    it=[('<span style="width:20px;height:10px;background:%s;border:0.75px solid %s;display:block;"></span>'%(C["ext"],C["exm"]),"exam coverage"),
        ('<span style="width:20px;height:10px;background:%s;border:0.75px solid %s;display:block;"></span>'%(C["exm"],C["ex"]),"final emphasis"),
        ('<span style="width:1.5px;height:11px;background:%s;display:block;"></span>'%C["ex"],"exam date"),
        ('<span style="width:22px;height:10px;background:%s;border-left:2.5px solid %s;border-radius:1px 5px 5px 1px;display:block;"></span>'%(C["hwm"],C["hw"]),"homework open → due"),
        ('<span style="width:22px;height:10px;background:%s;border-left:2.5px solid %s;border-radius:1px 5px 5px 1px;display:block;"></span>'%(C["labm"],C["lab"]),"lab report writing → due"),
        ('<span style="width:15px;height:10px;background:%s;border:0.75px solid %s;display:block;"></span>'%(HATCH,C["rule"]),"no class / break / finals"),
        ('<span style="width:6px;height:6px;border-radius:50%%;background:%s;display:block;"></span>'%C["lec"],"class meeting"),
        ('<span style="width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-bottom:6px solid %s;display:block;"></span>'%C["lec"],"exam review"),
        ('<span style="width:5px;height:5px;border-radius:50%%;border:1px dashed %s;display:block;"></span>'%C["ink3"],"optional")]
    return "".join('<div style="display:flex;align-items:center;gap:5px;">%s<span style="font-size:10px;color:%s;">%s</span></div>'%(s,C["ink2"],t) for s,t in it)

HTML="""<!doctype html>
<html><head><meta charset="utf-8"><script src="./support.js"></script></head><body>
<x-dc>
<helmet>
  
  <style>body{{margin:0;font-family:{SANS};-webkit-font-smoothing:antialiased;}} *{{box-sizing:border-box;}} a{{color:{hw};}}</style>
</helmet>
<div style="width:816px;background:{paper};color:{ink};padding:2px 4px 4px;">
  <div style="display:flex;flex-wrap:wrap;gap:4px 14px;align-items:center;padding:0 0 7px;">{legend}</div>
  {ruler}
  {lect}
  {exam}
  {hwl}
  {labl}
  {rib}
  <div style="display:flex;justify-content:flex-end;padding-top:5px;">
    <span style="font-family:{MONO};font-size:8px;color:{ink3};letter-spacing:0.02em;">SHADED WEEK NUMBER = 3 OR MORE DEADLINES &middot; VERTICAL RULE = EXAM DATE</span>
  </div>
</div>
</x-dc></body></html>
""".format(SANS=SANS,MONO=MONO,legend=legend(),ruler=ruler(),
           lect=lane("Classes",lectures(),46),
           exam=lane("Exams",exams(),64),
           hwl=lane("Homework",spans("hw",64,20,C["hwm"],C["hw"],C["hwd"]),64),
           labl=lane("Labs",spans("lab",24,20,C["labm"],C["lab"],C["labd"]),24),
           rib=lane("Weekly load",ribbon(),52),
           **C)
open("CompactTrack.dc.html","w").write(HTML)
print("bytes",len(HTML))
