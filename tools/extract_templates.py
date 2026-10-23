"""One-off: split today's 15 pages into shared partials + per-page sources (provenance of src/).
Run once from the repo root; build.py then regenerates the pages byte-for-byte."""
import os, re
PAGES = ["index", "books", "concept", "contact", "experience"]
LANGS = {"en": "", "ja": "ja/", "ru": "ru/"}
CRLF = "\r\n"
HDR_START = '<div style="width: 100%; box-sizing: border-box; background: #FFFFFF; border-bottom'
FTR_START = '<div style="background: #2A2130;">'

def rd(p): return open(p, encoding="utf-8", newline="").read().split(CRLF)
def wr(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="").write(CRLF.join(lines))

for lang, pre in LANGS.items():
    part = {}
    for slug in PAGES:
        t = rd(f"{pre}{slug}.html")
        hs = next(i for i, l in enumerate(t) if l.startswith(HDR_START))
        li = next(i for i, l in enumerate(t) if 'class="lang"' in l)
        fs = next(i for i, l in enumerate(t) if l == FTR_START)
        head_top, header, footer = t[0:5], t[hs:li + 3], t[fs:]
        # template the three language-switch links
        hdr = []
        for l in header:
            if 'class="lang"' in l:
                head, tail = l.split('class="lang">', 1)
                for ph in ("ja", "en", "ru"):
                    tail = re.sub(r'href="[^"]*"( hreflang="%s")' % ph, r'href="{{href_%s}}"\1' % ph, tail, count=1)
                l = head + 'class="lang">' + tail
            hdr.append(l)
        kind = "home" if slug == "index" else "inner"
        for name, val in (("head_top", head_top), (f"header_{kind}", hdr), ("footer", footer)):
            key = (name, CRLF.join(val))
            part.setdefault(name, key[1])
            assert part[name] == key[1], f"{lang}/{slug}: {name} differs from the first page"
        page = t[:0] + ["{{head_top}}"] + t[5:hs] + ["{{header_%s}}" % kind] + t[li + 3:fs] + ["{{footer}}"]
        wr(f"src/pages/{lang}/{slug}.html", page)
    for name, val in part.items():
        os.makedirs(f"src/partials/{lang}", exist_ok=True)
        open(f"src/partials/{lang}/{name}.html", "w", encoding="utf-8", newline="").write(val)
print("extracted")
