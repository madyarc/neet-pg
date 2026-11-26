# Workflow and progress log

Claude reads this file first in every session and updates it after every step (start of a module, fact sheet
done, build done, review done, commit). It is the single place to recall where the work stands. Rules for the
content itself are in CLAUDE.md; this file is about the flow and the state.

Last updated: 2026-11-23

## Now

- RESUMED 2026-11-26 02:34 after the terminal tab closed at 02:29 (no crash, no OOM, no core dump; Konsole was flooding
  notifications). New tab had no cap: set 9G/10G again. S01, O01, An01 builders resumed (S01/O01 had ~200 downloads each,
  no pages; An01 nothing). Server from the old session still serving :8765.
  Live wikitext audit COMPLETE (all titles, 0 failed). New beyond the fixed set, DONE and committed (c8f9664): Sarcomere (muscle-tissue 10), Skeletal_muscle (muscle-tissue 7), Tendon_sheath (connective-tissue 1),
  Anatomical_terms_of_motion in joints-ankle-foot (2), Osteoarthritis in joints-hip-knee (3); pages anatomy/general/
  muscle.html, connective-tissue.html, lower-limb/joints.html. (The audit also lists excluded quotes still kept in
  sheets as unused; expected.)
  USER (outside project): kernel btrfs zstd error also on inode 96460 = /var/lib/pacman/local/snappy-1.3.1-1/files
  (pacman DB entry; `sudo pacman -S snappy` rewrites it). wp_Spermiogenesis.txt replacement still awaiting the user.
- RESUMED 2026-11-25 (cap re-set to 10G on the new tab; server up): M01 fix agent resumed, F01 review running, FM01
  build restarted.
- PAUSED 2026-11-24 by user (session limit hit; resets 07:10 America/New_York). Resume state for round 1:
  - Committed and live: B01, P01, G01 (+ physiology 01–05 earlier).
  - F01 pharmacology: all 3 pages built (630 quotes, 0 bad); reviewed 2026-11-25 (18: GPCR drawn with 14 crossings,
    Drug B curve, simulator axis, --ther reuse and pale-green vs --fluid, attributions); fixes (676 quotes) [x] committed 2026-11-25. Next: one independent review
    of the whole module (pharmacokinetics, pharmacodynamics, principles-safety), fixes, docs, commit.
  - M01 microbiology: review done; fix agent stopped by the usage limit mid-way ("media, biochem, HGT additions" was
    next). Resume it (or a new fix agent with the review list in WORKFLOW/M01 notes) — check what is already fixed first.
  - FM01 forensic: build agent stopped early (downloads in progress in sources-local/modern/fill-fm01/). Restart.
  - Then continue round 1 order: C01, Pd01, Ps01, D01, S01, O01, An01, R01, E01, OG01, then B02, P02–P04, M02, FM02,
    C02, G02–G03, Pd02–Pd04, Ps02, D02, S02–S03, O02, An02, OG02–OG04.
  - SOURCE AUDIT 2026-11-25: Wikipedia articles citing Boundless/Lumen (only OpenStax was grepped before). Found in
    saved wikitext: Fontanelle (skull.html fixed), Human_fertilization (fill-embryo1, 12 quotes) and Thermoregulation
    (fill-physio3, 2 quotes): pages to re-source (agent running). 574 older WP articles had no saved wikitext: fetching and scanning
    (scratchpad wtaudit.sh); act on hits.
    Audit pass 1 (567 fetched): 13 more cite OpenStax: Anatomical_terms_of_muscle, Condyloid_joint, Connective_tissue,
    Deltoid_ligament, Epimysium, Facial_muscles, Fibrous_joint, Hinge_joint, Intercalated_disc, Joint, Muscles_of_mastication,
    Plane_joint, Saddle_joint (~77 quotes in muscle-tissue, joints-general, connective-tissue, joints-ankle-foot,
    hn-face-mastication, fill-ll). Sent to the re-sourcing agent (queued after its first two). Pass 2: redirects followed; 1 more (Myocyte → Muscle cell,
    OpenStax; muscle-tissue 4). The 23 "empty" were short redirects, all targets clean. 16 articles + Luteal phase + Smooth muscle
    re-sourced and COMMITTED 2026-11-25 (31bdbf9). Follow-up DONE and committed (93d2a73): Anatomical terms of motion, Osteoarthritis
    (OpenStax, joints-general F1/J4), Synchondrosis (Boundless in a cn tag: treated as citing). Saved wikitext can be
    stale (articles add OpenStax later): LIVE re-audit of all ~2685 titles running (scratchpad wplive).
    USER DECISION: sources-local/modern/fill-embryo1/wp_Spermiogenesis.txt unreadable (kernel: BTRFS zstd decompression
    failed, inode 1107686, from 17:31; also inode 96460 untraced); rebuilt identical copy in scratchpad; agent's
    replacement was blocked by permissions, so the user decides. Reusable: tools/test/wp_audit.sh OUTDIR.
  - Site-wide TODO (dedicated pass, not between modules): --mark and --clin identical in dark (#ff7b6f), ΔE≈10 in light;
    defined in atlas.css, 36 anatomy pages, ophthalmology pages and every subject's assets. Orange is taken by --ins, so
    pick new values with tools/test/colcheck.py and retest all pages. Reviewers flag it in every module.
  - Server and agents stopped at pause.

- USER 2026-11-24: BREADTH-FIRST ROUNDS. Each round = ~10% of every subject (modules = ceil(NMC topics / 10), min 1;
  ENT by competencies, ~6–8 per module), all not-started subjects first; anatomy/physiology/ophthalmology wait until the
  rest catch up. Skill-only competencies skipped. First module of a subject also creates <subject>/index.html,
  DATA-SOURCES.md, its own small assets (copy the physiology pattern; nothing shared across subjects) and a root card.
  Clinical subjects: doses/schedules/classifications only from a named, dated official guideline (CLAUDE rule 6).
  Round 1 (37 modules; order alternates basic and clinical; three agents at a time, one test browser at a time):
    biochemistry 2: B01 enzymes · B02 carbohydrate metabolism
    pathology 4: P01 cell injury+adaptation · P02 inflammation+healing · P03 haemodynamic disorders · P04 neoplasia
    pharmacology 1: F01 general pharmacology (PK/PD)
    microbiology 2: M01 general microbiology · M02 basic immunology+immunological disorders
    forensic 2: FM01 forensic pathology (death, PM changes) · FM02 mechanical injuries and wounds
    community medicine 2: C01 epidemiology · C02 biostatistics
    medicine 3: G01 heart failure+IHD · G02 diabetes mellitus · G03 hypertension
    paediatrics 4: Pd01 growth and development · Pd02 immunization (UIP) · Pd03 newborn care · Pd04 nutrition+breastfeeding
    psychiatry 2: Ps01 psychosis + mood (topics 4–6 together; NMC lists only 1 competency each) · Ps02 anxiety/stress +
      substance use
    dermatology 2: D01 papulosquamous (psoriasis, LP) · D02 leprosy
    surgery 3: S01 shock+metabolic response · S02 burns · S03 thyroid+parathyroid
    orthopaedics 2: O01 trauma and fracture principles (OR1.1, 1.3, 2.14, 2.15) · O02 peripheral nerve injuries
    anaesthesia 2: An01 CPR + oxygen + airway (AS2, AS11) · An02 general and regional anaesthesia (AS4, AS5)
    radiology 1: R01 modality choice and image interpretation basics (radiation safety)
    ENT 1: E01 ear anatomy-physiology + hearing tests
    obgyn 4: OG01 conception, placenta and maternal changes (OG3.1, 4.1, 7.1) · OG02 diagnosis of pregnancy + antenatal care · OG03 labour · OG04 contraception
  2026-11-24 integrity: 4 tracked files differed from git with a clean git status (2 bytes each, 4 bytes apart, bit
  0x40 flipped): thick-skin.jpg + ext_intercostal.bin in page cache only (disk intact), calc_tendon.bin + manubrium.bin
  on disk. Restored from git blobs, verified by direct read; fsck clean; commits unaffected. Keep the hash check before
  every commit.
  Status: B01 [x] build (336 quotes; tokens --enz --sub --inhib --cofac) [x] review (no blocking errors; attributions,
  CK timing, labels, --clin misuse, --inhib vs --ca) [x] fixes (351 quotes) [x] committed 2026-11-24 (b9ac13f). F01 split: first agent ran out of context after setup + ~190 downloads (assets, --ther token, scripts ok).
  F01a [x] PK + PD pages + index (355 quotes; FDA DDI table for inducers/inhibitors). F01b [ ] principles/ADR/PvPI
  page (running; then one review for the whole module; downloads ready, NLEM 2022
  official text missing). Inducer/inhibitor lists: use FDA DDI table (public domain) + Wikipedia/StatPearls. G01 [x] build (549 quotes; 3 pages; no new tokens; guidelines via open papers) [x] review (17: ACS picker
  pain overrode ECG/troponin (safety), reperfusion >24 h, thrombolysis list incomplete, NP cut-offs = ESC 2016, artery/vein
  colours used for oxygenation) [x] fixes (573 quotes) [x] committed 2026-11-24. S01 [x] build (243 quotes; EU trauma 2023 / ATLS 10th, Sepsis-3, SSC 2021, ERAS; Wikipedia Homeostasis excluded)
  [x] review (ERAS carbohydrate loading misattributed, TBI/spinal exception missing at the instruction (safety),
  ebb/flow curve directions, SSC 2021 gaps) [x] fixes (291 quotes) [x] committed 2026-11-26. ROUND 1 SECOND MODULES started: B02 [x] build (552 quotes) [x] review (Wikipedia misread Katz&Tayek 1998 Cori %, WHO joint criteria,
  ADA discordant wording, colours) [x] fixes (602 quotes) [x] committed 2026-11-26. P02 [x] build (427 quotes) [x] review (no wrong facts; one-source pairs, transmigration drawn transcellular,
  drug blocks off-arrow, path.js stepper focus) [ ] fixes (running).
  (bioc.js has the stepper-end focus fix in another form: verified; only path.js lacked it, P02 fix adds it.) M02 [ ] build (running; microbiology/immunology/, MI2.1–2.8).
  R01 [x] build (346 quotes) [x] review (PC-PNDT consent/Form G wrong for ultrasound, Form F indications,
  NICE head-injury adult rule, 10-day rule year, radiograph densities unsourced, PET geometry) [x] fixes (364 quotes) [x] committed 2026-11-26.
  TOOLING FIX 2026-11-26: tools/capped passed args through systemd-run env expansion (${X} in --js was mangled);
  now --expand-environment=no. Inline --js tests before this date that used ${...} may have been wrong. E01 [x] build (388 quotes; WHO 2021 grades, ASHA 1990; Wikipedia Rinne/Weber excluded; ABC/Schwabach cut)
  [x] review (audiogram symbol text reversed, ET angle reference planes mixed, bone>air nonsense, ear
  colours outside the audiogram) [x] fixes (418 quotes) [x] committed 2026-11-26. OG01 [x] build (422 quotes; PMC10964813 excluded for copying PMC4928162) [x] review (body-map head off-canvas,
  cycle chart fixed to 28 d, bilirubin/BP disagreements hidden, colour misuse) [x] fixes (433 quotes) [x] committed 2026-11-26.
  ALL 16 SUBJECTS NOW HAVE MODULE 01 LIVE (round 1 first modules complete). O01 [x] build (313 quotes; BOAST 2017, ATLS 11th 2025, WHO 2005/2018) [x] review (SALTER mnemonic orientation reversed,
  START missing airway-reposition RED branch, ATLS 11th C-spine wording + edition-switch bug) [x] fixes (341 quotes) [x] committed 2026-11-26. An01 [x] build (312 quotes; AHA 2020 (archived), ILCOR 2020, KACPR 2025, SRFAC 2026, BTS 2017, TSANZ 2022,
  DAS 2015; ERC only as reported (403)) [x] review (LMA/ETT drawn through the tongue, PC volume
  unbounded, quiz-sourced quotes, 4Hs4Ts open source found, depth scale) [x] fixes (341 quotes) [x] committed 2026-11-26. Ps01 [x] build (289 quotes) [x] review (no wrong facts; duration-picker logic, missing arrowheads,
  mesocortical path, synapse marks, clozapine schedule) [x] fixes (322 quotes) [x] committed 2026-11-25. C01 [x] build (328 quotes; CDC 2012, WHO 1968, SRS 2020, NFHS-5, IDSP; no new tokens) [x] review (no wrong formulas; disability limitation level
  one-source, rate/time misattribution, --accent/--clin misuse, gaps: indirect standardisation, field trial) [x] fixes (374 quotes) [x] committed 2026-11-25. Pd01 [x] build (458 quotes; WHO 2006/2007 LMS z-score chart, CDC 2022 milestones via Zubler 2022) [x] review.
  D01 [x] build (407 quotes; NICE CG153; Wikipedia Psoriasis excluded: cites cnx.org) [x] review (LP histology: Max-Joseph
  space inside epidermis, infiltrate below ridges; NICE CG153 date; copied erythroderma source) [x] fixes (431 quotes) [x] committed 2026-11-25.
  Pd01 review done (timeline colours overlap, pincer-grasp flag vs CDC, undated cut-offs, gaps: WHZ/BMI, Tanner,
  dentition) [x] fixes (506 quotes) [x] committed 2026-11-25. Anatomy skull.html: Wikipedia Fontanelle (cites Boundless) removed 2026-11-25.
  FM01 [x] build (397 quotes; THOA/THOT Rules 2014 Form 10, WHO ICD-11 2026 + RGI MCCD 2012; tokens --livor
  --livor-co --sulfhb) [x] review (livor shifting rule, children's Form 10 interval, consent
  under Rule 5(4)(a), VS overstated, IPC→BNS 2023, --accent misuse; Delhi THOA text unofficial/garbled) [x] fixes (430 quotes) [x] committed 2026-11-25.
  M01 [x] build (635 quotes; 3 pages; 7 stain/structure tokens;
  Wikipedia Koch's postulates excluded: cites Boundless) [x] review (blood-spill 1:100 vs 1:10 large spills (safety),
  ELISA antibodies drawn upside down, coccidia vs HLD, Koch dates, CDC-derived Wikipedia pairs) [x] fixes (694 quotes) [x] committed 2026-11-25. P01 [x] build (314 quotes; 3 Commons images; tokens --lipofuscin --haemosid --bili) [x] review (18: metaplasia
  disagreement, token clash with bioc dark, invisible soaps, dysplasia wording, labels) [x] fixes (326 quotes) [x] committed 2026-11-24.
  Site-wide colour checker now tools/test/colcheck.py (scans every subject; --skip own files).
  LATER (site-wide): --mark and --clin are identical in dark (#ff7b6f), ΔE 14 light; anatomy --pigment comment says
  "reticularis pigment" (= lipofuscin, now --lipofuscin in pathology).

- PAUSED 2026-11-23 (user has other work). Resume here:
  - Physiology 01–05 done, reviewed, committed, live (17 pages; PY1, PY2, PY3, PY4.1–4.11, PY5, PY6.1–6.9). Next:
    module 06 (renal, SYLLABUS §7) by the same flow: builder (fill-physio6, physiology/<branch>/) → independent reviewer →
    fixes → main session writes SYLLABUS/DATA-SOURCES/README/root card/search index → hash check → commit. Max three agents.
  - Feedback live: "Report it" note after every page's footer → .github/ISSUE_TEMPLATE/feedback.yml (label `feedback`;
    GitHub login redirects back to the form). New pages: run tools/home/feedback_links.py (CLAUDE.md step 7). Review open
    reports with `gh issue list -l feedback`. Google Form relay = fallback if reports stay low.
  - Anatomy partials, module 46, AN3.3 J Anat PDFs, older label overlaps: still deferred.
  - Cleaned at pause: test server stopped, agents stopped, stale agent wait-loops killed (pgrep -f self-match bug: tell
    agents to use `pgrep -f '[f]etch_xml.py'`-style patterns), scratchpad emptied, __pycache__ and pip cache removed.
    Kept: ~/.cache/selenium (driver for ffshot), sources-local/ downloads, tools/bones-rs/target.
  - Start next session: verify the 10 GB cap (claude-10g), start `python3 -m http.server 8765 --bind 127.0.0.1`.

- 2026-11-22 evening: resumed modules 44 (fixes) and 45 (build). Session was not under claude-8g, so the 7G/8G/1G
  limits were written to this tab's cgroup directly (verify each session: cat memory.max in /proc/self/cgroup's path).
  User: finish what's incomplete, then start another subject; anatomy partials later after a break.
- Next subject: PHYSIOLOGY (136 competencies, 0 done). P1 = general physiology + nerve and muscle (PY1.1–1.7,
  PY3.1–3.10): pages under physiology/general/ and physiology/nerve-muscle/, sheet fill-physio1, physiology/index.html
  created by the first module (CLAUDE.md: create subject index with the first module), root index line updated by
  main session. [x] build (679 quotes; 4 pages + physiology/index.html + assets/phys.css/js; ion tokens
  --na --k --cl --ca --ach) [x] review (cross-bridge drawing wrong, block-order disagreement, PMC10416754 copies
  Wikipedia, PMC13074981 cites OpenStax, Ca²⁺ arrows, --na near --n-ventral-rami, Darrow–Yannet loss missing)
  [x] fixes (680 quotes) [x] docs [x] commit. Done 2026-11-22.
  Physiology 02 haematology (fill-physio2, physiology/blood/) and 03 cardiovascular (fill-physio3, physiology/cvs/)
  03: [x] build (550 quotes; 3 pages; no new tokens) [x] review (11 items: AP stepper keyboard bug in phys.js,
  shock SVR/filling unsourced, HF preset EF 43%, unquoted claims, colours, labels, Wiggers timing) [x] fixes (576 quotes; phys.js stepper uses onkeydown).
  [x] committed with 02 2026-11-23.
  02: [x] build (791 quotes; 4 pages incl. immunity; tokens --rbc --platelet in phys.css; 7 Commons smears) [x] review
  (13 items: --ok undefined, WHO child cut-off, PMC5767294 via Boundless/OpenStax, LAB_NOTE over-claims, attributions,
  DIC readout, ESR preset, keyboard focus, IgA drawing) [ ] fixes (running). 04 GI [x] build (623 quotes; 3 pages; no new tokens) [x] review (no wrong facts; LFT picker
  classification, defecation arrow, ~15 attributions, --stom misuse, drawing labels) [x] fixes (630 quotes) [x] committed with 05 2026-11-23.
  (Reviewer's "st is undefined" on cardiac-electrophysiology: not reproducible via real chips/stepper/keys; stale-node clicks.) 05 respiratory [x] build (518 quotes; 3 pages; no new tokens) [x] review (5 wrong facts: DLCO shunt
  direction, hypoxaemia definition, A–a gradient, HAPE HPV disagreement, review year; attributions; classifier clip)
  [x] fixes (528 quotes) [x] committed with 04 2026-11-23.
  Then respiratory, renal, GI, endocrine,
  reproductive, CNS, senses.

- 2026-11-22 11:15 crash: Claude Code 2.1.330 segfaulted itself (coredump; no kernel/amdgpu errors at that time;
  user's memtest and scrub are clean). Same as the 11-20 crashes of 2.1.327/328. Repaired 3 corrupt .git loose objects
  (fsck clean). User reinstalled python, git and the others (clean); module 40 pushed. Standard http.server and plain ffshot work again.
  Module 40 review and module 41 build resumed. Later found 2 tracked files changed on disk with mtime unchanged
  (ul-nv.json, ll-nv.pack; git status missed them) and restored them from git; check with a full
  `git ls-files -s` vs `git hash-object --stdin-paths` compare before each commit.
- Module 40 (histology II): [x] build (520 quotes, 37 Commons micrographs, pages respiratory-digestive,
  urinary-reproductive, endocrine-senses-cns; OpenStax-flagged quotes found and removed; AN43.2, 43.3 partial)
  [x] review (15 findings: pituitary basophil fact, cord image h, --gm/--rcpt colour clashes, markers,
  appendix image, attributions; browser checks not run, server down) [x] fixes (all 15 items; +prostate corpora amylacea and Purkinje micrographs; 528 quotes)
  [x] browser checks (6 pages, 0 JS errors, no phone overflow) + colours softened
  [x] docs (+ module 38 pages' Histology links) [x] commit. Done 2026-11-22.
- Leftovers 2026-11-22: 46 unticked + 21 partial items. Plan: 43 general (AN1–6) and 44 abdominopelvic osteology,
  radiology, surface, sections (AN51, 53–55) running in parallel; then 45 limb/region leftovers (AN8.4, 9.2–9.3,
  12.9/10/15, 13.5–13.8, 18.7, 20.6/7/10, 23.1, 26.2, 42.1, 43.7, 43.9, 82.1); then the [~] partials.
- Module 43 (general: sheet fill-general2; terminology-bone, skin-lymphatics + muscle/blood-vessels additions)
  [x] build (300 quotes; AN3.3 shunt/spurt not covered: no open source) [x] review (aneurysm wall layers inverted, ipsilateral L/R swapped,
  nutrient-artery Wikipedia copies Gray, S1 band, --redmarrow/--clot hue and atlas clashes) [x] fixes (309 quotes) [x] docs
  [x] commit. Done 2026-11-22. AN3.3: reviewer also found no downloadable open source (J Anat 1959/1978 scans only; PDF fetch blocked);
  stays unticked — ask user whether to fetch those PDFs by hand.
- Module 44 (abdominopelvic: sheet fill-abdo2; bony-pelvis, imaging-abdomen, surface-sections + ap.js/css)
  [x] build (492 quotes, 7 Commons radiographs, sections cut from 3D models) [x] review (T10 cut through T11 so no oesophagus,
  section labels on wrong organs, true-conjugate naming, unsourced claims, T1/T2 missing) [x] fixes (511 quotes) [x] docs [x] commit. Done 2026-11-22.
  Left for later: pre-existing label overlaps on pelvis/perineum/organs drawings; lower-limb/bones.html heading still
  credits "Wikipedia" (the OpenStax-citing Pelvis article); organs.html still counts WP Transpyloric plane.
- Module 45 (limb leftovers AN8.4, 9.2–9.3, 12.9/10/15, 13.5/6/8, 18.7, 20.6/7/10: sheet fill-limbs3; breast.html,
  radiographs-landmarks per limb, embryology/limb-development.html + additions) [x] build (404 quotes; breast, radiographs-landmarks ×2,
  limb-development + additions; AN13.5, 20.6 partial: Commons 429 on films) [x] review (32 items: limb
  rotation drawing, child elbow side, ankle labels, pec minor drawing, OA alt text, 3D levels, unsourced lines,
  --mamm→--gland) [x] fixes (421 quotes) [x] docs [x] commit. Done 2026-11-22. [ ] fixes
  [ ] docs [ ] commit. Then 46: AN23.1, 26.2, 42.1, 43.7, 43.9, 82.1; then partials.
- Module 42 (genetics: AN73.1–75.5) started 2026-11-22: sheet fill-genetics, pages in anatomy/genetics/.
  [x] build (688 quotes; chromosomes-karyotype, inheritance-pedigrees, aberrations-clinical; 6 Commons images;
  tokens --mat --pat --mut --probe; check_quotes.py now maps MLP- keys) [x] review (26 findings: Punnett titles AA, CFTR 7q and splice
  missing, Wikipedia copying MedlinePlus, --mat/--pat/--mut/--clin misuse, dark contrast, drawings) [x] fixes (712 quotes) [x] docs
  [x] commit. Done 2026-11-22. Next: leftovers (general 1–6, radiology 54,
  sectional 51, osteology 53, surface 55, limb leftovers).
- Module 41 (systemic embryology: AN25.2–25.6, 43.4, 52.4–52.8, 64.2–64.3) started 2026-11-22: sheet fill-embryo2,
  pages in anatomy/embryology/. [x] build (747 quotes; heart-vessels, gut-urogenital, head-neck-cns; not browser-tested,
  gjs+rsvg only) [x] review (14 findings: fetal IVC into RV, arch/coarctation drawing, PDA chip, flexures, malrotation chips,
  ~30 unquoted or unattributed claims, --telen vs --parathy, text clipping; no JS errors) [x] fixes (all 14; 777 quotes) [x] docs [x] commit. Done 2026-11-22.
  Leftover on module 39 pages (pre-existing): clipped hour labels "1"/"28" on cyc-svg, som-svg overlap,
  phone overlaps in neu-svg and horm-svg (membranes-placenta).
- Module 40 commit 9a481ee is local only: push failed (git pack-objects SIGSEGV; /usr/bin/git fails pacman check).
  Push after `sudo pacman -S git ...`. After: genetics (73–75), then leftovers (general 1–6, radiology 54, sectional 51,
  osteology 53, surface 55, limb leftovers).
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

- The whole session is capped at 10 GB (user 2026-11-24; was 8 GB; the crash was at ~11.3 GB). Start Claude with
  `claude-10g` (in ~/.local/bin; `claude-8g` still exists), which puts Claude and everything it starts in one cgroup. Without it, the cap can be set by hand on the terminal's cgroup
  (`memory.max` under /sys/fs/cgroup/…/app-org.kde.konsole-*.scope/tab(*).scope).
- Every heavy command goes through `tools/capped` (default 4 GB, `--mem` to change): Blender exports,
  `bones build`, `tools/test/ffshot.py`, large Python jobs. It holds a lock, so only one heavy job runs at a time even
  when agents work in parallel.
- At most three agents at once (user 2026-11-24), and only when their work is independent. Tell each agent to use
  `tools/capped`.
- Only ONE test browser at a time, enforced: ~/personal/buildenv/lib/python3.14/site-packages/sitecustomize.py makes
  every selenium Firefox in the buildenv Python wait for a lock (`$XDG_RUNTIME_DIR/neet-pg-browser.lock`) and forces
  software rendering (llvmpipe), even in an agent's own script that skips tools/capped. Tested 2026-11-24: a second
  browser waited for the first to quit; both reported llvmpipe. Re-create the file if the venv is rebuilt.
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
