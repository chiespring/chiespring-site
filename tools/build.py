"""Build the chiespring.com pages from src/ (shared partials + per-page sources).

  python tools/build.py          write the pages (root, ja/, ru/)
  python tools/build.py --check  build in memory and compare with the files on disk (exit 1 on any difference)

Header, menu, language switch, footer and the page head start are edited once in src/partials/<lang>/;
each page source in src/pages/<lang>/ holds only what is unique to that page. Output keeps CRLF line ends.
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRLF = "\r\n"
LANGS = {"en": "", "ja": "ja/", "ru": "ru/"}
SLUGS = ["index", "books", "concept", "contact", "experience"]
PAGES_EXTRA = ["language-tools"]  # category pages
# "New" strip on the home page: date of the day the Russian tools went public (edit on go-public day)
NEW_STRIP_DATE = (2026, 10, 24)
NEW_STRIP_LABEL = {
    "ja": "%d年%d月%d日に追加",
    "en": "Added %d %s %d",
    "ru": "Добавлено: %02d.%02d.%d",
}
MONTHS_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def new_strip_label(lang):
    y, m, d = NEW_STRIP_DATE
    if lang == "ja": return NEW_STRIP_LABEL["ja"] % (y, m, d)
    if lang == "en": return NEW_STRIP_LABEL["en"] % (d, MONTHS_EN[m - 1], y)
    return NEW_STRIP_LABEL["ru"] % (d, m, y)

def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8", newline="").read()

def lang_hrefs(lang, slug):
    b = "" if slug == "index" else slug + ".html"
    if lang == "en":
        return {"ja": "ja/" + b, "en": "./" if slug == "index" else b, "ru": "ru/" + b}
    return {"ja": "../ja/" + b, "en": "../" + b, "ru": "../ru/" + b}

def build_page(lang, slug):
    lines = rd(f"src/pages/{lang}/{slug}.html").split(CRLF)
    hrefs = lang_hrefs(lang, slug)
    out = []
    for l in lines:
        if l.startswith("{{") and l.endswith("}}") and l[2:-2] in ("head_top", "header_home", "header_inner", "footer"):
            part = rd(f"src/partials/{lang}/{l[2:-2]}.html")
            for k, v in hrefs.items():
                part = part.replace("{{href_%s}}" % k, v)
            out.append(part)
        else:
            out.append(l)
    text = CRLF.join(out).replace("{{new_strip_label}}", new_strip_label(lang))
    assert "{{" not in text, f"unresolved placeholder in {lang}/{slug}"
    return text

def main():
    check = "--check" in sys.argv
    bad = 0
    for lang, pre in LANGS.items():
        for slug in SLUGS + PAGES_EXTRA:
            rel = f"{pre}{slug}.html"
            text = build_page(lang, slug)
            path = os.path.join(ROOT, rel)
            if check:
                cur = open(path, encoding="utf-8", newline="").read() if os.path.exists(path) else None
                if cur != text:
                    bad += 1; print("DIFFERENT:", rel)
            else:
                open(path, "w", encoding="utf-8", newline="").write(text)
    if check:
        print(("all %d pages identical to the build" % (3 * (len(SLUGS) + len(PAGES_EXTRA)))) if not bad else f"{bad} page(s) differ")
        sys.exit(1 if bad else 0)
    print("built")

main()
