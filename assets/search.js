/* Site search: <div class="sitesearch" data-index="search-index.json" data-base=""></div> + this script.
 * The index (tools/home/search_index.py) is fetched on first focus. A query matches page titles, section headings,
 * 3D topics, key terms and 3D part names; results open the page, or the section when a heading matched. */
(() => {
  const css = `.sitesearch{position:relative}
.sitesearch input{width:100%;box-sizing:border-box;font:500 16px var(--f-body,system-ui);padding:11px 14px 11px 38px;
  border:1px solid var(--line,#ccd);border-radius:10px;background:var(--surface,#fff);color:var(--ink,#111)}
.sitesearch input:focus{outline:2px solid var(--accent,#2c56cc);outline-offset:1px}
.sitesearch .ico{position:absolute;left:13px;top:12px;width:16px;height:16px;color:var(--muted,#667);pointer-events:none}
.sitesearch .res{list-style:none;margin:6px 0 0;padding:0;border:1px solid var(--line,#ccd);border-radius:10px;
  background:var(--surface,#fff);max-height:min(60vh,520px);overflow:auto}
.sitesearch .res:empty{display:none}
.sitesearch .res li{border-bottom:1px solid var(--line,#ccd)}
.sitesearch .res li:last-child{border-bottom:0}
.sitesearch .res a{display:block;padding:10px 14px;text-decoration:none;color:var(--ink,#111)}
.sitesearch .res a:hover,.sitesearch .res a:focus,.sitesearch .res a.on{background:var(--bg,#f4f5f8)}
.sitesearch .res .t{font-weight:600}
.sitesearch .res .s{font-size:12px;color:var(--muted,#667);margin-left:6px}
.sitesearch .res .m{display:block;font-size:13.5px;color:var(--muted,#667);margin-top:2px}
.sitesearch .res mark{background:none;color:var(--accent,#2c56cc);font-weight:600}
.sitesearch .none{padding:10px 14px;color:var(--muted,#667);font-size:14px}`;
  const st = document.createElement('style'); st.textContent = css; document.head.append(st);
  const esc = s => s.replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[’']/g, "'");
  for (const box of document.querySelectorAll('.sitesearch')) {
    const base = box.dataset.base || '', idxUrl = box.dataset.index || 'search-index.json';
    box.innerHTML = `<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input type="search" placeholder="${esc(box.dataset.placeholder || 'Search topics, structures, conditions…')}" aria-label="Search the site" autocomplete="off">
      <ul class="res" role="listbox"></ul>`;
    const inp = box.querySelector('input'), ul = box.querySelector('.res');
    let idx = null, loading = null, sel = -1;
    const load = () => loading || (loading = fetch(base + idxUrl).then(r => r.json()).then(j => {
      idx = j.map(p => ({...p, nt: norm(p.t), nd: norm(p.d), nh: p.h.map(h => norm(h[0])), nk: p.k.map(norm), nw: p.w.map(norm)}));
    }).catch(() => { idx = []; }));
    const hi = (text, words) => { let h = esc(text);
      for (const w of words) if (w.length > 1) h = h.replace(new RegExp('(' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>');
      return h; };
    function search(q) {
      const words = norm(q).split(/\s+/).filter(Boolean); if (!words.length || !idx) return [];
      const has = s => words.every(w => s.includes(w));
      const out = [];
      for (const p of idx) {
        let score = 0, match = null, anchor = '';
        if (has(p.nt)) score = 100 + (p.nt.startsWith(words[0]) ? 10 : 0);
        p.nh.forEach((h, i) => { if (has(h) && score < 70) { score = 70; match = p.h[i][0]; anchor = p.h[i][1]; } });
        p.nk.forEach((k, i) => { if (has(k) && score < 55) { score = 55 + (k === words.join(' ') ? 10 : 0); match = '3D: ' + p.k[i]; } });
        p.nw.forEach((w, i) => { if (has(w)) { const sc = 40 + (w === words.join(' ') ? 15 : 0) + (w.startsWith(words[0]) ? 8 : 0) - Math.min(10, w.length / 8);
          if (sc > score) { score = sc; match = p.w[i]; } } });
        if (!score && has(p.nd)) { score = 20; match = p.d.slice(0, 140); }
        if (score) out.push({p, score, match, anchor});
      }
      return out.sort((a, b) => b.score - a.score).slice(0, 25).map(r => ({...r, words}));
    }
    function render() {
      const q = inp.value.trim(); sel = -1;
      if (!q) { ul.innerHTML = ''; return; }
      const rs = search(q);
      ul.innerHTML = rs.length ? rs.map(r => `<li><a href="${esc(base + r.p.u + (r.anchor ? '#' + r.anchor : ''))}">` +
        `<span class="t">${hi(r.p.t, r.words)}</span><span class="s">${esc(r.p.s)}</span>` +
        (r.match ? `<span class="m">${hi(r.match, r.words)}</span>` : '') + '</a></li>').join('')
        : `<li class="none">Nothing found for “${esc(q)}”.</li>`;
    }
    inp.addEventListener('focus', load);
    inp.addEventListener('input', () => { if (idx) render(); else load().then(render); });
    inp.addEventListener('keydown', e => {
      const as = [...ul.querySelectorAll('a')]; if (!as.length) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + as.length) % as.length;
        as.forEach((a, i) => a.classList.toggle('on', i === sel)); as[sel].scrollIntoView({block: 'nearest'}); }
      else if (e.key === 'Enter') { e.preventDefault(); location.href = as[Math.max(sel, 0)].href; }
      else if (e.key === 'Escape') { inp.value = ''; render(); }
    });
  }
})();
