/* Shared helpers for the module-44 abdomen-pelvis pages (bony-pelvis, imaging-abdomen, surface-sections); a copy of
   genetics/gen.js: steppers, chips, tables, SVG text, radiographs with switchable labels, image credits. Data live in each page. */
(function () {
  'use strict';
  window.addEventListener('error', e => { window.loadError = window.loadError || String(e.message); });
  const G = {};
  G.$ = id => document.getElementById(id);
  /* SVG text; cls: s small grey, h heading, b bold, m mono, l outlined label, c clinical */
  G.T = (x, y, s, cls = '', a = 'start') => `<text x="${x}" y="${y}" class="${cls}" text-anchor="${a}">${s}</text>`;
  G.lead = (x1, y1, x2, y2) => `<path class="lead" d="M${x1} ${y1} L${x2} ${y2}"/>`;
  G.DEFS = '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" style="fill:var(--ink)"/></marker>'
    + '<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" style="fill:var(--surface)"/><line x1="0" y1="0" x2="0" y2="6" style="stroke:var(--ink);stroke-width:2"/></pattern></defs>';
  G.table = (id, head, rows) => {
    const t = G.$(id); t.classList.add('t', 'stack');
    t.innerHTML = '<tr>' + head.map(x => `<th>${x}</th>`).join('') + '</tr>' + rows.map(r => '<tr>' + r.map((c, i) => `<td data-h="${head[i]}">${c}</td>`).join('') + '</tr>').join('');
  };
  G.toggles = (id, items, onSel, start) => {
    const box = G.$(id); box.innerHTML = ''; box.classList.add('chips');
    for (const [key, label] of items) {
      const b = document.createElement('button'); b.className = 'chip'; b.type = 'button'; b.textContent = label; b.dataset.k = key;
      b.setAttribute('aria-pressed', String(key === start));
      b.onclick = () => { box.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b))); onSel(key); };
      box.append(b);
    }
  };
  G.stepper = (id, labels, onStep, state) => {
    const box = G.$(id); box.innerHTML = '';
    const prev = document.createElement('button'); prev.className = 'btn'; prev.type = 'button'; prev.textContent = '◀ Back'; prev.setAttribute('aria-label', 'Previous step');
    const next = document.createElement('button'); next.className = 'btn'; next.type = 'button'; next.textContent = 'Next ▶'; next.setAttribute('aria-label', 'Next step');
    const row = document.createElement('div'); row.className = 'chips'; row.setAttribute('aria-label', 'Steps');
    const go = i => {
      state.s = Math.max(0, Math.min(labels.length - 1, i));
      row.querySelectorAll('button').forEach((b, j) => b.setAttribute('aria-pressed', String(j === state.s)));
      prev.disabled = state.s === 0; next.disabled = state.s === labels.length - 1; onStep();
    };
    labels.forEach((l, i) => { const b = document.createElement('button'); b.className = 'chip'; b.type = 'button'; b.textContent = l; b.onclick = () => go(i); row.append(b); });
    prev.onclick = () => go(state.s - 1); next.onclick = () => go(state.s + 1);
    box.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { go(state.s + 1); e.preventDefault(); } if (e.key === 'ArrowLeft') { go(state.s - 1); e.preventDefault(); } });
    box.append(prev, row, next); go(state.s);
  };
  G.key = (id, items) => { G.$(id).innerHTML = items.map(([t, l, extra]) => `<span><i style="background:${t.startsWith('--') ? 'var(' + t + ')' : t}${extra ? ';' + extra : ''}"></i>${l}</span>`).join(''); };
  G.swipeHints = () => {
    document.querySelectorAll('.schbox').forEach(b => {
      if (b.querySelector('svg.fit')) return;
      const n = b.nextElementSibling;
      if (n && n.classList && n.classList.contains('swipe')) return;
      const p = document.createElement('p'); p.className = 'muted swipe'; p.textContent = 'Swipe sideways to see all of it.'; b.after(p);
    });
  };
  /* licences and credits (Wikimedia Commons metadata saved in sources-local/modern/fill-abdo2/img/*.json) */
  G.LIC = {
    pd: ['Public domain', 'https://creativecommons.org/publicdomain/mark/1.0/'],
    by4: ['CC BY 4.0', 'https://creativecommons.org/licenses/by/4.0/'],
    bysa3: ['CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0/'], bysa4: ['CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'],
    by2: ['CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/'], by3: ['CC BY 3.0', 'https://creativecommons.org/licenses/by/3.0/'], cc0: ['CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'],
  };
  G.credit = (file, author, lic, done, labelled) => `Image: <a href="https://commons.wikimedia.org/wiki/File:${encodeURIComponent(file.replace(/ /g, '_'))}">${file}</a> by ${author}, <a href="${G.LIC[lic][1]}">${G.LIC[lic][0]}</a>, via Wikimedia Commons; ${done}${labelled ? '; labels added (approximate)' : ''}.`;
  /* photo with switchable labels: m = {id, file, w, h, alt, title, cap, labels: [[x, y, text], ...] (fractions), credit} */
  let ro = null; const watched = new Set(), states = new WeakMap();
  G.micro = (box, m) => {
    const f = document.createElement('figure'); f.className = 'mg' + (m.narrow ? ' narrow' : ''); f.id = 'mg-' + m.id;
    f.innerHTML = `<div class="bar"><span class="t">${m.title}</span></div>` +
      `<div class="im${m.dark ? ' dark' : ''}"><img src="img/${m.file}" width="${m.w}" height="${m.h}" loading="lazy" alt="${m.alt}"><svg viewBox="0 0 ${m.w} ${m.h}" aria-hidden="true"></svg></div>` +
      `<figcaption>${m.cap}<span class="cr">${m.credit}</span></figcaption>`;
    box.append(f);
    const st = {m, f, on: true};
    if (m.labels && m.labels.length) {
      const b = document.createElement('button'); b.className = 'chip'; b.type = 'button'; b.textContent = 'Labels'; b.setAttribute('aria-pressed', 'true');
      b.onclick = () => { st.on = !st.on; b.setAttribute('aria-pressed', String(st.on)); draw(st); };
      f.querySelector('.bar').append(b);
    }
    draw(st);
    for (const x of watched) if (!x.isConnected) { if (ro) ro.unobserve(x); watched.delete(x); }
    if (window.ResizeObserver) {
      if (!ro) ro = new ResizeObserver(es => { for (const e of es) { const s = states.get(e.target); if (s) draw(s); } });
      const im = f.querySelector('.im'); states.set(im, st); watched.add(im); ro.observe(im);
    }
    return st;
  };
  function draw(st) {
    const {m, f} = st, S = f.querySelector('svg'), wpx = Math.max(160, f.querySelector('.im').clientWidth || 400), k = m.w / wpx;
    const fs = 12.5 * k; S.style.setProperty('--mg-fs', fs.toFixed(1) + 'px'); S.style.setProperty('--mg-sw', (2.6 * k).toFixed(1) + 'px'); S.style.setProperty('--mg-lw', (1.5 * k).toFixed(1) + 'px');
    let h = ''; const boxes = [];
    if (st.on && m.labels) for (const [x, y, t] of m.labels) {
      const X = x * m.w, Y = y * m.h, tw = t.length * fs * 0.56, gap = 9 * k;
      let right = x < 0.55;
      if (right && X + gap + tw > m.w - 4) right = false;
      if (!right && X - gap - tw < 4) right = true;
      let tx = right ? X + gap : X - gap;
      tx = Math.max(4 + (right ? 0 : tw), Math.min(m.w - 4 - (right ? tw : 0), tx));
      let ty = Math.max(fs, Math.min(m.h - 4, Y + fs * 0.35));
      const x0 = right ? tx : tx - tw, x1 = right ? tx + tw : tx;
      for (let tries = 0; tries < 6; tries++) {
        const hit = boxes.find(q => x0 < q[2] && x1 > q[0] && ty - fs < q[3] && ty > q[1] - fs * 0.15);
        if (!hit) break;
        ty = Math.min(m.h - 4, hit[3] + fs * 1.15);
      }
      boxes.push([x0, ty - fs, x1, ty]);
      if (Math.abs(ty - (Y + fs * 0.35)) > fs * 0.6) h += `<line x1="${X.toFixed(1)}" y1="${Y.toFixed(1)}" x2="${tx.toFixed(1)}" y2="${(ty - fs * 0.35).toFixed(1)}"/>`;
      h += `<circle cx="${X.toFixed(1)}" cy="${Y.toFixed(1)}" r="${(4.5 * k).toFixed(1)}"/><text x="${tx.toFixed(1)}" y="${ty.toFixed(1)}" text-anchor="${right ? 'start' : 'end'}">${t}</text>`;
    }
    S.innerHTML = h;
  }
  window.AP = G;
})();
