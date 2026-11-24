# Pathology — data sources and verification log

Open sources only: StatPearls abstracts (one source), open-access papers via NCBI PMC/BioC and Europe PMC, Wikipedia
(wikitext checked). Two independent sources per fact, or the single source named on the page.

## 01 Cell injury and adaptation — `general/cell-injury-death.html`, `general/adaptations-accumulations.html`

- Fact sheet `sources-local/facts/fill-p01.md` (326 quotes, script-checked against `sources-local/modern/fill-p01/`,
  downloads 2026-11-24; Europe PMC was down, NCBI efetch/BioC used; Part D lists the review fixes).
- No OpenStax/Boundless hits; copy check clean. Wikipedia Metaplasia closely follows PMC5998678 on reversibility, so it
  is not counted as independent there.
- Reviews: PMC3904795 (ischaemia–reperfusion 2012), PMC5864239 (NCCD 2018), PMC7325303 (BCL-2 2020), PMC12229594
  (caspases 2025), PMC5998678 (metaplasia 2017), PMC4166529 (Campisi 2013), PMC3836174 (López-Otín 2013). Studies and
  other papers: PMC4164887 (oral dysplasia 2014), PMC2789729 (rat airway 2009), PMC4829204, PMC4649990, PMC8186013,
  PMC8257163, PMC9614304, PMC11564275, PMC5987754, PMC12828800, PMC8081271. StatPearls 28613685 and others; Wikipedia.
- Contested, shown: nuclear fragmentation in necrosis (2012 review, in a passage contrasting it with apoptosis);
  metaplasia reversibility (Wikipedia and a 2009 rat study vs the 2017 review). Dysplasia grades quote the 2014 review's
  wording; CIN thirds not used (no source).
- Images (Commons, licences read 2026-11-24; resized, labelled): kidney infarct (Calicut Medical College, CC BY-SA 4.0);
  Barrett oesophagus (M. Häggström, CC0, top 20% cropped); fatty liver (M. Häggström, CC0). Caseous TB node and
  psammoma micrographs not obtainable (HTTP 429); caseous necrosis drawn as a schematic.
- Drawings schematic; the calcification classifier's "both" and "neither" answers are marked as the page's summary.
- Colour tokens (path.css): `--lipofuscin`, `--haemosid` (haemosiderin), `--bili` (bilirubin in tissue or plasma,
  distinct from physiology's `--bile` for bile in ducts).
- Independent review 2026-11-24, fixed: metaplasia disagreement, token clashes with biochemistry, calcium soaps and
  fibrinoid contrast, dysplasia wording, classifier summary, Russell-body attribution, unquoted labels, glycolysis
  leader, injury-slider threshold, `--clin` misuse, two micrograph labels, apoptosis drawing, ageing citations, airway
  drawing note.
