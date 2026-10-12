# Staged — kept out of the generated site, on purpose

`build-blog.py` reads `src/posts/` and `src/pages/` and nothing else, so
nothing here can become a page, appear in Updates, or be linked from the site
by accident.

**It is not private, though.** Pages serves the repo root verbatim, so these
files are fetchable as raw files —
`https://cauriflores.com/src/drafts/pacheco-1-1-post/en.html` answers 200 —
and the repo is public anyway. That is true of all of `src/`. Unlinked and
unindexed is the whole of the protection. Anything that genuinely must not be
readable before a date does not belong in this repo.

It holds the Pacheco 1.1 work, written on 2026-10-11 while **1.1 (6) was
Waiting for Review with manual release**. The App Store was still serving 1.0
on iOS 17.2 that day, so publishing any of it would have made the site wrong
about the app Apple was actually shipping.

**Apple approved it on 2026-10-12** — "eligible for distribution". That is not
the same as released: the release is manual and Cauri presses it. Checked that
morning, `itunes.apple.com/lookup?id=6806208255` still reported version 1.0,
minimumOsVersion 17.2. **That lookup is the gate.** Publish when it reports
1.1, not when the approval mail arrives and not on a timer — Apple allows up
to 24 hours after release for the listing to propagate.

```bash
curl -s "https://itunes.apple.com/lookup?id=6806208255" \
  | python3 -c "import json,sys; r=json.load(sys.stdin)['results'][0]; print(r['version'], r['minimumOsVersion'])"
```

## On release day

Once that prints `1.1 26.0`:

```bash
cd ~/Developer/cauriflores.com
mv src/drafts/pacheco-1-1-post src/posts/2026-MM-DD-pacheco-1-1   # the real release date
diff -u src/pages/pacheco-project/en.html src/drafts/pacheco-project-hub/en.html
diff -u src/pages/pacheco-project/es.html src/drafts/pacheco-project-hub/es.html
python3 tools/webp.py
python3 tools/build-blog.py
```

**Diff, do not copy.** The staged hub files are a snapshot of the live ones as
they were on 2026-10-11. Copying them over would silently discard anything
changed in the hub between then and release day. The staged change is only
three facts per file, so read the diff and apply those three by hand.

Then check these three things before committing:

1. **The post's date.** `post.json` says `2026-10-11`, the submission date, as a
   placeholder. Change it to the release date, and rename the directory to
   match — the slug carries the date too.
2. **The line about size.** `pacheco-project-hub/en.html` and `es.html` still
   carry your sentence *"The two are within two lines of each other — about
   4,300 lines apiece."* It is no longer true: iOS is 4,470 lines and the web
   app is 6,310 after SPEC §14. It is marked with an HTML comment in both
   files. Rewrite it or cut it — it is your sentence, so it was left alone.
3. **The summary in `page.json`** says the two versions are *"kept in step"*.
   Visual parity between iOS and the web has been an open item since
   2026-09-17. Same call, same reason: untouched.

## What was changed in the hub, and why

Only facts, in both languages:

| Was | Is | Checked against |
| --- | --- | --- |
| iOS 17.2 and later / or later (two places each) | iOS 26 | `IPHONEOS_DEPLOYMENT_TARGET = 26.0` |
| 45 tests (iPhone) | 66 tests | 61 unit + 5 UI, the same way 45 was counted at commit `53cc2c2` |
| 190 tests (web) | 199 tests | `it(` blocks in `pacheco-web/src` |

## Screenshots — done 2026-10-12

`day-screen.png` and `hour-screen.png`, 1206×2622, captured from an iPhone 17
Pro simulator on iOS 27 with live WeatherKit data and the location set to
Madrid, exactly as `Pacheco/CLAUDE.md` describes. The `Pacheco` scheme, so
English and metric, matching the existing hub gallery. Both carry the Apple
Weather mark.

The `.webp` siblings are already encoded at the project's quality 82, so the
move below needs no extra step — but `tools/webp.py` is in the commands anyway
and is cheap and idempotent.

They are shown two-up in a `.gallery two`, capped at 450px so each lands at the
same ~219px the hub's three-up gives its images.
