import sys, os, asyncio, json
from playwright.async_api import async_playwright
async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg = await b.new_page()
        await pg.goto('file://' + os.path.abspath(sys.argv[1]))
        r = await pg.evaluate(sys.argv[2])
        print(json.dumps(r)[:3000])
        await b.close()
asyncio.run(run())
