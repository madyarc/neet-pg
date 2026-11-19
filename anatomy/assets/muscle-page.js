/* NEET-PG — shared logic for the regional muscle pages (upper limb, lower limb, …).
 *
 * A page provides the DATA and calls
 *   MusclePage({
 *     base: '../models/<group>-muscles/', manifest: '<group>-muscles.json',
 *     DATA: {lede, based, models}, GROUPS: [[key, name]], NERVES: {key: [name, '--n-token']}, NERVE_TEXT: {key: html},
 *     M: {key: [group, origin, insertion, nerveKey, nerveText, action, note]},
 *     home: [x, y, z] (optional view direction, default front), glassBones: true (a selection keeps only the bones it
 *     attaches to solid: for packed regions such as the head, where the skull hides deep muscles), ghost: alpha of the rest,
 *     keepSolid: {group: [parts kept solid when one of its muscles is selected]}, view: {muscle: [x, y, z] view direction on selection}, tint: {partKey: '--token'} (context parts not drawn as bone: '--cart', '--soft'),
 *     extra: {key: 'wrist', parts: [keys of connective parts shown in that tab], build(api), enter(api)}   // optional 3rd tab
 *       (optional: colours: {partKey: '--token'} for extra parts that are not fascia, e.g. vessels loaded later with
 *       api.v.loadPart; leave(api): called when the reader leaves that tab)
 *   })
 * The page HTML has: #v #views #lede #based #models, tabs #tab-muscles #tab-nerves #tab-<extra>, panes #pane-…,
 * #detail #groups (muscles tab), #nerve-desc #nerve-list (nerves tab).
 * Attachment areas (attachments.json, from tools/zanat/areas.py) are drawn on the bones in --ori / --ins.
 * By bone (added to the muscles pane, before #groups): pick a bone in the list or tap it on the model to see all the
 * drawn areas on it, named, with the muscles listed (only muscles with checked facts; nothing new beyond the areas).
 */
'use strict';
function MusclePage(cfg) {
  const {M, GROUPS, NERVES, NERVE_TEXT = {}, DATA, extra} = cfg;
  const $ = id => document.getElementById(id);
  const v = new AtlasViewer($('v'));
  v.ghostAlpha = cfg.ghost || 0.12; window.atlas = v;   // for tests
  const card = v.addOverlay(document.createElement('div')); card.className = 'selcard'; card.hidden = true;
  let names = {}, colours = {}, attach = {}, tab = 'muscles', sel = null, group = null;
  const tabs = ['muscles', 'nerves'].concat(extra ? [extra.key] : []);
  const extraParts = new Set(extra ? extra.parts : []);
  const isMuscle = k => k in M, isFascia = k => extraParts.has(k);
  const BONES = () => v.order.filter(k => !isMuscle(k) && !isFascia(k));
  const LIMB = () => v.order.filter(k => !k.startsWith('ax_'));   // framing ignores the axial context bones
  for (const [label, dir] of [['Front', [0, -1, 0]], ['Lateral', [-1, 0, 0]], ['Back', [0, 1, 0]], ['Medial', [1, 0, 0]]]) {
    const b = document.createElement('button'); b.className = 'btn'; b.textContent = label;
    b.onclick = () => v.face(dir, {zoom: v.zoom}); $('views').append(b);
  }
  const pressed = (s, test) => document.querySelectorAll(s).forEach(b => b.setAttribute('aria-pressed', test(b.dataset.k)));
  const nerveOf = k => M[k] && M[k][3];
  const groupName = g => GROUPS.find(x => x[0] === g)[1];
  const GROUPS_KEYS = g => Object.keys(M).filter(k => M[k][0] === g && v.parts.has(k));

  function paint() {
    for (const k of v.order) {
      v.setVertexMarks(k, null);
      if (isMuscle(k)) v.setColour(k, tab === 'nerves' ? (nerveOf(k) ? NERVES[nerveOf(k)][1] : '--line') : (colours[k] || '--line'));
      else if (isFascia(k)) { v.setColour(k, (extra.colours || {})[k] || '--fascia'); v.setVisible(k, extra && tab === extra.key); }
      else v.setColour(k, (cfg.tint || {})[k] || '--bone');
    }
  }
  const focusOn = (keys, solid) => v.setFocus(keys ? keys.concat(cfg.glassBones ? (solid || []) : BONES()) : null);
  const clearRows = () => document.querySelectorAll('table.t tr[data-k]').forEach(r => r.setAttribute('aria-pressed', 'false'));

  function showDetail(k) {
    const d = $('detail');
    if (!k) { d.innerHTML = `<p class="cap key">${group ? `<b>${groupName(group)}.</b> Tap a muscle on the model or in the list.` : 'Tap a muscle on the model or in the list, or a group to frame it.'}</p>`; return; }
    const m = M[k], g = groupName(m[0]);
    if (m.length < 3) { d.innerHTML = `<h2>${names[k]}</h2><p class="sub">${g}</p><p class="pending">The facts for this muscle are still being checked in two sources.</p>`; return; }
    const [, ori, ins, nk, ntext, act, note] = m;
    const hasA = attach[k] && attach[k].length;
    const left = '<span class="pending">Left out (only one source).</span>';
    d.innerHTML = `<h2>${names[k]}</h2><p class="sub">${g}</p>
      <dl class="facts">
        <dt><span class="swatch" style="background:var(--ori)"></span>Origin</dt><dd>${ori || left}</dd>
        <dt><span class="swatch" style="background:var(--ins)"></span>Insertion</dt><dd>${ins || left}</dd>
        <dt><span class="swatch" style="background:var(${NERVES[nk][1]})"></span>Nerve</dt><dd>${ntext}</dd>
        <dt>Action</dt><dd>${act}</dd>
        ${note ? `<dt>Note</dt><dd>${note}</dd>` : ''}
      </dl>
      <p class="note">${hasA ? 'On the bones: origin in blue, insertion in orange. The areas are approximate, and only those that fit the model well are drawn.' : 'Its attachment areas are not drawn: the model does not show them reliably.'}</p>`;
  }
  function select(k, frame = false) {
    leaveBone();
    if (sel && v.parts.has(sel)) v.setVisible(sel, true);
    if (!k) { sel = null; card.hidden = true; pressed('.mlist button', () => false); paint(); focusOn(group ? GROUPS_KEYS(group) : null); if (tab === 'muscles') showDetail(null); return; }
    sel = k;
    pressed('.mlist button', x => x === k);
    paint();
    const byBone = {};
    for (const a of attach[k] || []) (byBone[a.bone] = byBone[a.bone] || []).push({verts: a.verts, colour: a.kind === 'ori' ? '--ori' : '--ins'});
    for (const b in byBone) v.setVertexMarks(b, byBone[b]);
    const ctx = ((cfg.keepSolid || {})[M[k] && M[k][0]] || []).filter(x => v.parts.has(x));
    focusOn([k], Object.keys(byBone).concat(ctx));
    if (frame) { v.fit([k].concat((attach[k] || []).map(a => a.bone), ctx)); if (cfg.view && cfg.view[k]) v.face(cfg.view[k], {zoom: 1}); }
    card.hidden = false;
    const hasA = attach[k] && attach[k].length;
    card.innerHTML = `<div class="what"><b>${names[k]}</b><span>${M[k] ? (tab === 'nerves' ? NERVES[nerveOf(k) || 'two'][0] : groupName(M[k][0])) : ''}</span></div>${hasA ? '<button class="go" id="peek" aria-pressed="false">See the bone</button>' : ''}<button class="x" aria-label="Clear">×</button>`;
    card.querySelector('.x').onclick = () => select(null);
    const peek = card.querySelector('#peek');
    if (peek) peek.onclick = () => { const on = peek.getAttribute('aria-pressed') !== 'true'; peek.setAttribute('aria-pressed', on);
      peek.textContent = on ? 'Show the muscle' : 'See the bone'; v.setVisible(k, !on); };
    if (tab === 'muscles') showDetail(k);
  }
  function buildGroups() {
    const box = $('groups'); box.replaceChildren();
    for (const [g, gname] of GROUPS) {
      const ks = GROUPS_KEYS(g); if (!ks.length) continue;
      const h = document.createElement('button'); h.className = 'group-h'; h.style.cssText = 'background:none;border:0;padding:0;cursor:pointer;text-align:left';
      h.textContent = gname + ' →'; h.onclick = () => { group = g; select(null); v.fit(ks); };
      const list = document.createElement('div'); list.className = 'mlist';
      for (const k of ks) {
        const b = document.createElement('button'); b.dataset.k = k; b.setAttribute('aria-pressed', 'false');
        b.innerHTML = `<i style="background:${colours[k] || '#999'}"></i>${names[k]}`;
        b.onclick = () => select(k, true);
        list.append(b);
      }
      box.append(h, list);
    }
  }
  function buildNerves() {
    const box = $('nerve-list'); box.replaceChildren();
    for (const [nk, [name, tok]] of Object.entries(NERVES)) {
      const ks = Object.keys(M).filter(k => nerveOf(k) === nk && v.parts.has(k));
      if (!ks.length) continue;
      const b = document.createElement('button'); b.dataset.k = nk; b.setAttribute('aria-pressed', 'false');
      b.innerHTML = `<i style="background:var(${tok})"></i><span>${name}</span><span class="n">${ks.length}</span>`;
      b.onclick = () => {
        leaveBone();
        if (sel && v.parts.has(sel)) v.setVisible(sel, true);
        pressed('#nerve-list button', x => x === nk); sel = null; card.hidden = true;
        $('nerve-desc').innerHTML = `<b>${name}.</b> ${NERVE_TEXT[nk] || ''} <span class="note">Muscles: ${ks.map(k => names[k]).join(', ')}.</span>`;
        focusOn(ks); v.fit(ks);
      };
      box.append(b);
    }
  }
  /* ---- by bone: pick a bone, see every drawn attachment area on it (origin / insertion) and the muscles ---- */
  let boneIdx = {}, bone = null;
  const css = t => getComputedStyle(document.documentElement).getPropertyValue(t).trim();
  function indexBones() {
    boneIdx = {};
    for (const k of Object.keys(attach)) {
      if (!M[k] || M[k].length < 3 || !v.parts.has(k)) continue;   // only muscles whose facts are checked and shown
      for (const a of attach[k]) if (v.parts.has(a.bone) && a.verts && a.verts.length) (boneIdx[a.bone] = boneIdx[a.bone] || []).push({k, kind: a.kind, verts: a.verts});
    }
  }
  function leaveBone() {
    if (!bone) return;
    bone = null; v.setMarkers(null);
    for (const k of v.order) if (isMuscle(k)) v.setVisible(k, true);
    const s = $('bone-pick'); if (s) s.value = '';
  }
  function areaPoint(m, verts) {   // the vertex of the area nearest its centroid (stays on the surface), and the mean normal
    const c = [0, 0, 0], n = [0, 0, 0];
    for (const i of verts) for (let j = 0; j < 3; j++) { c[j] += m.pos[i * 3 + j]; n[j] += m.nrm[i * 3 + j]; }
    for (let j = 0; j < 3; j++) c[j] /= verts.length;
    let best = verts[0], bd = 1e18;
    for (const i of verts) { const d = (m.pos[i * 3] - c[0]) ** 2 + (m.pos[i * 3 + 1] - c[1]) ** 2 + (m.pos[i * 3 + 2] - c[2]) ** 2; if (d < bd) { bd = d; best = i; } }
    const L = Math.hypot(n[0], n[1], n[2]) || 1;   // lift the point 1.5 mm off the surface, so a label on the far side of a thin bone hides
    return {p: [0, 1, 2].map(j => m.pos[best * 3 + j] + n[j] / L * 1.5), n};
  }
  function showBone(b) {
    if (sel && v.parts.has(sel)) v.setVisible(sel, true);
    leaveBone(); sel = null; group = null; pressed('.mlist button', () => false);
    if (!b || !boneIdx[b]) { select(null); return; }
    bone = b; const list = boneIdx[b], s = $('bone-pick'); if (s) s.value = b;
    paint();
    v.setVertexMarks(b, list.map(a => ({verts: a.verts, colour: a.kind === 'ori' ? '--ori' : '--ins'})));
    const ks = [...new Set(list.map(a => a.k))];
    for (const k of v.order) if (isMuscle(k)) v.setVisible(k, false);
    v.setFocus([b]);
    const part = v.parts.get(b), marks = [], dir = [0, 0, 0];
    for (const a of list) {
      const {p, n} = areaPoint(part.m, a.verts);
      for (let j = 0; j < 3; j++) dir[j] += n[j];
      marks.push({p, label: names[a.k], color: css(a.kind === 'ori' ? '--ori' : '--ins')});
    }
    v.setMarkers(marks);
    v.fit([b]);
    const h = Math.hypot(dir[0], dir[1]);
    v.face(h > 1e-3 ? [dir[0], dir[1], Math.max(-h, Math.min(h, dir[2])) * 0.6] : (cfg.home || [0, -1, 0]), {zoom: 0.85});
    card.hidden = false;
    card.innerHTML = `<div class="what"><b>${names[b]}</b><span>${ks.length} muscle${ks.length > 1 ? 's' : ''} with drawn areas</span></div><button class="go" id="peek" aria-pressed="false">Show the muscles</button><button class="x" aria-label="Clear">×</button>`;
    card.querySelector('.x').onclick = () => { leaveBone(); select(null); };
    const peek = card.querySelector('#peek');
    peek.onclick = () => { const on = peek.getAttribute('aria-pressed') !== 'true'; peek.setAttribute('aria-pressed', on);
      peek.textContent = on ? 'Hide the muscles' : 'Show the muscles';
      for (const k of ks) v.setVisible(k, on); v.setFocus(on ? [b].concat(ks) : [b]); };
    const btn = k => `<button data-k="${k}" aria-pressed="false"><i style="background:${colours[k] || '#999'}"></i>${names[k]}</button>`;
    const of = kind => [...new Set(list.filter(a => a.kind === kind).map(a => a.k))];
    const ori = of('ori'), ins = of('ins');
    const d = $('detail');
    d.innerHTML = `<h2>${names[b]}</h2><p class="sub">Muscle attachments on this bone</p>
      ${ori.length ? `<p class="cap"><span class="swatch" style="background:var(--ori)"></span> <b>Origins</b></p><div class="mlist">${ori.map(btn).join('')}</div>` : ''}
      ${ins.length ? `<p class="cap"><span class="swatch" style="background:var(--ins)"></span> <b>Insertions</b></p><div class="mlist">${ins.map(btn).join('')}</div>` : ''}
      <p class="note">Origin areas in blue, insertion areas in orange; each is named on the model where it faces you (turn the bone to see the rest). The areas are approximate, and only those that fit the model well are drawn, so a muscle whose area was left out is not listed here: see its own card. Tap a muscle to open it.</p>`;
    d.querySelectorAll('.mlist button').forEach(x => x.onclick = () => select(x.dataset.k, true));
  }
  function buildBones() {
    indexBones();
    const pane = $('pane-muscles'), groups = $('groups');
    if (!pane || !groups || !Object.keys(boneIdx).length) return;
    const old = $('bybone'); if (old) old.remove();
    const box = document.createElement('div'); box.id = 'bybone'; box.className = 'stack'; box.style.gap = '6px';
    const opts = v.order.filter(k => boneIdx[k]).map(k => `<option value="${k}">${names[k]} (${new Set(boneIdx[k].map(a => a.k)).size})</option>`).join('');
    box.innerHTML = `<label class="group-h" for="bone-pick">By bone: all the attachments on one bone</label>
      <select id="bone-pick" style="font:500 13.5px var(--f-body);color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:6px 8px;max-width:100%;width:100%"><option value="">Pick a bone (or tap one on the model)</option>${opts}</select>`;
    pane.insertBefore(box, groups);
    box.querySelector('select').onchange = e => { if (e.target.value) showBone(e.target.value); else { leaveBone(); select(null); } };
  }
  function setTab(name) {
    leaveBone();
    if (extra && extra.leave && tab === extra.key && name !== extra.key) extra.leave(api);
    if (sel && v.parts.has(sel)) v.setVisible(sel, true);
    tab = name; sel = null; group = null; card.hidden = true;
    for (const t of tabs) { $('tab-' + t).setAttribute('aria-pressed', t === name); $('pane-' + t).hidden = t !== name; }
    document.querySelectorAll('[aria-pressed][data-k]').forEach(b => b.setAttribute('aria-pressed', 'false')); clearRows();
    paint(); focusOn(null);
    const home = cfg.home || [0, -1, 0];   // the direction the model is first seen from (the back page: from behind)
    if (name === 'muscles') { showDetail(null); v.fit(LIMB()); v.face(home, {zoom: 1}); }
    if (name === 'nerves') { $('nerve-desc').innerHTML = 'Each muscle is coloured by the nerve that supplies it. Tap a nerve.'; v.fit(LIMB()); v.face(home, {zoom: 1}); }
    if (extra && name === extra.key) extra.enter(api);
  }
  for (const t of tabs) $('tab-' + t).onclick = () => setTab(t);
  v.onPick = hit => {
    if (!hit) { select(null); return; }
    if (isMuscle(hit.key)) { if (extra && tab === extra.key) setTab('muscles'); select(hit.key); }
    else if (tab === 'muscles' && boneIdx[hit.key]) showBone(hit.key);   // a bone: all its attachments
  };
  const api = {v, focusOn, pressed, clearRows, setTab, LIMB, has: k => v.parts.has(k), names: () => names, showBone};
  (async () => {
    $('lede').innerHTML = DATA.lede; $('based').innerHTML = DATA.based; $('models').innerHTML = DATA.models;
    const [c, a] = await Promise.all([fetch(cfg.base + 'colours.json').then(r => r.json()),
      fetch(cfg.base + 'attachments.json').then(r => r.ok ? r.json() : {}).catch(() => ({}))]);
    colours = c.colours; attach = a;
    const man = await v.load(cfg.base + cfg.manifest);
    for (const p of man.parts) names[p.key] = p.name;
    buildGroups(); buildNerves(); buildBones(); if (extra) extra.build(api);
    setTab('muscles');
    window.ready = true;
  })().catch(e => { $('detail').textContent = 'Could not load the 3D model: ' + e.message; window.loadError = String(e); });
  return api;
}
