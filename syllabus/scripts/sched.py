# -*- coding: utf-8 -*-
import csv
from datetime import datetime, date, timedelta
from collections import defaultdict
D="/Users/daniellander/Library/Mobile Documents/com~apple~CloudDocs/RPI/_Teaching/CIVL 2050 - Fluid Mechanics/_AI_automation/_archive/matplotlib_prep_v0_3/CIVL2050_semester_prep_system_v0_3/data/"
p=lambda s: datetime.strptime(s,"%Y-%m-%d").date()
rd=lambda f: list(csv.DictReader(open(D+f)))
LABD=D

CAL={p(r["date"]):r for r in rd("calendar_days.csv")}
_S=rd("sessions.csv")
for r in _S:
    r.setdefault("short_label", "C%02d" % int(r["session_no"]))
SESS={p(r["date"]):r for r in _S if r["type"]!="exam"}     # lectures + reviews + contingency
SESSION_NO={p(r["date"]):int(r["session_no"]) for r in _S}
N_SESSIONS=len(_S)
N_LECT=sum(1 for r in _S if r["type"]=="lecture")
N_REV=sum(1 for r in _S if r["type"]=="review")
N_COUNTED=N_LECT+N_REV
HW=[{"id":r["id"],"a":p(r["available_date"]),"d":p(r["due_date"]),"note":r["rule_note"],
     "covers":r.get("covers_classes", ""),"topics":r.get("topics", ""),"drop":r.get("drop_eligible", "yes")=="yes"}
    for r in rd("homework.csv")]
LABS=[{"id":r["id"],"num":r["id"][-1],"title":r["title"],"s01":p(r["s01_date"]),
       "s23":p(r["s02_date"]),"due":p(r["report_due_date"])}
      for r in csv.DictReader(open(LABD+"labs.csv"))]
EX=[{"id":r["id"],"label":r["label"],"date":None if r["date"]=="TBA" else p(r["date"]),
     "cs":p(r["coverage_start"]),"ce":p(r["coverage_end"]),
     "es":p(r["emphasis_start"]) if r["emphasis_start"] else None,
     "ee":p(r["emphasis_end"]) if r["emphasis_end"] else None,
     "note":r["scope_note"]} for r in rd("exams.csv")]

START,END=date(2026,8,24),date(2026,12,22)
WEEKS=[]; d=START; n=1
while d<=END:
    WEEKS.append({"n":n,"start":d,"end":d+timedelta(days=6)}); d+=timedelta(days=7); n+=1
# weeks 17-18 hold no sessions and no deliverables -> merged into one closing band
CLOSE_FROM=17

CHIP=defaultdict(list)
for dt,s in SESS.items():
    k={"review":"review","contingency":"contingency"}.get(s["type"],"lecture")
    CHIP[dt].append({"role":"lect","kind":k,"text":s["short_label"]})
for e in EX:
    if e["date"]: CHIP[e["date"]].append({"role":"exam","kind":"exam","text":e["label"].upper()})
for h in HW: CHIP[h["d"]].append({"role":"hw","kind":"due","text":h["id"]})
for l in LABS:
    CHIP[l["s01"]-timedelta(days=1)].append({"role":"lab","kind":"prelab","text":"PL%s 01"%l["num"]})
    CHIP[l["s23"]-timedelta(days=1)].append({"role":"lab","kind":"prelab","text":"PL%s 02·03"%l["num"]})
    CHIP[l["s01"]].append({"role":"lab","kind":"session","text":"Lab%s 01"%l["num"]})
    CHIP[l["s23"]].append({"role":"lab","kind":"session","text":"Lab%s 02·03"%l["num"]})
    CHIP[l["due"]].append({"role":"lab","kind":"report","text":"R%s"%l["num"]})
ORDER={"exam":0,"lecture":1,"review":1,"contingency":1,"session":2,"due":3,"prelab":4,"report":3}
for k in CHIP: CHIP[k].sort(key=lambda c:ORDER[c["kind"]])

SPANS=[]
for h in HW:  SPANS.append({"role":"hw","id":h["id"],"s":h["a"],"e":h["d"]})
for l in LABS: SPANS.append({"role":"lab","id":"Report %s"%l["num"],"s":l["s23"],"e":l["due"]})
def pack(items):
    ends=[]
    for it in sorted(items,key=lambda x:(x["s"],x["e"])):
        for ln in range(len(ends)):
            if ends[ln] < it["s"]:
                it["lane"]=ln; ends[ln]=it["e"]; break
        else:
            it["lane"]=len(ends); ends.append(it["e"])
    return len(ends)
NLANES=pack(SPANS)
SPANS.sort(key=lambda x:(x["lane"],x["s"]))

def week_segments(w):
    out=[]
    for sp in SPANS:
        if sp["e"] < w["start"] or sp["s"] > w["end"]: continue
        vs=max(sp["s"],w["start"]); ve=min(sp["e"],w["end"])
        out.append({"role":sp["role"],"id":sp["id"],"lane":sp["lane"],
                    "c0":(vs-w["start"]).days,"c1":(ve-w["start"]).days,
                    "cl":sp["s"]<w["start"],"cr":sp["e"]>w["end"]})
    return out
def status(dt):
    c=CAL.get(dt)
    return (c["status"],c["label"]) if c else ("","")
TOTAL_DUE={}
for w in WEEKS:
    days=[w["start"]+timedelta(days=i) for i in range(7)]
    TOTAL_DUE[w["n"]]=[c for dt in days for c in CHIP.get(dt,[]) if c["kind"] in ("due","prelab","report","exam")]
N_DEADLINES=sum(len(v) for v in TOTAL_DUE.values())+1
