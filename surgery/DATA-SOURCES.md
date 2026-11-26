# General Surgery — data sources and verification log

Clinical numbers only from named, dated guidelines (or open papers that reprint them, named on the page). Two
independent sources per fact, or the single source named on the page. No doses beyond a guideline's own statements.

## 01 Metabolic response to injury and shock — `general/metabolic-response.html`, `general/shock.html`

- Fact sheet `sources-local/facts/fill-s01.md` (291 quotes, script-checked against `sources-local/modern/fill-s01/`,
  downloads 2026-11-25/26; reviewed and fixed 2026-11-26).
- metabolic-response.html: StatPearls (Stress Reaction, Acute Phase Reactants, ERAS); reviews PMC11121777, PMC12831963,
  PMC7388795, PMC6780066, PMC5753602, PMC3053509, PMC8139218; ERAS Society liver 2022 (PMC9726826) and emergency
  laparotomy 2021/2023 (PMC8026421/PMC10241558, one source; it does not recommend carbohydrate loading); Wikipedia
  hormone and metabolism articles. Excluded: Wikipedia Homeostasis (cites OpenStax); Acute-phase protein copies
  PMC3053509.
- shock.html: EU guideline on major bleeding and coagulopathy following trauma, 6th ed. 2023 (PMC9977110; Table 2
  reprints ATLS 10th ed. 2018); Sepsis-3 2016 (PMC4968574, PMC4910392); Surviving Sepsis Campaign 2021 (PMC8486643);
  ESICM 2014 (PMC4239778); reviews PMC3672555 (2012), PMC6520577, PMC6507212, PMC8541346, PMC8634278, PMC3672480
  (Mutschler 2013), PMC11515103, PMC6698590, PMC3654944; StatPearls shock chapters; Wikipedia. Not independent:
  Wikipedia's ATLS numeric list cites StatPearls 2018 (shown as an older version); Septic shock and SOFA restate Sepsis-3.
- Contested, shown: ebb/flow timing; GH direction; ATLS class III boundary (31 vs 30%); permissive hypotension target
  (SBP 80–90 vs MAP 40–50); FFP:pRBC ≥1:2 vs 1:1:1; septic-shock mortality; shock-index cut-offs; commonest shock type
  (hypovolaemic vs septic).
- Safety: permissive hypotension shown with the guideline's exclusion (not with TBI or spinal injury; caution in the
  elderly and chronic hypertension).
- Colour tokens reused (`--rbc`, `--fluid`, `--platelet`, `--fat`, `--artery`); no new tokens.
- Independent review 2026-11-26, fixed: ERAS carbohydrate-loading attribution; TBI/spinal exception at every
  instruction; ebb/flow curve directions and baseline; SSC 2021 additions (restrictive transfusion, antimicrobials
  within 1 h, vasopressin, steroids); neurogenic-shock wording; ATLS labels; shock-index off-scale; colours; added
  treatment principles by type, SIRS, TXA within 3 h.
