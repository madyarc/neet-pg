"""Write neet-pg/<subject>/SYLLABUS.md + root SYLLABUS.md from cbme.json and the hub outline.
Usage: python3 -I write_syllabus.py cbme.json hub-sections.txt <neet-pg dir>"""
import json, re, sys, os, collections

d = json.load(open(sys.argv[1]))
hub_txt = open(sys.argv[2]).read()
root = sys.argv[3]

# (NMC subject name, folder, display name, NMC volume, hub subject number)
SUBJECTS = [
    ('Anatomy', 'anatomy', 'Anatomy', 'I', 9),
    ('Physiology', 'physiology', 'Physiology', 'I', 10),
    ('Biochemistry', 'biochemistry', 'Biochemistry', 'I', 11),
    ('Pathology', 'pathology', 'Pathology', 'I', 3),
    ('Pharmacology', 'pharmacology', 'Pharmacology', 'I', 2),
    ('Microbiology', 'microbiology', 'Microbiology', 'I', 5),
    ('Forensic Medicine & Toxicology', 'forensic-medicine', 'Forensic Medicine & Toxicology', 'I', 12),
    ('Community Medicine (PSM)', 'community-medicine', 'Community Medicine (PSM)', 'II', 4),
    ('General Medicine', 'medicine', 'General Medicine', 'II', 1),
    ('Paediatrics', 'paediatrics', 'Paediatrics', 'II', 8),
    ('Psychiatry', 'psychiatry', 'Psychiatry', 'II', 19),
    ('Dermatology, Venereology & Leprosy', 'dermatology', 'Dermatology, Venereology & Leprosy', 'II', 18),
    ('General Surgery', 'surgery', 'General Surgery', 'III', 7),
    ('Orthopaedics', 'orthopaedics', 'Orthopaedics', 'III', 15),
    ('Anaesthesiology', 'anaesthesia', 'Anaesthesiology', 'III', 16),
    ('Radiodiagnosis', 'radiology', 'Radiodiagnosis', 'III', 17),
    ('Otorhinolaryngology (ENT)', 'ent', 'Otorhinolaryngology (ENT)', 'III', 13),
    ('Ophthalmology', 'ophthalmology', 'Ophthalmology', 'III', 14),
    ('Obstetrics & Gynaecology', 'obstetrics-gynaecology', 'Obstetrics & Gynaecology', 'III', 6),
]
INFERRED = {('General Surgery', 24): 'Pancreas', ('General Surgery', 27): 'Vascular & lymphatic diseases'}
SOURCE_NOTES = {
    'General Surgery': 'SU26.2 is not in the PDF (numbering gap in the source). Topics 24 and 27 have no header in the PDF; their names here are inferred from the competencies and marked *(name inferred)*.',
    'Orthopaedics': 'OR2.9 is not in the PDF (numbering gap in the source).',
    'Anaesthesiology': 'AS5.4 is not in the PDF (numbering gap in the source).',
    'Paediatrics': "NMC's summary table says 35 topics / 406 competencies, but the chapter itself has 32 topics and 253 competencies (its own topic headers add up to this, reading the typo \"(050\" in topic 21 as 5). Topic 24 (Pediatric Emergencies) is printed \"Topic: 24\".",
    'Microbiology': "NMC's summary table says 74 competencies; the chapter has 73.",
    'General Medicine': "Coded GM in the 2024 curriculum (IM in the 2019 one). GM9.8, GM14.1 and GM14.2 are printed twice in the PDF; listed once here. GM8.9 is not in the PDF.",
    'Biochemistry': 'BC14.1 is printed without its prefix ("14.1") in the PDF; restored here.',
    'Pathology': 'PA29.1 is printed "PA.29.1" in the PDF; restored here.',
    'Forensic Medicine & Toxicology': 'FM2.12 is not in the PDF (numbering gap in the source).',
    'Pharmacology': '',
}
# Rule of thumb, not NMC's own classification: competencies whose verb is a hands-on
# skill are less likely to be asked as MCQs. Tagged so the build can prioritise.
SKILL = re.compile(r'^(Demonstrate|Perform|Counsel|Elicit|Obtain|Participate|Communicate|Document|Assist|Observe|Administer|Insert|Palpate|Examine|Take|Prepare|Record|Collect|Visit|Teach|Educate|Advise|Set up|Display|Present|Conduct)\b', re.I)

def is_skill(i):
    dm = i.get('domain')
    return bool(dm) and 'K' not in dm

# hub outline per subject number
hub = {}
cur = None
for line in hub_txt.split('\n'):
    m = re.match(r'^# > Subject (\d+)', line)
    if m: cur = int(m.group(1)); hub[cur] = []; continue
    if cur is None or not line.strip(): continue
    if line.startswith('## '):
        hub[cur].append([re.sub(r'^\d+\s+', '', re.sub(r'\s+(General Medicine|Pharmacology|Pathology|PSM \(Community Medicine\)|Microbiology|Obstetrics & Gynaecology|Surgery|Paediatrics|Anatomy|Physiology|Biochemistry|Forensic Medicine|ENT|Ophthalmology|Orthopaedics|Anaesthesia|Radiology|Dermatology|Psychiatry)$', '', line[3:])), []])
    elif line.startswith('- '):
        hub[cur][-1][1].append(re.sub(r'^\d+\s+', '', line[2:]))

def clean(s):
    s = re.sub(r'\s+', ' ', s).strip().rstrip(',;')
    s = re.sub(r'\s+([,.;:])', r'\1', s)
    return s

SRC = ('NMC, *Competency Based Medical Education Curriculum 2024* (revised guidelines, '
       'notice D-11011/500/2024-AcademicCell, 12 Sept 2024), Volume')

index_rows = []
for nmc, folder, name, vol, hubno in SUBJECTS:
    topics = d[nmc]
    n_comp = sum(len(t['items']) for t in topics)
    n_skill = sum(1 for t in topics for i in t['items'] if is_skill(i))
    hubch = hub.get(hubno, [])
    hub_secs = sum(len(c[1]) for c in hubch)
    out = [f'# {name} — syllabus checklist', '',
           f'Source: {SRC} {vol}. Every topic and competency below is from that document, with its NMC code. '
           f'NEET-PG has no syllabus of its own: NBEMS says questions come from the MBBS curriculum, which is this document.', '',
           f'**{len(topics)} topics · {n_comp} competencies** ({n_skill} tagged *skill*).', '',
           '- `[ ]` not covered yet · `[~]` partly covered · `[x]` covered — add the module name after the code when ticking.',
           '- *skill* = NMC lists the competency\'s domain as skill, attitude or communication only (no **K**nowledge). '
           'These are hands-on items, unlikely to be asked as written MCQs, though the knowledge behind them may be.',
           '- Wording is NMC\'s, lightly cleaned (line breaks and spacing from the PDF).', '']
    note = SOURCE_NOTES.get(nmc)
    if note: out += [f'Source notes: {note}', '']
    out += ['## Topics', '']
    for t in topics:
        tname = INFERRED.get((nmc, t['num']))
        title = f'{tname} *(name inferred)*' if tname else clean(re.sub(r'\s*Number\s*of\s*[Cc]ompeten.*$', '', t['name'])).rstrip(' -–:')
        out.append(f'### {t["num"]}. {title}')
        out.append('')
        for i in t['items']:
            tag = ' *(skill)*' if is_skill(i) else ''
            out.append(f'- [ ] **{i["code"]}** {clean(i["desc"])}{tag}')
        out.append('')
    out += ['## Existing material: Revision Hub', '',
            f'`source/NEET-PG-2026_Revision-Hub.html` covers this subject in {len(hubch)} chapters / {hub_secs} sections. '
            'Not yet mapped to the topics above.', '']
    for k, (ch, secs) in enumerate(hubch, 1):
        out.append(f'{k}. **{ch}** — ' + '; '.join(secs))
    out.append('')
    os.makedirs(os.path.join(root, folder), exist_ok=True)
    open(os.path.join(root, folder, 'SYLLABUS.md'), 'w').write('\n'.join(out))
    index_rows.append((name, folder, vol, len(topics), n_comp, n_skill, len(hubch), hub_secs))

tot = [sum(r[i] for r in index_rows) for i in (3, 4, 5, 6, 7)]
idx = ['# NEET-PG — complete topic list', '',
       'NEET-PG has no separate syllabus. NBEMS says the questions come from the MBBS curriculum, which is the NMC '
       '*Competency Based Medical Education Curriculum 2024* (revised guidelines, 12 Sept 2024). Each subject\'s '
       '`SYLLABUS.md` lists every NMC topic and competency for that subject, with its code, as a checklist.', '',
       '| Subject | NMC vol. | Topics | Competencies | of which *skill* | Revision Hub chapters / sections |',
       '|---|---|---:|---:|---:|---:|']
for name, folder, vol, nt, nc, ns, hc, hs in index_rows:
    idx.append(f'| [{name}]({folder}/SYLLABUS.md) | {vol} | {nt} | {nc} | {ns} | {hc} / {hs} |')
idx.append(f'| **Total** | | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | **{tot[3]} / {tot[4]}** |')
idx += ['', '*Skill* = NMC gives the competency\'s domain as skill, attitude or communication only, with no knowledge component. '
        'These are hands-on items, unlikely to be asked as written MCQs. 5 competencies have no domain printed and are not tagged.', '',
        'Order: pre-clinical (Phase 1), para-clinical (Phase 2), then the clinical subjects, as in the NMC volumes.', '',
        '## Not in these lists', '',
        '- **AETCOM** (attitude, ethics and communication) is a separate NMC course (the CBME guideline points to the AETCOM module on the NMC website), '
        'not part of the subject competency tables. '
        'Ethics and medical law are covered by Forensic Medicine topic 10.',
        '- **Depth.** Competencies are written at topic level (Psychiatry has only 17, e.g. "Describe common psychosexual disorders"). '
        'NEET-PG asks details inside them, so each module needs its own sub-topic list, built from standard textbooks when the module is planned.',
        '- **Recent guidelines and national programmes** (drug doses, schedules, programme targets) change between curriculum '
        'revisions. They are tested, but the source for each must be the current official guideline, checked when a module is written.',
        '- **Subject weightage.** News reports say the current NBEMS bulletin gives no subject-wise question split (not yet checked '
        'against the bulletin itself). Per-subject numbers on coaching sites are estimates; none are used here.', '',
        '## How this was built', '',
        'Text extracted from the NMC PDF with `pdftotext -layout`, then parsed into topics and coded competencies. Checked against '
        'the PDF\'s own counts: topic counts match NMC\'s summary table for every subject except Paediatrics (see its notes); '
        'competency counts match or differ by codes that are missing from the PDF itself (noted per subject). '
        'A handful of rows the parser could not read were filled in by hand from the PDF text. '
        'The scripts are in `tools/syllabus/` (see its README to regenerate).', '']
open(os.path.join(root, 'SYLLABUS.md'), 'w').write('\n'.join(idx))
print('\n'.join(idx[4:26]))
