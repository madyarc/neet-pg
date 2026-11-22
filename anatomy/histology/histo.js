/* Shared helpers for the histology pages: micrographs with toggleable labels, chips, tables, SVG drawing. */
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const H = {};
  H.$ = id => document.getElementById(id);
  /* schematic label scale: larger on phones */
  H.SM = window.matchMedia && matchMedia('(max-width:600px)').matches ? 1.25 : 1;
  H.el = (tag, a = {}, parent) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); if (parent) parent.append(e); return e; };
  H.text = (s, x, y, t, a = {}) => { const e = H.el('text', Object.assign({x, y}, a), s); e.textContent = t; return e; };
  H.pressed = (box, key) => box.querySelectorAll('[data-k]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.k === key)));
  H.chips = (box, list, onPick) => {
    for (const [k, name] of list) {
      const b = document.createElement('button'); b.className = 'chip'; b.dataset.k = k; b.setAttribute('aria-pressed', 'false');
      b.textContent = name; b.onclick = () => onPick(k); box.append(b);
    }
  };
  /* table: heads = column names, rows = arrays of cells (HTML); first cell bold; data-h for the phone layout */
  H.table = (t, heads, rows, keys) => {
    t.classList.add('t', 'stack');
    const head = heads.some(h => h) ? '<tr>' + heads.map(h => `<th>${h}</th>`).join('') + '</tr>' : '';
    if (!head) t.classList.add('nohead');
    t.onkeydown = e => { const r = e.target.closest && e.target.closest('tr[data-k]'); if (r && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); r.click(); } };
    t.innerHTML = head + rows.map((r, j) =>
      `<tr${keys ? ` data-k="${keys[j]}" aria-pressed="false" tabindex="0"` : ''}>` + r.map((c, i) => `<td data-h="${i ? heads[i] : ''}">${i === 0 ? '<b>' + c + '</b>' : c}</td>`).join('') + '</tr>').join('');
  };
  /* micrograph: m = {id, file, w, h, alt, title, cap, labels: [[x, y, text], ...] (fractions of the image), credit} */
  const figs = [];
  H.micro = (box, m) => {
    const f = document.createElement('figure'); f.className = 'mg'; f.id = 'mg-' + m.id;
    f.innerHTML = `<div class="bar"><span class="t">${m.title}</span></div>` +
      `<div class="im"><img src="img/${m.file}" width="${m.w}" height="${m.h}" loading="lazy" alt="${m.alt}"><svg viewBox="0 0 ${m.w} ${m.h}" aria-hidden="true"></svg></div>` +
      `<figcaption>${m.cap}<span class="cr">${m.credit}</span></figcaption>`;
    box.append(f);
    const st = {m, f, on: true, sel: null};
    if (m.labels && m.labels.length) {
      const b = document.createElement('button'); b.className = 'chip'; b.textContent = 'Labels'; b.setAttribute('aria-pressed', 'true');
      b.onclick = () => { st.on = !st.on; b.setAttribute('aria-pressed', String(st.on)); draw(st); };
      f.querySelector('.bar').append(b);
    }
    figs.push(st); draw(st);
    if (window.ResizeObserver) new ResizeObserver(() => draw(st)).observe(f.querySelector('.im'));
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
  H.credit = (c) => `Image: <a href="https://commons.wikimedia.org/wiki/File:${encodeURIComponent(c.file.replace(/ /g, '_'))}">${c.file}</a> by ${c.author}, <a href="${c.licUrl}">${c.lic}</a>, via Wikimedia Commons; ${c.done}; labels added (approximate).`;
  window.Histo = H;
})();
