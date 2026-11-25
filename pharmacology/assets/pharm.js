/* Shared helpers for the pharmacology pages (pharmacology/<branch>/*.html): steppers, chips, tables, sliders, SVG building and simple
   plots. Copied from physiology/assets/phys.js (nothing is shared across subjects). Facts and data live in each page's script, not here. */
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
  /* reduced motion */
  P.reduced = () => { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } };
  window.Pharm = P;
})();
