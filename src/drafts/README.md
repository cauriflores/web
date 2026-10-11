# Staged — not published, on purpose

`build-blog.py` reads `src/posts/` and `src/pages/` and nothing else, so
everything in this directory is invisible to the build. Nothing here can reach
the site by accident.

It holds the Pacheco 1.1 work, written on 2026-10-11 while **1.1 (6) was
Waiting for Review with manual release**. The App Store was still serving 1.0
on iOS 17.2 that day, so publishing any of it would have made the site wrong
about the app Apple was actually shipping.

## On release day

After Apple approves **and** you press Release in App Store Connect:

```bash
cd ~/Developer/cauriflores.com
mv src/drafts/pacheco-1-1-post src/posts/2026-MM-DD-pacheco-1-1   # the real release date
diff -u src/pages/pacheco-project/en.html src/drafts/pacheco-project-hub/en.html
diff -u src/pages/pacheco-project/es.html src/drafts/pacheco-project-hub/es.html
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

## Screenshots — not done

The post has no figure, and this is an open job, not a note. The two new
screens — a day opened from the 9-day forecast, and an hour opened from the
24-hour strip — have never been captured, by anyone. They would have to come
out of the Simulator with enough saved friends to match the existing hub
gallery (Madrid, Abuela, Kenji).

Whoever does it: PNG into the post directory, which the build has copied
through since 2026-10-11, then `tools/webp.py` and the build.
