/* Shared helpers for the pathology pages (pathology/<branch>/*.html): steppers, chips, tables, sliders, SVG building and a micrograph with
   switchable labels. Copied from physiology/assets/phys.js (nothing is shared across subjects). Facts and data live in each page script. */
(function () {
  'use strict';
  window.addEventListener('error', e => { window.loadError = window.loadError || String(e.message); });
  const P = {};
  P.$ = id => document.getElementById(id);
  /* SVG text; cls: s small grey, h heading, b bold, m mono, l outlined label, c clinical */
  /* typographic minus for negative numbers (U+2212) */
  P.mn = v => String(v).replace(/-(?=\d)/g, '−');
  P.T = (x, y, s, cls = '', a = 'start', extra = '') => `<text x="${(+x).toFixed(1)}" y="${(+y).toFixed(1)}" class="${cls}" text-anchor="${a}"${extra}>${P.mn(s)}</text>`;
  P.lead = (x1, y1, x2, y2) => `<path class="lead" d="M${x1} ${y1} L${x2} ${y2}"/>`;
  P.DEFS = '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" style="fill:var(--ink)"/></marker>'
    + '<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" style="fill:var(--fluid)"/><line x1="0" y1="0" x2="0" y2="6" style="stroke:var(--ink);stroke-width:1.2;stroke-opacity:.45"/></pattern></defs>';
  P.arrowDef = (id, col) => `<marker id="${id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" style="fill:${col}"/></marker>`;
  P.table = (id, head, rows) => {
    const t = P.$(id); t.classList.add('t', 'stack');
    t.innerHTML = '<tr>' + head.map(x => `<th>${x}</th>`).join('') + '</tr>' + rows.map(r => '<tr>' + r.map((c, i) => `<td data-h="${head[i].replace(/<[^>]+>/g, '')}">${c}</td>`).join('') + '</tr>').join('');
  };
  P.toggles = (id, items, onSel, start) => {
    const box = P.$(id); box.innerHTML = ''; box.classList.add('chips');
    for (const [key, label] of items) {
      const b = document.createElement('button'); b.className = 'chip'; b.type = 'button'; b.innerHTML = label; b.dataset.k = key;
      b.setAttribute('aria-pressed', String(key === start));
      b.onclick = () => { box.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b))); onSel(key); };
      box.append(b);
    }
  };
  P.stepper = (id, labels, onStep, state) => {
    const box = P.$(id); box.innerHTML = '';
    const prev = document.createElement('button'); prev.className = 'btn'; prev.type = 'button'; prev.textContent = '◀ Back'; prev.setAttribute('aria-label', 'Previous step');
    const next = document.createElement('button'); next.className = 'btn'; next.type = 'button'; next.textContent = 'Next ▶'; next.setAttribute('aria-label', 'Next step');
    const row = document.createElement('div'); row.className = 'chips'; row.setAttribute('aria-label', 'Steps');
    const go = i => {
      state.s = Math.max(0, Math.min(labels.length - 1, i));
      row.querySelectorAll('button').forEach((b, j) => b.setAttribute('aria-pressed', String(j === state.s)));
      prev.disabled = state.s === 0; next.disabled = state.s === labels.length - 1;
      if (document.activeElement && document.activeElement.disabled) row.children[state.s].focus();   // keep keyboard focus at the ends
      onStep();
    };
    labels.forEach((l, i) => { const b = document.createElement('button'); b.className = 'chip'; b.type = 'button'; b.textContent = l; b.onclick = () => go(i); row.append(b); });
    prev.onclick = () => go(state.s - 1); next.onclick = () => go(state.s + 1);
    box.onkeydown = e => { if (e.key === 'ArrowRight') { go(state.s + 1); e.preventDefault(); } if (e.key === 'ArrowLeft') { go(state.s - 1); e.preventDefault(); } }; // property, not addEventListener: a rebuilt stepper replaces the old handler
    box.append(prev, row, next); go(state.s);
    return go;
  };
  /* slider: spec = {id, label, min, max, step, value, fmt(v) -> string}; onInput(v) */
  P.slider = (box, spec, onInput) => {
    const d = document.createElement('div'); d.className = 'sl';
    const iid = 'sl-' + spec.id;
    d.innerHTML = `<label for="${iid}">${spec.label}</label><output id="${iid}-o" for="${iid}"></output><input type="range" id="${iid}" min="${spec.min}" max="${spec.max}" step="${spec.step}" value="${spec.value}">`;
    (typeof box === 'string' ? P.$(box) : box).append(d);
    const inp = d.querySelector('input'), out = d.querySelector('output');
    const upd = () => { const v = +inp.value; out.textContent = P.mn(spec.fmt ? spec.fmt(v) : String(v)); onInput(v); };
    inp.addEventListener('input', upd);
    return {el: inp, set: v => { inp.value = v; upd(); }, get: () => +inp.value, init: () => { out.textContent = spec.fmt ? spec.fmt(+inp.value) : inp.value; }};
  };
  P.key = (id, items) => { P.$(id).innerHTML = items.map(([t, l, extra]) => `<span><i style="background:${t.startsWith('--') ? 'var(' + t + ')' : t}${extra ? ';' + extra : ''}"></i>${l}</span>`).join(''); };
  P.swipeHints = () => {
    document.querySelectorAll('.schbox').forEach(b => {
      if (b.querySelector('svg.fit')) return;
      const n = b.nextElementSibling;
      if (n && n.classList && n.classList.contains('swipe')) return;
      const p = document.createElement('p'); p.className = 'muted swipe'; p.textContent = 'Swipe sideways to see all of it.'; b.after(p);
    });
  };
  /* linear scale */
  P.scale = (d0, d1, r0, r1) => v => r0 + (v - d0) * (r1 - r0) / (d1 - d0);
  /* path from points */
  P.path = pts => pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ');
  /* an ion as a small dot */
  P.ION = {ca: ['Ca²⁺', '--ca']};  /* only Ca2+ is drawn as an ion on the pathology pages */
  P.dot = (x, y, ion, r = 4.2) => `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r}" style="fill:var(${P.ION[ion][1]});stroke:var(--surface);stroke-width:1"/>`;
  /* reduced motion */
  P.reduced = () => { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } };
  /* ---- a micrograph with switchable labels, as anatomy/histology/histo.js H.micro.
     m = {id, file (path relative to the page), w, h, alt, title, cap, credit, labels: [[x, y, text], ...] (fractions of the image)} ---- */
  P.micro = (box, m) => {
    const f = document.createElement('figure'); f.className = 'mg'; f.id = 'mg-' + m.id;
    f.innerHTML = `<div class="bar"><span class="t">${m.title}</span></div><div class="im"><img src="${m.file}" width="${m.w}" height="${m.h}" loading="lazy" alt="${m.alt}"><svg viewBox="0 0 ${m.w} ${m.h}" aria-hidden="true"></svg></div><figcaption>${m.cap}<span class="cr">${m.credit}</span></figcaption>`;
    (typeof box === 'string' ? P.$(box) : box).append(f);
    const st = {on: true};
    const draw = () => {
      const S = f.querySelector('svg'), wpx = Math.max(160, f.querySelector('.im').clientWidth || 400), k = m.w / wpx, fs = 12.5 * k;
      S.style.setProperty('--mg-fs', fs.toFixed(1) + 'px'); S.style.setProperty('--mg-sw', (2.6 * k).toFixed(1) + 'px'); S.style.setProperty('--mg-lw', (1.5 * k).toFixed(1) + 'px');
      let h = ''; const boxes = [];
      if (st.on) for (const [x, y, t] of m.labels || []) {
        const X = x * m.w, Y = y * m.h, tw = t.length * fs * 0.56, gap = 9 * k;
        let right = x < 0.55; if (right && X + gap + tw > m.w - 4) right = false; if (!right && X - gap - tw < 4) right = true;
        const tx = Math.max(4 + (right ? 0 : tw), Math.min(m.w - 4 - (right ? tw : 0), right ? X + gap : X - gap));
        let ty = Math.max(fs, Math.min(m.h - 4, Y + fs * 0.35)); const x0 = right ? tx : tx - tw, x1 = right ? tx + tw : tx;
        for (let i = 0; i < 6; i++) { const hit = boxes.find(q => x0 < q[2] && x1 > q[0] && ty - fs < q[3] && ty > q[1] - fs * 0.15); if (!hit) break; ty = Math.min(m.h - 4, hit[3] + fs * 1.15); }
        boxes.push([x0, ty - fs, x1, ty]);
        if (Math.abs(ty - (Y + fs * 0.35)) > fs * 0.6) h += `<line x1="${X.toFixed(1)}" y1="${Y.toFixed(1)}" x2="${tx.toFixed(1)}" y2="${(ty - fs * 0.35).toFixed(1)}"/>`;
        h += `<circle cx="${X.toFixed(1)}" cy="${Y.toFixed(1)}" r="${(4.5 * k).toFixed(1)}"/><text x="${tx.toFixed(1)}" y="${ty.toFixed(1)}" text-anchor="${right ? 'start' : 'end'}">${t}</text>`;
      }
      S.innerHTML = h;
    };
    if (m.labels && m.labels.length) {
      const b = document.createElement('button'); b.className = 'chip'; b.type = 'button'; b.textContent = 'Labels'; b.setAttribute('aria-pressed', 'true');
      b.onclick = () => { st.on = !st.on; b.setAttribute('aria-pressed', String(st.on)); draw(); };
      f.querySelector('.bar').append(b);
    }
    draw();
    if (window.ResizeObserver) new ResizeObserver(draw).observe(f.querySelector('.im'));
    return f;
  };
  P.credit = c => `Image: <a href="https://commons.wikimedia.org/wiki/File:${encodeURIComponent(c.file.replace(/ /g, '_'))}">${c.file}</a> by ${c.author}, ${c.licUrl ? `<a href="${c.licUrl}">${c.lic}</a>` : c.lic}, via Wikimedia Commons; ${c.done}.`;
  window.Patho = P;
})();
