# Paediatrics — data sources and verification log

Classifications and cut-offs only from named, dated official documents (WHO Child Growth Standards 2006, WHO 2007
growth reference, WHO/UNICEF 2009, WHO 2013, IAP 2015, CDC 2022). Two independent sources per fact, or the single source
named on the page. No doses.

## 01 Growth and development — `growth-development/growth.html`, `growth-development/development.html`

- Fact sheet `sources-local/facts/fill-pd01.md` (506 quotes, script-checked against `sources-local/modern/fill-pd01/`,
  downloads 2026-11-25).
- LMS values extracted from the official WHO xlsx tables (weight-for-age, length/height-for-age, head
  circumference-for-age 0–60 months; WHO 2007 height-for-age; weight-for-length and weight-for-height at whole cm) with
  `lms_extract.py`; z-scores hand-checked with `zcheck.py`; an independent review re-parsed all 426 values.
- CDC 2022 milestones from Zubler et al., Pediatrics 2022 (PMC9680195), Tables 2–5 (cdc.gov refused automated access).
  IAP 2015 via the open IAP paper (PMC4481652); its centile tables are not plotted.
- Excluded: Wikipedia "Fontanelle" (cites a Boundless text). Wikipedia Kwashiorkor repeats the WHO SAM criteria (not
  counted as independent).
- Contested, shown: weight doubling/tripling/quadrupling vs WHO medians (the textbook "doubles by 5 months" has no open
  source); head-circumference gain in year 2; fontanelle closure; first tooth; Tanner year; microcephaly cut-off; global
  developmental delay definition; pincer-grasp red flag vs the CDC age; short-stature screening tests.
- No new colour tokens; CDC ages drawn as ink diamonds, red flags as `--clin` triangles in their own lane.
- Independent review 2026-11-25, fixed: timeline shapes, dated WHO cut-offs, source labels by topic, IAP wording,
  bone-age picker (fast velocity), weight floor, percentile wording, SVG collisions; added weight-for-length/height,
  teeth, Tanner, body proportions, first investigations, FTT causes, DQ, primitive reflexes. Not covered (no open
  source): BMI-for-age, segment-ratio values, a DQ cut-off.
