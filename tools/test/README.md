# Page tests (headless Chromium)

Run from `~/personal` with the venv (Chromium is installed inside it, hence `PLAYWRIGHT_BROWSERS_PATH=0`):

```bash
PLAYWRIGHT_BROWSERS_PATH=0 buildenv/bin/python -I neet-pg/tools/test/screenshots.py <page.html> <outdir>   # light/dark, 1200/400 px, console errors
PLAYWRIGHT_BROWSERS_PATH=0 buildenv/bin/python -I neet-pg/tools/test/find_quiz.py <page.html>              # bone pages: find-it quiz hits every landmark
PLAYWRIGHT_BROWSERS_PATH=0 buildenv/bin/python -I neet-pg/tools/test/probe.py <page.html> "<js expression>"  # evaluate JS in the page, print JSON
```

`screenshots.py` and `find_quiz.py` drive the femur page's element ids; adapt them for other modules.
