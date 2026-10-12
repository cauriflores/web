# Staged — kept out of the generated site, on purpose

**Empty right now.** The Pacheco 1.1 work that lived here shipped on
2026-10-12; what follows is the convention, for the next time something is
written before it may be published.

`build-blog.py` reads `src/posts/` and `src/pages/` and nothing else, so
nothing here can become a page, appear in Updates, or be linked from the site
by accident.

**It is not private, though.** Pages serves the repo root verbatim, so these
files are fetchable as raw files — `https://cauriflores.com/src/drafts/…`
answers 200 — and the repo is public anyway. That is true of all of `src/`.
Unlinked and unindexed is the whole of the protection. Anything that genuinely
must not be readable before a date does not belong in this repo.

## How it is used

A post waits here as a complete directory (`post.json` + `en.html` + `es.html`
+ screenshots) and moves into `src/posts/<date>-<slug>/` when it may publish.

A change to an existing **page** cannot be staged as a copy — a copy goes stale
the moment the live page changes, and copying it back would discard whatever
changed in between. Keep the intended change as a note here and apply it by
hand, or keep a copy and **`diff` it** rather than `cp` it.

Anything written for a staged page but not meant to publish — a flag about a
sentence, a reminder — goes in an HTML comment, and HTML comments ship to the
browser. Strip them when the content moves into `src/`.

## What release day taught us, 2026-10-12

**Approval is not release.** Apple's "eligible for distribution" mail means
review passed. With manual release the App Store keeps serving the old version
until the Release button is pressed, and then for a while longer.

**Key the publish to the Store, not to the mail or a timer:**

```bash
curl -s "https://itunes.apple.com/lookup?id=6806208255" \
  | python3 -c "import json,sys; r=json.load(sys.stdin)['results'][0]; print(r['version'], r['minimumOsVersion'])"
```

**That lookup is cached per storefront and they do not flip together.** On
release day `us` and `gb` reported `1.1 26.0` while `es` still reported
`1.0 17.2`, with the real Spanish storefront already offering 1.1. Check more
than one country, and trust `currentVersionReleaseDate` for the real date —
1.1 went out at 2026-10-12T10:27:50Z.
