"""Hand patches for rows the layout parser can't read (checked against the PDF text)."""
import json
d = json.load(open('cbme.json'))
FIX = {
 'BC13.1': 'Describe oncogenesis, oncogenes & its activation with focus on p53 & apoptosis.',
 'BC14.2': 'Describe estimation of pH by pH meter or ABG analyser and interpretation of results with paper case scenarios.',
}
INSERT = {  # code: (insert before, description)
 'BC14.1': ('BC14.2', 'Describe commonly used laboratory apparatus equipments, good / safe laboratory practice, Biomedical hazards & waste management.'),
 'PA29.1': ('PA29.2', 'Describe the epidemiology, pathogenesis, etiology, pathology, screening, diagnosis and progression of carcinoma of the cervix'),
}
for s, ts in d.items():
    for t in ts:
        for it in t['items']:
            if it['code'] in FIX: it['desc'] = FIX[it['code']]
        for code, (before, desc) in INSERT.items():
            for k, it in enumerate(t['items']):
                if it['code'] == before and not any(x['code'] == code for x in t['items']):
                    t['items'].insert(k, {'code': code, 'desc': desc, 'domain': 'K'}); break
for s_, ts_ in d.items():
    for t_ in ts_:
        for it in t_['items']:
            if it['code'] == 'MI1.1': it['desc'] = it['desc'].replace('developments and K contributions', 'developments and contributions')
json.dump(d, open('cbme.json', 'w'), indent=1, ensure_ascii=False)
print(sum(len(t['items']) for ts in d.values() for t in ts))
