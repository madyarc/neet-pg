# Workflow and progress log

Claude reads this file first in every session and updates it after every step (start of a module, fact sheet
done, build done, review done, commit). It is the single place to recall where the work stands. Rules for the
content itself are in CLAUDE.md; this file is about the flow and the state.

Last updated: 2026-11-21

## Now

- Module 40 (histology II: organs; AN25.1, 43.2, 43.3, 52.1–52.3, 64.1) started 2026-11-22: sheet fill-histo2,
  pages in anatomy/histology/ (reusing histo.js/css).
- Local test server: 127.0.0.1:8765.

## Small follow-ups

- `--sl` #f9f1d0 on histology pages is close to other cream tokens.
- Home vessel layer: straight and occipital sinuses sit in front of the brainstem (Z-Anatomy): check or hide.

## Questions for the user

Don't block on a question. Write it here with the default chosen, carry on, and ask these when the user asks for
status. Remove each once answered.

- (none)

## Next (the plan, in order)

| # | Module | Page | Model | Notes |
|---|--------|------|-------|-------|
| 33 | Neuroanatomy | | | |
| 34 | Histology, embryology, genetics | | | |

For each region: add it to `REGION_PAGES` in anatomy/index.html so a second tap on the home page opens the page.

## Still partly covered (searched twice, no two open sources)

- AN10.8: the bedside test for latissimus dorsi.
- AN13.3: the proximal radio-ulnar joint's own nerve and artery supply.
- AN31.5: the definition of primary versus secondary deviation.
- AN20.8: the anterior tibial pulse at the ankle has one source (Gray 291); the other four pulses are done (module 25).
- AN25.9: heart (module 26) and pleura, lungs, trachea (module 30) done; midclavicular levels of lung and pleura are Gray only.
- AN23.2 (thoracic duct tributaries), AN23.3 (hemiazygos origin), AN47.12 (secondary plexuses): Gray only (Wikipedia
  copies Gray); modules 27–28. AN48.5: the part of the tube used for ligation (module 35).
- AN27.1: scalp wound bleeding and gaping (Wikipedia only).
- AN43.6: only the subclavian vein's surface line is missing (one source).
- AN37.2: sinus functions are Wikipedia only (module 33).
- AN58.4: "crossed diplegia" read as cruciate paralysis, one source (module 36).
- AN69.1 (elastic artery and vein micrographs: Commons rate limit), AN70.2 (no tonsil micrograph), AN71.1 (woven vs
  lamellar: only OpenStax-derived source) — module 38.
- AN77.6: the sex-selection law (PCPNDT) has no open source (module 39).
- AN47.6: the clinical use of the splenic notch has no open source (module 31).
- AN13.7: surface lines and pulses are done (module 24); the muscle tests for pectoralis major, serratus anterior,
  latissimus dorsi, deltoid, biceps and brachioradialis are not. Could go on the upper-limb muscles page.

Progress: anatomy 316 covered, 19 partial, 78 not started; ophthalmology 6 covered, 1 partial, 55 not started.

## Steps for every module (do them in this order, tick them here as they finish)

1. Plan: list the competencies (SYLLABUS.md), the 3D parts needed, and what Z-Anatomy lacks.
2. Fact sheet `sources-local/facts/<name>.md`: two independent open sources per fact; passes
   `sources-local/facts/check_quotes.py` with 0 bad quotes. Check every `wp_` file's title matches its request.
3. Model: config script, `bones build` (through `tools/capped`), post step, check the pack size.
4. Page: build it; test desktop, phone and dark theme with ffshot (through `tools/capped`); look at the screenshots.
5. Independent reviewer agent (give it the page and the fact sheet, not my conclusions); fix everything it finds.
6. Docs: SYLLABUS.md ticks with italic notes, DATA-SOURCES.md, README.md row, root index.html counts, CLAUDE.md if
   a new pattern appeared.
7. Integrity checks (git hash-object vs index, control-character scan, `git fsck`), commit, push, live test.
8. Update this file, give the user a short report, and start the next module straight away (user, 2026-11-21: work
   continuously; don't wait for "proceed").

## Resource rules (the machine ran out of memory before)

The last long session's terminal reached 11.3 GB, mostly from several agents each running headless Firefox or
builds at the same time.

- The whole session is capped at 8 GB. Start Claude with `claude-8g` (in ~/.local/bin), which puts Claude and
  everything it starts in one 8 GB cgroup. Without it, the cap can be set by hand on the terminal's cgroup
  (`memory.max` under /sys/fs/cgroup/…/app-org.kde.konsole-*.scope/tab(*).scope).
- Every heavy command goes through `tools/capped` (default 4 GB, `--mem` to change): Blender exports,
  `bones build`, `tools/test/ffshot.py`, large Python jobs. It holds a lock, so only one heavy job runs at a time even
  when agents work in parallel.
- At most two agents at once, and only when their work is independent. Tell each agent to use `tools/capped`.
- Don't print big files into the context: read with offsets, grep, or summaries. Large downloads stay on disk.
- Clean up after each module: delete my own screenshots and temporary files in the scratchpad.

## Testing

- Server: `cd ~/personal/neet-pg && python3 -m http.server 8765 --bind 127.0.0.1` (run in the background, once).
- Screens: `tools/capped ~/personal/buildenv/bin/python -I tools/test/ffshot.py URL OUT.png [--phone] [--js …]`.
  It must print llvmpipe (software rendering). Never the GPU, Chrome or Playwright. Leave the user's own Firefox alone.
- Byte ranges don't work on GitHub Pages under gzip; pages check the `NPM1` header and fall back to the whole file.

## Briefs for agents

- Fill or module agents: tools/agents/fill-brief.md (rules, sources, models, files not to edit, testing, reply format).
- Reviewer agents: give the page path, the fact sheet path and CLAUDE.md content rules; ask for errors with the quote
  that disproves each claim.

## Log (newest first)

- 2026-11-22: Module 39 (general embryology, two pages in anatomy/embryology/): 753 quotes, step-through schematics,
  germ-layer tokens; review found 16 items (yolk sac inside the amnion, amniocentesis needle through the placenta,
  colours, chart alignment), all fixed; 29 ticked, AN77.6 partial.

- 2026-11-22: Module 38 (histology I, three pages in anatomy/histology/): 414 quotes, 20 Commons micrographs with
  switchable labels; review found 15 items (seven labels on the neighbouring structure), all fixed; 9 ticked, 3
  partial. --nucleus moved to #1e4f99 (was the accessory nerve's colour); --fat unified to #f3e3a6.

- 2026-11-22: Module 37 (cerebrum, ventricles, pathways; nervous system general plan, two pages): 621 quotes,
  123-part 998 KB `models/neuro2`; review found 14 items (genu lesion overstated, capsule caption side, nucleus
  column order unsourced), all fixed; 17 ticked.

- 2026-11-22: Module 36 (meninges, CSF, cord; brainstem and cerebellum, two pages in anatomy/neuro/): 609 quotes,
  121-part 810 KB `models/neuro1`; review found no side or level errors, 11 drawing/source/code items, all fixed;
  21 ticked, AN58.4 partial. New 'Brain and spinal cord' group on the Anatomy page. Follow-up: the home vessel layer's
  straight and occipital sinuses lie in front of the brainstem (misplaced in Z-Anatomy) — check or hide them.

- 2026-11-22: Navigation: site search (assets/search.js, search-index.json), grouped Anatomy page with filters and
  region jumps, Bones on/off on every 3D page, Joints and ligaments and Organs layers on the Anatomy home.

- 2026-11-22: Module 35 (pelvic viscera; perineum and male genitalia, two pages): 796 quotes, 77-part 391 KB male
  `models/pelv`, female organs schematic; review found 26 items (palpable vs relations, extravasation of urine,
  one-source tables, model caveats), all fixed; 15 ticked, AN48.3 completed, AN48.5 partial. Search index now lists
  only git-tracked pages.

- 2026-11-22 01:46: user saw memory errors: three capped jobs (module 36 agent, compare.py on Startup.blend, 3G cap)
  were OOM-killed in their own scopes; the machine itself had 59 GB free. Brief now says 6G for .blend reads, batch
  parts, no retry loops.

- 2026-11-22: Module 34 (ear and eye): 522 quotes, 83-part 631 KB `models/eareye` (Z-Anatomy temporal bone and inner
  ear, CC BY-NC-SA), CC BY-SA otoscope photo; review found 14 items (labels drifting onto the wrong spots, model
  chorda and tube, cone of light one source, field layout), all fixed; 10 ticked; AN31.5 still partial.

- 2026-11-22: Module 33 (mouth, pharynx, nose, larynx): 430 quotes, 107-part 653 KB `models/oro` with a midline clip;
  review found 10 items (pyriform fold lateral in the model, V2 clipped away, model caveats), all fixed; 9 ticked,
  AN37.2 partial.

- 2026-11-22: Module 32 (face and neck regions and glands): 531 quotes, 141-part 636 KB `models/hn-reg`; review found 13
  items (face sensory map, parotid section mirrored, carotid sheath contents, model caveats), all fixed except thyroid
  ligation advice (no open source); 14 ticked; AN43.6 now only lacks the subclavian vein.

- 2026-11-21: Module 31 (abdominal cavity, peritoneum, organs): 582 quotes, 100-part 664 KB `models/abdo` with the
  Z-Anatomy kidney (CC BY-NC, better fit); review found 18 items (biopsy needle wording, labels, schematics), all fixed;
  8 ticked, AN47.6 partial. Spleen on the home opens the page.

- 2026-11-21: Licence: content now CC BY-NC-SA 4.0 (user: never commercial); NC models/images allowed, chosen by
  accuracy and load speed (Z-Anatomy kidney and inner ear now usable). Code stays AGPL.

- 2026-11-21: Module 30 (lungs, pleura, trachea): 372 quotes, 168-part 798 KB `models/lung`, surface lines computed on
  the model's ribs, CC0 chest X-ray and CC BY-SA barium frame; review found 13 items (a tap level below the pleura,
  dropped labels, colours), all fixed; 7 ticked, AN25.9 still partial. Pulmonary vessels on the home open the page.

- 2026-11-21: Module 29 (head and neck NV): 610 quotes, 204-part 884 KB `models/hn-nv` (tools/head-neck/nv_config.py);
  review found 9 groups (3D node levels, subclavian schematic, ~30 single-source lines), all fixed; 18 ticked, AN27.1
  and AN43.6 partial. Home: 'Head and neck' parts open the page.

- 2026-11-21: Modules 27 (thorax: 402 quotes, 887 KB thorax-nv) and 28 (abdomen and pelvis: 651 quotes, 860 KB abd-nv),
  built in parallel; reviews found 11 and 9 problems, all fixed. 14 competencies ticked, 4 partial. Home: Trunk parts
  open the thorax/abdomen/limb page via tools/home/region_pages.py; sigmoid veins tagged portal.
- 2026-11-21: Module 26 (the heart): 398 quotes, 73-part 522 KB model `models/heart` (tools/thorax/heart_config.py),
  reviewer found 11 problems (two mirrored schematics among them), 10 fixed, conducting-tissue colour kept; AN22.1–22.7
  ticked, AN25.9 partial; heart parts on the Anatomy home open the page.
- 2026-11-21: check_quotes.py used to skip quote keys with brackets or apostrophes silently; now it reports them
  (SKIPPED). Re-ran every fill sheet: the skipped quotes all match their sources (fill-ll has one 42-word quote).
- 2026-11-21: Licence: code AGPL-3.0-or-later (LICENSE), content CC BY-SA 4.0 (LICENSE-CONTENT), README section.
- 2026-11-21: Module 25 (nerves, vessels and lymph nodes of the lower limb): 636 quotes, 209-part 865 KB model
  `models/ll-nv` (tools/lower-limb/nv_config.py), reviewer found 12 problems, all fixed; 10 competencies ticked, AN20.8
  partial; lower-limb vessels, nerves and nodes on the Anatomy home open the page.
- 2026-11-21: Memory fix. Session cap 8 GB (first 4 GB), `tools/capped` for heavy jobs, `claude-8g` launcher, pip cache cleared
  (2.6 GB), this file and tools/agents/fill-brief.md added.
- Module 24 (e751f03): nerves, vessels and lymph nodes of the upper limb; 764 quotes; 18 competencies ticked.
- Partly-ticked items completed (aef5008 and earlier): lower limb, trunk, skull, head and neck, histology,
  ophthalmology fills; whole-body vessel, nerve and lymph layers on the home page.
- Module 23: Blood Vessels (general), with the vascular home layer.
