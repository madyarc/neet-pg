/* NEET-PG anatomy viewer — shared by the skull, whole-body and bone pages.
 *
 * Loads parts built by tools/bones-rs ("NPM1" binaries + a manifest) and draws them in the BodyParts3D
 * body frame (mm; +x = body's left, +y = posterior, +z = up). Plain WebGL 1, no library.
 *
 *   const v = new AtlasViewer(hostElement, {background: false});
 *   await v.load('../models/skull/skull.json');           // manifest written by `bones build`
 *   v.setColour('frontal', '#c9a227'); v.setVisible('mandible', false);
 *   v.onPick = (key, point) => …;  v.view('anterior');  v.setClip([0, 0, 1], z) / v.setClip(null)
 *   v.setVertexMarks('frontal', Uint32Array of vertex ids, '#000')   // e.g. sutures
 *   v.setMarkers([{p:[x,y,z], label:'Bregma', color:'#…'}])
 */
'use strict';
(function () {
  const css = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const rgb = c => {
    if (c.startsWith('--')) c = css(c);
    const h = c.replace('#', ''), f = h.length === 3 ? h.split('').map(x => x + x).join('') : h;
    return [0, 2, 4].map(i => parseInt(f.slice(i, i + 2), 16) / 255);
  };
  const SVGNS = 'http://www.w3.org/2000/svg';
  const b64u32 = s => { const b = Uint8Array.from(atob(s), c => c.charCodeAt(0)); return new Uint32Array(b.buffer); };

  function decode(buf) {
    const dv = new DataView(buf);
    const magic = String.fromCharCode(...new Uint8Array(buf, 0, 4));
    if (magic !== 'NPM1') throw new Error('not an NPM1 mesh');
    const nv = dv.getUint32(4, true), nt = dv.getUint32(8, true);
    const lo = [dv.getFloat32(12, true), dv.getFloat32(16, true), dv.getFloat32(20, true)], span = dv.getFloat32(24, true);
    const ib = dv.getUint32(28, true);
    let o = 32;
    const q = new Uint16Array(buf.slice(o, o + nv * 6)); o += nv * 6;
    const pos = new Float32Array(nv * 3);
    for (let i = 0; i < nv * 3; i++) pos[i] = lo[i % 3] + q[i] / 65535 * span;
    const nrm = new Int8Array(buf.slice(o, o + nv * 3)); o += nv * 3;
    o = (o + 3) & ~3;
    const idx = ib === 2 ? new Uint16Array(buf.slice(o, o + nt * 6)) : new Uint32Array(buf.slice(o, o + nt * 12));
    return {nv, nt, pos, nrm, idx};
  }

  const VS = `attribute vec3 p; attribute vec3 nm; attribute vec3 vc;
    uniform mat3 R; uniform vec3 C; uniform vec2 S; uniform vec2 PN;
    varying vec3 vn; varying vec3 vp; varying vec3 vcol;
    void main(){ vec3 q = R*(p - C); gl_Position = vec4((q.x-PN.x)*S.x, (q.z-PN.y)*S.y, q.y/2000.0, 1.0);
      vn = R*nm; vp = p; vcol = vc; }`;
  const FS = `#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
    #else
    precision mediump float;
    #endif
    varying vec3 vn; varying vec3 vp; varying vec3 vcol;
    uniform vec3 COL; uniform float MODE; uniform vec4 CLIP; uniform float USEVC; uniform float DIM; uniform vec3 IDC; uniform float ALPHA;
    void main(){
      if (CLIP.w > -1e8 && dot(vp, CLIP.xyz) > CLIP.w) discard;
      if (MODE > 0.5 && MODE < 1.5) { gl_FragColor = vec4(IDC, 1.0); return; }          // id pass
      if (MODE > 1.5) {                                                              // depth pass (24 bit)
        float d = gl_FragCoord.z; vec3 enc = fract(d * vec3(1.0, 255.0, 65025.0)); enc -= enc.yzz * vec3(1.0/255.0, 1.0/255.0, 0.0);
        gl_FragColor = vec4(enc, 1.0); return; }
      vec3 base = USEVC > 0.5 && vcol.x >= 0.0 ? vcol : COL;
      vec3 n = normalize(vn); bool back = n.y > 0.0; if (back) n = -n;
      vec3 l1 = normalize(vec3(0.35,-0.75,0.55)); vec3 l2 = normalize(vec3(-0.6,-0.3,-0.4));
      float d = max(dot(n,l1),0.0)*0.70 + max(dot(n,l2),0.0)*0.18 + 0.30;
      float s = pow(max(dot(reflect(-l1,n), vec3(0.0,-1.0,0.0)),0.0), 24.0)*0.10;
      vec3 c = base*d + s;
      if (back) c *= 0.55;                     // inside surfaces seen through a cut are darker
      c = mix(c, vec3(dot(c, vec3(0.3,0.59,0.11))), DIM*0.75);
      gl_FragColor = vec4(c, ALPHA); }`;

  class AtlasViewer {
    constructor(host, opts = {}) {
      this.host = host; this.parts = new Map(); this.order = [];
      this.yaw = 0; this.pitch = 0; this.zoom = 1; this.pan = [0, 0]; this.centre = [0, 0, 0]; this.fitH = 200;
      this.clip = null; this.markers = []; this.onPick = null; this.dimOthers = null; this.labelsOn = true;
      host.classList.add('viewer');
      host.innerHTML = '<canvas></canvas><svg aria-hidden="true"></svg><div class="hint">drag · pinch/scroll · tap</div><div class="loading">Loading 3D model…</div>';
      this.c = host.querySelector('canvas'); this.svg = host.querySelector('svg'); this.loadingEl = host.querySelector('.loading');
      const gl = this.gl = this.c.getContext('webgl', {antialias: true, alpha: true, premultipliedAlpha: false, preserveDrawingBuffer: false});
      if (!gl) { host.innerHTML = '<div class="nogl">3D needs WebGL, which this browser has turned off.</div>'; this.dead = true; return; }
      this.u32 = !!gl.getExtension('OES_element_index_uint');
      const sh = (t, src) => { const s = gl.createShader(t); gl.shaderSource(s, src); gl.compileShader(s);
        if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; };
      const pr = this.pr = gl.createProgram();
      gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr);
      gl.useProgram(pr);
      this.loc = {};
      for (const a of ['p', 'nm', 'vc']) this.loc[a] = gl.getAttribLocation(pr, a);
      for (const u of ['R', 'C', 'S', 'PN', 'COL', 'MODE', 'CLIP', 'USEVC', 'DIM', 'IDC', 'ALPHA']) this.loc[u] = gl.getUniformLocation(pr, u);
      gl.enable(gl.DEPTH_TEST);
      this.bindInput();
      new ResizeObserver(() => this.resize()).observe(host);
      matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => this.draw());
      this.resize();
    }

    /* ---------- loading ---------- */
    async load(manifestUrl, only = null) {
      const base = manifestUrl.slice(0, manifestUrl.lastIndexOf('/') + 1);
      const man = await (await fetch(manifestUrl)).json();
      this.manifest = man;
      const list = man.parts.filter(p => !only || only.includes(p.key));
      await Promise.all(list.map(async p => {
        const m = decode(await (await fetch(base + p.file)).arrayBuffer());
        this.addPart(p.key, m, p);
      }));
      this.contacts = (man.contacts || []).map(c => ({a: c.a, b: c.b, va: b64u32(c.va), vb: b64u32(c.vb)}));
      this.fit();
      this.loadingEl.remove();
      return man;
    }
    addPart(key, m, info = {}) {
      if (this.dead) return;
      const gl = this.gl, buf = (data, target = gl.ARRAY_BUFFER) => { const b = gl.createBuffer(); gl.bindBuffer(target, b); gl.bufferData(target, data, gl.STATIC_DRAW); return b; };
      if (m.idx instanceof Uint32Array && !this.u32) throw new Error('mesh needs 32-bit indices');
      const vcol = new Float32Array(m.nv * 3).fill(-1);
      const part = {key, info, m, colour: '#d9cfb6', visible: true,
        bp: buf(m.pos), bn: buf(m.nrm), bc: buf(vcol), vcol, useVC: false, bi: buf(m.idx, gl.ELEMENT_ARRAY_BUFFER),
        id: this.order.length + 1, bbox: info.bbox || null};
      if (!part.bbox) { const lo = [1e9, 1e9, 1e9], hi = [-1e9, -1e9, -1e9];
        for (let i = 0; i < m.nv; i++) for (let k = 0; k < 3; k++) { lo[k] = Math.min(lo[k], m.pos[i*3+k]); hi[k] = Math.max(hi[k], m.pos[i*3+k]); }
        part.bbox = [lo, hi]; }
      this.parts.set(key, part); this.order.push(key); this.draw();
    }
    /** frame the visible parts */
    fit(keys = null) {
      const lo = [1e9, 1e9, 1e9], hi = [-1e9, -1e9, -1e9];
      for (const k of keys || this.order) { const p = this.parts.get(k); if (!p || (!keys && !p.visible)) continue;
        for (let i = 0; i < 3; i++) { lo[i] = Math.min(lo[i], p.bbox[0][i]); hi[i] = Math.max(hi[i], p.bbox[1][i]); } }
      if (lo[0] > hi[0]) return;
      this.centre = lo.map((x, i) => (x + hi[i]) / 2);
      this.fitH = Math.max(hi[2] - lo[2], (hi[0] - lo[0]) * this.h / Math.max(this.w, 1), hi[1] - lo[1]) * 1.08;
      this.pan = [0, 0]; this.draw();
    }

    /* ---------- appearance ---------- */
    setColour(key, c) { const p = this.parts.get(key); if (p) { p.colour = c; this.draw(); } }
    setVisible(key, on) { const p = this.parts.get(key); if (p) { p.visible = on; this.draw(); } }
    /** dim every part except these keys (null = none dimmed) */
    setFocus(keys) { this.dimOthers = keys ? new Set(keys) : null; this.draw(); }
    /** colour some vertices of a part (others keep the part colour); list = [{verts: Uint32Array, colour}] */
    setVertexMarks(key, list) {
      const p = this.parts.get(key); if (!p) return;
      p.vcol.fill(-1);
      for (const {verts, colour} of list || []) { const c = rgb(colour); for (const v of verts) p.vcol.set(c, v * 3); }
      p.useVC = !!(list && list.length);
      const gl = this.gl; gl.bindBuffer(gl.ARRAY_BUFFER, p.bc); gl.bufferData(gl.ARRAY_BUFFER, p.vcol, gl.DYNAMIC_DRAW);
      this.draw();
    }
    /** cut away everything on the side of the plane n·p > d (mm); null removes the cut */
    setClip(n, d) { this.clip = n ? [...n, d] : null; this.draw(); }
    setMarkers(list) { this.markers = list || []; this.draw(); }

    /* ---------- camera ---------- */
    matrix() {
      const cy = Math.cos(this.yaw), sy = Math.sin(this.yaw), cp = Math.cos(this.pitch), sp = Math.sin(this.pitch);
      const rz = [[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]], rx = [[1, 0, 0], [0, cp, -sp], [0, sp, cp]];
      return [0, 1, 2].map(i => [0, 1, 2].map(j => rx[i][0] * rz[0][j] + rx[i][1] * rz[1][j] + rx[i][2] * rz[2][j]));
    }
    scale() { return this.zoom * this.h / this.fitH; }
    toCam(p) { const R = this.matrix(), c = this.centre, d = [p[0] - c[0], p[1] - c[1], p[2] - c[2]];
      return [0, 1, 2].map(i => R[i][0] * d[0] + R[i][1] * d[1] + R[i][2] * d[2]); }
    toScreen(q) { const s = this.scale(); return [this.w / 2 + (q[0] - this.pan[0]) * s, this.h / 2 - (q[2] - this.pan[1]) * s]; }
    /** turn so that direction n (body frame) faces the viewer; optional zoom and focus point */
    face(n, opts = {}) {
      const h = Math.hypot(n[0], n[1]);
      const yaw = h > 1e-6 ? Math.atan2(n[0], n[1]) + Math.PI : this.yaw;
      const pitch = Math.max(-1.45, Math.min(1.45, Math.atan2(n[2], Math.max(h, 1e-6)) * (opts.pitchK ?? 1)));
      this.animate(yaw, pitch, opts.zoom ?? 1, opts.focus ?? null);
    }
    view(name) {
      const d = {anterior: [0, -1, 0], posterior: [0, 1, 0], left: [1, 0, 0], right: [-1, 0, 0],
        superior: [0, -0.001, 1], inferior: [0, -0.001, -1]}[name];
      this.face(d);
    }
    animate(yaw, pitch, zoom, focus) {
      const dy = ((yaw - this.yaw) % (2 * Math.PI) + 3 * Math.PI) % (2 * Math.PI) - Math.PI;
      const y0 = this.yaw, p0 = this.pitch, z0 = this.zoom, pan0 = this.pan.slice();
      let pan1 = [0, 0];
      if (focus) { const sv = [this.yaw, this.pitch]; this.yaw = y0 + dy; this.pitch = pitch; const q = this.toCam(focus); pan1 = [q[0], q[2]]; [this.yaw, this.pitch] = sv; }
      const t0 = performance.now(), dur = matchMedia('(prefers-reduced-motion: reduce)').matches ? 1 : 520;
      const step = now => {
        const k = Math.min(1, (now - t0) / dur), e = k < .5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2;
        this.yaw = y0 + dy * e; this.pitch = p0 + (pitch - p0) * e; this.zoom = z0 + (zoom - z0) * e;
        this.pan = [pan0[0] + (pan1[0] - pan0[0]) * e, pan0[1] + (pan1[1] - pan0[1]) * e];
        this.draw(); if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }
    reset() { this.animate(0, 0, 1, null); }

    /* ---------- drawing ---------- */
    resize() {
      if (this.dead) return;
      const dpr = Math.min(2, devicePixelRatio || 1), w = this.host.clientWidth, h = this.host.clientHeight;
      this.w = w; this.h = h; this.c.width = Math.round(w * dpr); this.c.height = Math.round(h * dpr); this.dpr = this.c.width / Math.max(w, 1);
      this.svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
      this.draw();
    }
    draw() {
      if (this.dead || !this.w) return;
      this.stale = true;
      if (this.raf) return;
      this.raf = requestAnimationFrame(() => { this.raf = 0; this.render(0); this.scheduleMarkers(); });
    }
    render(mode, target = null) {
      const gl = this.gl, R = this.matrix(), s = this.scale(), L = this.loc;
      gl.bindFramebuffer(gl.FRAMEBUFFER, target);
      gl.viewport(0, 0, this.c.width, this.c.height);
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.useProgram(this.pr);
      gl.uniformMatrix3fv(L.R, false, new Float32Array([R[0][0], R[1][0], R[2][0], R[0][1], R[1][1], R[2][1], R[0][2], R[1][2], R[2][2]]));
      gl.uniform3fv(L.C, this.centre); gl.uniform2f(L.S, 2 * s / this.w, 2 * s / this.h); gl.uniform2f(L.PN, this.pan[0], this.pan[1]);
      gl.uniform1f(L.MODE, mode); gl.uniform4fv(L.CLIP, this.clip || [0, 0, 0, -1e9]);
      const ghost = mode === 0 && this.dimOthers;
      const drawPart = (key, alpha) => {
        const p = this.parts.get(key);
        gl.bindBuffer(gl.ARRAY_BUFFER, p.bp); gl.enableVertexAttribArray(L.p); gl.vertexAttribPointer(L.p, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, p.bn); gl.enableVertexAttribArray(L.nm); gl.vertexAttribPointer(L.nm, 3, gl.BYTE, true, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, p.bc); gl.enableVertexAttribArray(L.vc); gl.vertexAttribPointer(L.vc, 3, gl.FLOAT, false, 0, 0);
        gl.uniform3fv(L.COL, rgb(p.colour)); gl.uniform1f(L.USEVC, p.useVC ? 1 : 0);
        gl.uniform1f(L.DIM, this.dimOthers && !this.dimOthers.has(key) ? 1 : 0); gl.uniform1f(L.ALPHA, alpha);
        gl.uniform3fv(L.IDC, [(p.id & 255) / 255, ((p.id >> 8) & 255) / 255, 0]);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, p.bi);
        gl.drawElements(gl.TRIANGLES, p.m.nt * 3, p.m.idx instanceof Uint32Array ? gl.UNSIGNED_INT : gl.UNSIGNED_SHORT, 0);
      };
      let vis = this.order.filter(k => this.parts.get(k).visible);
      // labels test against the depth of what is drawn solid: with glass parts, only the selected ones
      if (mode === 2 && this.dimOthers) vis = vis.filter(k => this.dimOthers.has(k));
      if (!ghost) { for (const k of vis) drawPart(k, 1); }
      else {
        // selected parts solid; the rest as faint glass over them, so bones deep in the skull stay visible
        for (const k of vis) if (this.dimOthers.has(k)) drawPart(k, 1);
        gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.depthMask(false);
        for (const k of vis) if (!this.dimOthers.has(k)) drawPart(k, this.ghostAlpha ?? 0.16);
        gl.depthMask(true); gl.disable(gl.BLEND);
      }
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    }
    /** off-screen pass (id or depth); returns RGBA bytes of the whole canvas */
    offscreen(mode) {
      const gl = this.gl;
      if (!this.fb || this.fbW !== this.c.width || this.fbH !== this.c.height) {
        this.fb = gl.createFramebuffer(); const tex = gl.createTexture(); const rb = gl.createRenderbuffer();
        gl.bindTexture(gl.TEXTURE_2D, tex); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, this.c.width, this.c.height, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        gl.bindRenderbuffer(gl.RENDERBUFFER, rb); gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT16, this.c.width, this.c.height);
        gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb);
        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);
        gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, rb);
        gl.bindFramebuffer(gl.FRAMEBUFFER, null); this.fbW = this.c.width; this.fbH = this.c.height;
      }
      this.render(mode, this.fb);
      const px = new Uint8Array(this.c.width * this.c.height * 4);
      gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb); gl.readPixels(0, 0, this.c.width, this.c.height, gl.RGBA, gl.UNSIGNED_BYTE, px);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      return px;
    }
    /** which part is under client point (x, y), and the 3D point there */
    pick(clientX, clientY) {
      const r = this.c.getBoundingClientRect();
      const X = Math.round((clientX - r.left) * this.dpr), Y = Math.round((r.bottom - clientY) * this.dpr);
      const ids = this.offscreen(1), i = (Y * this.c.width + X) * 4;
      const id = ids[i] + (ids[i + 1] << 8); if (!id) return null;
      const key = this.order[id - 1];
      const dep = this.offscreen(2), z = (dep[i] / 255 + dep[i + 1] / 65025 + dep[i + 2] / 16581375);
      const s = this.scale(), qx = (clientX - r.left - this.w / 2) / s + this.pan[0], qz = -(clientY - r.top - this.h / 2) / s + this.pan[1];
      const qy = (z * 2 - 1) * 2000;
      const R = this.matrix(), c = this.centre;   // R is orthonormal: inverse = transpose
      const p = [0, 1, 2].map(k => R[0][k] * qx + R[1][k] * qy + R[2][k] * qz + c[k]);
      return {key, p};
    }

    /* ---------- labels ---------- */
    scheduleMarkers() {
      clearTimeout(this.mkTimer);
      this.drawMarkers(this.lastDepth || null);
      this.mkTimer = setTimeout(() => { if (this.markers.length) { this.lastDepth = this.offscreen(2); this.drawMarkers(this.lastDepth); } }, 120);
    }
    drawMarkers(depth) {
      const svg = this.svg; svg.replaceChildren();
      if (!this.markers.length) return;
      const dots = [];
      for (const m of this.markers) {
        const q = this.toCam(m.p), [sx, sy] = this.toScreen(q);
        if (sx < -20 || sy < -20 || sx > this.w + 20 || sy > this.h + 20) continue;
        if (this.clip && m.p[0] * this.clip[0] + m.p[1] * this.clip[1] + m.p[2] * this.clip[2] > this.clip[3]) continue;
        let hidden = false;
        if (depth) {
          const X = Math.round(sx * this.dpr), Y = Math.round((this.h - sy) * this.dpr);
          if (X >= 0 && Y >= 0 && X < this.c.width && Y < this.c.height) {
            const i = (Y * this.c.width + X) * 4;
            if (depth[i + 3]) { const z = depth[i] / 255 + depth[i + 1] / 65025 + depth[i + 2] / 16581375; const zq = (q[1] / 2000 + 1) / 2; hidden = zq > z + 3 / 4000; }
          }
        }
        if (hidden && !m.always) continue;
        dots.push({m, sx, sy, hidden});
      }
      const boxes = [], overlaps = b => boxes.some(o => b.x0 < o.x1 && b.x1 > o.x0 && b.y0 < o.y1 && b.y1 > o.y0), labels = [];
      for (const d of dots) boxes.push({x0: d.sx - 6, x1: d.sx + 6, y0: d.sy - 6, y1: d.sy + 6});
      for (const d of [...dots].sort((a, b) => a.sy - b.sy)) {
        if (!d.m.label || !this.labelsOn) continue;
        const wdt = d.m.label.length * 7 + 6, pref = d.sx > this.w * .6; let best = null;
        for (const dy of [0, 15, -15, 30, -30, 45, -45, 60, -60]) {
          for (const left of [pref, !pref]) {
            const y = d.sy + dy, b = left ? {x0: d.sx - 12 - wdt, x1: d.sx - 8, y0: y - 9, y1: y + 7} : {x0: d.sx + 8, x1: d.sx + 12 + wdt, y0: y - 9, y1: y + 7};
            if (b.x0 >= 2 && b.x1 <= this.w - 2 && !overlaps(b)) { best = {b, y, left}; break; }
          }
          if (best) break;
        }
        if (best) { boxes.push(best.b); labels.push({d, ...best}); }
      }
      const mk = (tag, a) => { const e = document.createElementNS(SVGNS, tag); for (const k in a) e.setAttribute(k, a[k]); return e; };
      for (const {d, left, y} of labels) if (Math.abs(y - d.sy) > 1)
        svg.append(mk('line', {x1: d.sx, y1: d.sy, x2: left ? d.sx - 10 : d.sx + 10, y2: y - 3, stroke: css('--muted'), 'stroke-width': 1, opacity: d.hidden ? .35 : .8}));
      for (const d of dots) svg.append(mk('circle', {cx: d.sx, cy: d.sy, r: d.m.big ? 6.5 : 4.5, fill: d.m.color || css('--mark'), stroke: css('--surface'), 'stroke-width': 2, opacity: d.hidden ? .35 : 1}));
      for (const {d, left, y} of labels) { const t = mk('text', {x: left ? d.sx - 10 : d.sx + 10, y: y + 4, 'text-anchor': left ? 'end' : 'start', opacity: d.hidden ? .35 : 1}); t.textContent = d.m.label; svg.append(t); }
    }

    /* ---------- input ---------- */
    bindInput() {
      const el = this.host, pts = new Map(); let down = null, pinch = null;
      el.addEventListener('pointerdown', e => {
        el.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]);
        if (pts.size === 1) down = {x: e.clientX, y: e.clientY, t: performance.now(), moved: false, pan: e.shiftKey || e.button === 2};
        if (pts.size === 2) { const [a, b] = [...pts.values()]; pinch = {d: Math.hypot(a[0] - b[0], a[1] - b[1]), z: this.zoom, mid: [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]}; if (down) down.moved = true; }
      });
      el.addEventListener('pointermove', e => {
        if (!pts.has(e.pointerId)) return;
        const prev = pts.get(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]);
        const dx = e.clientX - prev[0], dy = e.clientY - prev[1];
        if (pts.size === 2 && pinch) {
          const [a, b] = [...pts.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]), mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
          this.zoom = Math.max(.5, Math.min(12, pinch.z * d / pinch.d));
          const s = this.scale(); this.pan[0] -= (mid[0] - pinch.mid[0]) / s; this.pan[1] += (mid[1] - pinch.mid[1]) / s; pinch.mid = mid;
          this.draw(); return;
        }
        if (!down) return;
        if (Math.abs(e.clientX - down.x) + Math.abs(e.clientY - down.y) > 6) down.moved = true;
        if (down.pan) { const s = this.scale(); this.pan[0] -= dx / s; this.pan[1] += dy / s; }
        else { this.yaw += dx * 0.0105; this.pitch = Math.max(-1.5, Math.min(1.5, this.pitch + dy * 0.0105)); }
        this.draw();
      });
      const up = e => {
        pts.delete(e.pointerId); if (pts.size < 2) pinch = null;
        if (down && pts.size === 0) {
          if (!down.moved && performance.now() - down.t < 500 && this.onPick) this.onPick(this.pick(e.clientX, e.clientY));
          down = null;
        }
      };
      el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
      el.addEventListener('contextmenu', e => e.preventDefault());
      el.addEventListener('wheel', e => {
        e.preventDefault();
        const r = this.c.getBoundingClientRect(), s0 = this.scale();
        const fx = (e.clientX - r.left - this.w / 2) / s0 + this.pan[0], fz = -(e.clientY - r.top - this.h / 2) / s0 + this.pan[1];
        this.zoom = Math.max(.5, Math.min(12, this.zoom * Math.exp(-e.deltaY * 0.0015)));
        const s1 = this.scale(); this.pan[0] = fx - (e.clientX - r.left - this.w / 2) / s1; this.pan[1] = fz + (e.clientY - r.top - this.h / 2) / s1;
        this.draw();
      }, {passive: false});
    }
  }
  window.AtlasViewer = AtlasViewer;
})();
