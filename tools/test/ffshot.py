"""Headless Firefox screenshots with SOFTWARE rendering (no GPU: the AMD iGPU driver on this machine has faulted
under browser rendering). Prints the WebGL renderer so you can confirm it is llvmpipe/software.

usage: ffshot.py URL OUT.png [--w 1200 --h 900] [--phone] [--wait js-expr] [--js "script" ...]
  --phone   load the page in a 390 px iframe (headless Firefox ignores device pixel ratio tricks) and report
            any element wider than the viewport
  --wait    JS expression polled until truthy (default: document.readyState=='complete')"""
import os, sys, time, argparse, urllib.parse
os.environ['LIBGL_ALWAYS_SOFTWARE'] = '1'          # Mesa: llvmpipe instead of the GPU
os.environ['__GLX_VENDOR_LIBRARY_NAME'] = 'mesa'    # the NVIDIA driver ignores the line above: pick Mesa explicitly
os.environ['__EGL_VENDOR_LIBRARY_FILENAMES'] = '/usr/share/glvnd/egl_vendor.d/50_mesa.json'
os.environ['__NV_PRIME_RENDER_OFFLOAD'] = '0'
os.environ['MOZ_WEBRENDER'] = '0'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

ap = argparse.ArgumentParser()
ap.add_argument('url'); ap.add_argument('out')
ap.add_argument('--w', type=int, default=1200); ap.add_argument('--h', type=int, default=900)
ap.add_argument('--phone', action='store_true'); ap.add_argument('--wait', default="document.readyState=='complete'")
ap.add_argument('--js', action='append', default=[])
a = ap.parse_args()

o = Options(); o.add_argument('-headless')
for k, v in {'gfx.webrender.software': True, 'layers.acceleration.disabled': True, 'gfx.webrender.all': False,
             'media.hardware-video-decoding.enabled': False, 'webgl.force-enabled': True, 'webgl.sanitize-unmasked-renderer': False}.items():
    o.set_preference(k, v)
d = webdriver.Firefox(options=o)
try:
    rend = None
    if a.phone:
        d.set_window_size(600, 1000)
        html = f'<body style="margin:0"><iframe id="f" src="{a.url}" style="width:390px;height:4200px;border:0"></iframe></body>'
        d.get('data:text/html,' + urllib.parse.quote(html)); time.sleep(0.5)
        f = d.find_element(By.ID, 'f'); d.switch_to.frame(f)
    else:
        d.set_window_size(a.w, a.h); d.get(a.url)
    for _ in range(120):
        if d.execute_script('return !!(' + a.wait + ')'): break
        time.sleep(0.25)
    time.sleep(0.8)
    for s in a.js: d.execute_script(s); time.sleep(0.4)
    rend = d.execute_script("""try{const c=document.createElement('canvas').getContext('webgl');const e=c&&c.getExtension('WEBGL_debug_renderer_info');
        return c?(e?c.getParameter(e.UNMASKED_RENDERER_WEBGL):c.getParameter(c.RENDERER)):'no webgl'}catch(e){return String(e)}""")
    err = d.execute_script('return window.loadError || ""')
    if a.phone:
        h = d.execute_script('return document.documentElement.scrollHeight')
        sw = d.execute_script('return document.documentElement.scrollWidth'); cw = d.execute_script('return document.documentElement.clientWidth')
        wide = d.execute_script("""return [...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>document.documentElement.clientWidth+1).slice(0,5).map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().right))""")
        d.switch_to.default_content()
        d.execute_script(f"document.getElementById('f').style.height='{h}px'"); d.set_window_size(600, min(h + 120, 8000)); time.sleep(0.4)
        f.screenshot(a.out)
        print('scrollWidth', sw, 'clientWidth', cw, 'overflowing:', wide)
    else:
        d.save_screenshot(a.out)
    print('renderer:', rend, '| loadError:', err or 'none')
finally:
    d.quit()
