"""Add a "Report a problem" note after the footer of every page (idempotent: replaces an existing one).
The link opens the GitHub issue form .github/ISSUE_TEMPLATE/feedback.yml with the page title and live URL filled in.
usage: python3 -I tools/home/feedback_links.py [page.html ...]   (default: every tracked page except tools/, source/)"""
import html, os, re, subprocess, sys
from urllib.parse import quote
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
REPO, SITE = 'https://github.com/madyarc/neet-pg', 'https://madyarc.github.io/neet-pg/'
START, END = '<!-- feedback -->', '<!-- /feedback -->'
STYLE = ('margin:18px 0 0;padding:12px 14px;border:1px solid var(--line,#ccd);border-radius:10px;'
         'font-size:14px;line-height:1.5;color:var(--muted,#556)')

def block(rel, title):
    page = SITE + ('' if rel == 'index.html' else rel)
    url = (REPO + '/issues/new?template=feedback.yml&title=' + quote('[' + title + '] ', safe='')
           + '&page=' + quote(page, safe=''))
    return (f'{START}\n<p class="feedback" style="{STYLE}">Spotted a mistake, or something unclear? '
            f'<a href="{html.escape(url)}" target="_blank" rel="noopener"><b>Report it</b></a>: a short form on GitHub, '
            'with this page already filled in. No GitHub account? Sign up in a few seconds with your Google account. '
            'Signing in keeps out spam, and every report is checked against our sources, so your fix helps everyone. '
            "Reports are public: please don't include personal details.</p>\n" + END)

files = sys.argv[1:] or [f for f in subprocess.run(['git', '-C', ROOT, 'ls-files', '*.html'], capture_output=True,
                         text=True).stdout.split() if not f.startswith(('tools/', 'source/', 'practice/'))]
n = 0
for rel in files:
    p = os.path.join(ROOT, rel); s = open(p, encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S) or re.search(r'<title>(.*?)</title>', s, re.S)
    title = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))).strip() if m else rel
    s2 = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', s, flags=re.S)
    i = s2.find('</footer>')
    if i < 0: print('no footer:', rel); continue
    i += len('</footer>')
    s2 = s2[:i] + '\n' + block(rel, title) + s2[i:]
    if s2 != s: open(p, 'w', encoding='utf-8').write(s2); n += 1
print(n, 'pages updated')
