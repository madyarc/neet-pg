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
  /* one ResizeObserver for all micrographs; figures removed from the page (chip changes) are unobserved and forgotten */
  let ro = null; const watched = new Set(), states = new WeakMap();
  const prune = () => { for (const x of watched) if (!x.isConnected) { if (ro) ro.unobserve(x); watched.delete(x); } };
  H.prune = prune;
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
    draw(st);
    prune();
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
  H.credit = (c) => `Image: <a href="https://commons.wikimedia.org/wiki/File:${encodeURIComponent(c.file.replace(/ /g, '_'))}">${c.file}</a> by ${c.author}, <a href="${c.licUrl}">${c.lic}</a>, via Wikimedia Commons; ${c.done}; labels added (approximate).`;
  /* ---- added for the organ pages (respiratory-digestive, urinary-reproductive, endocrine-senses-cns) ---- */
  /* legend HTML from [[cssVar, label, opacity], ...] */
  H.keyHTML = items => items.map(([c, l, o]) => `<span><i style="background:var(${c})${o ? ';opacity:' + o : ''}"></i>${l}</span>`).join('');
  /* label in a schematic (mono, outlined) */
  H.lab = (s, x, y, t, a = 'start', size = 9.5) => H.text(s, x, y, t, {'text-anchor': a, class: 'lab', style: `font-size:${size * H.SM}px`});
  /* Wall of a hollow organ, lumen at the top, drawn from a spec (schematic, not to scale):
     w = {parts: [{x0, x1, epi, surf, glands, goblet}], vh (villus height), lp (lamina propria depth), mm (muscularis mucosae),
          sub (submucosa depth), subf: ['mucous'|'brunner'|'peyer'|'lymph'|'cart'|'plates'|'seromucous'],
          me: [[kind 'smooth'|'skel'|'mixed', dir 'circ'|'long'|'obl'|'spiral'|'bundles'|'taenia', h, label]], outer: 'serosa'|'adventitia', labels: extra [y, text]}
     epi: 'sq' stratified squamous, 'col' simple columnar, 'resp' pseudostratified ciliated, 'trans' transitional, 'pst' pseudostratified with stereocilia, 'cil' ciliated columnar.
     surf: 'flat', 'villi', 'leaf', 'short', 'folds', 'branch' (branched folds).
     glands: 'fundic', 'pyloric', 'cardiac', 'crypts', 'crypts-few'. Returns legend items. */
  H.wall = (s, w) => {
    s.replaceChildren();
    const el = H.el, W = 250, keys = [], used = new Set();
    const key = (c, l, o) => { if (!used.has(l)) { used.add(l); keys.push([c, l, o]); } };
    const vh = w.vh || 0, lp = w.lp || 30, top = 18 + vh, yLP = top + lp, mm = w.mm || 0, sub = w.sub || 0;
    const ySub0 = yLP + mm, ySub1 = ySub0 + sub;
    const labs = [];
    const L = (y, t) => labs.push([y, t]);
    const EPW = {sq: 13, col: 6, resp: 8, trans: 10, pst: 8, cil: 6, cub: 5};
    const EPN = {sq: 'Stratified squamous epithelium', col: 'Simple columnar epithelium', resp: 'Pseudostratified ciliated epithelium', trans: 'Transitional epithelium (urothelium)', pst: 'Pseudostratified epithelium with stereocilia', cil: 'Ciliated columnar epithelium', cub: 'Cuboidal epithelium'};
    /* connective tissue under everything */
    el('rect', {x: 0, y: top - 2, width: W, height: ySub1 - top + 2, fill: 'var(--collagen)', opacity: .28}, s);
    for (const p of w.parts) {
      const x0 = p.x0 ?? 0, x1 = p.x1 ?? W, ew = EPW[p.epi] || 6;
      /* surface outline */
      let d = `M${x0} ${top}`;
      if (p.surf === 'villi' || p.surf === 'leaf' || p.surf === 'short') {
        const sp = p.surf === 'leaf' ? 40 : 26, vw = p.surf === 'leaf' ? 26 : 12, h = p.surf === 'short' ? vh * 0.55 : vh;
        for (let x = x0 + 6; x + vw < x1; x += sp) d += ` L${x} ${top} L${x} ${top - h + vw / 2} a${vw / 2} ${vw / 2} 0 0 1 ${vw} 0 L${x + vw} ${top}`;
      } else if (p.surf === 'folds' || p.surf === 'branch') {
        for (let x = x0; x + 40 <= x1; x += 40) d += ` Q${x + 10} ${top} ${x + 14} ${top - vh * 0.9} Q${x + 20} ${top - vh * 1.05} ${x + 26} ${top - vh * 0.9} Q${x + 30} ${top} ${x + 40} ${top}`;
      }
      d += ` L${x1} ${top}`;
      el('path', {d: d + ` L${x1} ${yLP} L${x0} ${yLP} Z`, fill: 'var(--collagen)', opacity: .45}, s);
      if (p.surf === 'branch') for (let x = x0; x + 40 <= x1; x += 40) for (const dx of [-9, 9]) el('path', {d: `M${x + 20} ${top - vh * 0.5} l${dx} ${-vh * 0.3}`, stroke: 'var(--cyto)', 'stroke-width': 5, 'stroke-linecap': 'round'}, s);
      /* glands in the lamina propria */
      const g = p.glands;
      if (g) {
        const fund = g === 'fundic', pyl = g === 'pyloric', card = g === 'cardiac', few = g === 'crypts-few';
        const step = few ? 34 : fund ? 16 : (pyl || card) ? 22 : 18;
        for (let x = x0 + 9; x < x1 - 4; x += step) {
          if (p.surf === 'villi' || p.surf === 'leaf' || p.surf === 'short') { /* crypts open between villi */ }
          const pit = fund ? lp * 0.25 : pyl ? lp * 0.55 : card ? lp * 0.4 : lp - 6;
          el('rect', {x: x - 3.5, y: top, width: 7, height: pit, fill: 'var(--cyto)'}, s);
          el('line', {x1: x, y1: top, x2: x, y2: top + pit, stroke: 'var(--surface)', 'stroke-width': 1}, s);
          if (fund) {
            el('rect', {x: x - 3.5, y: top + pit, width: 7, height: lp - pit - 4, fill: 'var(--zym)'}, s);
            for (let yy = top + pit + 4; yy < top + lp * 0.7; yy += 9) el('circle', {cx: x + ((yy / 9) % 2 > 1 ? 3 : -3), cy: yy, r: 3, fill: 'var(--eosin)'}, s);
            key('--eosin', 'Parietal (oxyntic) cells, eosin-stained (Gray)'); key('--zym', 'Chief (zymogenic) cells');
          } else if (pyl || card) {
            for (const [dx, dy] of [[-4, 4], [4, 7], [-3, 12], [5, 15]]) el('circle', {cx: x + dx, cy: top + pit + dy, r: 3.6, fill: 'var(--mucin)', stroke: 'var(--ink)', 'stroke-width': .4}, s);
            key('--mucin', pyl ? 'Pyloric glands (mucous cells: Wikipedia)' : 'Cardiac glands (like pyloric glands, Gray)');
          } else {
            const gob = p.goblet || 2;
            for (let k = 0; k < gob; k++) el('ellipse', {cx: x + (k % 2 ? 2.5 : -2.5), cy: top + 5 + k * (pit - 8) / Math.max(1, gob - 1), rx: 2, ry: 2.8, fill: 'var(--mucin)'}, s);
            key('--mucin', 'Goblet cells (mucus)');
          }
        }
        if (fund || pyl || card) key('--cyto', 'Gastric pits (surface mucous cells)');
      }
      el('path', {d, fill: 'none', stroke: 'var(--cyto)', 'stroke-width': ew, 'stroke-linejoin': 'round'}, s);
      if (p.epi === 'sq') el('path', {d, fill: 'none', stroke: 'var(--nucleus)', 'stroke-width': 1, 'stroke-dasharray': '1 5', transform: 'translate(0 2)'}, s);
      if (p.epi === 'resp' || p.epi === 'cil') el('path', {d, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 3, 'stroke-dasharray': '.6 1.6', transform: `translate(0 ${-ew / 2 - 1.5})`, opacity: .7}, s);
      if (p.epi === 'pst') el('path', {d, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 4, 'stroke-dasharray': '.6 3', transform: `translate(0 ${-ew / 2 - 2})`, opacity: .6}, s);
      if (p.epi === 'trans') el('path', {d, fill: 'none', stroke: 'var(--cyto)', 'stroke-width': 3, 'stroke-dasharray': '6 2', transform: `translate(0 ${-ew / 2 - 1})`}, s);
      if (p.goblet && !g) for (let x = x0 + 12; x < x1 - 6; x += 30) el('ellipse', {cx: x, cy: top, rx: 2.2, ry: 3, fill: 'var(--mucin)'}, s);
      key('--cyto', EPN[p.epi]);
      if (p.lab) L(top - vh * 0.5, p.lab);
    }
    const EPS = {sq: 'stratified squamous', col: 'simple columnar', resp: 'pseudostratified ciliated', trans: 'transitional epithelium', pst: 'pseudostrat. + stereocilia', cil: 'ciliated columnar', cub: 'cuboidal epithelium'};
    L(Math.max(top, 26) + (vh ? -vh / 2 : 0), w.epiLab ?? (w.parts.length > 1 ? '' : EPS[w.parts[0].epi]));
    L(top + lp * 0.55, w.lpLab || 'lamina propria');
    key('--collagen', 'Connective tissue', .45);
    if (mm) { el('rect', {x: 0, y: yLP, width: W, height: mm, fill: 'var(--t-musc)'}, s); L(yLP + mm / 2 + 3, w.mmLab || 'muscularis mucosae'); key('--t-musc', 'Smooth muscle'); }
    /* submucosa features */
    const f = w.subf || [];
    if (sub) {
      for (const k of f) {
        if (k === 'mucous' || k === 'seromucous' || k === 'brunner') {
          const n = k === 'brunner' ? 9 : 3;
          for (let i = 0; i < n; i++) {
            const cx = 20 + i * (k === 'brunner' ? 26 : 80) + (k === 'brunner' ? 0 : 20), cy = ySub0 + sub * (k === 'brunner' ? 0.4 : f.includes('cart') || f.includes('plates') ? 0.2 : 0.55);
            for (const [dx, dy] of [[-6, 0], [6, 0], [0, -6], [0, 6], [0, 0]]) el('circle', {cx: cx + dx, cy: cy + dy, r: 4, fill: k === 'seromucous' && (dx + dy) % 12 ? 'var(--zym)' : 'var(--mucin)', stroke: 'var(--ink)', 'stroke-width': .4}, s);
            if (k !== 'brunner' || i % 3 === 0) el('line', {x1: cx, y1: cy - 8, x2: cx, y2: top, stroke: 'var(--cyto)', 'stroke-width': 2}, s);
          }
          key('--mucin', k === 'brunner' ? 'Duodenal (Brunner\'s) glands' : 'Mucous glands');
          if (k === 'seromucous') key('--zym', 'Serous cells');
          L(ySub0 + sub * (f.includes('cart') || f.includes('plates') ? 0.2 : 0.45), k === 'brunner' ? 'Brunner\'s glands' : k === 'seromucous' ? 'seromucous glands' : 'mucous glands');
        }
        if (k === 'peyer' || k === 'lymph') {
          const xs = k === 'peyer' ? [70, 150] : [30, 95, 160, 222];  /* last follicle kept inside the 250-wide wall, clear of the label column */
          for (const cx of xs) { el('ellipse', {cx, cy: yLP + 2, rx: k === 'peyer' ? 34 : 26, ry: k === 'peyer' ? sub * 0.55 : lp * 0.5, fill: 'var(--lymph)', opacity: .9}, s); el('circle', {cx, cy: yLP, r: 9, fill: 'var(--gc)'}, s); }
          key('--lymph', 'Lymphoid follicles'); key('--gc', 'Germinal centre');
          L(yLP + 4, k === 'peyer' ? 'Peyer\'s patch' : 'lymphoid follicles');
        }
        if (k === 'cart' || k === 'plates') {
          const y0 = ySub0 + sub * 0.42, h = sub * 0.5;
          if (k === 'cart') el('rect', {x: 0, y: y0, width: W * 0.72, height: h, rx: 6, fill: 'var(--cart)', stroke: 'var(--perich)', 'stroke-width': 2}, s);
          else for (const x of [10, 120]) el('rect', {x, y: y0, width: 80, height: h, rx: 10, fill: 'var(--cart)', stroke: 'var(--perich)', 'stroke-width': 2}, s);
          for (let i = 0; i < 14; i++) { const x = (k === 'cart' ? 10 : 18 + (i > 6 ? 110 : 0)) + (i % 7) * (k === 'cart' ? 24 : 10); el('circle', {cx: x, cy: y0 + h / 2 + (i % 2 ? 5 : -5), r: 2, fill: 'var(--nucleus)'}, s); }
          key('--cart', 'Hyaline cartilage');
          L(y0 + h / 2, k === 'cart' ? 'C-shaped hyaline cartilage' : 'cartilage plates');
          if (k === 'cart') { el('rect', {x: W * 0.74, y: y0, width: W * 0.26, height: h, fill: 'var(--t-musc)'}, s); L(y0 + h / 2 + 12, 'trachealis (gap of the C)'); key('--t-musc', 'Smooth muscle'); }
        }
      }
      if (w.subLab !== '') L(ySub0 + sub * (f.length ? 0.85 : 0.5), w.subLab || 'submucosa');
    }
    /* muscle coats */
    let y = ySub1;
    for (const [kind, dir, h, lab] of (w.me || [])) {
      const col = kind === 'skel' ? 'var(--fibre)' : 'var(--t-musc)';
      if (dir === 'taenia') {
        el('rect', {x: 0, y, width: W, height: 3, fill: col}, s); el('rect', {x: 80, y, width: 90, height: h, rx: 3, fill: col}, s);
        for (let x = 86; x < 168; x += 8) for (let yy = y + 4; yy < y + h - 2; yy += 6) el('circle', {cx: x, cy: yy, r: 1.3, fill: 'var(--surface)', opacity: .7}, s);
      } else {
        if (kind === 'mixed') { el('rect', {x: 0, y, width: W / 2, height: h, fill: 'var(--fibre)'}, s); el('rect', {x: W / 2, y, width: W / 2, height: h, fill: 'var(--t-musc)'}, s); }
        else el('rect', {x: 0, y, width: W, height: h, fill: col}, s);
        if (dir === 'circ') for (let yy = y + 3; yy < y + h - 1; yy += 4) el('line', {x1: 0, y1: yy, x2: W, y2: yy, stroke: 'var(--surface)', 'stroke-width': .5, opacity: .6}, s);
        else if (dir === 'long') for (let x = 4; x < W; x += 8) for (let yy = y + 3; yy < y + h - 1; yy += 5) el('circle', {cx: x + (yy % 2) * 3, cy: yy, r: 1.2, fill: 'var(--surface)', opacity: .7}, s);
        else if (dir === 'obl' || dir === 'spiral') for (let x = -h; x < W; x += 9) el('line', {x1: x, y1: y + h, x2: x + h, y2: y, stroke: 'var(--surface)', 'stroke-width': .6, opacity: .6}, s);
        else if (dir === 'bundles') { el('rect', {x: 0, y, width: W, height: h, fill: 'var(--collagen)', opacity: .5}, s); for (let x = 6; x + 20 <= W; x += 30) el('rect', {x, y: y + 3, width: 20, height: h - 6, rx: 5, fill: col}, s); }
      }
      key(kind === 'skel' ? '--fibre' : '--t-musc', kind === 'skel' ? 'Skeletal muscle' : 'Smooth muscle');
      if (kind === 'mixed') { key('--fibre', 'Skeletal muscle'); key('--t-musc', 'Smooth muscle'); }
      L(y + h / 2 + 3, lab); y += h;
    }
    if (w.outer === 'serosa') { el('rect', {x: 0, y, width: W, height: 5, fill: 'var(--collagen)', opacity: .5}, s); el('rect', {x: 0, y: y + 5, width: W, height: 2.5, fill: 'var(--cyto)'}, s); L(y + 6, 'serosa (peritoneum)'); y += 8; }
    if (w.outer === 'adventitia') { el('rect', {x: 0, y, width: W, height: 14, fill: 'var(--collagen)', opacity: .6}, s); L(y + 10, 'adventitia'); y += 14; }
    H.lab(s, 4, 11, w.lumen || 'lumen', 'start', 9);
    for (const [ly, t] of w.labels || []) L(ly, t);
    /* labels in the right-hand column, pushed apart */
    labs.filter(l => l[1]).sort((a, b) => a[0] - b[0]).reduce((prev, [ly, t]) => { const yy = Math.max(ly, prev + 11.5 * H.SM); H.lab(s, W + 6, yy, t, 'start', 9); return yy; }, 0);
    s.setAttribute('viewBox', `0 0 400 ${Math.max(y + 6, labs.length * 11.5 * H.SM + 12)}`);
    return keys;
  };
  /* widen the viewBox so that no label is clipped (labels grow on phones, H.SM) */
  H.fit = svg => {
    try {
      const v = svg.viewBox.baseVal, bb = svg.getBBox(), pad = 3;
      const x0 = Math.min(v.x, bb.x - pad), y0 = Math.min(v.y, bb.y - pad), x1 = Math.max(v.x + v.width, bb.x + bb.width + pad), y1 = Math.max(v.y + v.height, bb.y + bb.height + pad);
      svg.setAttribute('viewBox', `${x0.toFixed(1)} ${y0.toFixed(1)} ${(x1 - x0).toFixed(1)} ${(y1 - y0).toFixed(1)}`);
    } catch (e) { /* not rendered yet */ }
  };
  /* An organ chooser: chips + drawing + legend + text + micrographs.
     o = {chips, svg, key, text, micro, items: [{k, name, ident, text, micros: [ids], draw(svg) -> legend items, none: 'why no micrograph'}], mk(box, id)} */
  H.organs = o => {
    const aria = o.svg.getAttribute('aria-label') || '';
    const pick = k => {
      const it = o.items.find(x => x.k === k);
      const keys = it.draw ? it.draw(o.svg, it) : [];
      H.fit(o.svg);
      o.svg.setAttribute('aria-label', `Schematic of ${it.name}${/lumen at the top/.test(aria) ? ': wall with the lumen at the top' : ''} (not to scale)`);
      if (o.key) o.key.innerHTML = H.keyHTML(keys || []);
      o.text.innerHTML = `<p class="ident"><b>Identify by:</b> ${it.ident}</p>` + (it.text ? `<p>${it.text}</p>` : '');
      o.micro.replaceChildren(); prune();
      for (const id of it.micros || []) o.mk(o.micro, id);
      if (!(it.micros || []).length) o.micro.innerHTML = `<p class="muted">${it.none || 'No usable open micrograph was found; see the drawing.'}</p>`;
      H.pressed(o.chips, k);
    };
    H.chips(o.chips, o.items.map(x => [x.k, x.name]), pick); pick(o.items[0].k);
    return pick;
  };
  window.Histo = H;
})();
