# cauriflores.com

Writing, and the apps. Served by GitHub Pages from this repo at
**https://cauriflores.com/**, on a custom domain.

## What is here

    index.html            the writing index — the front page
    posts/<slug>/         generated articles
    src/posts/<slug>/     their sources: post.json + en.html + es.html
    pacheco/              the Angular web app, built from the private
                          pacheco-web repo by its own tools/deploy.sh
    style.css, lang.js    shared with the support site, copied not linked

Build the writing with `python3 tools/build-blog.py` and commit the result.
There is no Jekyll — `.nojekyll` is deliberate, so publishing is a file copy
that cannot fail.

## What is NOT here, and why

**https://cauriflores.github.io/ is Pacheco's App Store support URL** and
`/privacy.html` is the privacy policy Apple checks. Both live in the separate
`cauriflores.github.io` repo, which is frozen.

They are not here because **the Support URL is a version-level field in App
Store Connect**: changing it requires a new app version and a full App Review.
Keeping the two sites apart means nothing published here can ever reach the
pages Apple has on file. The nav links across to them absolutely, on purpose —
a relative href would 404.
