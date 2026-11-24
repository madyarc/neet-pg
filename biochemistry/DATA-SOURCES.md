# Biochemistry — data sources and verification log

Open sources only: StatPearls abstracts (one source), IUBMB/IUPAC official nomenclature, open-access papers via Europe
PMC/NCBI, Wikipedia (wikitext checked). Two independent sources per fact, or the single source named on the page.

## 01 Enzymes — `enzymes/enzymes-kinetics.html`, `enzymes/clinical-enzymes.html`

- Fact sheet `sources-local/facts/fill-b01.md` (351 quotes, script-checked against `sources-local/modern/fill-b01/`,
  downloads 2026-11-24; Part C lists the review fixes).
- Official documents: IUBMB enzyme list, rules and 17 enzyme entries; NC-IUB kinetics recommendations 1981; IUPAC-IUB
  multiple forms of enzymes 1976. Main second source for kinetics: PMC4692135 (Essays Biochem 2015).
- Excluded: Wikipedia Troponin (cites OpenStax). The Fourth Universal Definition of MI (2018) and the Revised Atlanta
  classification (2012) are used only through open-access reviews (PMC8078947, PMC10930800, PMC11727869, PMC8404461,
  PMC7954292; PMC10237108) and Wikipedia.
- Disagreements shown: troponin timing; CK-MB share of heart CK; ribozyme year; whether healthy people have abzymes;
  amylase threshold wording. One-source facts attributed on the pages. The Total CK timing is from presentation
  (StatPearls).
- Colour tokens in bioc.css: `--enz` (enzyme protein), `--sub` (substrate), `--inhib` (inhibitor), `--cofac` (cofactor);
  organ tokens reused from anatomy and physiology with their meanings.
- Independent review 2026-11-24, fixed: abzyme views, CK timing from presentation, marker attributions, AST tissues,
  ALP/GGT wording, label collisions, `--clin` and `--enz` misuse, inhibitor and dark substrate colours, stepper focus at
  the last step, missing quotes and footer sources; added 5′-nucleotidase and MI types 3–5.
