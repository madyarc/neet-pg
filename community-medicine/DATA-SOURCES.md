# Community Medicine — data sources and verification log

CDC Principles of Epidemiology (2012), WHO documents, Indian official data sources (ORGI/SRS, MoHFW NFHS and IDSP),
US FDA, StatPearls, open-access papers and Wikipedia. Two independent sources per fact, or the single source named on
the page; official sources named with year.

## 01 Epidemiology — `epidemiology/concepts-measures.html`, `epidemiology/study-designs.html`, `epidemiology/transmission-outbreak-screening.html`

- Fact sheet `sources-local/facts/fill-c01.md` (374 quotes, script-checked against `sources-local/modern/fill-c01/`,
  downloads 2026-11-25).
- Official documents: CDC Principles of Epidemiology 3rd ed. (2012, full book); Wilson & Jungner, WHO 1968 (IRIS); WHO
  2001 age standardisation; SRS Statistical Report 2020; NFHS-5 India Fact Sheet (2019–21); MoHFW "About IDSP" (page
  updated 2026; Wayback copy); US FDA clinical-research phases (2018).
- Not independent: seven Wikipedia articles cite CDC (Epidemiology, Attack rate, Secondary attack rate, Mortality
  rate, Incubation period, Epidemic curve, Outbreak) and are not counted for CDC facts; Wikipedia IDSP copies the
  official page; the three 2016 methodology papers by one author count as one source. No OpenStax/Lumen/Boundless.
- Contested, shown: neonatal period < 28 days (CDC) vs < 29 days (SRS 2020); IDSP "S" form suspected vs syndromic;
  phase 2 trial size; disability limitation under secondary (Wikipedia) vs tertiary prevention (2024 review).
- One source, attributed: field trial (Smith, Morrow & Ross 2015 abstract; the book itself refused automated download);
  Neyman bias; perinatal mortality and stillbirth rates (SRS 2020); census facts (Wikipedia; no official text
  reachable).
- Calculator examples are CDC or StatPearls worked examples, or labelled made-up. No new colour tokens.
- Independent review 2026-11-25, fixed: disability-limitation disagreement and Leavell & Clark label dropped; rate
  definition attribution; lead-time bias attribution; statements beyond the quotes; dated official sources;
  `--accent`/`--clin` misuse; added SMR and indirect standardisation, person-time, PMR, SBR, U5MR, matching, Berkson,
  Hawthorne and Neyman bias, serial interval shorter than incubation, isolation and quarantine, triad and iceberg;
  calculator input validation.
