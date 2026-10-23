# chiespring-site

Static files exactly as served at the public site (baseline 2026-09-26, exported from the live server).
Languages: English at the root, Japanese in /ja/, Russian in /ru/ (where present).
Every change to main goes through a pull request; name the Work Board ID in each commit and pull request.
No passwords, keys or server configuration belong in this repository.

## Building the pages
The pages are generated from `src/`: shared header, menu, language switch, footer and page start live once per language in `src/partials/<lang>/`; each page source in `src/pages/<lang>/` holds only what is unique to that page.
- Change a shared part: edit the partial, run `python tools/build.py`, commit the source and the generated pages together.
- `python tools/build.py --check` rebuilds in memory and fails if any generated page differs from the file on disk (use it before every pull request).
- `tools/extract_templates.py` is the one-off script that split the original pages; it is kept as provenance and is not needed again.
