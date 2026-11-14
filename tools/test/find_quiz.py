import sys, os, asyncio
from playwright.async_api import async_playwright
async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg = await b.new_page(viewport={'width': 1200, 'height': 900})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://' + os.path.abspath(sys.argv[1]))
        await pg.click('#mode-find')
        ok = 0; tried = 0
        for _ in range(18):
            await pg.wait_for_timeout(700)
            # turn to face the target, then tap on its screen position (only if visible)
            pos = await pg.evaluate("""(() => { vE.face(lmDir(target), {zoom: 1.4, focus: GEO.L[target]}); return target; })()""")
            await pg.wait_for_timeout(700)
            xy = await pg.evaluate("""(() => { const q = vE.toCam(GEO.L[target]); const [x, y] = vE.toScreen(q);
                const r = vE.c.getBoundingClientRect(); return [r.left + x, r.top + y, target]; })()""")
            await pg.mouse.click(xy[0], xy[1])
            await pg.wait_for_timeout(200)
            v = await pg.inner_text('#find-verdict')
            tried += 1; ok += v.startswith('Yes')
            print(xy[2], '->', v[:70])
            await pg.click('#find-next')
        print('hits', ok, '/', tried, 'errors', errs)
        await b.close()
asyncio.run(run())
