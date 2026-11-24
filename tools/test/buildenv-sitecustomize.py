"""NEET-PG project guard (loaded automatically by every ~/personal/buildenv Python, including with -I).

Any script that starts Firefox through selenium:
  1. waits for a machine-wide lock, so only ONE test browser runs at a time (other agents queue; no parallel browsers);
  2. is forced onto software rendering (Mesa llvmpipe, no WebRender/GPU): the AMD GPU driver faulted under browser
     rendering on this machine.
The lock is held until driver.quit() or the end of the process. The user's own Firefox is not affected.
"""
import importlib.abc, importlib.util, os, sys

_LOCK = os.path.join(os.environ.get('XDG_RUNTIME_DIR') or '/tmp', 'neet-pg-browser.lock')
_SOFT_ENV = {'LIBGL_ALWAYS_SOFTWARE': '1', '__GLX_VENDOR_LIBRARY_NAME': 'mesa',
             '__EGL_VENDOR_LIBRARY_FILENAMES': '/usr/share/glvnd/egl_vendor.d/50_mesa.json',
             '__NV_PRIME_RENDER_OFFLOAD': '0', 'MOZ_WEBRENDER': '0'}
_SOFT_PREFS = {'gfx.webrender.software': True, 'layers.acceleration.disabled': True, 'gfx.webrender.all': False,
               'media.hardware-video-decoding.enabled': False}


def _patch(mod):
    import fcntl
    WD = mod.WebDriver
    if getattr(WD, '_neetpg_guard', False):
        return
    orig_init, orig_quit = WD.__init__, WD.quit

    def __init__(self, *a, **k):
        fd = os.open(_LOCK, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('[neet-pg] another test browser is running; waiting for it to finish…', file=sys.stderr, flush=True)
            fcntl.flock(fd, fcntl.LOCK_EX)
        os.environ.update(_SOFT_ENV)
        opts = k.get('options')
        if opts is None:
            from selenium.webdriver.firefox.options import Options
            opts = k['options'] = Options()
        for p, v in _SOFT_PREFS.items():
            opts.set_preference(p, v)
        self._neetpg_lock = fd
        try:
            orig_init(self, *a, **k)
        except BaseException:
            os.close(fd); self._neetpg_lock = None
            raise

    def quit(self):
        try:
            orig_quit(self)
        finally:
            fd = getattr(self, '_neetpg_lock', None)
            if fd is not None:
                self._neetpg_lock = None
                os.close(fd)          # releases the lock (it is also released when the process exits)

    WD.__init__, WD.quit, WD._neetpg_guard = __init__, quit, True


class _Finder(importlib.abc.MetaPathFinder):
    TARGET = 'selenium.webdriver.firefox.webdriver'

    def find_spec(self, name, path, target=None):
        if name != self.TARGET:
            return None
        sys.meta_path.remove(self)
        try:
            spec = importlib.util.find_spec(name)
        finally:
            sys.meta_path.insert(0, self)
        if spec is None or spec.loader is None:
            return spec
        exec_module = spec.loader.exec_module

        def exec_and_patch(module):
            exec_module(module)
            _patch(module)
        spec.loader.exec_module = exec_and_patch
        return spec


sys.meta_path.insert(0, _Finder())
