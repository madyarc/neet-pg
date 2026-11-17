"""Contact sheet of attachment areas: one shot per (muscle, bone) area, framed on the bone and viewed from the side
the area faces, using tools/test/muscle-dev.html (software rendering, like ffshot.py).
usage: attach_sheet.py manifest.json attachments.json out_prefix [muscle,muscle...]"""
import os, sys, time, io, json, struct, urllib.parse
import numpy as np
os.environ.update({'LIBGL_ALWAYS_SOFTWARE': '1', '__GLX_VENDOR_LIBRARY_NAME': 'mesa',
                   '__EGL_VENDOR_LIBRARY_FILENAMES': '/usr/share/glvnd/egl_vendor.d/50_mesa.json', 'MOZ_WEBRENDER': '0'})
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'zanat'))
from areas import decode
man_p, att_p, out = sys.argv[1:4]
only = sys.argv[4].split(',') if len(sys.argv) > 4 else None
A = json.load(open(att_p)); base = os.path.dirname(man_p)
root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
rel = lambda p: '../../' + os.path.relpath(os.path.abspath(p), root)
jobs = []
for m, lst in A.items():
    if only and m not in only: continue
    for a in lst:
        if not a['verts']: continue
        B = decode(os.path.join(base, a['bone'] + '.bin'))[0]
        dv = B[a['verts']].mean(0) - B.mean(0); dv[2] = 0          # look from the side the area faces, level
        n = np.linalg.norm(dv); dv = dv / n if n > 1e-6 else np.array([0, -1, 0]); dv[2] = 0.25
        h = B[:, 2].max() - B[:, 2].min()
        P = B[a['verts']]; pad = 25.0
        box = np.concatenate([P.min(0) - pad, P.max(0) + pad])
        jobs.append((m, a['bone'], a['kind'], dv, box))
o = Options(); o.add_argument('-headless')
for k, v in {'gfx.webrender.software': True, 'layers.acceleration.disabled': True, 'webgl.force-enabled': True}.items(): o.set_preference(k, v)
d = webdriver.Firefox(options=o); shots = []
try:
    d.set_window_size(420, 460)
    for m, b, kind, dv, box in jobs:
        q = urllib.parse.urlencode({'m': rel(man_p), 'areas': rel(att_p), 'show': 'none', 'focus': m, 'box': ','.join('%.1f' % x for x in box), 'dir': ','.join('%.3f' % x for x in dv), 'zoom': 1})
        d.get('http://localhost:8765/tools/test/muscle-dev.html?' + q)
        for _ in range(80):
            if d.execute_script('return window.ready'): break
            time.sleep(0.25)
        time.sleep(0.8)
        im = Image.open(io.BytesIO(d.get_screenshot_as_png())).convert('RGB'); im.thumbnail((400, 440))
        ImageDraw.Draw(im).text((6, 4), f'{m} / {b} ({kind})', fill=(0, 0, 0)); shots.append(im)
finally:
    d.quit()
cols, W, H = 6, 400, 440
for i in range(0, len(shots), 24):
    page = shots[i:i + 24]; rows = (len(page) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * W, rows * H), 'white')
    for j, im in enumerate(page): sheet.paste(im, ((j % cols) * W, (j // cols) * H))
    sheet.save(f'{out}-{i // 24}.png'); print(f'{out}-{i // 24}.png', len(page))
