# Anaesthesiology — data sources and verification log

Numbers only from named, dated guidelines (or open reviews reporting them, named as such on the page). Two independent
sources per fact, or the single source named on the page. Doses only where an open guideline text states them, and
attributed to it.

## 01 Resuscitation, oxygen and airway — `resuscitation-airway/cpr-bls-als.html`, `resuscitation-airway/oxygen-airway.html`

- Fact sheet `sources-local/facts/fill-an01.md` (341 quotes, script-checked against `sources-local/modern/fill-an01/`,
  downloads 2026-11-26; review fixes in Part D).
- cpr-bls-als.html: AHA 2020 Parts 3–5 (Internet Archive copies; supportive text only, recommendation tables are
  images); ILCOR CoSTR 2020; KACPR 2025; SRFAC 2026 (CME quiz items not used). Reported by reviews (full texts HTTP
  403): ERC 2021 (BJA Educ 2022, PMC9214439), ERC 2025 newborn (PMC13253025), RCUK 2021 (PMC9346505), ERC 2025 ALS
  reversible causes (PMC13026813); UK paramedic report PMC9983061; StatPearls; Wikipedia.
- oxygen-airway.html: BTS 2017 (PMC5531304); TSANZ 2022 (PMC9303673); DAS 2015 (PMC4650961); SRFAC 2026; KACPR 2025;
  AHA 2020; reviews PMC11486880, PMC10926037, PMC13409782, PMC3672640, PMC8043306, PMC12384858, PMC8022065; StatPearls;
  Wikipedia.
- Excluded: Wikipedia Mechanical ventilation (cites Boundless) and Targeted temperature management (cites OpenStax).
- Contested, shown: adult compression depth; paediatric ratio and infant technique; adrenaline and amiodarone timing;
  newborn adrenaline timing; post-ROSC SpO₂, MAP and temperature; 4H/4T vs 5H/5T lists; FiO₂ per device; SpO₂ targets
  (BTS vs TSANZ; the physiology page quotes JRCALC 2009 via Wikipedia).
- Not covered (one source or none): predicted-body-weight formula; SIMV.
- No new colour tokens; schematics labelled.
- Independent review 2026-11-26, fixed: LMA/ETT drawings (anatomy redrawn, devices on a neutral head); pressure-control
  limits and over-volume warning; quiz-sourced quotes replaced; 4 Hs and 4 Ts added with amiodarone/lidocaine timing;
  ERC 2025 newborn quote; depth scale; device bars; tidal volume context (post-arrest vs ARDS); temperature row label;
  DAS 2015 attempt limits and scalpel cricothyroidotomy; compression fraction; phone layout.
