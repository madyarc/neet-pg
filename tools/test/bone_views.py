"""Landmark placing helper (needs `python3 -m http.server 8765` in neet-pg). Env MANIFEST=<url relative to
tools/test/> picks another model set (default: skull-detail); ZOOM / FOCUS for the views command.
  views <key> <outdir> [dir ...]       screenshots from standard (or given 'x,y,z') directions, with a pixel grid
  pick  <key> <json>                   json: [{"name", "dir":[x,y,z], "xy":[x,y], "zoom"?}] -> prints points (3D, body frame)
  check <key> <json-with-p> <outdir>   screenshots with markers at the given points from each one's dir
"""
import sys, os, json, asyncio
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw
BASE = 'http://127.0.0.1:8765/tools/test/bone-dev.html?b='
DIRS = {'ant': [0, -1, 0], 'post': [0, 1, 0], 'left': [1, 0, 0], 'right': [-1, 0, 0], 'sup': [0, -0.001, 1], 'inf': [0, -0.001, -1]}
def grid(path):
    im = Image.open(path).convert('RGB'); d = ImageDraw.Draw(im)
    for i in range(0, 800, 50):
        c = (255, 120, 120) if i % 100 == 0 else (255, 200, 200)
        d.line([(i, 0), (i, 799)], fill=c, width=1); d.line([(0, i), (799, i)], fill=c, width=1)
        if i % 100 == 0: d.text((i + 2, 2), str(i), fill=(200, 0, 0)); d.text((2, i + 2), str(i), fill=(200, 0, 0))
    im.save(path)
async def page(p, key):
    b = await p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    pg = await b.new_page(viewport={'width': 800, 'height': 800})
    pg.on('pageerror', lambda e: print('ERR', e))
    m = os.environ.get('MANIFEST')
    await pg.goto(BASE + key + (f'&m={m}' if m else '') + ('&fitall=1' if os.environ.get('FITALL') else '') + ('&colour=1' if os.environ.get('COLOUR') else '')); await pg.wait_for_function('window.ready', timeout=60000)
    return b, pg
def pdir(s): return DIRS[s] if s in DIRS else [float(x) for x in s.split(',')]
async def main():
    cmd, key = sys.argv[1], sys.argv[2]
    async with async_playwright() as p:
        b, pg = await page(p, key)
        if cmd == 'views':
            out = sys.argv[3]; os.makedirs(out, exist_ok=True)
            Z = float(os.environ.get('ZOOM', 1)); F = os.environ.get('FOCUS'); F = json.dumps([float(x) for x in F.split(',')]) if F else 'null'
            for name in (sys.argv[4:] or DIRS):
                await pg.evaluate(f'faceNow({json.dumps(pdir(name))}, {Z}, {F})'); await pg.wait_for_timeout(150)
                f = f'{out}/{key.split(",")[0]}-{name.replace(",", "_")}.png'
                await pg.locator('#v').screenshot(path=f); grid(f)
                ax = await pg.evaluate('''(() => { const c = v.centre, o = v.toScreen(v.toCam(c)), r = {};
                  for (const [n, d] of [['ant', [0, -1, 0]], ['sup', [0, 0, 1]], ['left', [1, 0, 0]]]) {
                    const s = v.toScreen(v.toCam(c.map((x, i) => x + d[i] * 10))); r[n] = [Math.round(s[0] - o[0]), Math.round(s[1] - o[1])]; }
                  return r; })()''')
                print(f, 'screen offset of 10 mm toward', ax)
        elif cmd == 'pick':
            items = json.load(open(sys.argv[3])); res = []
            for it in items:
                if 'rims' in it:    # centre of a hole: mean of surface points picked on its rim
                    await pg.evaluate(f'faceNow({json.dumps(pdir(it["dir"]))}, {it.get("zoom", 1)}, {json.dumps(it.get("focus"))})')
                    ps = [await pg.evaluate(f'pickAt({x}, {y})') for x, y in it['rims']]
                    ps = [h['p'] for h in ps if h]
                    it['p'] = [round(sum(q[i] for q in ps) / len(ps), 2) for i in range(3)] if len(ps) >= 2 else None
                    res.append(it); print(it['name'], 'hole', len(ps), it['p']); continue
                if 'xy' not in it and 'aim' not in it: res.append(it); print(it['name'], 'fixed', it.get('p')); continue   # point given directly (e.g. centre of a hole)
                await pg.evaluate(f'faceNow({json.dumps(pdir(it["dir"]) if isinstance(it["dir"], str) else it["dir"])}, {it.get("zoom", 1)}, {json.dumps(it.get("focus"))})')
                if it.get('aim'):   # aim at a 3D point: project it, then pick the surface seen there
                    it['xy'] = await pg.evaluate(f'v.toScreen(v.toCam({json.dumps(it["aim"])})).map(Math.round)')
                h = await pg.evaluate(f'pickAt({it["xy"][0]}, {it["xy"][1]})')
                it['p'] = [round(x, 2) for x in h['p']] if h else None; it['hit'] = h and h['key']; res.append(it)
                print(it['name'], it['hit'], it['p'])
            json.dump(res, open(sys.argv[3], 'w'), indent=1)
        elif cmd == 'check':
            items = json.load(open(sys.argv[3])); out = sys.argv[4]; os.makedirs(out, exist_ok=True)
            for i, it in enumerate(items):
                d = pdir(it['dir']) if isinstance(it['dir'], str) else it['dir']
                await pg.evaluate(f'v.markers = [{{p: {json.dumps(it["p"])}, label: {json.dumps(it["name"])}, big: true}}]; faceNow({json.dumps(d)}, {it.get("zoom", 1)}); v.drawMarkers(v.offscreen(2))')
                await pg.wait_for_timeout(100)
                f = f'{out}/check-{i:02d}.png'; await pg.locator('#v').screenshot(path=f); print(f, it['name'])
        elif cmd == 'all':      # all points of a json as labelled markers, from the given views
            items = json.load(open(sys.argv[3])); out = sys.argv[4]; os.makedirs(out, exist_ok=True)
            mk = [{'p': it['p'], 'label': it['name'], 'always': False} for it in items if it.get('p')]
            for name in sys.argv[5:] or DIRS:
                await pg.evaluate(f'v.markers = {json.dumps(mk)}; faceNow({json.dumps(pdir(name))}); v.drawMarkers(v.offscreen(2))')
                await pg.wait_for_timeout(100)
                f = f'{out}/all-{key.split(",")[0]}-{name.replace(",", "_")}.png'; await pg.locator('#v').screenshot(path=f); print(f)
        await b.close()
asyncio.run(main())
