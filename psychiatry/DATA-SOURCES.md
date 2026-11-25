# Psychiatry — data sources and verification log

Classifications from WHO ICD-11 CDDR (2024); DSM-5 cited only through open secondary sources. Guidelines named with year
(WHO mhGAP 2016/2023, NICE, Indian Psychiatric Society). Two independent sources per fact, or the single source named on
the page. No doses; lithium target levels are NICE CG185's (named, dated).

## 01 Psychotic and mood disorders — `psychosis-mood/schizophrenia-psychosis.html`, `psychosis-mood/mood-disorders.html`

- Fact sheet `sources-local/facts/fill-ps01.md` (322 quotes, script-checked against `sources-local/modern/fill-ps01/`,
  downloads 2026-11-25; review fixes in Part E).
- schizophrenia-psychosis.html: WHO CDDR 2024 (6A20–6A25, ATPD, schizoaffective, delusional disorder); DSM-5 via
  Wikipedia and StatPearls; first-rank symptoms (Wikipedia, PMC6986488, PMC11272318); dopamine pathways (Wikipedia,
  PMC10618092, PMC4065707, PMC12423237); EPS timing (PMC4065707, PMC6283785, Wikipedia); NMS (WHO mhGAP 2016/2023,
  StatPearls, PMC4812801, PMC5248946, PMC6734608); clozapine monitoring: IPS 2026 (PMC12900051) vs the 2025 European task
  force as quoted in PMC12900052 (disagreement shown); catatonia (Wikipedia, IPS 2023, IPS 2026).
- mood-disorders.html: CDDR 2024 and NICE NG222 (2022); bipolar (CDDR, StatPearls, Wikipedia, PMC6970089); suicide
  assessment WHO mhGAP-IG 2016; antidepressant safety (NICE NG222, mhGAP 2023/2016); lithium NICE CG185 (2014, updated
  2025) levels, PMC5164879, PMC6274637, IPS 2025; valproate (mhGAP 2016, Wikipedia, IPS 2025); ECT IPS 2023
  (PMC10096214); MAO location (Wikipedia, one source); MHCA 2017 s.115, s.95 (India Code, Wayback copy); BNS 2023 note via
  Wikipedia (effect on s.115 not covered).
- Excluded: Wikipedia "Atypical antipsychotic" (cites Boundless).
- Contested, shown: schizophrenia duration (ICD-11 1 month vs DSM-5 6 months); delusional disorder (3 months vs 1
  month); hypomania ("several days" vs 4 days); Schneider's first-rank year (1939 vs 1959); clozapine monitoring
  schedules; lithium haemodialysis thresholds (no number given).
- Not stated for want of a quote: pathway-by-pathway effects of mesolimbic/mesocortical D2 blockade; the DSM-5 core
  psychotic-symptom rule (the checker tests DSM duration only).
- No new colour tokens.
- Independent review 2026-11-25, fixed: duration-picker logic (mood episode, exact cut-offs, DSM schizoaffective
  conditional, delusional bands), arrowheads, mesocortical path, synapse marks and MAO on a mitochondrion, clozapine
  schedule disagreement, attributions, `--accent` misuse; added NMS management, catatonia, antidepressant safety,
  valproate and neural-tube defects, olanzapine metabolic risk.
