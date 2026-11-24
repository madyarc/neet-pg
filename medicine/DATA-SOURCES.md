# General Medicine — data sources and verification log

Clinical classifications and targets only from named, dated guidelines or society statements, quoted from open texts
(or from open papers that report them, named on the page). Two independent sources per fact, or the single source named
on the page. No doses unless an open guideline states them.

## 01 Cardiology: heart failure, valves and endocarditis, IHD and ACS — `cardiology/heart-failure.html`, `cardiology/valves-endocarditis.html`, `cardiology/ihd-acs.html`

- Fact sheet `sources-local/facts/fill-g01.md` (573 quotes, script-checked against `sources-local/modern/fill-g01/`,
  downloads 2026-11-24; Part E lists the review fixes, E9 the items left out for want of a second source).
- Sources: StatPearls abstracts; NCBI BioC full texts; Wikipedia (wikitext grepped for OpenStax/Boundless: none).
- Guideline texts were not open (OUP/AHA/Wiley 403): ESC 2021 HF and 2023 update, ESC 2023 ACS, ESC valve and
  endocarditis guidelines, ACC/AHA/HFSA 2022, AHA Jones 2015, Duke-ISCVID 2023. Quoted through PMC10704008, PMC8420965,
  PMC5911656, PMC5346434, PMC11355459, PMC13203618, PMC11317809, PMC12787086, PMC8970581 and CSI 2017 STEMI statement
  (PMC5388060, open).
- Labels: natriuretic-peptide cut-offs = ESC 2016 (via a 2019 review; a 2022 review agrees); LDL goals = ESC/EAS 2019,
  kept in the 2025 update; door-to-needle/door-to-balloon = ACC/AHA via Wikipedia, no year; thrombolysis
  contraindications = CSI 2017 Table 11 vs Wikipedia (White & Van de Werf 1998), disagreements shown.
- Contested, shown: HFrEF ≤40 vs <40; rheumatic fever latency; CRP threshold wording; low-salt diet (guideline vs 2024
  meta-analysis); ARNI sequencing; rheumatic fever after skin infection; papillary-muscle and free-wall rupture rates;
  Dressler timing; digoxin's pathognomonic arrhythmia.
- Colours: tokens reused with their meanings; vessels coloured by structure (pulmonary artery = artery colour),
  oxygenation shown by labels and arrow style. No new tokens.
- Independent review 2026-11-24, fixed: ACS picker now decides by ECG and troponin before pain pattern (safety);
  reperfusion helper beyond 24 h; full CSI 2017 thrombolysis list; ESC 2016 named; BNP rounding; skin-infection
  disagreement; rule-6 labels; vessel colours; Duke and Jones examples; IE culture rules; attributions; layout.
