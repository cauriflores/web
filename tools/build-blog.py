#!/usr/bin/env python3
"""Generate cauriflores.com from the sources in src/.

The site is served with .nojekyll, so GitHub Pages copies files rather than
building them. Pages here are generated on this machine and committed, the same
way the Angular app under /pacheco/ is — a build that cannot run cannot fail.

This repo is NOT the one Apple links to. cauriflores.github.io holds Pacheco's
support page and /privacy.html and is frozen; see NAV below.

    python3 tools/build-blog.py

Each post is a directory under src/posts/<slug>/ holding:

    post.json   { "date": "2026-09-05",
                  "title": {"en": ..., "es": ...},
                  "summary": {"en": ..., "es": ...} }
    en.html     the body, as HTML fragments — no <html>, no <body>
    es.html     the same in Spanish

Both languages ship in every page and stack without JavaScript, which is how
the rest of this site already works: nobody is left without something readable.
"""

import html
import json
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "posts"
POSTS_OUT = ROOT / "posts"
# The writing index IS the front page of this site, so it lands at the root.
INDEX_OUT = ROOT

# Standing project pages (Store·Mall, and any future one) — not dated, not in
# the Writing feed, just a page reachable from nav. See src/pages/<slug>/.
SRC_PAGES = ROOT / "src" / "pages"

ASSET_VERSION = 8  # bump when style.css or lang.js changes, or browsers cache the old one

# One honest line on the index while the site is still taking shape. Set to
# False to drop it everywhere at once.
BUILDING_NOTE = True
BUILDING_TEXT = {
    "en": "This site is being built in the open; some pages are still taking shape.",
    "es": "Este sitio se construye a la vista; algunas páginas todavía están tomando forma.",
}

# ⚠️ Support and Privacy are ABSOLUTE, and on a different host on purpose.
# https://cauriflores.github.io/ is Pacheco's App Store support URL and
# /privacy.html the privacy policy Apple checks. Moving either costs a full App
# Store submission, so that site stays frozen and this one links across to it.
# A relative href here would 404 on cauriflores.com.
HUB = "https://cauriflores.github.io"
NAV = [
    ("home", "/", "Updates", "Novedades"),
    # The live Angular app stays at /pacheco/ (its deploy script rsyncs there);
    # the nav goes to the project hub, which links to the app.
    ("pacheco", "/pacheco-project/", "Pacheco", "Pacheco"),
    ("shopmall", "/shopmall/", "Store·Mall", "Store·Mall"),
]
# Support and Privacy (the HUB pages Apple has on file) are Pacheco's, not the
# site's: they are linked from the Pacheco hub page only, never from the chrome.

MONTHS = {
    "en": "January February March April May June July August September October November December".split(),
    "es": "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split(),
}


def long_date(iso: str, lang: str) -> str:
    y, m, d = (int(part) for part in iso.split("-"))
    month = MONTHS[lang][m - 1]
    return f"{month} {d}, {y}" if lang == "en" else f"{d} de {month} de {y}"


def nav_html(current: str, lang: str, depth: int) -> str:
    links = []
    for key, href, en, es in NAV:
        label = en if lang == "en" else es
        if key == current:
            links.append(f'<a href="{href}" aria-current="page">{label}</a>')
        else:
            links.append(f'<a href="{href}">{label}</a>')
    return "<nav>" + "".join(links) + "</nav>"


def page(*, title_en, title_es, description, body_en, body_es, current, depth) -> str:
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title_en)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="{up}favicon.ico?v={ASSET_VERSION}" sizes="any">
<link rel="icon" type="image/png" href="{up}favicon-32.png?v={ASSET_VERSION}" sizes="32x32">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png?v={ASSET_VERSION}">
<meta name="theme-color" content="#c2185b">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,600&family=IBM+Plex+Sans:wght@400;600&display=swap">
<link rel="stylesheet" href="{up}style.css?v={ASSET_VERSION}">
<script>try{{var t=localStorage.getItem("pacheco-theme");if(t==="dark"||t==="light")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
<div class="wrap">

  <div class="langbar" hidden>
    <button type="button" class="theme" aria-pressed="false" aria-label="Dark mode" data-label-en="Dark mode" data-label-es="Modo oscuro">
      <svg viewBox="0 0 24 24" aria-hidden="true"><mask id="moon-mask"><rect width="24" height="24" fill="#fff"/><circle class="mask-moon" cx="26" cy="10" r="7" fill="#000"/></mask><circle class="sun" cx="12" cy="12" r="6" fill="currentColor" mask="url(#moon-mask)"/><g class="rays" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="12" y1="1.5" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22.5"/><line x1="1.5" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22.5" y2="12"/><line x1="4.6" y1="4.6" x2="6.3" y2="6.3"/><line x1="17.7" y1="17.7" x2="19.4" y2="19.4"/><line x1="4.6" y1="19.4" x2="6.3" y2="17.7"/><line x1="17.7" y1="6.3" x2="19.4" y2="4.6"/></g></svg>
    </button>
    <button type="button" data-lang="en">English</button>
    <button type="button" data-lang="es">Español</button>
  </div>
  <span hidden data-title-en="{html.escape(title_en)}" data-title-es="{html.escape(title_es)}"></span>

  <div class="langblock" lang="en">
{body_en}
  </div>

  <div class="langblock" lang="es">
{body_es}
  </div>

</div>
<script src="{up}lang.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


MAIL_USER, MAIL_DOMAIN = "commonerdev", "gmail.com"


def write_to_me(lang: str) -> str:
    text = (
        "Questions, corrections, or just to say it worked for you — write to me at"
        if lang == "en"
        else "Preguntas, correcciones, o solo para contarme que te funcionó: escríbeme a"
    )
    # lang.js turns this into a mailto: link; without JavaScript it stays readable.
    return (
        f'  <p class="write">{text} '
        f'<a class="mail" data-u="{MAIL_USER}" data-d="{MAIL_DOMAIN}" href="#">'
        f"{MAIL_USER} [at] {MAIL_DOMAIN}</a>.</p>"
    )


def post_body(meta, body, lang, current="writing") -> str:
    title = meta["title"][lang]
    back = "All updates" if lang == "en" else "Todas las novedades"
    return f"""  <header>
    <p class="eyebrow">{long_date(meta['date'], lang)}</p>
    <h1>{html.escape(title)}</h1>
    <p class="lede">{html.escape(meta['summary'][lang])}</p>
    {nav_html(current, lang, 2)}
  </header>

{body.rstrip()}

{write_to_me(lang)}

  <p class="back"><a href="/">&larr; {back}</a></p>"""


def project_page_body(meta, body, lang, current) -> str:
    """A project hub: icon, name, tagline, the platforms it ships on, then the body.

    Modelled on an App Store listing. `icon` and `platforms` in page.json are
    optional; a platform that does not exist yet is simply not listed.
    """
    icon = ""
    if meta.get("icon"):
        # "app" (default) is a square store icon, rounded; "mascot" is a cut-out
        # character on a transparent background, shown as-is.
        kind = " mascot" if meta.get("icon_kind") == "mascot" else ""
        icon = f'<img class="hub-icon{kind}" src="{meta["icon"]}" alt="" width="96" height="96">'

    platforms = ""
    if meta.get("platforms"):
        label = "Available on" if lang == "en" else "Disponible en"
        links = "".join(
            f'<a href="{p["href"]}">{html.escape(p["label"][lang])}</a>'
            for p in meta["platforms"]
        )
        platforms = f'<p class="platforms"><span>{label}</span>{links}</p>'

    return f"""  <header class="hub">
    <div class="hub-head">
      {icon}
      <div>
        <p class="eyebrow">{html.escape(meta['eyebrow'][lang])}</p>
        <h1>{html.escape(meta['title'][lang])}</h1>
      </div>
    </div>
    <p class="lede">{html.escape(meta['summary'][lang])}</p>
    {platforms}
    {nav_html(current, lang, 1)}
  </header>

{body.rstrip()}"""


def index_body(posts, lang) -> str:
    heading = "Updates" if lang == "en" else "Novedades"
    lede = (
        "Notes on the things I build, and how they turned out."
        if lang == "en"
        else "Notas sobre lo que construyo, y cómo resultó."
    )
    empty = "Nothing here yet." if lang == "en" else "Todavía no hay nada."

    items = []
    for meta, slug in posts:
        items.append(
            f"""    <article class="entry">
      <p class="entry-date">{long_date(meta['date'], lang)}</p>
      <h2><a href="/posts/{slug}/">{html.escape(meta['title'][lang])}</a></h2>
      <p>{html.escape(meta['summary'][lang])}</p>
    </article>"""
        )

    listing = "\n".join(items) if items else f"    <p>{empty}</p>"
    note = f'\n    <p class="building">{BUILDING_TEXT[lang]}</p>' if BUILDING_NOTE else ""
    return f"""  <header>
    <p class="eyebrow">Cauri Flores</p>
    <h1>{heading}</h1>
    <p class="lede">{lede}</p>{note}
    {nav_html('home', lang, 0)}
  </header>

{listing}"""


def main() -> int:
    posts = []
    if SRC.exists():
        for directory in sorted(SRC.iterdir()):
            if not (directory / "post.json").exists():
                continue
            meta = json.loads((directory / "post.json").read_text())
            for field in ("date", "title", "summary"):
                if field not in meta:
                    sys.exit(f"{directory.name}: post.json is missing {field!r}")
            for lang in ("en", "es"):
                if not (directory / f"{lang}.html").exists():
                    sys.exit(f"{directory.name}: missing {lang}.html — both languages ship")
            posts.append((meta, directory.name))

    # Newest first, and a date that has not happened yet is almost always a typo.
    posts.sort(key=lambda item: item[0]["date"], reverse=True)
    today = date.today().isoformat()
    for meta, slug in posts:
        if meta["date"] > today:
            print(f"  note: {slug} is dated {meta['date']}, which is in the future")

    for meta, slug in posts:
        directory = SRC / slug
        out = POSTS_OUT / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(
            page(
                title_en=meta["title"]["en"],
                title_es=meta["title"]["es"],
                description=meta["summary"]["en"],
                body_en=post_body(meta, (directory / "en.html").read_text(), "en"),
                body_es=post_body(meta, (directory / "es.html").read_text(), "es"),
                current="home",
                depth=2,
            )
        )
        print(f"  /posts/{slug}/")

    (INDEX_OUT / "index.html").write_text(
        page(
            title_en="Updates — Cauri Flores",
            title_es="Novedades — Cauri Flores",
            description="Notes on the things I build, and how they turned out.",
            body_en=index_body(posts, "en"),
            body_es=index_body(posts, "es"),
            current="home",
            depth=0,
        )
    )
    print(f"  /  ({len(posts)} post{'s' if len(posts) != 1 else ''})")

    if SRC_PAGES.exists():
        for directory in sorted(SRC_PAGES.iterdir()):
            if not (directory / "page.json").exists():
                continue
            slug = directory.name
            meta = json.loads((directory / "page.json").read_text())
            for field in ("title", "eyebrow", "summary"):
                if field not in meta:
                    sys.exit(f"{slug}: page.json is missing {field!r}")
            for lang in ("en", "es"):
                if not (directory / f"{lang}.html").exists():
                    sys.exit(f"{slug}: missing {lang}.html — both languages ship")

            out = ROOT / slug
            out.mkdir(parents=True, exist_ok=True)
            (out / "index.html").write_text(
                page(
                    title_en=meta["title"]["en"],
                    title_es=meta["title"]["es"],
                    description=meta["summary"]["en"],
                    body_en=project_page_body(meta, (directory / "en.html").read_text(), "en", slug),
                    body_es=project_page_body(meta, (directory / "es.html").read_text(), "es", slug),
                    current=slug,
                    depth=1,
                )
            )
            # Anything besides the three source files (page.json, en.html, es.html)
            # is a static asset — screenshots, mainly — copied through as-is.
            for asset in directory.iterdir():
                if asset.name in {"page.json", "en.html", "es.html"}:
                    continue
                shutil.copy2(asset, out / asset.name)
            print(f"  /{slug}/")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
