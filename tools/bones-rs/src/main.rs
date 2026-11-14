//! bones — mesh pipeline for the NEET-PG anatomy pages.
//!
//! `bones build <config.json>` reads BodyParts3D OBJ meshes straight from the zip archives, merges duplicate
//! vertices, simplifies each part to an absolute error limit (mm), computes normals, and writes one compact
//! binary per part plus a manifest (JSON) with bounding boxes and the contacts between parts (vertices of one
//! part lying within `contact_mm` of another — these are the sutures / joint surfaces and give the
//! neighbour graph used for colouring).
//!
//! Coordinates stay in the BodyParts3D body frame (mm: +x toward the body's left, +y posterior, +z up), so
//! parts built separately assemble without any transform.
//!
//! Binary format "NPM1" (little endian):
//!   b"NPM1", u32 nverts, u32 ntris, f32 lo[3], f32 span, u32 index_bytes (2|4),
//!   u16 pos[nverts*3] (lo + q/65535*span), i8 nrm[nverts*3] (/127), pad to 4, u16|u32 idx[ntris*3]

use anyhow::{Context, Result, anyhow, bail};
use base64::Engine;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::io::{Read, Write};
use std::path::{Path, PathBuf};

#[derive(Deserialize)]
struct Config {
    /// name of the group, e.g. "skull"; the manifest is written as <out>/<name>.json
    name: String,
    /// zip archives searched in order for each part's OBJ files
    zips: Vec<PathBuf>,
    out: PathBuf,
    /// simplification error limit in mm (absolute); 0 = no simplification
    #[serde(default)]
    error_mm: f32,
    /// optional cap on triangles per part (simplification stops at whichever comes first)
    #[serde(default)]
    max_tris: Option<usize>,
    #[serde(default = "default_contact")]
    contact_mm: f32,
    parts: Vec<PartCfg>,
}
fn default_contact() -> f32 { 1.5 }

#[derive(Deserialize, Clone)]
struct PartCfg {
    key: String,
    name: String,
    /// FMA id of the part (recorded in the manifest)
    fma: String,
    /// OBJ file names (without .obj) inside the zip: BodyParts3D element ids (FJ...) or FMA ids
    files: Vec<String>,
}

#[derive(Serialize)]
struct PartOut {
    key: String,
    name: String,
    fma: String,
    file: String,
    nverts: usize,
    ntris: usize,
    source_tris: usize,
    error_mm: f32,
    bbox: [[f32; 3]; 2],
    bytes: usize,
}

#[derive(Serialize)]
struct ContactOut {
    a: String,
    b: String,
    /// number of vertices of a / of b within contact distance of the other part
    na: usize,
    nb: usize,
    /// base64 of u32 LE vertex indices (into the simplified meshes)
    va: String,
    vb: String,
}

#[derive(Serialize)]
struct Manifest {
    name: String,
    source: String,
    contact_mm: f32,
    parts: Vec<PartOut>,
    contacts: Vec<ContactOut>,
}

struct Mesh {
    pos: Vec<[f32; 3]>,
    idx: Vec<u32>,
}

fn parse_obj(text: &str) -> Result<Mesh> {
    let mut pos = Vec::new();
    let mut idx = Vec::new();
    for line in text.lines() {
        let mut it = line.split_whitespace();
        match it.next() {
            Some("v") => {
                let v: Vec<f32> = it.take(3).map(|s| s.parse::<f32>()).collect::<Result<_, _>>()?;
                if v.len() != 3 { bail!("bad vertex line: {line}"); }
                pos.push([v[0], v[1], v[2]]);
            }
            Some("f") => {
                let f: Vec<u32> = it
                    .map(|s| s.split('/').next().unwrap().parse::<i64>())
                    .collect::<Result<Vec<_>, _>>()?
                    .into_iter()
                    .map(|i| if i < 0 { (pos.len() as i64 + i) as u32 } else { (i - 1) as u32 })
                    .collect();
                for k in 1..f.len().saturating_sub(1) { idx.extend_from_slice(&[f[0], f[k], f[k + 1]]); }
            }
            _ => {}
        }
    }
    Ok(Mesh { pos, idx })
}

/// merge vertices at identical positions (to 1 µm) and drop degenerate triangles
fn weld(m: Mesh) -> Mesh {
    let mut map: HashMap<[i64; 3], u32> = HashMap::new();
    let mut pos = Vec::new();
    let remap: Vec<u32> = m.pos.iter().map(|p| {
        let key = [(p[0] * 1000.0).round() as i64, (p[1] * 1000.0).round() as i64, (p[2] * 1000.0).round() as i64];
        *map.entry(key).or_insert_with(|| { pos.push(*p); (pos.len() - 1) as u32 })
    }).collect();
    let mut idx = Vec::with_capacity(m.idx.len());
    for t in m.idx.chunks_exact(3) {
        let (a, b, c) = (remap[t[0] as usize], remap[t[1] as usize], remap[t[2] as usize]);
        if a != b && b != c && a != c { idx.extend_from_slice(&[a, b, c]); }
    }
    Mesh { pos, idx }
}

fn simplify(m: &Mesh, error_mm: f32, max_tris: Option<usize>) -> Result<Mesh> {
    let bytes: &[u8] = unsafe { std::slice::from_raw_parts(m.pos.as_ptr() as *const u8, m.pos.len() * 12) };
    let adapter = meshopt::VertexDataAdapter::new(bytes, 12, 0).map_err(|e| anyhow!("{e:?}"))?;
    let target = max_tris.map(|t| (t * 3).min(m.idx.len())).unwrap_or(0);
    let mut idx = if error_mm > 0.0 {
        meshopt::simplify(&m.idx, &adapter, target, error_mm, meshopt::SimplifyOptions::ErrorAbsolute, None)
    } else { m.idx.clone() };
    idx = meshopt::optimize_vertex_cache(&idx, m.pos.len());
    let mut pos = m.pos.clone();
    let pos = meshopt::optimize_vertex_fetch(&mut idx, &mut pos);
    Ok(Mesh { pos, idx })
}

fn normals(m: &Mesh) -> Vec<[f32; 3]> {
    let mut n = vec![[0f32; 3]; m.pos.len()];
    for t in m.idx.chunks_exact(3) {
        let (a, b, c) = (m.pos[t[0] as usize], m.pos[t[1] as usize], m.pos[t[2] as usize]);
        let u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]];
        let v = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
        let f = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
        for &i in t { for k in 0..3 { n[i as usize][k] += f[k]; } }
    }
    for v in n.iter_mut() {
        let l = (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]).sqrt().max(1e-12);
        for k in 0..3 { v[k] /= l; }
    }
    n
}

fn bbox(pos: &[[f32; 3]]) -> [[f32; 3]; 2] {
    let mut lo = [f32::MAX; 3];
    let mut hi = [f32::MIN; 3];
    for p in pos { for k in 0..3 { lo[k] = lo[k].min(p[k]); hi[k] = hi[k].max(p[k]); } }
    [lo, hi]
}

fn encode(m: &Mesh) -> Vec<u8> {
    let [lo, hi] = bbox(&m.pos);
    let span = (0..3).map(|k| hi[k] - lo[k]).fold(0f32, f32::max).max(1e-6);
    let ib: u32 = if m.pos.len() < 65536 { 2 } else { 4 };
    let mut out = Vec::new();
    out.extend_from_slice(b"NPM1");
    for v in [m.pos.len() as u32, (m.idx.len() / 3) as u32] { out.extend_from_slice(&v.to_le_bytes()); }
    for v in [lo[0], lo[1], lo[2], span] { out.extend_from_slice(&v.to_le_bytes()); }
    out.extend_from_slice(&ib.to_le_bytes());
    for p in &m.pos {
        for k in 0..3 {
            let q = (((p[k] - lo[k]) / span) * 65535.0).round().clamp(0.0, 65535.0) as u16;
            out.extend_from_slice(&q.to_le_bytes());
        }
    }
    for n in normals(m) { for k in 0..3 { out.push(((n[k] * 127.0).round() as i8) as u8); } }
    while out.len() % 4 != 0 { out.push(0); }
    for &i in &m.idx {
        if ib == 2 { out.extend_from_slice(&(i as u16).to_le_bytes()); } else { out.extend_from_slice(&i.to_le_bytes()); }
    }
    out
}

/// uniform grid over a point set, for "any point within d" queries
struct Grid { cell: f32, map: HashMap<[i32; 3], Vec<u32>> }
impl Grid {
    fn new(pos: &[[f32; 3]], cell: f32) -> Grid {
        let mut map: HashMap<[i32; 3], Vec<u32>> = HashMap::new();
        for (i, p) in pos.iter().enumerate() { map.entry(Self::key(p, cell)).or_default().push(i as u32); }
        Grid { cell, map }
    }
    fn key(p: &[f32; 3], cell: f32) -> [i32; 3] { [(p[0] / cell).floor() as i32, (p[1] / cell).floor() as i32, (p[2] / cell).floor() as i32] }
    fn any_within(&self, pos: &[[f32; 3]], p: &[f32; 3], d: f32) -> bool {
        let k = Self::key(p, self.cell);
        for dx in -1..=1 { for dy in -1..=1 { for dz in -1..=1 {
            if let Some(v) = self.map.get(&[k[0] + dx, k[1] + dy, k[2] + dz]) {
                for &i in v {
                    let q = pos[i as usize];
                    if (q[0] - p[0]).powi(2) + (q[1] - p[1]).powi(2) + (q[2] - p[2]).powi(2) <= d * d { return true; }
                }
            }
        }}}
        false
    }
}

fn read_from_zips(zips: &[PathBuf], file: &str) -> Result<String> {
    for z in zips {
        let f = std::fs::File::open(z).with_context(|| format!("open {}", z.display()))?;
        let mut ar = zip::ZipArchive::new(f)?;
        let name = (0..ar.len()).find_map(|i| {
            let n = ar.by_index(i).ok()?.name().to_string();
            let base = n.rsplit(['/', '\\']).next().unwrap_or(&n);
            (base == format!("{file}.obj")).then_some(n)
        });
        if let Some(n) = name {
            let mut s = String::new();
            ar.by_name(&n)?.read_to_string(&mut s)?;
            return Ok(s);
        }
    }
    bail!("{file}.obj not found in any zip")
}

fn build(cfg_path: &Path) -> Result<()> {
    let cfg: Config = serde_json::from_str(&std::fs::read_to_string(cfg_path)?)?;
    let base = cfg_path.parent().unwrap_or(Path::new("."));
    let zips: Vec<PathBuf> = cfg.zips.iter().map(|z| base.join(z)).collect();
    let out = base.join(&cfg.out);
    std::fs::create_dir_all(&out)?;

    // read + weld + simplify each part (in parallel)
    let meshes: Vec<(PartCfg, Mesh, usize)> = cfg.parts.par_iter().map(|p| -> Result<_> {
        let mut all = Mesh { pos: vec![], idx: vec![] };
        for f in &p.files {
            let m = parse_obj(&read_from_zips(&zips, f)?).with_context(|| format!("parse {f}"))?;
            let off = all.pos.len() as u32;
            all.pos.extend(m.pos);
            all.idx.extend(m.idx.iter().map(|i| i + off));
        }
        let m = weld(all);
        let src = m.idx.len() / 3;
        let s = simplify(&m, cfg.error_mm, cfg.max_tris)?;
        Ok((p.clone(), s, src))
    }).collect::<Result<_>>()?;

    let mut parts = Vec::new();
    for (p, m, src) in &meshes {
        let bytes = encode(m);
        let file = format!("{}.bin", p.key);
        std::fs::File::create(out.join(&file))?.write_all(&bytes)?;
        parts.push(PartOut {
            key: p.key.clone(), name: p.name.clone(), fma: p.fma.clone(), file,
            nverts: m.pos.len(), ntris: m.idx.len() / 3, source_tris: *src, error_mm: cfg.error_mm,
            bbox: bbox(&m.pos), bytes: bytes.len(),
        });
        eprintln!("{:<28} {:>7} -> {:>7} tris  {:>8} bytes", p.key, src, m.idx.len() / 3, bytes.len());
    }

    // contacts between every pair of parts whose boxes come within contact distance
    let d = cfg.contact_mm;
    let grids: Vec<Grid> = meshes.par_iter().map(|(_, m, _)| Grid::new(&m.pos, d.max(0.5))).collect();
    let boxes: Vec<[[f32; 3]; 2]> = meshes.iter().map(|(_, m, _)| bbox(&m.pos)).collect();
    let pairs: Vec<(usize, usize)> = (0..meshes.len()).flat_map(|i| (i + 1..meshes.len()).map(move |j| (i, j)))
        .filter(|&(i, j)| (0..3).all(|k| boxes[i][0][k] - d <= boxes[j][1][k] && boxes[j][0][k] - d <= boxes[i][1][k]))
        .collect();
    let b64 = base64::engine::general_purpose::STANDARD;
    let near = |a: usize, b: usize| -> Vec<u32> {
        meshes[a].1.pos.iter().enumerate()
            .filter(|(_, p)| grids[b].any_within(&meshes[b].1.pos, p, d))
            .map(|(i, _)| i as u32).collect()
    };
    let mut contacts: Vec<ContactOut> = pairs.par_iter().filter_map(|&(i, j)| {
        let va = near(i, j);
        if va.is_empty() { return None; }
        let vb = near(j, i);
        let enc = |v: &[u32]| b64.encode(v.iter().flat_map(|x| x.to_le_bytes()).collect::<Vec<u8>>());
        Some(ContactOut { a: meshes[i].0.key.clone(), b: meshes[j].0.key.clone(), na: va.len(), nb: vb.len(), va: enc(&va), vb: enc(&vb) })
    }).collect();
    contacts.sort_by(|x, y| (x.a.as_str(), x.b.as_str()).cmp(&(y.a.as_str(), y.b.as_str())));
    for c in &contacts { eprintln!("contact {:<22} {:<22} {:>6} {:>6}", c.a, c.b, c.na, c.nb); }

    let man = Manifest {
        name: cfg.name.clone(),
        source: "BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan".into(),
        contact_mm: d, parts, contacts,
    };
    std::fs::write(out.join(format!("{}.json", cfg.name)), serde_json::to_string(&man)?)?;
    Ok(())
}

/// `bones list <zip>`: print the OBJ names in an archive (to find element ids)
fn list(zip_path: &Path) -> Result<()> {
    let mut ar = zip::ZipArchive::new(std::fs::File::open(zip_path)?)?;
    for i in 0..ar.len() { println!("{}", ar.by_index(i)?.name()); }
    Ok(())
}

fn main() -> Result<()> {
    let args: Vec<String> = std::env::args().collect();
    match args.get(1).map(String::as_str) {
        Some("build") if args.len() == 3 => build(Path::new(&args[2])),
        Some("list") if args.len() == 3 => list(Path::new(&args[2])),
        _ => { eprintln!("usage: bones build <config.json> | bones list <zip>"); std::process::exit(2) }
    }
}
