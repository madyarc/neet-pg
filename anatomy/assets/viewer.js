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
 *   await v.loadPart('D:frontal', '../models/skull-detail/frontal.bin')     // one extra part from its own file
 *   await v.load(url, null, {fit: false, onProgress: f => …, extra: man => [{key, m, info}]})   // a second layer
 *   v.mirrored(key, newKey, {m: 3x3, t: [x,y,z]}, info) -> {key, m, info}   // a reflected copy (left from right)
 *
 * Smoothness: a model packed into one file (manifest parts with `offset`) is one request; each load's parts share
 * one set of GPU buffers (32-bit indices), so a part costs one draw call; colours are resolved once, not per frame;
 * a tap renders only the pixel under it.
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

  function decode(buf, o0 = 0) {
    const dv = new DataView(buf, o0);
    const magic = String.fromCharCode(...new Uint8Array(buf, o0, 4));
    if (magic !== 'NPM1') throw new Error('not an NPM1 mesh');
    const nv = dv.getUint32(4, true), nt = dv.getUint32(8, true);
    const lo = [dv.getFloat32(12, true), dv.getFloat32(16, true), dv.getFloat32(20, true)], span = dv.getFloat32(24, true);
    const ib = dv.getUint32(28, true);
    let o = o0 + 32;
    const q = new Uint16Array(buf.slice(o, o + nv * 6)); o += nv * 6;
    const pos = new Float32Array(nv * 3);
    for (let i = 0; i < nv * 3; i++) pos[i] = lo[i % 3] + q[i] / 65535 * span;
    const nrm = new Int8Array(buf.slice(o, o + nv * 3)); o += nv * 3;
    o = o0 + ((o - o0 + 3) & ~3);
    const idx = ib === 2 ? new Uint16Array(buf.slice(o, o + nt * 6)) : new Uint32Array(buf.slice(o, o + nt * 12));
    return {nv, nt, pos, nrm, idx};
  }

  const VS = `attribute vec3 p; attribute vec3 nm; attribute vec3 vc;
    uniform mat3 R; uniform vec3 C; uniform vec2 S; uniform vec2 PN; uniform mat3 MR; uniform vec3 MT;
    varying vec3 vn; varying vec3 vp; varying vec3 vcol;
    void main(){ vec3 w = MR*p + MT; vec3 q = R*(w - C); gl_Position = vec4((q.x-PN.x)*S.x, (q.z-PN.y)*S.y, q.y/2000.0, 1.0);
      vn = R*(MR*nm); vp = w; vcol = vc; }`;
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

  /** fetch a binary, reporting roughly the fraction received. The length the server gives can be the compressed size
   *  (GitHub Pages gzips), while the stream yields decompressed bytes: collect every chunk, use the length only for
   *  the progress figure. */
  async function fetchBuf(url, onProgress) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(url + ': HTTP ' + r.status);
    const total = +r.headers.get('content-length') || 0;
    if (!onProgress || !total || !r.body) return r.arrayBuffer();
    const zipped = /gzip|br|deflate/i.test(r.headers.get('content-encoding') || '');
    const rd = r.body.getReader(), chunks = []; let n = 0;
    for (;;) {
      const {done, value} = await rd.read(); if (done) break;
      chunks.push(value); n += value.length;
      onProgress(Math.min(0.99, n / (zipped ? total * 1.3 : total)));   // compressed: a rough guess
    }
    const out = new Uint8Array(n); let o = 0;
    for (const c of chunks) { out.set(c, o); o += c.length; }
    return out.buffer;
  }
  const nextFrame = () => new Promise(r => requestAnimationFrame(() => r()));

  class AtlasViewer {
    constructor(host, opts = {}) {
      this.host = host; this.parts = new Map(); this.order = [];
      this.yaw = 0; this.pitch = 0; this.zoom = 1; this.pan = [0, 0]; this.centre = [0, 0, 0]; this.fitH = 200;
      this.clip = null; this.markers = []; this.onPick = null; this.dimOthers = null; this.labelsOn = true; this.contacts = [];
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
      for (const u of ['R', 'C', 'S', 'PN', 'COL', 'MODE', 'CLIP', 'USEVC', 'DIM', 'IDC', 'ALPHA', 'MR', 'MT']) this.loc[u] = gl.getUniformLocation(pr, u);
      gl.enable(gl.DEPTH_TEST);
      this.bindInput();
      new ResizeObserver(() => this.resize()).observe(host);
      new MutationObserver(() => { for (const p of this.parts.values()) p.rgb = rgb(p.colour); this.draw(); this.scheduleMarkers(); }).observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
      this.resize();
    }

    /* ---------- loading ---------- */
    async load(manifestUrl, only = null, opts = {}) {
      const base = manifestUrl.slice(0, manifestUrl.lastIndexOf('/') + 1);
      const man = await (await fetch(manifestUrl)).json();
      if (!this.manifest) this.manifest = man;
      const list = man.parts.filter(p => !only || only.includes(p.key));
      const prog = opts.onProgress || null;
      let items;
      if (list.length && list[0].offset !== undefined) {         // one packed file for the whole model
        const buf = await fetchBuf(base + list[0].file, prog && (f => prog(f * 0.9)));
        items = [];
        for (let i = 0; i < list.length; i++) {
          items.push({key: list[i].key, m: decode(buf, list[i].offset), info: list[i]});
          if (i % 40 === 39) await nextFrame();                  // keep the page responsive while decoding
        }
      } else {
        let done = 0;
        items = await Promise.all(list.map(async p => {
          const m = decode(await fetchBuf(base + p.file)); if (prog) prog(0.9 * ++done / list.length);
          return {key: p.key, m, info: p};
        }));
      }
      if (opts.extra) items = items.concat(opts.extra(man, items));
      this.addParts(items);
      if (prog) prog(1);
      this.contacts = this.contacts.concat((man.contacts || []).map(c => ({a: c.a, b: c.b, va: b64u32(c.va), vb: b64u32(c.vb)})));
      if (opts.fit !== false) this.fit();
      if (this.loadingEl.isConnected) this.loadingEl.remove();
      return man;
    }
    /** a reflected copy of a loaded mesh: p' = M p + t (normals by M; M is a reflection, so orthonormal) */
    mirrored(m, M, t) {
      const pos = new Float32Array(m.pos.length), nrm = new Int8Array(m.nrm.length);
      for (let i = 0; i < m.nv; i++) {
        const x = m.pos[i*3], y = m.pos[i*3+1], z = m.pos[i*3+2], a = m.nrm[i*3], b = m.nrm[i*3+1], c = m.nrm[i*3+2];
        for (let k = 0; k < 3; k++) {
          pos[i*3+k] = M[k][0] * x + M[k][1] * y + M[k][2] * z + t[k];
          nrm[i*3+k] = Math.max(-127, Math.min(127, Math.round(M[k][0] * a + M[k][1] * b + M[k][2] * c)));
        }
      }
      return {nv: m.nv, nt: m.nt, pos, nrm, idx: m.idx};
    }
    /** add one more part from its own binary (e.g. a detailed copy of a bone over a lighter model) */
    async loadPart(key, url, info = {}) {
      const m = decode(await (await fetch(url)).arrayBuffer());
      this.addPart(key, m, info);
      if (this.loadingEl.isConnected) this.loadingEl.remove();
      return this.parts.get(key);
    }
    addPart(key, m, info = {}) { this.addParts([{key, m, info}]); }
    /** upload parts into one shared set of buffers (one batch): drawing a part is then a single draw call */
    addParts(items) {
      if (this.dead || !items.length) return;
      if (!this.u32) {                                    // no 32-bit indices: one batch per part (each < 65536 verts)
        if (items.length > 1) { for (const it of items) this.addParts([it]); return; }
        if (items[0].m.idx instanceof Uint32Array) throw new Error('mesh needs 32-bit indices');
      }
      const gl = this.gl, buf = (data, target, usage = gl.STATIC_DRAW) => { const b = gl.createBuffer(); gl.bindBuffer(target, b); gl.bufferData(target, data, usage); return b; };
      let nv = 0, ni = 0;
      for (const {m} of items) { nv += m.nv; ni += m.nt * 3; }
      const pos = new Float32Array(nv * 3), nrm = new Int8Array(nv * 3), vcol = new Float32Array(nv * 3).fill(-1);
      const idx = this.u32 ? new Uint32Array(ni) : new Uint16Array(ni);
      const batch = {vcol};
      let v0 = 0, i0 = 0;
      for (const {key, m, info = {}} of items) {
        pos.set(m.pos, v0 * 3); nrm.set(m.nrm, v0 * 3);
        for (let i = 0; i < m.idx.length; i++) idx[i0 + i] = m.idx[i] + v0;
        const part = {key, info, m, colour: '#d9cfb6', rgb: rgb('#d9cfb6'), visible: true, batch, v0, i0, count: m.nt * 3,
          vcol: vcol.subarray(v0 * 3, (v0 + m.nv) * 3), useVC: false, id: this.order.length + 1, bbox: info.bbox || null};
        if (!part.bbox) { const lo = [1e9, 1e9, 1e9], hi = [-1e9, -1e9, -1e9];
          for (let i = 0; i < m.nv; i++) for (let k = 0; k < 3; k++) { lo[k] = Math.min(lo[k], m.pos[i*3+k]); hi[k] = Math.max(hi[k], m.pos[i*3+k]); }
          part.bbox = [lo, hi]; }
        this.parts.set(key, part); this.order.push(key);
        v0 += m.nv; i0 += m.nt * 3;
      }
      batch.bp = buf(pos, gl.ARRAY_BUFFER); batch.bn = buf(nrm, gl.ARRAY_BUFFER);
      batch.bc = buf(vcol, gl.ARRAY_BUFFER, gl.DYNAMIC_DRAW); batch.bi = buf(idx, gl.ELEMENT_ARRAY_BUFFER);
      batch.itype = this.u32 ? gl.UNSIGNED_INT : gl.UNSIGNED_SHORT; batch.isize = this.u32 ? 4 : 2;
      this.draw();
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
    /** move a part rigidly: p' = m p + t (m: 3x3 rows, a rotation; null = back in place). See rotation(). */
    setTransform(key, m, t) {
      const p = this.parts.get(key); if (!p) return;
      p.xf = m ? {m: new Float32Array([m[0][0], m[1][0], m[2][0], m[0][1], m[1][1], m[2][1], m[0][2], m[1][2], m[2][2]]), t: Float32Array.from(t)} : null;
      this.draw();
    }
    /** rotation by deg about a unit axis through point c, as {m, t} for setTransform */
    static rotation(axis, deg, c) {
      const a = deg * Math.PI / 180, [x, y, z] = axis, co = Math.cos(a), si = Math.sin(a), k = 1 - co;
      const m = [[co + x*x*k, x*y*k - z*si, x*z*k + y*si], [y*x*k + z*si, co + y*y*k, y*z*k - x*si], [z*x*k - y*si, z*y*k + x*si, co + z*z*k]];
      return {m, t: [0, 1, 2].map(i => c[i] - (m[i][0] * c[0] + m[i][1] * c[1] + m[i][2] * c[2]))};
    }
    setColour(key, c) { const p = this.parts.get(key); if (p && p.colour !== c) { p.colour = c; p.rgb = rgb(c); this.draw(); } }
    setVisible(key, on) { const p = this.parts.get(key); if (p && p.visible !== on) { p.visible = on; this.draw(); } }
    /** dim every part except these keys (null = none dimmed) */
    setFocus(keys) { this.dimOthers = keys ? new Set(keys) : null; this.draw(); }
    /** colour some vertices of a part (others keep the part colour); list = [{verts: Uint32Array, colour}] */
    setVertexMarks(key, list) {
      const p = this.parts.get(key); if (!p) return;
      const on = !!(list && list.length);
      if (!on && !p.useVC) return;                        // nothing to clear
      p.vcol.fill(-1);
      for (const {verts, colour} of list || []) { const c = rgb(colour); for (const v of verts) p.vcol.set(c, v * 3); }
      p.useVC = on;
      const gl = this.gl; gl.bindBuffer(gl.ARRAY_BUFFER, p.batch.bc); gl.bufferSubData(gl.ARRAY_BUFFER, p.v0 * 12, p.vcol);
      this.draw();
    }
    /** cut away everything on the side of the plane n·p > d (mm); null removes the cut */
    setClip(n, d) { this.clip = n ? [...n, d] : null; this.draw(); }
    setMarkers(list) { this.markers = list || []; this.draw(); }
    /** straight lines over the model, e.g. an axis of movement: [{a: [x,y,z], b: [x,y,z], color, dash}] */
    setLines(list) { this.lines = list || []; this.draw(); }

    /** put an element over the viewer (e.g. a selection card); taps on it do not reach the model */
    addOverlay(el) {
      for (const ev of ['pointerdown', 'pointerup', 'pointermove', 'wheel']) el.addEventListener(ev, e => e.stopPropagation());
      this.host.append(el); return el;
    }

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
    render(mode, target = null, px = null) {
      const gl = this.gl, R = this.matrix(), s = this.scale(), L = this.loc;
      gl.bindFramebuffer(gl.FRAMEBUFFER, target);
      gl.viewport(0, 0, this.c.width, this.c.height);
      if (px) { gl.enable(gl.SCISSOR_TEST); gl.scissor(px[0], px[1], 1, 1); }   // a tap: only the pixel under it
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.useProgram(this.pr);
      gl.uniformMatrix3fv(L.R, false, new Float32Array([R[0][0], R[1][0], R[2][0], R[0][1], R[1][1], R[2][1], R[0][2], R[1][2], R[2][2]]));
      gl.uniform3fv(L.C, this.centre); gl.uniform2f(L.S, 2 * s / this.w, 2 * s / this.h); gl.uniform2f(L.PN, this.pan[0], this.pan[1]);
      gl.uniform1f(L.MODE, mode); gl.uniform4fv(L.CLIP, this.clip || [0, 0, 0, -1e9]);
      const ghost = mode === 0 && this.dimOthers;
      // state is set only when it changes: with hundreds of parts most calls would repeat the previous value
      let curBatch = null, curUVC = -1, curDim = -1, curAlpha = -1, curXf;
      const ID = this.idXf || (this.idXf = {m: new Float32Array([1, 0, 0, 0, 1, 0, 0, 0, 1]), t: new Float32Array(3)});
      for (const a of [L.p, L.nm, L.vc]) gl.enableVertexAttribArray(a);
      const drawPart = (key, alpha) => {
        const p = this.parts.get(key), b = p.batch;
        if (b !== curBatch) {
          curBatch = b;
          gl.bindBuffer(gl.ARRAY_BUFFER, b.bp); gl.vertexAttribPointer(L.p, 3, gl.FLOAT, false, 0, 0);
          gl.bindBuffer(gl.ARRAY_BUFFER, b.bn); gl.vertexAttribPointer(L.nm, 3, gl.BYTE, true, 0, 0);
          gl.bindBuffer(gl.ARRAY_BUFFER, b.bc); gl.vertexAttribPointer(L.vc, 3, gl.FLOAT, false, 0, 0);
          gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, b.bi);
        }
        const xf = p.xf || ID;
        if (xf !== curXf) { gl.uniformMatrix3fv(L.MR, false, xf.m); gl.uniform3fv(L.MT, xf.t); curXf = xf; }
        if (mode === 1) gl.uniform3f(L.IDC, (p.id & 255) / 255, ((p.id >> 8) & 255) / 255, 0);
        else if (mode === 0) {
          gl.uniform3fv(L.COL, p.rgb);
          const u = p.useVC ? 1 : 0, d = this.dimOthers && !this.dimOthers.has(key) ? 1 : 0;
          if (u !== curUVC) { gl.uniform1f(L.USEVC, u); curUVC = u; }
          if (d !== curDim) { gl.uniform1f(L.DIM, d); curDim = d; }
          if (alpha !== curAlpha) { gl.uniform1f(L.ALPHA, alpha); curAlpha = alpha; }
        }
        gl.drawElements(gl.TRIANGLES, p.count, b.itype, p.i0 * b.isize);
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
      if (px) gl.disable(gl.SCISSOR_TEST);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    }
    /** off-screen pass (id or depth); returns RGBA bytes of the whole canvas */
    offscreen(mode, px = null) {
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
      this.render(mode, this.fb, px);
      gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb);
      let out;
      if (px) { out = new Uint8Array(4); gl.readPixels(px[0], px[1], 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, out); }
      else { out = new Uint8Array(this.c.width * this.c.height * 4); gl.readPixels(0, 0, this.c.width, this.c.height, gl.RGBA, gl.UNSIGNED_BYTE, out); }
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      return out;
    }
    /** which part is under client point (x, y), and the 3D point there */
    pick(clientX, clientY) {
      const r = this.c.getBoundingClientRect();
      const X = Math.round((clientX - r.left) * this.dpr), Y = Math.round((r.bottom - clientY) * this.dpr);
      if (X < 0 || Y < 0 || X >= this.c.width || Y >= this.c.height) return null;
      const ids = this.offscreen(1, [X, Y]);
      const id = ids[0] + (ids[1] << 8); if (!id) return null;
      const key = this.order[id - 1];
      const dep = this.offscreen(2, [X, Y]), z = (dep[0] / 255 + dep[1] / 65025 + dep[2] / 16581375);
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
      for (const l of this.lines || []) {
        const [x1, y1] = this.toScreen(this.toCam(l.a)), [x2, y2] = this.toScreen(this.toCam(l.b));
        const e = document.createElementNS(SVGNS, 'line');
        for (const [k, val] of Object.entries({x1, y1, x2, y2, stroke: l.color && l.color.startsWith('--') ? css(l.color) : (l.color || css('--mark')),
          'stroke-width': 2.5, 'stroke-linecap': 'round', 'stroke-dasharray': l.dash || ''})) e.setAttribute(k, val);
        svg.append(e);
      }
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
