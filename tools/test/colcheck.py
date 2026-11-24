# Site-wide colour check: compares tokens with atlas.css (incl. --n-*) and with every token on every other page/asset of every subject (pass your own files with --skip).
"""Colour check for the module 40 histology pages, both themes. CIE76 distance of each candidate to atlas.css meaning
colours (want >= 20), to every other anatomy page token outside the pages named with --skip (want >= 12), and between the
candidates themselves (want >= 20). usage: colcheck3.py repo [--skip a.html,b.html] name=#light/#dark ..."""
import sys, re, glob, os
def lab(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + .055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    X = (r*.4124 + g*.3576 + b*.1805) / .95047; Y = r*.2126 + g*.7152 + b*.0722; Z = (r*.0193 + g*.1192 + b*.9505) / 1.08883
    t = lambda v: v ** (1/3) if v > 0.008856 else 7.787 * v + 16/116
    return 116*t(Y) - 16, 500*(t(X) - t(Y)), 200*(t(Y) - t(Z))
def d(a, b): return sum((x - y) ** 2 for x, y in zip(lab(a), lab(b))) ** .5
def tokens(text):
    """returns (light, dark) dicts name->hex from :root{...} and :root[data-theme="dark"]{...} blocks"""
    li, dk = {}, {}
    for m in re.finditer(r':root(\[data-theme="dark"\])?\s*\{([^}]*)\}', text):
        tgt = dk if m.group(1) else li
        for n, c in re.findall(r'(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})', m.group(2)): tgt.setdefault(n, c.lower())
    return li, dk
args = sys.argv[1:]; root = args.pop(0); skip = []
if args and args[0] == '--skip': args.pop(0); skip = args.pop(0).split(',')
A = tokens(open(os.path.join(root, 'anatomy/assets/atlas.css')).read())
atlas = [{c: n for n, c in t.items() if not n.startswith('--n-') or n in ('--n-phrenic', '--n-facial')} for t in A]
NALL = [{c: n for n, c in t.items() if n.startswith('--n-')} for t in A]
other = [{}, {}]
for f in [g for g in glob.glob(os.path.join(root, '*/*/*.html')) + glob.glob(os.path.join(root, '*/*/*.css')) + glob.glob(os.path.join(root, '*/assets/*.css')) if '/sources-local/' not in g and '/tools/' not in g]:
    if os.path.basename(f) in skip: continue
    for i, t in enumerate(tokens(open(f, errors='replace').read())):
        for n, c in t.items(): other[i].setdefault(c, n + '@' + os.path.basename(f))
mine = {}
for a in args:
    n, v = a.split('='); l, k = v.split('/'); mine[n] = (l.lower(), k.lower())
for n, cs in mine.items():
    for i, th in enumerate(('light', 'dark')):
        c = cs[i]
        a = min((d(c, h), v) for h, v in atlas[i].items()); o = min(((d(c, h), v) for h, v in other[i].items() if v.split('@')[0] != n), default=(99, '-'))
        p = min(((d(c, c2[i]), n2) for n2, c2 in mine.items() if n2 != n), default=(99, '-'))
        flag = '' if a[0] >= 20 and o[0] >= 12 and p[0] >= 20 else '  <<'
        print('%-12s %-5s %s atlas %4.1f %-10s other %4.1f %-30s mine %4.1f %-10s%s' % (n, th, c, a[0], a[1], o[0], o[1][:30], p[0], p[1], flag))
print('-- nearest --n-* nerve token (by hand check; nerves of one limb only)')
for n, cs in mine.items():
    for i, th in enumerate(('light', 'dark')):
        c = cs[i]; a = min((d(c, h), v) for h, v in NALL[i].items()); print('%-10s %-5s %s nearest %4.1f %s' % (n, th, c, a[0], a[1]))
