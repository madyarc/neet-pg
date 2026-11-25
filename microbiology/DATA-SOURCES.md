# Microbiology — data sources and verification log

Open sources only: StatPearls, open-access reviews, Wikipedia (wikitext checked), and CDC/WHO/ICMR documents. Two
independent sources per fact, or the single source named on the page.

## 01 General microbiology — `general/bacteria-structure-growth.html`, `general/genetics-lab-diagnosis.html`, `general/sterilisation-epidemiology.html`

- Fact sheet `sources-local/facts/fill-m01.md` (694 quotes, script-checked against `sources-local/modern/fill-m01/`,
  downloads 2026-11-24; Part E lists the review fixes).
- Official documents: CDC/HICPAC Guideline for Disinfection and Sterilization in Healthcare Facilities 2008 (update
  2024; PDF via the web archive), CDC Principles of Epidemiology 3rd ed. 2012, ICMR Bacteriology SOP 2nd ed. 2019, WHO
  Laboratory Biosafety Manual 4th ed. 2020.
- Excluded: Wikipedia "Koch's postulates" (cites Boundless); the postulates rest on Wikipedia "Germ theory of disease"
  (probably derived from it, noted) and EID 2011 (PMC3298383). PMC6031597 (by the CDC guideline's authors) not counted.
- Not independent: Wikipedia Sterilization and Transmission copy CDC; Epidemic quotes CDC; Dry heat sterilization and
  Natural reservoir cite CDC; Prion cites Rutala & Weber; Indole test overlaps ICMR. Facts resting on these are
  attributed to CDC (or ICMR) alone, or have another second source (prions: PMC5082740).
- Contested, shown: Gram's year (1882 vs 1884); autoclave hold times (CDC vs a 2026 review vs Wikipedia); cause of the
  stationary phase; ELISA "indirect" terminology; Koch dates as given by the sources still in use.
- Colour tokens (micro.css): `--cv` crystal violet, `--redye` safranin/carbol fuchsin (never beside `--rbc`/`--artery`),
  `--mb` methylene blue, `--om` outer membrane/LPS, `--bcap` bacterial capsule, `--dna` (olive/amber), `--donor`
  transferred DNA. Peptidoglycan drawn as an ink mesh.
- Independent review 2026-11-24, fixed: blood-spill dilutions (small 1:100, large clean then 1:10; safety); ELISA
  redrawn with correct antibody orientation; Cryptosporidium not reliably killed by HLD; Koch quotes re-keyed; CDC-only
  attributions; mycobacterial outer membrane and capsule; unquoted labels removed; layout; `--dna` recoloured;
  exam-point additions (endotoxin/exotoxin, stains, media, IMViC/TSI, tyndallisation, R plasmids, lysogenic conversion).
