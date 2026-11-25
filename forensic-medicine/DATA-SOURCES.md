# Forensic Medicine — data sources and verification log

Official Indian and WHO texts, StatPearls, open-access PMC papers and Wikipedia; no textbooks. Two independent sources
per fact, or the single source named on the page. Laws and rules named with their year. Schematics only; no photographs.

## 01 Death and post-mortem changes — `thanatology/death.html`, `thanatology/postmortem-changes.html`

- Fact sheet `sources-local/facts/fill-fm01.md` (430 quotes, script-checked against `sources-local/modern/fill-fm01/`,
  downloads 2026-11-24/25).
- death.html: WHO ICD-11 Reference Guide (2026) and the RGI Physicians' Manual on MCCD, 5th ed. (2012): chain rules,
  WHO four lines vs India's three plus the extra line of §2.3.3, police certificate in medico-legal cases. THOA 1994 as
  amended 2011 from an unofficial consolidated text (Delhi government; India Code and NOTTO unreachable), labelled as
  such on the page; THOT Rules 2014 (G.S.R. 218(E), 27 Mar 2014) from the Tamil Nadu Gazette reprint (reliable); Form 10
  checked against Dhanwate, IJCCM 2014 (PMC4166875). The three wordings for a missing neurologist (Act proviso, Form 10
  Note I, Rule 5(4)(c)) are shown and said to differ; near-relative consent per Rule 5(4)(a). Penalties and the IPC
  definition left out; RBD clauses cited "as printed in the RGI manual 2012". Sudden-death definitions disagree
  (Encyclopedia of Forensic and Legal Medicine vs IJMR 2025). The classical modes-of-death scheme has no open source.
- postmortem-changes.html: livor review (Cureus 2025: timing, complete/incomplete shifting, fixed pattern, colours,
  bruise, Tardieu spots, Casper's dictum); PMI reviews (Diagnostics 2025, Front Microbiol 2025); Henssge validation
  2025; rigor case reports 2011 and 2017; mummification 2023; adipocere 2019 and 2025; maceration 2016, 2018, 2020; cold
  stiffening 2018. No cooling formula (Glaister is Wikipedia-only). All timings shown per source; the rigor map is read
  as hours after death (labelled).
- Colour tokens (fmt.css): `--livor` (usual lividity), `--livor-co` (cherry-red/pink lividity), `--sulfhb` (putrefactive
  green); `--ok`/`--flag` with atlas values for valid/invalid; `--actin`, `--myosin`, `--ca` from physiology.
- Independent review 2026-11-25, fixed: livor shifting rule (complete < 3 h, incomplete 3–6 h, fixed unchanged);
  children's Form 10 interval; consent and neurologist-replacement wording; Act renaming and unofficial-text label;
  MCCD extra line, neutral rule states, illustrative cases; vegetative state no longer "permanent"; `--accent` misuse;
  rigor reading and stiff eyelids; sudden-death series labels; additions (Casper's dictum, Tardieu spots, rigor
  re-establishment).
