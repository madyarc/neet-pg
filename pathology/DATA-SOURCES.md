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

## 02 Inflammation and healing — `general/inflammation.html`, `general/healing-repair.html`

- Fact sheet `sources-local/facts/fill-p02.md` (472 quotes, script-checked against `sources-local/modern/fill-p02/`,
  downloads 2026-11-26; current Wikipedia revisions via curl).
- Excluded: Wikipedia Eicosanoid (cites a LibreTexts copy of Boundless A&P); PMC7122703 (publisher chapter, not openly
  licensed). Not independent: Wikipedia Wound healing's factors section copies Guo & DiPietro 2010 (PMC2903966);
  Wikipedia Inflammation's chronic-duration and chronic-cell sentences and Wikipedia Granuloma's definition cite
  StatPearls (one source each).
- Reviews: PMC3081099 (prostaglandins 2011), PMC2480489 (permeability 2008), PMC2861890, PMC4629053, PMC3197933,
  PMC3271231, PMC7063431 (LAD 2020), PMC11663721 (TB granuloma 2024), PMC6797840 (2019), PMC9035892 (giant cells 2022),
  PMC2903966 (Guo 2010), PMC7536089 (Wilkinson 2020), PMC7443169, PMC5372622, PMC7818137; StatPearls; Wikipedia.
- Contested, shown: the fifth cardinal sign; loss of function; keloid/hypertrophic boundary; contracture in keloids.
- Not covered (no two open sources): exudate specific gravity and protein values; pseudomembranous and catarrhal
  patterns; wound strength at suture removal; toxic exposure as a cause of chronic inflammation.
- Images (Commons, licences read 2026-11-26; labels checked with marks.py): tuberculous node granuloma (Calicut Medical
  College, CC BY-SA 4.0, frame trimmed); oedematous granulation tissue (M. Häggström, CC0).
- No new colour tokens. path.js: stepper keeps keyboard focus at the ends (all pathology pages).
- Independent review 2026-11-26, fixed: one-source attributions; transmigration drawn at the junction; drug blocks on
  the arachidonic map; vasoconstriction timing; Celsus citation; VEGF source; missing quotes; wording; CGD row;
  capillary colour; SVG collisions; added causes of chronic inflammation, mediator source cells, preformed vs
  synthesised and oxygen-independent killing.
