"""Screenshot checks for a page. Usage: shot.py <html> <outdir> [actions...]"""
import sys, os, asyncio
from playwright.async_api import async_playwright

page_path, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        for name, w, h, scheme in [('desk-light', 1200, 900, 'light'), ('phone-dark', 400, 860, 'dark')]:
            ctx = await b.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme, device_scale_factor=1)
            pg = await ctx.new_page()
            errs = []
            pg.on('console', lambda m, errs=errs: errs.append(f'{m.type}: {m.text}') if m.type in ('error', 'warning') else None)
            pg.on('pageerror', lambda e, errs=errs: errs.append(f'pageerror: {e}'))
            await pg.goto('file://' + os.path.abspath(page_path))
            await pg.wait_for_timeout(800)
            gl = await pg.evaluate("!!document.createElement('canvas').getContext('webgl')")
            print(name, 'webgl', gl, 'errors', errs)
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            print(name, 'scrollWidth', sw, 'viewport', w)
            await pg.screenshot(path=f'{outdir}/{name}-top.png')
            # explore: pick a landmark
            await pg.click('#lm-chips .chip[data-k="lesser_trochanter"]')
            await pg.wait_for_timeout(900)
            await pg.locator('#h-explore').scroll_into_view_if_needed()
            await pg.screenshot(path=f'{outdir}/{name}-explore-lt.png')
            await pg.click('#lm-chips .chip[data-k="intercondylar_fossa"]')
            await pg.wait_for_timeout(900)
            await pg.screenshot(path=f'{outdir}/{name}-explore-fossa.png')
            # side
            await pg.locator('#h-side').scroll_into_view_if_needed()
            await pg.click('#side-back')
            await pg.wait_for_timeout(900)
            await pg.locator('#h-side').scroll_into_view_if_needed()
            await pg.screenshot(path=f'{outdir}/{name}-side.png')
            # attachments: each group
            for gi in range(7):
                await pg.locator('#att-groups .chip').nth(gi).click()
                await pg.wait_for_timeout(800)
                if True:
                    await pg.locator('#h-att').scroll_into_view_if_needed()
                    await pg.screenshot(path=f'{outdir}/{name}-att{gi}.png')
            await pg.locator('#att-legend button').nth(0).click()
            await pg.wait_for_timeout(900)
            await pg.locator('#h-att').scroll_into_view_if_needed()
            await pg.screenshot(path=f'{outdir}/{name}-att-clinical.png')
            # ossification
            for k in (0, 2, 5, 9):
                await pg.evaluate(f"(()=>{{const s=document.getElementById('oss-slider');s.value={k};s.oninput();}})()")
                await pg.wait_for_timeout(200)
                await pg.locator('#h-oss').scroll_into_view_if_needed()
                await pg.screenshot(path=f'{outdir}/{name}-oss{k}.png')
            print(name, 'errors after actions', errs)
            await ctx.close()
        await b.close()
asyncio.run(run())
