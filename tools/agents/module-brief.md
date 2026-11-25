# Brief for a module builder (any subject) — NEET-PG site

Your task message names the subject, the module code (e.g. B01), the NMC topic(s) and competency codes, the folder,
and whether this is the subject's FIRST module. Read and obey, in this order: CLAUDE.md, WORKFLOW.md (top),
tools/agents/fill-brief.md (sources, testing, memory, "What reviewers keep finding" — all of it applies), the subject's
SYLLABUS.md section(s) for your competencies (full text), and the newest physiology modules as the pattern:
physiology/respiratory/*.html, physiology/gi/*.html, physiology/assets/phys.css + phys.js, physiology/index.html,
physiology/DATA-SOURCES.md, and the fact sheets sources-local/facts/fill-physio4.md / fill-physio5.md with their
scripts (expand.py pastes quotes from saved search output; shingle/copy checks; wt2txt.py; fetch scripts) and their
"REVIEW FIX" parts — those list the mistakes reviewers caught; do not repeat them.

## First module of a subject
- Create `<subject>/index.html` (copy physiology/index.html's structure: back link to ../index.html, theme script,
  module list with your Module 01 section only), and `<subject>/assets/<short>.css` + `.js` by COPYING what you need
  from physiology/assets (nothing is shared across subjects; keep the same token names and meanings for the same
  things — ions, fluids, artery/vein, --accent selection only, --clin clinical only). Do not create DATA-SOURCES.md,
  SYLLABUS ticks, root index card or README rows: give their text in your reply; the main session writes them.
- Later modules: add only your section to `<subject>/index.html`; edit the subject assets only if essential (re-read
  first, keep small, retest the subject's other pages).

## Content
- Every fact: two independent open sources (StatPearls, Wikipedia — not independent where it copies another source,
  open-access reviews/guidelines via PMC/Europe PMC/NCBI BioC, WHO/ICMR/MoHFW/NMC/NCDC official documents, Gray 1918
  for anatomy). One-source facts: name the source in the visible page text. Unsourced: cut. No reasoning beyond the
  quotes. Sheet: sources-local/facts/fill-<code>.md (e.g. fill-b01.md), downloads in sources-local/modern/fill-<code>/,
  scripts in sources-local/facts/fill-<code>-scripts/; must pass check_quotes.py with 0 bad (MLP- keys are for other
  open documents, e.g. a WHO guideline saved as mlp_<name>.txt).
- No OpenStax and no Lumen/Boundless: grep every download (txt, json, xml reference lists, wikitext) for openstax, cnx,
  Betts, lumenlearning, boundless; exclude Wikipedia articles and papers that cite them. No pirated or library books.
  Fetch the CURRENT wikitext (action=raw, follow redirects) for every Wikipedia article you quote: older saved copies
  go stale. tools/test/wp_audit.sh checks all quoted articles. Already excluded: see the EXCLUDED notes in the sheets
  (e.g. Fontanelle, Joint, Connective tissue, Psoriasis, Atypical antipsychotic, Standard anatomical position).
- Clinical content: drug doses, schedules, cut-offs, staging and classifications only from a named, dated official
  guideline or society statement (say "<body> <year>" on the page); otherwise give the principle without numbers.
  No patient photos. Indian national programme facts from MoHFW/NCDC/ICMR documents, with year.
- Exam-first: the facts NEET-PG asks (classifications, hallmark findings, "most common", investigations of choice,
  drugs of choice) — each with two sources or attributed.
- Learning material only; no quiz items.

## Graphics first
Each idea as something to manipulate: steppers (Phys.stepper pattern, keyboard arrows, onkeydown), pickers on a
schematic, sliders with live readouts, calculators (hand-check every preset; presets must fall inside the page's own
cut-offs), classifiers. Drawings mechanically right (arrows, order, sides). Text is the caption. Schematic = labelled
"schematic". Images optional: openly licensed Commons only (licence/author from saved metadata, crop stated, labels
checked with sources-local/facts/fill-histo2-scripts/marks.py).

## Colours
One meaning per colour site-wide. Reuse existing tokens with their meanings (atlas.css, anatomy organ tokens,
physiology tokens). New tokens only when needed: check with tools/test/colcheck.py (`colcheck.py . --skip your.css,page.html name=#light/#dark ...`; scans every subject)
(≥20 ΔE from atlas.css incl. --n-*, ≥12 from every other page's tokens), chosen by meaning. Never an undefined var().

## Testing (required)
Server http://127.0.0.1:8765/ (running; never start another). Only
`tools/capped ~/personal/buildenv/bin/python -I tools/test/ffshot.py URL out.png [--phone] [--js ...]` (llvmpipe).
Desktop + --phone, light + dark: no JS errors (window error + unhandledrejection), every control at min/mid/max and
every preset, focus stays on the activated control after redraw, steppers by arrow keys after switching chips, no page
overflow at 390 px, no clipped/overlapping SVG text (getBBox in every state). Screenshots only in the scratchpad folder
your task names; delete it at the end. Background loops: `pgrep -f '[n]ame'` (a plain pattern matches itself and never
ends); stop every loop you start before replying. Heavy jobs via tools/capped; one browser at a time.

## Limits
Create only your pages, your sources-local folders, and (first module) the subject index and assets. Never edit other
subjects, any SYLLABUS.md, DATA-SOURCES.md, README.md, root index.html, CLAUDE.md, WORKFLOW.md. No commits.

## Final reply (under 900 words)
Pages and coverage per competency ([x]/[~] with what's missing); quote count + checker result; excluded and
non-independent sources; disagreements shown; one-source claims attributed and claims cut; guidelines named with year;
images; new tokens (with colcheck numbers); the DATA-SOURCES.md text for the module (first module: also a one-line
subject header); SYLLABUS italic notes per competency; (first module) root-card text: a tags line and one sentence;
README row text; browser results incl. calculator hand-checks.
