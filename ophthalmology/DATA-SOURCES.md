# Ophthalmology — data sources and verification log

Open sources only: public-domain texts, CC-licensed open-access papers (via Europe PMC), StatPearls, EyeWiki, Wikipedia
(checked for copying). No library-licensed books are used, even ones the owner can access.

Full quotes (each ≤40 words, with how it was obtained) are in the local fact sheets, which are not in git:
`sources-local/facts/ophth-pathway.md` and `sources-local/facts/ophth-refraction.md`. Downloads are in
`sources-local/modern/ophth/`. Each publisher counts as one source (all EyeWiki pages = one; all StatPearls = one).

## 01 The Visual Pathway and Field Defects — `neuro-ophthalmology/visual-pathway.html`

| Statement on the page | Sources |
|---|---|
| Pathway order; striate cortex, area 17, calcarine sulcus | Gray 1918; PMC8053434; PMC4181645; PMC5829892; EyeWiki |
| Nasal fibres cross, temporal stay; image inverted on the retina | EyeWiki; Wikipedia; Schijns & Koehler, *Brain* 2020, PMC7089649; PMC11306754 |
| Meyer's loop (lower retina, upper field, temporal lobe); parietal fibres (lower field) | PMC7089649; PMC5829892; PMC8053434; EyeWiki; Wikipedia |
| Cuneus = lower field, lingual gyrus = upper field | PMC4181645; PMC8053434; PMC4030586; Wikipedia |
| Optic nerve → monocular loss; partial → scotoma | PMC8053434; EyeWiki |
| Junctional scotoma (ipsilateral central + contralateral superotemporal) | EyeWiki; PMC11306754; PMC11182331; Wikipedia. Wilbrand's knee disputed (Wikipedia, "Chiasmal syndrome"); page says so |
| Bitemporal hemianopia; pituitary adenoma most common, craniopharyngioma, meningioma, glioma | EyeWiki; PMC8053434; PMC11306754; StatPearls (Homonymous Hemianopsia); Wikipedia |
| From below: superotemporal first, then inferotemporal, inferonasal | EyeWiki (Pituitary Adenoma); PMC11306754 |
| From above: inferotemporal *tends* to go first | PMC11306754 ("suprachiasmal lesions"); Wikipedia (Craniopharyngioma, "may"). Medium confidence; worded "tend to" |
| Lateral chiasma → ipsilateral nasal defect; binasal usually ocular disease; carotid aneurysm | PMC8053434; PMC9209951; EyeWiki; Wikipedia. "Calcified carotid" is Wikipedia only, not used |
| Optic tract → contralateral homonymous hemianopia, incongruous if partial; RAPD in the eye with temporal loss | PMC8053434; PMC5829892; PMC4181645; EyeWiki |
| LGB: rare, sector-shaped, incongruous | PMC8053434; PMC4181645; PMC5829892; EyeWiki |
| Whole radiation → homonymous hemianopia | Wikipedia; PMC5829892 |
| Occipital → congruous hemianopia with macular sparing; "thought to be" dual PCA/MCA supply; mechanism debated | PMC8053434; EyeWiki; PMC5829892; PMC4181645; Wikipedia |
| Congruity increases posteriorly (a tendency) | PMC5829892; PMC4181645; PMC8053434 |
| Field extent ≈60° nasal, >90° temporal, ≈60° up, ≈70° down (values vary) | PMC5519947; PMC3678209; PMC8349196; Wikipedia |
| Blind spot = optic disc, ≈15° temporal, just below horizontal | EyeWiki; PMC8568268; Wikipedia; Gray 1918 |

**Left out:** 53% crossing figure (one source); junctional scotoma of Traquair (EyeWiki only); LGB sector mapping;
"Baum's loop" (a fabricated eponym). **Errors found in sources, not copied:** PMC12650385 maps Meyer's loop backwards;
PMC12568719 names a non-existent "superior geniculate nucleus"; one EyeWiki page calls Argyll Robertson pupils
"regular"; Gray 1918 is out of date on the pupil pathway.

**Schematic choices (labelled on the page):** the macular-sparing radius (5°) and central-scotoma radius (12°) are drawn
sizes, not data; sources give sparing of the central 2–10°.

- Physiology of vision (2026-11-18; fact sheet `sources-local/facts/fill-op.md`, 277 quotes, script-checked):
  retinal layers from Gray 1918 p.225 and Wikipedia; rods and cones StatPearls 29261952, PMC10828017, PMC11221215,
  Wikipedia; phototransduction PMC9790638, PMC9796346, Wikipedia; dark adaptation PMC9796346, PMC8911214, Wikipedia
  (cone plateau 5 vs 9–10 min shown); colour PMC11221215, Wikipedia. Drawings schematic; curves are bell shapes, not
  data. RPE described by structure only (its functions and the ELM wording were Wikipedia only). Source error not
  used: PMC4727664 reverses the effect of cGMP.

## 02 Pupil Reflexes — `neuro-ophthalmology/pupil-reflexes.html`

Facts from `sources-local/facts/ophth-pathway.md`, sections 5–6.

| Statement on the page | Sources |
|---|---|
| Afferent: retina → optic nerve → chiasma → tract → pretectal nucleus (not the LGB), level of superior colliculus; nasal fibres cross to the opposite pretectal nucleus | EyeWiki (Reflexes and the Eye); PMC12568719; PMC13015004; Wikipedia (Pupillary light reflex). Wikipedia's "ipsilateral pretectal nucleus" ignores the crossing: not used |
| Each pretectal nucleus → both Edinger–Westphal nuclei; direct and consensual reflexes | EyeWiki; PMC12568719; PMC5365042 (*Community Eye Health*); Wikipedia |
| Efferent: oculomotor nerve → ciliary ganglion → short ciliary nerves → sphincter pupillae | EyeWiki; PMC12568719; Gray 1918 (which calls the fibres "sympathetic", old usage) |
| Complete optic nerve lesion: light in the blind eye, neither constricts; in the other eye, both | Wikipedia; PMC12568719; EyeWiki RAPD (both constrict when the good eye is lit) |
| Oculomotor lesion: affected pupil dilated, no direct or consensual reaction; light in that eye constricts the other pupil | PMC12568719; Wikipedia; PMC13015004 |
| RAPD: asymmetric retina / optic nerve disease; swinging light: both dilate on reaching the affected eye; symmetrical disease gives no RAPD | StatPearls (Marcus Gunn Pupil); EyeWiki (two pages, one source); PMC5365042; Wikipedia |
| Near triad; near afferent route via LGB and visual cortex | EyeWiki; PMC12568719 |
| Argyll Robertson: small, irregular, usually both; little or no light reaction, brisk near; neurosyphilis; lesion thought to be dorsal rostral midbrain / pretectal; cause uncertain | EyeWiki; PMC13015004; StatPearls; PMC12568719; Wikipedia |
| Adie: dilated, usually one side; poor light reaction; slow tonic near reaction; ciliary ganglion / short ciliary nerves; dilute pilocarpine 0.1–0.125% (not specific); Holmes–Adie with reduced tendon reflexes | EyeWiki (Adie Pupil); PMC13015004; Wikipedia (Adie syndrome) |
| Optic tract lesion: RAPD in the eye with temporal field loss | EyeWiki; PMC4181645 |

**Left out (one source):** Argyll Robertson pupil size (<2 mm vs <3 mm); AR-like pupils in diabetes and other
conditions (EyeWiki only); "tabes dorsalis, general paresis" (one review); Adie pupil "becomes smaller over time" and
"aberrant reinnervation" / "post-inflammatory" cause (one source each); pupil equality in afferent defects (indirect).
**Model:** pupil sizes and reaction strengths are schematic. The near response is shown only for normal, Argyll
Robertson and Adie pupils, where the sources describe it.

**Independent review (2026-11-16):** simulation logic and pathway drawing confirmed for every condition. Fixed: the
near-response rule implied the Adie pupil is a midbrain lesion; it now says Adie's lesion is in the ciliary ganglion.
The oculomotor condition is now named "involving the pupil", since the model shows a pupil-involving palsy.

## 03 Refractive Errors — `refraction/refractive-errors.html`

| Statement on the page | Sources |
|---|---|
| Eye ≈60 D; cornea ≈43 D, two-thirds, mostly front surface (air–tear), back ≈−6 D; lens ≈18–20 D, one-third | StatPearls (Spherical Equivalent); Ozkan & Utine 2025, PMC12528774; Meek et al. 2025, PMC11885422; EyeWiki; Wikipedia |
| Axial length 23–24 mm; indices cornea 1.376, aqueous 1.336 | EyeWiki; StatPearls; Wikipedia |
| Emmetropia; dioptre = 1/f | Wikipedia; StatPearls; IMI |
| Myopia definition (−0.50 D; high −6.00 D); axial commoner; curvature/index; far point = 1/D; concave lens | IMI 2019 (*IOVS*, PMC6735818); StatPearls (Childhood Myopia); EyeWiki; Wikipedia |
| 2–3 D per mm (textbook ≈3 D; measured ≈2 D) | Wikipedia (Farsightedness); IMI 2023, PMC10153577. Disagreement shown on the page |
| Pathological myopia features; no single cut-off | StatPearls; IMI; EyeWiki |
| Hypermetropia definition; axial commonest; convex lens; latent/manifest/facultative/absolute; angle closure | StatPearls; EyeWiki; Wikipedia |
| Astigmatism: definition, regular/irregular, WTR/ATR/oblique, simple/compound/mixed, conoid of Sturm, circle of least confusion, toric and RGP lenses | StatPearls (Spherical Equivalent); PMC11826581; EyeWiki; Wikipedia |
| Accommodation (Helmholtz), near reflex | EyeWiki; StatPearls; Wikipedia |
| Amplitude ≈13 D adolescence, 10 D at 25, 6 D at 40, 2 D at 50, 1 D at 60 | Trojacka 2025, PMC12786713; Wikipedia (Dioptre). EyeWiki gives lower objective values; page says so |
| Presbyopia onset early–mid 40s; hypermetropes earlier; plus add | EyeWiki; StatPearls; Wikipedia |
| Anisometropia ≥1 D; aniseikonia ≈1% per D | EyeWiki; StatPearls (per-D figure medium confidence, worded "roughly") |
| Aphakia: high hypermetropia, no accommodation | StatPearls; Wikipedia |
| Amblyopia definition, types, critical period (≈7–10 y; treatment helps to ≈12), treatment (glasses first; patching 2 h/6 h; atropine as effective; reverse amblyopia) | EyeWiki; Wikipedia; Ibrahimi & García-Martínez 2026, PMC13204035 (Cochrane review cited) |
| LASIK / PRK / SMILE; myopic ablation flattens centre | EyeWiki; Wikipedia; PMC9745030 |
| Residual stromal bed ≥250 µm (300 µm preferred); phakic IOL, ACD ≈3 mm | EyeWiki; Wikipedia; Way et al. 2024, PMC10974391; PMC9745030; phakic IOL: StatPearls, EyeWiki, Wikipedia, PMC13431208 (chamber depth) |
| Pinhole principle | EyeWiki; StatPearls; Wikipedia |

**Left out (one source or none):** Gullstrand / reduced-eye numbers; aphakic spectacle power (+10 to +12 D) and its
magnification; "14 D at age 10"; latent hyperopia ≈1 D; 1 mm corneal radius ≈6 D; reading-add sizes by age; which
amblyopia type is commonest; minimum corneal thickness 480 µm.

**Model (labelled on the page):** a single-lens schematic eye of +60 D in a medium of index 1.336, so its relaxed length
is about 22.3 mm (shorter than a real eye, whose principal planes lie behind the cornea); the page therefore shows only
changes in length. The correcting lens is treated as if on the cornea. The eye may use all of its accommodation.

- Candidacy and contraindications (2026-11-18, `fill-op.md`): PMC12286648 (Cureus 2025), PMC10974391 (J Clin Med 2024),
  PMC13668166, Wikipedia LASIK / Refractive surgery; ranges per source with year (Eye Vis 2014, J Clin Med 2024,
  Front Ophthalmol 2026 for the EVO ICL label). SMILE: FDA approval 2016 only (its dioptre range had one source).
  Pregnancy/breastfeeding apply to corneal laser only, as in the sources. Lens exchange PMC7856935, PMC4655463; phakic
  IOL StatPearls 32809598 ("an option").

## 04 Diseases of the Optic Nerve — `neuro-ophthalmology/optic-nerve.html`

- Fact sheet `sources-local/facts/fill-op.md`. StatPearls (8 chapters); PMC13485077, PMC12938181, PMC12214357,
  PMC5398730, PMC9187153, PMC6166610, PMC10661278, PMC11510045, PMC9428633, PMC9750907, PMC12650965, PMC12178413,
  PMC5365044, PMC13260974; Wikipedia. Treatments carry their trial/guideline: ONTT 1988–91/1992, IIHTT 2014, IIH
  consensus 2018, IONDT 1995, BSR 2020, EMA 2015 (idebenone), Indian optic neuritis consensus 2026.
- Disagreements shown: fellow-eye NAION 15–25 %; pallor onset 2–6 weeks; "secondary vs consecutive" atrophy terms.
  Left out (one source): appearance of each atrophy type, chalky-white disc in arteritic AION, ICL dioptre range,
  methanol antidotes, painless onset/severe swelling as atypical neuritis features. Source error not used:
  PMC10661278 says P100 latency is "reduced" in optic neuritis.
- Photos (Wikimedia Commons, licence read on each file page): Häggström (CC0), Trobe (CC BY 3.0), Manaviat et al.
  (CC BY 2.0).
- Independent review (2026-11-18), fixed: SMILE range removed; RPE function removed; neuritis onset "over days";
  atypical features cut to those with two sources; LASIK/PRK ranges separated; phakic IOL "an option"; pregnancy
  limited to laser; NAION advice and GCA wording; PMR "associated"; idebenone "EMA, disease-specific"; toxic
  neuropathy and primary atrophy wording; normal fundus caption; ONTT MS figure attributed.

## Independent review (2026-11-16)

A separate reviewer agent checked both pages against EyeWiki and Europe PMC, without reading the fact sheets first.

- **Visual pathway:** all lesion logic, fibre colouring and field conventions confirmed. Changed: LGB defects "may be
  congruous or incongruous" (Luco 1992, PMID 1548490: vascular LGB lesions "moderately to completely congruent";
  Shacklett 1984, PMID 6476052: one congruous, one incongruous; PMC5829892 had said incongruous); pituitary order now
  "classically"; lateral-chiasma cause now "internal carotid artery pressing on it, e.g. an aneurysm".
- **Refractive errors:** facts confirmed. Fixed: astigmatism type was named from where the rays landed (so a corrected
  eye was called "simple hypermetropic"); it is now named from each meridian's own error. Sliders now show each
  meridian's refractive error (minus = focuses in front). Hypermetropia, emmetropia and presbyopia messages corrected
  for every lens / near / cycloplegia combination (all 40 checked in a headless browser). Model D/mm now "2.3–3.1".
  Amblyopia "cannot be explained *solely* by a structural abnormality"; atropine as effective "for moderate amblyopia";
  anisometropia "commonly defined as 1 D or more".
- **Not independently re-verified by the reviewer** (kept, each has two sources in the fact sheet): phakic IOL chamber
  depth ≈3 mm; aniseikonia ≈1% per D; "nearer 2 D/mm" in progressing myopia.
