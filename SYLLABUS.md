# NEET-PG — complete topic list

NEET-PG has no separate syllabus. NBEMS says the questions come from the MBBS curriculum, which is the NMC *Competency Based Medical Education Curriculum 2024* (revised guidelines, 12 Sept 2024). Each subject's `SYLLABUS.md` lists every NMC topic and competency for that subject, with its code, as a checklist.

| Subject | NMC vol. | Topics | Competencies | of which *skill* | Revision Hub chapters / sections |
|---|---|---:|---:|---:|---:|
| [Anatomy](anatomy/SYLLABUS.md) | I | 82 | 413 | 1 | 8 / 14 |
| [Physiology](physiology/SYLLABUS.md) | I | 12 | 136 | 15 | 9 / 15 |
| [Biochemistry](biochemistry/SYLLABUS.md) | I | 14 | 83 | 10 | 8 / 16 |
| [Pathology](pathology/SYLLABUS.md) | I | 35 | 182 | 32 | 10 / 45 |
| [Pharmacology](pharmacology/SYLLABUS.md) | I | 10 | 92 | 3 | 10 / 54 |
| [Microbiology](microbiology/SYLLABUS.md) | I | 11 | 73 | 9 | 9 / 23 |
| [Forensic Medicine & Toxicology](forensic-medicine/SYLLABUS.md) | I | 14 | 157 | 30 | 8 / 12 |
| [Community Medicine (PSM)](community-medicine/SYLLABUS.md) | II | 20 | 136 | 47 | 10 / 43 |
| [General Medicine](medicine/SYLLABUS.md) | II | 29 | 529 | 171 | 10 / 127 |
| [Paediatrics](paediatrics/SYLLABUS.md) | II | 32 | 253 | 83 | 9 / 19 |
| [Psychiatry](psychiatry/SYLLABUS.md) | II | 13 | 17 | 7 | 7 / 10 |
| [Dermatology, Venereology & Leprosy](dermatology/SYLLABUS.md) | II | 15 | 48 | 6 | 8 / 9 |
| [General Surgery](surgery/SYLLABUS.md) | III | 30 | 132 | 29 | 9 / 21 |
| [Orthopaedics](orthopaedics/SYLLABUS.md) | III | 14 | 39 | 2 | 8 / 12 |
| [Anaesthesiology](anaesthesia/SYLLABUS.md) | III | 11 | 51 | 29 | 7 / 9 |
| [Radiodiagnosis](radiology/SYLLABUS.md) | III | 7 | 21 | 0 | 8 / 9 |
| [Otorhinolaryngology (ENT)](ent/SYLLABUS.md) | III | 4 | 63 | 8 | 6 / 9 |
| [Ophthalmology](ophthalmology/SYLLABUS.md) | III | 10 | 59 | 14 | 8 / 13 |
| [Obstetrics & Gynaecology](obstetrics-gynaecology/SYLLABUS.md) | III | 38 | 142 | 26 | 10 / 26 |
| **Total** | | **401** | **2626** | **522** | **162 / 486** |

*Skill* = NMC gives the competency's domain as skill, attitude or communication only, with no knowledge component. These are hands-on items, unlikely to be asked as written MCQs. 5 competencies have no domain printed and are not tagged.

Order: pre-clinical (Phase 1), para-clinical (Phase 2), then the clinical subjects, as in the NMC volumes.

## Not in these lists

- **AETCOM** (attitude, ethics and communication) is a separate NMC course (the CBME guideline points to the AETCOM module on the NMC website), not part of the subject competency tables. Ethics and medical law are covered by Forensic Medicine topic 10.
- **Depth.** Competencies are written at topic level (Psychiatry has only 17, e.g. "Describe common psychosexual disorders"). NEET-PG asks details inside them, so each module needs its own sub-topic list, built from standard textbooks when the module is planned.
- **Recent guidelines and national programmes** (drug doses, schedules, programme targets) change between curriculum revisions. They are tested, but the source for each must be the current official guideline, checked when a module is written.
- **Subject weightage.** News reports say the current NBEMS bulletin gives no subject-wise question split (not yet checked against the bulletin itself). Per-subject numbers on coaching sites are estimates; none are used here.

## How this was built

Text extracted from the NMC PDF with `pdftotext -layout`, then parsed into topics and coded competencies. Checked against the PDF's own counts: topic counts match NMC's summary table for every subject except Paediatrics (see its notes); competency counts match or differ by codes that are missing from the PDF itself (noted per subject). A handful of rows the parser could not read were filled in by hand from the PDF text. The scripts are in `tools/syllabus/` (see its README to regenerate).
