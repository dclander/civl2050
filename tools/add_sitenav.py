#!/usr/bin/env python3
"""Insert (or refresh) the shared site navigation in every published page.

Run from the repository root after adding or replacing anything under docs/:

    python3 tools/add_sitenav.py

It edits docs/index.html, docs/aids/index.html and docs/aids/*/index.html in
place. The block it writes is delimited by <!--sitenav:start--> ... <!--sitenav:end-->
and is removed before being rewritten, so running the script twice is safe and
the working copies of the aids never need to carry the markup themselves.

The bar's content column is matched to each page by reading that page's own
.wrap{max-width:...} rule, so the links line up with the text beneath them.
"""
import os, re, sys

CSS = """<style>
.sitenav{--nv-ink:#4E565F;--nv-ink2:#8A857C;--nv-on:#15181C;--nv-rule:#DCD9D3;
 font-family:"IBM Plex Sans",system-ui,-apple-system,sans-serif;font-size:13.5px;
 border-bottom:1px solid var(--nv-rule)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .sitenav{
 --nv-ink:#A7B0B8;--nv-ink2:#78828B;--nv-on:#E9ECEE;--nv-rule:#2C3339}}
:root[data-theme="dark"] .sitenav{
 --nv-ink:#A7B0B8;--nv-ink2:#78828B;--nv-on:#E9ECEE;--nv-rule:#2C3339}
.sitenav-in{max-width:var(--navw,1140px);margin:0 auto;
 padding:10px var(--navp,24px);display:flex;align-items:baseline;gap:20px}
.sitenav-brand{font-weight:600;color:var(--nv-on);letter-spacing:-.01em;margin-right:auto}
.sitenav a{color:var(--nv-ink);text-decoration:none;white-space:nowrap}
.sitenav a:hover{color:var(--nv-on)}
.sitenav a[aria-current="page"]{color:var(--nv-on);font-weight:600}
@media (max-width:520px){.sitenav-brand{display:none}.sitenav-in{gap:16px}}
</style>"""

START, END = "<!--sitenav:start-->", "<!--sitenav:end-->"
LINKS = [("Schedule", "sched"), ("In-class aids", "aids")]


def bar(depth, here, width, pad):
    """depth: 0 at docs/, 1 at docs/aids/, 2 at docs/aids/<slug>/."""
    if depth == 0:
        href = {"sched": "./", "aids": "aids/"}
    elif depth == 1:
        href = {"sched": "../", "aids": "./"}
    else:
        href = {"sched": "../" * depth, "aids": "../"}
    out = []
    for label, key in LINKS:
        cur = ' aria-current="page"' if key == here else ""
        out.append('<a href="%s"%s>%s</a>' % (href[key], cur, label))
    return ('<nav class="sitenav" style="--navw:%dpx;--navp:%dpx" aria-label="Site">'
            '<div class="sitenav-in"><span class="sitenav-brand">CIVL 2050</span>'
            '%s</div></nav>' % (width, pad, "".join(out)))


def strip(s):
    while START in s and END in s:
        a, b = s.index(START), s.index(END) + len(END)
        s = s[:a] + s[b:]
    return s


def width_of(s, default=1140):
    m = re.search(r"\.wrap\{[^}]*max-width:\s*(\d+)px", s)
    return int(m.group(1)) if m else default


def pad_of(s, default=24):
    """The page's horizontal .wrap padding, so the bar lines up with the text."""
    m = re.search(r"\.wrap\{[^}]*?padding-left:\s*(\d+)px", s)
    if m:
        return int(m.group(1))
    m = re.search(r"\.wrap\{[^}]*?padding:\s*(\d+)px(?:\s+(\d+)px)?", s)
    if m:
        return int(m.group(2) or m.group(1))
    return default


def process(path, depth, here):
    s = open(path, encoding="utf-8").read()
    s = strip(s)
    if "</head>" not in s:
        print("  skip (no </head>):", path); return
    m = re.search(r"<body[^>]*>", s)
    if not m:
        print("  skip (no <body>):", path); return
    block_head = START + CSS + END
    block_body = START + bar(depth, here, width_of(s), pad_of(s)) + END
    s = s.replace("</head>", block_head + "</head>", 1)
    m = re.search(r"<body[^>]*>", s)
    s = s[:m.end()] + "\n" + block_body + s[m.end():]
    open(path, "w", encoding="utf-8").write(s)
    print("  ok  ", path)


def main(root="docs"):
    if not os.path.isdir(root):
        sys.exit("run this from the repository root (no %s/ here)" % root)
    process(os.path.join(root, "index.html"), 0, "sched")
    aids = os.path.join(root, "aids")
    process(os.path.join(aids, "index.html"), 1, "aids")
    for name in sorted(os.listdir(aids)):
        p = os.path.join(aids, name, "index.html")
        if os.path.isfile(p):
            process(p, 2, None)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs")
