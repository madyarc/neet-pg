"""Check the viewer's Bones on/off button on every 3D page (headless Firefox, software rendering).

usage: tools/capped ~/personal/buildenv/bin/python -I tools/test/bonescheck.py [--shots DIR] [page.html ...]
Prints, per page: whether the button shows, its text, loadError; with --shots, saves the viewer before and after
turning bones off (first page only, or every page given)."""
import os, sys, time, glob, argparse
os.environ['LIBGL_ALWAYS_SOFTWARE'] = '1'; os.environ['__GLX_VENDOR_LIBRARY_NAME'] = 'mesa'
os.environ['__EGL_VENDOR_LIBRARY_FILENAMES'] = '/usr/share/glvnd/egl_vendor.d/50_mesa.json'
os.environ['__NV_PRIME_RENDER_OFFLOAD'] = '0'; os.environ['MOZ_WEBRENDER'] = '0'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ap = argparse.ArgumentParser(); ap.add_argument('pages', nargs='*'); ap.add_argument('--shots')
a = ap.parse_args()
pages = a.pages or sorted(p[len(ROOT) + 1:] for p in glob.glob(ROOT + '/anatomy/**/*.html', recursive=True)
                          if 'viewer.js' in open(p).read())
o = Options(); o.add_argument('-headless')
for k, v in {'gfx.webrender.software': True, 'layers.acceleration.disabled': True, 'webgl.force-enabled': True}.items():
    o.set_preference(k, v)
d = webdriver.Firefox(options=o); d.set_window_size(1200, 900)
try:
    d.get('http://127.0.0.1:8765/index.html'); d.execute_script("localStorage.removeItem('neetpg-bones')")
    for i, pg in enumerate(pages):
        d.get('http://127.0.0.1:8765/' + pg)
        for _ in range(120):
            if d.execute_script("return document.readyState=='complete' && !document.querySelector('.viewer .loading')"): break
            time.sleep(0.25)
        time.sleep(1.5)
        st = d.execute_script("const b=document.querySelector('.bonesbtn');return b?[!b.hidden,b.textContent]:[null,'']")
        err = d.execute_script('return window.loadError || ""')
        print(f'{pg:55s} button={st[0]!s:5s} {st[1]:10s} loadError={err or "none"}')
        if a.shots and st[0] and (a.pages or i == 0):
            v = d.find_element(By.CSS_SELECTOR, '.viewer'); n = os.path.basename(pg)[:-5]
            v.screenshot(f'{a.shots}/{n}-on.png'); d.find_element(By.CSS_SELECTOR, '.bonesbtn').click(); time.sleep(0.8)
            v.screenshot(f'{a.shots}/{n}-off.png'); d.find_element(By.CSS_SELECTOR, '.bonesbtn').click(); time.sleep(0.3)
finally:
    d.quit()
