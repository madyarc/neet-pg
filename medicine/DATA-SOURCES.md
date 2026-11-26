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

## 02 Diabetes mellitus — `endocrine/diabetes-types-pathogenesis.html`, `endocrine/complications-emergencies.html`, `endocrine/diabetes-treatment.html`

- Fact sheet `sources-local/facts/fill-g02.md` (454 quotes, script-checked against `sources-local/modern/fill-g02/`,
  downloads 2026-11-26; Part D = review fixes).
- Guidelines (open): ADA Standards of Care 2026 (PMC HTML); 2024 ADA/EASD/JBDS/AACE/DTS hyperglycaemic crises consensus
  (PMC11272983 = PMC11343900, one source); 2009 ADA consensus (PMC2699725); JBDS 2023 HHS (PMC10107355); KDIGO 2024 CKD
  and KDIGO 2022 diabetes-in-CKD (kdigo.org PDFs, facts quoted only). ADA 2026 Table 16.1 is adapted from the 2024
  consensus and is not counted as independent.
- Edition changes shown: DKA glucose >250 → ≥200 or known diabetes; β-hydroxybutyrate ≥3.0; HHS effective osmolality
  >320 → >300; insulin held until K >3.3 (2009) → >3.5 (2024); bicarbonate if pH <6.9 → <7.0; pH 7.25 mild (2009) →
  moderate (2024), the 2009 gap at 7.24 counted as moderate (stated). Doses are the consensus reports' adult doses,
  attributed; paediatric management not covered.
- Contested, shown: UACR at 300 (KDIGO A2 vs ADA ≥300); NPH peak; twin concordance; pioglitazone hypoglycaemia; 2009 HHS
  bicarbonate; Somogyi effect ("contested"); necrobiosis lipoidica association.
- Not covered (not open or not sourced): India prevalence and economic burden (ICMR-INDIAB); Wagner/SINBAD foot grades;
  Mogensen stages; most drug interactions.
- Existing med.css tokens only. Calculators hand-checked (4 presets × 2 editions), severity boundaries in both editions,
  all 512 drug-picker combinations free of contradictions.
- Independent review 2026-11-26, fixed: garbled criteria note; severity per edition; drug-picker HF/kidney conflicts;
  ADA recs 9.6, 9.10 caveat, 9.11, 9.12, 9.18; tirzepatide row; metformin eGFR thresholds (ADA + KDIGO); adult-dose
  labels; UACR 300; hypoglycaemia alert value; anion-gap wording; added LDL goals, teplizumab, GLP-1 RA aspiration,
  skin lesions, dawn vs Somogyi.
