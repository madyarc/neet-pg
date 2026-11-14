"""Screenshots of the skull page in each tab. Needs a local http server (fetch of model files).
Usage: skull_shots.py <url> <outdir>"""
import sys, os, asyncio
from playwright.async_api import async_playwright
url, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        for name, w, h, scheme in [('desk', 1280, 900, 'light'), ('phone', 400, 860, 'dark')]:
            pg = await b.new_page(viewport={'width': w, 'height': h}, color_scheme=scheme)
            errs = []; pg.on('pageerror', lambda e, errs=errs: errs.append(str(e))); pg.on('console', lambda m, errs=errs: errs.append(m.text) if m.type in ('error', 'warning') else None)
            await pg.goto(url); await pg.wait_for_function('window.ready || window.loadError', timeout=60000)
            print(name, 'loadError', await pg.evaluate('window.loadError || null'), 'scrollWidth', await pg.evaluate('document.documentElement.scrollWidth'))
            await pg.wait_for_timeout(900)
            async def shot(tag):
                await pg.wait_for_timeout(900)
                await pg.locator('.split').first.screenshot(path=f'{out}/{name}-{tag}.png')
            await shot('bones-front')
            await pg.click('#views .btn:nth-child(2)'); await shot('bones-left')
            await pg.click('#bone-list button[data-k="sphenoid"]'); await shot('bones-sphenoid')
            await pg.click('#tab-sutures'); await shot('sut-left')
            await pg.click('#pt-list button[data-k="pterion_r"]'); await shot('pt-pterion')
            await pg.click('#pt-list button[data-k="bregma"]'); await shot('pt-bregma')
            await pg.click('#sut-list button[data-k="lambdoid"]'); await shot('sut-lambdoid')
            await pg.click('#tab-inside'); await shot('inside')
            await pg.click('#fos-list button[data-k="middle"]'); await shot('inside-middle')
            print(name, 'errors', errs)
            await pg.close()
        await b.close()
asyncio.run(run())
