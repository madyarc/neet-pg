"""Search index for the site: one entry per page with its title, subject, lede, section headings (with their ids, so a
result can open that section), 3D topic names, key terms (bold words in the text, table headers) and the names of the
3D parts it shows (bones only on bone pages, so a search for "clavicle" doesn't list every page with a glass skeleton).

usage: (git add the new pages first) python3 -I tools/home/search_index.py  ->  search-index.json at the repo root (read by assets/search.js)"""
import json, os, re, html, glob
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SUBJECTS = {'anatomy': 'Anatomy', 'ophthalmology': 'Ophthalmology', 'physiology': 'Physiology', 'biochemistry': 'Biochemistry', 'pathology': 'Pathology'}
BONES = set(json.load(open(os.path.join(ROOT, 'anatomy/models/bone-keys.json'))))
BONE_MODELS = {'skeleton', 'skull', 'skull-detail', 'spine', 'spine-detail', 'thorax', 'thorax-detail', 'upper-limb',
               'upper-limb-detail', 'lower-limb', 'lower-limb-detail'}
TAG = re.compile(r'<[^>]+>')
clean = lambda t: re.sub(r'\s+', ' ', html.unescape(TAG.sub('', t))).strip(' .,:;—-')


def part_names(src, path):
    """names of the parts in the models this page loads"""
    out = set()
    context = set() if path.startswith('anatomy/general/') else {'body-lymph', 'body-nerves', 'body-vessels', 'body-muscles', 'skeleton'}
    for m in set(re.findall(r"models/([a-z0-9-]+)/", src)) - context:   # whole-body layers are context on regional pages
        f = os.path.join(ROOT, 'anatomy/models', m, m + '.json')
        if not os.path.exists(f): continue
        for p in json.load(open(f))['parts']:
            if p['key'] in BONES and m not in BONE_MODELS: continue
            n = re.sub(r'^(Right|Left) ', '', p.get('name', '')).strip()
            n = re.sub(r'\.(r|l)$', '', n)
            if 2 < len(n) < 60: out.add(n[0].upper() + n[1:])
    return out


import subprocess
# only pages git knows about (committed or staged), so a page still being built is not listed
TRACKED = set(subprocess.run(['git', '-C', ROOT, 'ls-files', '--cached'], capture_output=True, text=True).stdout.split())
pages = []
for sub, subname in SUBJECTS.items():
    for f in sorted(glob.glob(os.path.join(ROOT, sub, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        if rel.endswith('index.html') or rel not in TRACKED: continue
        src = open(f, encoding='utf-8').read()
        src = re.sub(r'<!-- feedback -->.*?<!-- /feedback -->', '', src, flags=re.S)   # the site-wide report note is not page content
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', src, re.S)
        if not h1: continue
        lede = re.search(r'<p class="lede"[^>]*>(.*?)</p>', src, re.S)
        heads = [[clean(t), i] for i, t in re.findall(r'<h2[^>]*id="([^"]+)"[^>]*>(.*?)</h2>', src, re.S)]
        heads += [[clean(t), ''] for t in re.findall(r'<h2(?![^>]*id=)[^>]*>(.*?)</h2>', src, re.S)]
        topics = sorted({clean(t) for t in re.findall(r"\bname: *'([^']{3,70})'", src)})
        terms = {clean(t) for t in re.findall(r'<b>([^<]{3,50})</b>', src)}
        terms |= {clean(t) for t in re.findall(r'<th[^>]*>([^<]{3,50})</th>', src)}
        terms |= part_names(src, rel)
        ok = lambda t: 2 < len(t) < 60 and not t.isdigit() and not re.search(r"\$\{|' \+|\+ '|[{}<>]", t)
        terms = sorted(t for t in terms if ok(t))
        topics = [t for t in topics if ok(t)]
        pages.append({'t': clean(h1.group(1)), 'u': rel, 's': subname, 'd': clean(lede.group(1)) if lede else '',
                      'h': [h for h in heads if h[0]], 'k': topics, 'w': terms})
json.dump(pages, open(os.path.join(ROOT, 'search-index.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(pages), 'pages', os.path.getsize(os.path.join(ROOT, 'search-index.json')) // 1024, 'KB')
