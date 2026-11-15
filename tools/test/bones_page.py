"""Screenshots of the bones-of-the-skull page for every bone (needs `python3 -m http.server 8765` in neet-pg).
Usage: bones_page.py <outdir> [bone ...]"""
import sys, os, asyncio
from playwright.async_api import async_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
BONES = sys.argv[2:] or ['frontal', 'parietal', 'occipital', 'temporal', 'sphenoid', 'ethmoid', 'nasal', 'maxilla', 'lacrimal', 'zygomatic', 'palatine', 'concha', 'vomer', 'mandible', 'hyoid']
async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        pg = await b.new_page(viewport={'width': 1280, 'height': 900})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None)
        await pg.goto('http://127.0.0.1:8765/anatomy/head-neck/skull-bones.html#' + BONES[0]); await pg.wait_for_function('window.ready || window.loadError', timeout=90000)
        print('loadError', await pg.evaluate('window.loadError || null'))
        for bone in BONES:
            await pg.evaluate(f'location.hash = "{bone}"'); await pg.wait_for_timeout(2500)
            await pg.locator('.split').first.screenshot(path=f'{out}/{bone}-lm.png')
            await pg.click('#tab-art'); await pg.wait_for_timeout(900)
            await pg.click('#ctx'); await pg.wait_for_timeout(900)
            await pg.locator('.split').first.screenshot(path=f'{out}/{bone}-art.png')
            await pg.click('#ctx'); await pg.click('#tab-lm'); await pg.wait_for_timeout(300)
            print(bone, 'ok')
        print('errors', errs)
        await b.close()
asyncio.run(run())
