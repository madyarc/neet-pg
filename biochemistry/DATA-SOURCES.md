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

## 02 Carbohydrate chemistry and metabolism — `carbohydrates/carb-chemistry-glycolysis.html`, `carbohydrates/tca-gluconeogenesis-glycogen.html`, `carbohydrates/minor-pathways-glucose.html`

- Fact sheet `sources-local/facts/fill-b02.md` (602 quotes, script-checked against `sources-local/modern/fill-b02/`,
  downloads 2026-11-26; Part D lists the review fixes).
- Official documents: ADA Standards of Care in Diabetes—2026, Section 2 (PMC12690183); WHO/IDF 2006 diagnosis report;
  WHO 2011 HbA1c report; CPIC expanded G6PD guideline 2023 (PMC10281211); IUBMB entries for 57 enzymes; IUPAC-IUBMB
  2-Carb-36 (1996). GeneReviews abstracts (GSD I–VI and IX, galactosaemia, HFI, PDC deficiency).
- Primary study: Katz & Tayek 1998 (PMID 9725823): gluconeogenesis supplied 41/71/92% of glucose production at
  12/20/40 h (the Cori cycle 18/35/36%). Wikipedia gives 41/71/92% as the Cori share; the page shows the study's figures
  and notes the difference.
- Reviews: J Biol Chem 2024 (glycolysis), 2023 (TCA), 2018 (gluconeogenesis); Adeva-Andany 2016 pair (one source);
  pentose phosphate 2015; G6PD 2022 ×2; GalNet 2017, galactosaemia 2022; HFI 2022; fructose errors 2017; polyol 2007,
  2018; PDC deficiency consensus 2026. StatPearls; Wikipedia (current wikitext checked; none excluded).
- Not independent: Wikipedia Fructolysis ≈ PMC5409695 (aldolase B); Wikipedia Glucose tolerance test ≈ StatPearls
  (OGTT); StatPearls reproduces CPIC.
- Contested, shown: gluconeogenesis rate-limiting enzyme; ATP per glucose 30–38; PK deficiency ranking; WHO 110 vs ADA
  100 IFG cut-off; Katz & Tayek vs Wikipedia.
- No new colour tokens.
- Independent review 2026-11-26, fixed: Katz & Tayek figures; WHO joint categories; ADA confirmation and discordance
  wording; preset chips; GSD IX second source and missing quotes; colour meanings; PFK-1 verdict removed; glycerol
  wording; SVG collisions; CPIC year and primaquine dose nuance; red-cell ATP drawing; added GSD 0 and VII,
  galactosaemia III, TPP enzymes, glycolysis inhibitors and shuttles (attributed).
