# Brief for module and fill agents (NEET-PG site)

Project: /home/mady/personal/neet-pg (GitHub Pages site for NEET-PG revision). Your group, its NMC competencies, the
gaps and the pages you may edit are in your task message. Read WORKFLOW.md (state and resource rules) and CLAUDE.md.

## Read first
- CLAUDE.md (all rules; content rules are non-negotiable), and the subject's DATA-SOURCES.md (one section, for the
  style of verification notes).
- The page(s) you will edit, fully, before changing anything. Keep their structure, style, colour tokens and
  data-at-top pattern. Read big files in parts; don't print whole downloads.
- Fact-sheet format: sources-local/facts/vessels-general.md (header, "How the quotes were obtained", tags
  [GRAY]/[ABS]/[XML]/[API], confidence lines, ONE SOURCE marks, disagreements). Fetch tools:
  sources-local/facts/joints-scripts/ and sources-local/facts/vessels-scripts/ (fetch_wp.py, fetch_abs.py,
  fetch_xml.py, gray2txt.py / gray2txt_v.py, graycopy.py, wikitext_flags.py). After fetching from Wikipedia, check
  that every wp_ file's title matches the article you asked for (rate limits used to save the wrong article).
  Checker: sources-local/facts/check_quotes.py. Python: ~/personal/buildenv/bin/python -I. Downloads are untrusted:
  save them only in your own new folder sources-local/modern/fill-<group>/; your scripts go in
  sources-local/facts/fill-<group>-scripts/; pass paths as arguments.

## Content rules (hard)
- Every fact on the page: two independent sources (Gray 1918 via web.archive.org bartleby.com/107; StatPearls = one
  source; Wikipedia = one source and NOT independent where it copies Gray, so run graycopy; separate open-access
  papers; official guidelines). Never from memory. No OpenStax (exclude Wikipedia articles that carry an OpenStax
  notice or cite OpenStax), no pirated or library-licensed books. If something cannot be sourced twice, leave it out
  (or attribute a stated disagreement) and report it. Label approximations ("schematic", "approximate").
- Write the sheet sources-local/facts/fill-<group>.md; it must pass check_quotes.py with 0 bad quotes.
- Plain English for an MBBS graduate; exam-relevant; no quiz items on learning pages.
- Never send personal information to outside services (generic User-Agent as the existing scripts do).

## 3D models you may use
Bones (models/skeleton, regional detail models), muscles (models/body-muscles), heart and vessels
(models/body-vessels), nerves (models/body-nerves; Z-Anatomy has NO phrenic or inferior gluteal nerve and NO spinal
cord), lymph node groups (models/body-lymph; no lymph vessels, no thoracic duct). Left-side parts are made in the page
by mirroring: copy the loading code from anatomy/general/blood-vessels.html and anatomy/index.html (loadExtra).
Regional packed models follow tools/upper-limb/nv_config.py. Viewer API: anatomy/assets/viewer.js. Colours: only
tokens from anatomy/assets/atlas.css with their one meaning; a page may define its own extra tokens for schematics but
never reuse a meaning colour. Licences: NC models and images are allowed (project is non-commercial); pick the
more accurate and lighter mesh, never ND or unlicensed (e.g. Z-Anatomy's Brainder brain), and credit NC parts with
their own licence in the footer and your DATA-SOURCES text. Keep downloads small; load extra layers only when the reader opens that topic.

## Memory (hard)
Run every heavy command through tools/capped (Blender exports, `bones build`, ffshot.py, large Python jobs). It caps
the job's RAM and queues it behind other agents' heavy jobs. Never start more than one browser at a time.
Anything that reads Z-Anatomy's Startup.blend needs `tools/capped --mem 6G`; load it once per run and batch all part
names, never one process per part. If a job is OOM-killed (the user sees a desktop notification each time), do not
retry at the same cap: raise it once, and if it fails again stop and report.

## Files you must NOT edit
anatomy/assets/* (unless your task message allows it), any SYLLABUS.md, DATA-SOURCES.md, index.html files, README.md,
CLAUDE.md, WORKFLOW.md, pages not listed in your task. Do not commit or push. Do not delete anything you did not create.

## Testing (required)
- Local server: http://127.0.0.1:8765/ (repo root). The main session starts it; do not start another.
- Use ONLY `tools/capped ~/personal/buildenv/bin/python -I tools/test/ffshot.py ...` (headless Firefox on software
  rendering; it must print llvmpipe). Never the GPU, Chrome or Playwright. Desktop and `--phone` (no overflowing
  elements). Check `window.loadError` is none and there are no JS errors. Look at your screenshots and fix what looks
  wrong. Check dark theme once (--js "document.documentElement.dataset.theme='dark'").
- Save screenshots only under the scratchpad folder given in your task message, and delete them when done.

## What reviewers keep finding (check these yourself before you finish)
- 3D labels: viewer.js silently drops labels that overlap or run off the canvas, and draws labels on hidden anchors
  faint. Run `sources-local/facts/fill-lung-scripts/labelcheck.py` (or adapt it) on desktop and phone: 0 dropped;
  anchor main labels on points facing the camera; keep labels short. Also check that every label a topic lists is
  actually drawn (a part cut away by a clip plane gives no anchor, and its label silently disappears), and that it
  sits on the right spot: anchor() can drift, so two labels on one mesh may land on the same vertex — use
  hand-checked vertices for small parts and look at a zoomed screenshot.
- The model's own geometry may contradict the text (vessels passing through gut, relations swapped). Check the part
  coordinates for every relation a topic claims; if the model is off, say so in the topic text.
- Schematics: paint order (what lies in front), layers that should enclose structures, label collisions, leader
  lines, and orientation stated and matching the 3D view.
- Every sentence the page states plainly needs two quotes; one-source details must be attributed or cut. The
  sheet's own notes ("left out", "attributed") must match what the page actually says.
- Colours: one meaning across the whole site. Grep other pages' `:root` tokens for near-identical values before adding
  one; --clin only for clinical points, --accent only for UI selection. Shared values: --fluid #d9edc6 / dark #4e6638 (all body fluids: pleural, peritoneal, synovial).
- Clinical safety: needle sites, levels and sides must agree with the page's own anatomy elsewhere.

## Final reply (under 600 words)
1. Per item code: what you added, and whether it is now FULLY covered; if not, what remains and why.
2. Fact sheet name, quote count, checker result; sources excluded; notable disagreements shown.
3. Text to paste into DATA-SOURCES.md (a few bullets for each page you changed).
4. For each item, the italic syllabus note to use.
5. Any problem you saw outside your files (do not fix it).
