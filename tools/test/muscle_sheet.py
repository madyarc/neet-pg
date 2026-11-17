"""Per-muscle check sheet: for each job (muscle, view dir, bones to hide) two shots framed on the muscle:
the muscle shown, and the bone alone with its attachment areas (blue origin, orange insertion).
usage: muscle_sheet.py manifest.json attachments.json out.png 'muscle:dx,dy,dz[:hide1+hide2]' ..."""
import os, sys, time, io, json, urllib.parse
import numpy as np
os.environ.update({'LIBGL_ALWAYS_SOFTWARE': '1', '__GLX_VENDOR_LIBRARY_NAME': 'mesa',
                   '__EGL_VENDOR_LIBRARY_FILENAMES': '/usr/share/glvnd/egl_vendor.d/50_mesa.json', 'MOZ_WEBRENDER': '0'})
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'zanat'))
from areas import decode
man_p, att_p, out = sys.argv[1:4]
root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
rel = lambda p: '../../' + os.path.relpath(os.path.abspath(p), root)
base = os.path.dirname(man_p); A = json.load(open(att_p))
jobs = []
for j in sys.argv[4:]:
    parts = j.split(':'); m = parts[0]; dv = parts[1] if len(parts) > 1 else '-1,0,0'; hide = parts[2].replace('+', ',') if len(parts) > 2 else ''
    P = decode(os.path.join(base, m + '.bin'))[0]
    for a in A.get(m, []):
        if a['verts']: P = np.vstack([P, decode(os.path.join(base, a['bone'] + '.bin'))[0][a['verts']]])
    box = np.concatenate([P.min(0) - 12, P.max(0) + 12])
    for show in (m, 'none'): jobs.append((m, show, dv, hide, box))
o = Options(); o.add_argument('-headless')
for k, v in {'gfx.webrender.software': True, 'layers.acceleration.disabled': True, 'webgl.force-enabled': True}.items(): o.set_preference(k, v)
d = webdriver.Firefox(options=o); shots = []
try:
    d.set_window_size(420, 460)
    for m, show, dv, hide, box in jobs:
        q = {'m': rel(man_p), 'areas': rel(att_p), 'show': show, 'focus': m, 'box': ','.join('%.1f' % x for x in box), 'dir': dv, 'zoom': 1}
        if hide: q['hide'] = hide
        d.get('http://localhost:8765/tools/test/muscle-dev.html?' + urllib.parse.urlencode(q))
        for _ in range(80):
            if d.execute_script('return window.ready'): break
            time.sleep(0.25)
        time.sleep(0.5)
        im = Image.open(io.BytesIO(d.get_screenshot_as_png())).convert('RGB'); im.thumbnail((400, 440))
        ImageDraw.Draw(im).text((6, 4), m + ('' if show == 'none' else ' (muscle)'), fill=(0, 0, 0)); shots.append(im)
finally:
    d.quit()
cols, W, H = 6, 400, 440
rows = (len(shots) + cols - 1) // cols
sheet = Image.new('RGB', (cols * W, rows * H), 'white')
for j, im in enumerate(shots): sheet.paste(im, ((j % cols) * W, (j // cols) * H))
sheet.save(out); print(out, len(shots))
