"""Parse the NMC CBME 2024 competency tables (pdftotext -layout output) into
per-subject topic -> competency lists. Usage: python3 -I parse_cbme.py cbme.txt outdir"""
import re, sys, json, collections

SUBJ = {
    'AN': 'Anatomy', 'PY': 'Physiology', 'BC': 'Biochemistry', 'PH': 'Pharmacology',
    'PA': 'Pathology', 'MI': 'Microbiology', 'FM': 'Forensic Medicine & Toxicology',
    'CM': 'Community Medicine (PSM)', 'GM': 'General Medicine', 'IM': 'General Medicine',
    'PE': 'Paediatrics', 'PS': 'Psychiatry', 'DR': 'Dermatology, Venereology & Leprosy',
    'SU': 'General Surgery', 'OP': 'Ophthalmology', 'EN': 'Otorhinolaryngology (ENT)',
    'OR': 'Orthopaedics', 'AS': 'Anaesthesiology', 'RD': 'Radiodiagnosis',
    'OG': 'Obstetrics & Gynaecology',
}
CODE = re.compile(r'^(\s*)([A-Z]{2})\s?(\d{1,2})\s?\.\s?(\d{1,2})\*?(?:\s+(\S.*))?\s*$')
TOPIC = re.compile(r'^\s*Topic\s*:?\s*(\d+)\s*[:.\-–]?\s*(.*?)(?:\s{2,}Number of.*)?$', re.I)
DOMAIN_ONLY = re.compile(r'^(K|S|A|C|P|SH|KH|Y|N|K/S|K,S|S/K)$')
VERB = re.compile(r'^(Describe|Discuss|Enumerate|Perform|Identify|Demonstrate|Explain|Define|Classify|Elicit|Counsel|Interpret|Choose|Calculate|List|Observe|Assist|Distinguish|Recognise|Recognize|Plan|Prescribe|Administer|Select|Outline|Compare|Correlate|Estimate|Analyse|Analyze|Provide|Educate|Diagnose|Order|Assess|Communicate|Apply|Understand|Know|Obtain|Conduct|Measure|Elaborate|Detect|Narrate|Mention|Write|Summarize|Summarise|Participate|Formulate|Develop|Use|Take|Show|Display|Prepare|Maintain|Visit|Collect|Document|Present|Enlist|Name|State|Differentiate|Draw|Label|Locate|Palpate|Teach|Recall|Interpret|Evaluate|Monitor|Manage|Promote|Advise|Set|Insert|Record|Examine|Recognise|Integrate|Justify|Critically|Briefly)\b')
DOMAIN = re.compile(r'\s{2,}(K|S|A|C|K\s?/\s?S|K,\s?S|S\s?/\s?K|K/S/A|K,S,A|A/C)\s{2,}.*$')

lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
start = next(i for i, l in enumerate(lines) if re.match(r'^\s*AN1\.1\b', l)) - 3

subjects = collections.OrderedDict()   # prefix -> list of topics
pending_topic = None
cur = None          # current competency dict
desc_col = None

def first_chunk(s):
    s = DOMAIN.sub('', s)
    return re.split(r'\s{3,}', s.strip())[0]

for l in lines[start:]:
    um = re.match(r'^\s*Topic\s*:\s*([A-Za-z].*?)\s*-?\s*Number of', l)
    if um:
        pending_topic = (None, um.group(1).strip()); cur = None; continue
    m = TOPIC.match(l)
    if m and 'competenc' in l.lower() or (m and len(l.strip()) < 120 and l.strip().lower().startswith('topic')):
        name = m.group(2).strip().rstrip('-–: ')
        pending_topic = (int(m.group(1)), name)
        cur = None
        continue
    m = CODE.match(l)
    if m and m.group(2) in SUBJ:
        pre = m.group(2)
        code = f'{pre}{int(m.group(3))}.{int(m.group(4))}'
        topics = subjects.setdefault(pre, [])
        if pending_topic is not None:
            topics.append({'num': pending_topic[0], 'name': pending_topic[1], 'items': []})
            pending_topic = None
        if not topics:
            topics.append({'num': 0, 'name': '(untitled)', 'items': []})
        fc = first_chunk(m.group(5) or '')
        cur = {'code': code, 'frags': [fc] if fc and not DOMAIN_ONLY.match(fc) else []}
        dom = None
        for tok in re.split(r'\s{2,}', (m.group(5) or '').strip()):
            tok = tok.replace(' ', '').upper()
            if re.fullmatch(r'[KSAC](?:[/,][KSAC])*', tok): dom = tok.replace(',', '/'); break
        cur['domain'] = dom
        topics[-1]['items'].append(cur)
        desc_col = l.index(m.group(5)) if m.group(5) and fc and not DOMAIN_ONLY.match(fc) else desc_col
        continue
    if cur is not None and l.strip():
        lead = len(l) - len(l.lstrip())
        if desc_col is not None and abs(lead - desc_col) <= 4:
            frag = first_chunk(l)
            if frag and not re.match(r'^(Page|\d+$|COMPETENCY|Number of)', frag):
                cur['frags'].append(frag)

STRAY = re.compile(r'^(The student should be able to|Number|COMPETENCY|Predominant|Level|Domain|K/S/A/C|H/P)$')
for pre, topics in subjects.items():
    items = [i for t in topics for i in t['items']]
    for k, it in enumerate(items):
        it['frags'] = [f for f in it['frags'] if not STRAY.match(f)]
    for k, it in enumerate(items):
        bad = not it['frags'] or not VERB.match(it['frags'][0])
        if bad and k > 0:
            prev = items[k-1]['frags']
            for j in range(len(prev)-1, 0, -1):
                if VERB.match(prev[j]):
                    it['frags'] = prev[j:] + it['frags']; del prev[j:]; break
    for it in items:
        it['desc'] = re.sub(r'\s*The student should be able to\s*', ' ', ' '.join(it.pop('frags'))).strip()
    # drop sample-table strays and exact duplicate codes
    for t in topics:
        seen = set(); keep = []
        for it in t['items']:
            if it['code'].startswith('IM') or it['code'] in seen: continue
            seen.add(it['code']); keep.append(it)
        t['items'] = keep
allcodes = set()
for pre, topics in subjects.items():
    for t in topics:
        t['items'] = [i for i in t['items'] if not (i['code'] in allcodes or allcodes.add(i['code']))]

# regroup by chapter number of the code (NMC topic N == competency chapter N)
for pre, topics in list(subjects.items()):
    names = {}
    for t in topics:
        if t['items']:
            ch = int(re.match(r'[A-Z]+(\d+)', t['items'][0]['code'])[1])
            if t['num'] == ch or t['num'] is None: names.setdefault(ch, t['name'])
        if t['num'] is not None: names.setdefault(t['num'], t['name'])
    groups = collections.OrderedDict()
    for t in topics:
        for it in t['items']:
            ch = int(re.match(r'[A-Z]+(\d+)', it['code'])[1])
            groups.setdefault(ch, []).append(it)
    subjects[pre] = [{'num': ch, 'name': names.get(ch, '(no topic header in the NMC PDF)'), 'items': its}
                     for ch, its in sorted(groups.items())]

out = {}
for pre, topics in subjects.items():
    out.setdefault(SUBJ[pre], []).extend(topics)
json.dump(out, open(sys.argv[2] + '/cbme.json', 'w'), indent=1, ensure_ascii=False)
for s, t in out.items():
    print(f'{s:40s} topics {len(t):3d}  competencies {sum(len(x["items"]) for x in t):4d}')
