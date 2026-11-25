# Pharmacology — data sources and verification log

Open sources only: StatPearls abstracts (one source), open-access reviews via PMC/Europe PMC (each author group one
source), official documents (US FDA, WHO, WHO-UMC, CDSCO Drugs and Cosmetics Rules, IPC/PvPI, PIB), Wikipedia (wikitext
checked; not counted where it copies another source). Two independent sources per fact, or the single source named on
the page. No doses for real drugs; simulators use a hypothetical drug.

## 01 General pharmacology — `general/pharmacokinetics.html`, `general/pharmacodynamics.html`, `general/principles-safety.html`

- Fact sheet `sources-local/facts/fill-f01.md` (676 quotes, script-checked against `sources-local/modern/fill-f01/`;
  downloads 2026-11-24, review-fix additions 2026-11-25). Built by three agents (setup; pages 1–2; page 3) and one
  fix agent.
- Not independent: Wikipedia CYP3A4 lists copy the FDA categories, so the inducer/inhibitor table rests on the FDA
  "Drug Development and Drug Interactions" table (content of 29 May 2026) plus Ment Health Clin 2016 (antiseizure drugs);
  ritonavir FDA only. Wikipedia Naranjo algorithm copies Seger 2013: weights given as in Naranjo 1981, reproduced in
  Lung India 2011 and Seger 2013. No OpenStax, Lumen or Boundless in any download; Sackett 1996 and PMC1005027 (scans)
  not used.
- Official documents: Drugs and Cosmetics Rules 1945 (CDSCO text as amended to 31 Dec 2016; H1 by G.S.R. 588(E),
  30 Aug 2013); FDA PLLR (final rule Dec 2014, labelling from 30 June 2015); WHO rational-use and pharmacovigilance pages;
  WHO EML 24th list (Sept 2025); NLEM 2022 (PIB release 13 Sept 2022; official PDF unreachable); WHO-UMC causality 2018
  (via the web archive); IPC PvPI pages (programme July 2010).
- Contested, shown: CYP share of metabolism (80–90 % vs ~60 %); phenobarbital strength (FDA moderate vs review potent);
  erythromycin and grapefruit (FDA moderate vs Wikipedia strong); steady state 4–5 vs 3–5 half-lives; chloroquine Vd;
  Naranjo cut-offs (> 9 vs ≥ 9; doubtful 0 vs < 1); protein-binding displacement importance.
- Colour token `--ther` (therapeutic range band only), drawn at .55 opacity with an outline so it stays clear of
  `--fluid`; `--rcpt`, `--enz`, `--inhib` (also receptor antagonists) reused from biochemistry.
- Independent review 2026-11-25, fixed: GPCR redrawn with 7 crossings; Drug B reference curves; simulator axis at
  extremes; bioequivalence band neutral; `--ther` contrast; receptor drawings; attributions (grapefruit, transdermal,
  author-year labels, Naranjo provenance, ADR letters, IV, protein binding); layout and clamped readouts; ADR and WHO-UMC
  orderings; no dosing intervals; added epidural route, non-receptor targets, spare receptors, receptor regulation,
  risk–benefit, renal handling, TDM, pharmacogenetic examples. Not covered (one source only): enterohepatic
  circulation, intranasal route, per-route disadvantages.
