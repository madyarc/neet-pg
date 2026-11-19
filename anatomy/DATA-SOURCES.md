# Anatomy — data sources and verification log

## 3D models

- **BodyParts3D 4.0**, The Database Center for Life Science (DBCLS). README:
  https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/README_e.html (updated Feb 2025, says CC BY 4.0).
  The OBJ file headers say CC BY-SA 2.1 Japan; we follow the stricter (share-alike) licence. Files used:
  `partof_BP3D_4.0_obj_99.zip` (99 % polygon reduction), parts list `partof_parts_list_e.txt`,
  element list `partof_element_parts.txt`.

## Femur — `lower-limb/femur.html`

**Mesh:** `FJ3365.obj` = right femur (FMA24474, BP10053). 1574 vertices, 3102 triangles; 466 mm tall in the model
frame. Fitted head radius 23.0 mm. Left femur on the page = the right mesh mirrored.
Built with `tools/bones/build_femur.py`; landmark points found from the shape, checked by eye on the check image
(anterior / medial / posterior / lateral views) and in the page.

**Sources for every statement on the page**

| Topic | Source |
|---|---|
| Head (direction, fovea position, ligament of the head), neck (≈125° in the adult; wider in infancy; nearer a right angle in the female; forward projection 12–14° on average; vascular foramina) | Gray's *Anatomy of the Human Body*, 20th ed. (1918), "The Femur" — text via the Internet Archive copy of bartleby.com/107/59.html |
| Greater trochanter (≈1 cm lower than the head; gluteus medius on the diagonal impression of the lateral surface; gluteus minimus on the lateral part of the anterior border; piriformis on the upper border; obturator internus + gemelli above and in front of the trochanteric fossa; obturator externus in the fossa; vastus lateralis from the inferior border) | Gray's 1918, femur |
| Lesser trochanter (psoas major on the summit; iliacus between the pectineal line and the medial ridge; pectineus on the pectineal line) | Gray's 1918, femur |
| Intertrochanteric line (iliofemoral ligament on the upper half; vastus medialis from the lower half) and crest (quadratus femoris at the middle) | Gray's 1918, femur |
| Linea aspera and its prolongations: gluteus maximus (gluteal tuberosity), adductor magnus (linea aspera, lateral prolongation above, medial below to the adductor tubercle), adductor longus + brevis and iliacus + pectineus between adductor magnus and vastus medialis, short head of biceps between vastus lateralis and adductor magnus below; nutrient canal below the centre, directed upward; popliteal surface and popliteal artery | Gray's 1918, femur |
| Vastus intermedius (upper three-fourths of anterior and lateral surfaces); articularis genu | Gray's 1918, femur |
| Lower end: condyles (lateral more prominent and broader; medial longer, lower with the shaft vertical; same plane in the natural oblique position), patellar surface (lateral part broader and higher), intercondylar fossa (ACL: upper back of lateral wall; PCL: lower front of medial wall), epicondyles (tibial and fibular collateral ligaments), adductor tubercle, gastrocnemius heads, plantaris, popliteus (depression below the lateral epicondyle; oblique groove in flexion, vertical in extension) | Gray's 1918, femur |
| Siding rules (head up, medially and a little forward; linea aspera behind; condyles project backward) | Gray's 1918, femur |
| Ossification: 5 centres; shaft ≈7th fetal week (earliest of the long bones except the clavicle); lower end 9th fetal month; head end of 1st year; greater trochanter 4th year; lesser trochanter 13th–14th year; union in reverse order, lower end not until the 20th year | Gray's 1918, femur, "Ossification" |
| Medial circumflex femoral artery gives most of the supply to the head and neck via posterior retinacular arteries; often torn in neck fractures and hip dislocation; avascular necrosis | Moore, *Clinically Oriented Anatomy*, 8th ed. (2018), p. 713, as cited in Wikipedia "Medial circumflex femoral artery" (read 2026-11-14) |
| Head articulates with the acetabulum; artery of the ligament of the head becomes crucial after a neck fracture | Wikipedia "Femur" and "Femoral head" (text from Gray's 1918 and Saladin), read 2026-11-14 |

**Not stated on the page (could not verify here):** capsule attachment on the front of the neck, intracapsular vs
extracapsular fracture terms, the level of the lower epiphyseal line, the medicolegal use of the lower-end centre. Add
them only with a source (Gray's hip-joint chapter, BD Chaurasia, a forensic text).

**Checks done (2026-11-14):** headless Chromium (playwright): no console errors in light/dark at 1200 and 400 px, no
sideways scroll; all 18 landmarks visible when selected; all 30 attachment areas visible when selected; find-it quiz
hits all 18 landmarks when tapped at the marker.

## Skull — `head-neck/skull.html`

**Sources.** Every statement is checked in two places: Gray's *Anatomy of the Human Body*, 20th ed. (1918), chapters
"The Skull" (bartleby.com/107/30), each bone (107/31–45), "The Exterior of the Skull" (107/46) and "The Interior of the
Skull" (107/47), read from the Internet Archive copy; and the Wikipedia article on each bone, each suture, the pterion,
asterion, bregma, lambda, nasion, the middle meningeal artery and each cranial fossa (read 2026-11-14, plain-text API).
Correction: the local copy fetched as "Asterion" was the mythology article; the asterion definition was re-checked
against StatPearls "Anatomy, Head and Neck: Asterion" and Wikipedia "Asterion (anatomy)" — confirmed.
Local copies in `sources-local/text/` (not in git).

OpenStax *Anatomy and Physiology 2e* was read once and then dropped: its licence page forbids ingestion by AI systems
without permission. Nothing from it is used.

**Disagreements and how they were settled**

| Point | Gray 1918 | Wikipedia / other | On the page |
|---|---|---|---|
| Lambdoid suture | between the parietals and the occipital; continues below as the occipitomastoid suture (occipital–mastoid temporal) | same | Gray's wording. (OpenStax said "occipital to parietal and temporal" — loose.) |
| Parts of the temporal bone | five: squama, petrous, mastoid, tympanic, styloid process | four: squamous, mastoid, petrous, tympanic | "four parts … plus the styloid process (which Gray counts as a fifth part)" |
| Parts of the ethmoid | four: cribriform plate, perpendicular plate, two lateral masses | three: cribriform plate, labyrinth, perpendicular plate | the parts named without a count |
| Lacrimal bone | "the smallest and most fragile bone of the face" | "small and fragile" | "small and fragile" |
| Mandible | "largest and strongest bone of the face" | "strongest bone of the facial skeleton"; "only movable bone" | "strongest bone of the face and the only movable bone of the skull" |
| Pterion position | ~3 cm behind the frontozygomatic region | 2.6 cm behind, 1.3 cm above the frontozygomatic suture | no distance given |
| Pterion definition | the point at the posterior end of the sphenoparietal suture | the region where frontal, parietal, temporal and sphenoid join | both given |
| Superior/middle conchae part of the ethmoid | yes (middle concha explicit) | not stated in the articles read | not stated; the inferior concha is "the lowest of the three nasal conchae" |
| Sphenoid "like a bat" | Gray's simile | not in Wikipedia | left out |

**Single-source points (kept because the second source is derived from the first):** the cranial-fossa descriptions —
Wikipedia's fossa articles reproduce Gray's text. Contents (frontal lobes; temporal lobes and pituitary; cerebellum,
pons, medulla) are in both.

**Clinical point:** pterion — anterior branch of the middle meningeal artery beneath it; weakest part of the skull;
fracture may tear the artery → extradural (epidural) haematoma: Wikipedia "Pterion" and "Middle meningeal artery".
Gray 1918 does not discuss it in these chapters. Independent second source: StatPearls, "Neuroanatomy, Middle
Meningeal Arteries" (statpearls.com/point-of-care/25132) and "Anatomy, Head and Neck, Skull" (NCBI Bookshelf NBK499834) —
the anterior branch runs beneath the pterion; rupture, most often there, typically gives an epidural haematoma.

**Whole-body model (2026-11-14 update):** sternum (manubrium, body, xiphoid process) and costal cartilages 1–7 added
from BodyParts3D 4.0 (partof); cartilages are drawn in the cartilage colour. BodyParts3D has no 8th–10th costal
cartilages, so the lower costal margin is open in the model (said in the footer).

**Model:** BodyParts3D 3.0 (95 % polygon reduction) meshes for the 22 bones and the hyoid, simplified by
`tools/bones-rs` (absolute error limit in the config). Bone colours: `tools/bones/assign_colours.py` (Paul Tol "light"
palette; bones that touch never share a colour). Sutures = vertices of two named bones within `contact_mm` of each other,
outer surface only (`tools/bones/skull_points.py`); points = where the named bones meet. The inion (external occipital
protuberance) is NOT shown: the simple rule ("most posterior midline point") finds the opisthocranion region instead.

**Independent review (2026-11-14):** a separate reviewer checked every statement against Gray and Wikipedia: no
anatomical errors; 9 wording issues, all fixed — colour note (colours do repeat), clivus (sphenoid body + basilar
occipital: Wikipedia "Posterior cranial fossa", "Occipital bone"), chiasmatic groove in the anterior/middle fossa
boundaries (Gray 47), ear ossicles not counted in the 22 (Wikipedia "Skull"), "bony" nasal septum, lacrimal as Gray's
"smallest and most fragile" (attributed to Gray), pterion caveat (sphenoparietal suture can be absent — Gray 46),
superior and middle conchae belong to the ethmoid (Gray 36; Wikipedia "Inferior nasal concha"). Single-source kept:
hyoid "touches no other bone" (Wikipedia "Hyoid bone"; Gray says only that it hangs by ligaments).

**Skull model choice (2026-11-14):** BodyParts3D 3.0 (95 %) and 4.0 (99 %) skull meshes are almost the same shape (4.0
is a cleaned copy); 3.0 has slightly finer surface detail and is used (1.0 MB for the 23 parts at 0.15 mm error).
Neither models the small foramina: the sphenoid has one opening per side, at the base of the lateral pterygoid plate,
where Gray places the foramen ovale; rotundum, spinosum, optic canal etc. are not holes in the mesh. Foramina will be
shown as labelled markers at text-checked positions, never as invented holes.

## Bones of the Skull — `head-neck/skull-bones.html`

**Sources.** Gray 1918, chapter on each bone (bartleby 107/31–45, with 46 and 47), and the Wikipedia article on each
bone. Fact sheets with verbatim quotes from both (every quote checked as an exact substring of the source text) are in
`sources-local/facts/` (not in git). Much of Wikipedia's bone text is copied from Gray, so "in both" is often not
independent; every statement was therefore also checked by an independent reviewer against StatPearls (NCBI
Bookshelf) and recent papers (2026-11-14).

**Independent review (2026-11-14):** no factual errors; about 30 exam-relevant statements confirmed (articulation counts,
contents of the optic canal, superior orbital fissure, rotundum, hypoglossal canal, stylomastoid foramen, foramen
magnum, mandibular/mental/infraorbital foramina, muscle and ligament attachments, hyoid articulating with no bone).
Fixed: (1) metopic suture — Gray "obliterated by the eighth year", modern: closes in infancy (StatPearls
"Trigonocephaly", NBK565874); both given. (2) spheno-occipital fusion — Gray 18–25 years, modern CT: usually adolescence
(PubMed 35141949; PMC7731241); both given. (3) foramen ovale — accessory meningeal artery and lesser petrosal nerve
added (Gray 35; StatPearls "Skull Foramen", NBK545298). (4) foramen spinosum — meningeal branch of the mandibular nerve
added (Gray 35/47). (5) internal acoustic meatus — "labyrinthine artery" (modern name of Gray's internal auditory
artery; StatPearls NBK544288). (6) maxillary sinus first appears earlier than Gray's fourth month (PMC9544638); both
given. (7) anterior fontanelle — StatPearls 13–24 months (NBK542197) beside Gray's year and a half. (8) mandibular angle
at birth — Gray 175°, StatPearls about 160° (NBK532292); both given.

**Single-source (Gray) points kept** (old descriptive anatomy, no modern disagreement found): frontal eminence 3 cm above
the supraorbital margin; supraorbital notch at the medial/intermediate third junction; lacrimal fossa of the frontal;
optic canal between the roots of the lesser wing; crista galli, cribriform plate, middle concha; external acoustic
meatus; ossification details of the nasal, palatine, vomer; parietal single centre (some texts say two).

**Disagreements noted on the page:** temporal parts (Gray 5 / Wikipedia 4); ethmoid articulations (Gray 15 /
Wikipedia 13, sphenoidal conchae); internal occipital crest (Gray: falx cerebelli / Wikipedia: falx cerebri);
zygomaticofacial foramen (malar surface / frontal process); nasion ("middle" / "most anterior point" of the frontonasal
suture). Lacrimal drainage: Wikipedia's "into the nasopharynx" is not used; Gray: the canal opens into the inferior
meatus.

**Models.** `configs/skull-detail.json`: BodyParts3D 3.0 (95 %) at 0.04 mm error (about the source detail), 2.5 MB for
23 parts; the page loads only the chosen bone. Contact areas ("joins with") are the detailed model's contacts
(1.2 mm). Some articulations in Gray's lists do not touch in the model (e.g. sphenoid–vomer, maxilla–vomer); the page
says so instead of drawing them. 110 landmarks placed by hand (`tools/bones/landmarks/`, `tools/test/bone_views.py`) from
the textbook wording, each checked by eye in several views. Foramina that the mesh does not model (supraorbital,
spinosum, zygomaticotemporal, nasal foramen) are markers at the described position and say so. The fossa of the
temporal bone was cross-checked against where the mandible touches it in the model.

## Skull — Foramina tab (`head-neck/skull.html`, 2026-11-14)

Eleven openings of the cranial floor, grouped by fossa. Contents as on Bones of the Skull (Gray 1918, checked against
StatPearls "Skull Foramen" NBK545298 and the review above). New here:
- **Jugular foramen** — Gray 46/47: between the petrous temporal and the occipital; IX, X, XI, inferior petrosal sinus,
  and the "transverse sinus" (the part now called the sigmoid sinus, continuing as the internal jugular vein).
  StatPearls "Anatomy, Head and Neck: Jugular Foramen" (statpearls.com/articlelibrary/viewarticle/36073): IX, X, XI,
  internal jugular vein, inferior petrosal sinus. Agree.
- **Foramen lacerum** — Gray 46 (the internal carotid passes across the upper surface of the fibrocartilage) and Gray
  47 (its upper part "transmits" the artery) differ; modern accounts (StatPearls "Foramen Lacerum", PubMed 31082070, and
  a microanatomy study) say no significant structure passes completely through it. The page says the artery crosses
  its upper part and that nothing large passes right through.
Points: paired openings on the right only. The internal acoustic meatus, jugular foramen and foramen spinosum were
re-placed on the inner (cranial) surface of the assembled base (`bone_views.py pick` with `aim`/`focus`); the others
reuse the bone-page landmarks; the lacerum and jugular foramen were placed at the centres of their openings in the model.

## Vertebral column — `back/vertebral-column.html`, `back/vertebrae.html` (2026-11-14)

**Sources.** Gray 1918: 107/19–25 (column, vertebrae, sacrum, coccyx, ossification) and 107/72–74 (joints), from dated
Internet Archive snapshots of bartleby.com; Wikipedia "Vertebra", "Cervical vertebrae", "Atlas (anatomy)", "Axis
(anatomy)", "Thoracic vertebrae", "Lumbar vertebrae", "Sacrum", "Coccyx", "Intervertebral disc", "Vertebral column"
(mostly copied from Gray). Quote-checked fact sheets in `sources-local/facts/vertebrae-*.md`.

**Independent review (2026-11-14, StatPearls via search excerpts, Radiopaedia, PMC papers):** about 115 statements
confirmed. Fixed: (1) costal element of a cervical transverse process — includes both tubercles and the bar, only the
posterior root is the true transverse process (Gray's own footnote; gpnotebook); (2) C7 foramen transversarium usually
transmits only the (accessory) vertebral vein; the artery enters at C6 (StatPearls NBK539734); (3) atlas inferior facets
— Gray "slightly convex", Radiopaedia "flat or slightly concave": both given; (4) secondary curves begin before birth and
become evident after it (Kenhub; Gray "developed after birth" quoted); (5) ossicle at the tip of the dens appears at
about 3–6 years (PMC4498315) vs Gray's second year: both given; (6) C7 not always the most prominent spine (PMC3847791)
instead of Wikipedia's "70 %"; (7) sacral fusion starts around puberty (StatPearls) vs Gray's 18th year: both given.
23 discs is the standard count (one StatPearls disc article says 25; not used).

**Words in neither Gray nor the Wikipedia copies, left out:** "hatchet-shaped" lumbar spine, "wedge-shaped" L5 body.
"Sacral hiatus", "promontory" are Wikipedia's names for features Gray describes in other words; both given.

**Models.** `configs/spine.json` (0.2 mm, 0.9 MB, assembled column with 23 discs) and `configs/spine-detail.json`
(0.04 mm, single vertebrae). BodyParts3D's "sacrum" includes the coccyx. 63 hand-placed landmarks
(`tools/spine/landmarks/`), checked in two oblique views each; vertebral-foramen centres of T6 and L3 set between the
back of the body and the laminae (picking from above sees through the canal).

## Thorax — `thorax/thoracic-cage.html`, `thorax/ribs.html` (2026-11-14)

**Sources.** Gray 1918: 107/26–29 (thorax, sternum, ribs, costal cartilages), 107/76–77 (costovertebral and sternocostal
joints); Wikipedia "Sternum", "Xiphoid process", "Sternal angle", "Rib", "Rib cage", "Costal cartilage", "Superior
thoracic aperture" (largely copied from Gray). Quote-checked fact sheet `sources-local/facts/thorax.md`. Two Wikipedia
errors not used: "first two pairs"/"top five ribs" join the sternum (Gray and Wikipedia "Rib cage": seven), and the xiphoid
"celiac plexus" sentence.

**Independent review (2026-11-14; StatPearls/Radiopaedia via search excerpts):** no factual errors; ~22 exam facts
confirmed (typical ribs 3–9; first-rib grooves and contents; single-vertebra ribs 1, 10–12; cervical rib on the lower
trunk; aperture boundaries). Fixed: sternal angle at the T4/T5 disc with what lies there (StatPearls NBK459336);
xiphoid ossification from ~3 years, variable (Radiopaedia 50176) vs Gray's 5–18; joint classes added — manubriosternal
secondary cartilaginous (symphysis), 1st sternocostal synchondrosis, 2–7 and costovertebral/costotransverse synovial
plane; false ribs: Gray 8–12 (8–10 vertebrochondral, 11–12 floating) vs StatPearls 8–10, both given; interchondral
9–10 usually ligamentous (Gray's own next sentence).

**Models.** `configs/thorax.json` (BodyParts3D 3.0, 0.25 mm: ribs, cartilages 1–7, sternum, T1–T12) and
`configs/thorax-detail.json` (0.04 mm: right ribs 1, 2, 6, 10, 11, 12 and the sternum). BodyParts3D has no cartilages
for ribs 8–10. 29 hand-placed landmarks (`tools/thorax/landmarks/`), checked in two views each.

## Upper limb — `upper-limb/upper-limb.html`, `upper-limb/bones.html` (2026-11-14)

**Sources.** Gray 1918: 107/49–56 (clavicle to phalanges); Wikipedia "Clavicle", "Scapula", "Humerus", "Radius (bone)",
"Ulna", "Carpal bones", "Scaphoid bone", "Hamate bone", "Metacarpal bones", "Phalanx bone", "Anatomical snuffbox" (much
copied from Gray). Quote-checked fact sheets `sources-local/facts/upper-limb-a.md`, `-b.md`. Neither source gives
side-determination rules, so the pages give none yet (AN8.1 marked partial).

**Independent review (2026-11-14; StatPearls, Radiopaedia, Orthobullets, papers via search excerpts):** no factual
errors; ~95 statements confirmed. Fixed: carpal ossification order and ages (Radiopaedia 12232; Gray's differ, both
given); lower ends of radius (~1 year) and ulna (5–6 years) vs Gray; humeral upper-end centres (StatPearls NBK534821) vs
Gray, growing end added; radial groove on the back of the shaft behind the deltoid tuberosity (Gray: antero-lateral
surface, noted); suprascapular artery/vein usually above the transverse ligament, nerve below; brachialis on the front
of the coronoid; flexor carpi ulnaris reaches the hook of the hamate via the pisohamate ligament; 2nd metacarpal the
longest of all five (PMC8461199); clavicle mainly membranous, medial epiphysis the last to fuse (PMC7749897);
lunate–hamate contact only in many wrists.

**Models.** `configs/upper-limb.json` (BodyParts3D 3.0, 0.2 mm, 32 bones of the right limb) and
`configs/upper-limb-detail.json` (0.04 mm). 69 landmarks (`tools/upper-limb/landmarks/`): long-bone points picked in
zoomed views (`ZOOM`/`FOCUS`, per-item `focus`/`zoom`); carpal points from the meshes (most palmar point for the hook of
the hamate and the scaphoid and trapezium tubercles; each bone's palmar or dorsal surface at its centroid).

## Lower limb — `lower-limb/lower-limb.html`, `lower-limb/bones.html` (2026-11-15)

**Sources.** Gray 1918: 107/57–65 (hip bone, pelvis, femur, patella, tibia, fibula, tarsus, metatarsus, phalanges);
Wikipedia "Hip bone", "Pelvis", "Ilium (bone)", "Ischium", "Pubis (bone)", "Acetabulum", "Obturator foramen", "Greater"/
"Lesser sciatic foramen", "Femur", "Femoral neck", "Linea aspera", "Patella", "Tibia", "Tuberosity of the tibia",
"Fibula", "Talus bone", "Calcaneus", "Navicular bone", "Cuboid bone", "Cuneiform bones", "Tarsus (skeleton)",
"Metatarsal bones", "Phalanx bone", "Sesamoid bone", "Arches of the foot" (much copied from Gray; the arches are
Wikipedia-only among these). Quote-checked fact sheets `sources-local/facts/lower-limb-a.md` (510 quotes) and `-b.md`
(456 quotes). Neither source gives side-determination rules; only the femur page has one (AN14.1 partial). Left out as
unsourced: the neck of the fibula and the common fibular nerve, the lateral process of the talus (marker kept in the
data, not listed), keystones of the arches, "law of ossification" by name.

**Independent review (2026-11-15; Radiopaedia, StatPearls, TeachMeAnatomy, papers — Radiopaedia and StatPearls read
through search excerpts):** ~140 statements confirmed. Errors fixed: greater sciatic foramen is closed by the
sacrotuberous and sacrospinous ligaments (Radiopaedia "greater sciatic foramen"); bipartite patella is an unfused
accessory centre, ~2%, superolateral (Radiopaedia "bipartite patella") — Wikipedia's contrary claim dropped. Modern
figures given beside Gray's: femoral head 4–6 months, greater trochanter 2–4 years, lesser about puberty, fusion
14–18 / distal 16–19 (Radiopaedia "ossification centres of the hip and pelvis"; DDH literature); lower femoral centre
as a sign of a term fetus; neck–shaft angle 125–130°, anteversion 10–15° (Acta Orthop cadaver series; PMC2911927);
patella 3–6 years (StatPearls "Knee Patella"); tibia lower end 6–12 months, tibial tuberosity centre 8–14 years, fusion
(PMC5761927 and cited studies); fibula lower end ~1 year, the fibula breaks the appear-first-fuse-last rule; calcaneal
apophysis 5–8 years (Radiopaedia 40790), which also confirms Gray's tarsal order; ischiopubic rami 4–8 years. Changed:
intertrochanteric line (capsule and iliofemoral ligament along it; vastus lateralis above, medialis below —
TeachMeAnatomy); lesser trochanter = iliopsoas (PMC4732368); fibular share of load 6–17% (PMC6594497); subpubic angle
figures removed (studies range widely, PMC7118257); pubic tubercle "3 cm" removed (no source). Added: pudendal nerve
behind the ischial spine; shared semitendinosus/biceps origin; supports of the medial and transverse arches.

**Models.** `configs/lower-limb.json` (BodyParts3D 3.0, 0.2 mm, 31 bones of the right limb + the hallux sesamoids) and
`configs/lower-limb-detail.json` (0.04 mm). 90 landmarks (`tools/lower-limb/landmarks/`): long bones picked in zoomed
views; joint facets (tibia–fibula, tibia–talus) from `near.py`; foot points from the meshes (`dorsal.py`, extremes for
the posterior process, sustentaculum, tuberosity processes, 5th metatarsal tuberosity), checked in colour-coded views.
The old `lower-limb/femur.html` stays as the femur's attachments and side page.

## Additions after re-search (2026-11-15) — side determination, fibular neck, arches, talus, ossification law

**Left or right** (`upper-limb/bones.html`, `lower-limb/bones.html`): fact sheet `sources-local/facts/side-determination.md`.
Rules from Hall et al., *Introduction to Human Osteology* (Grand Valley State Univ. 2010, CC BY-NC, via archive.org),
J. Robinson's A&P lab manual (LibreTexts, CC BY 4.0) and the Cuyamaca College handout "Identifying Left or Right
Bones" (low authority, used only where another source agrees), with orientation facts from Kenhub, TeachMeAnatomy and
StatPearls. Not taken: source L's "radial notch medial" (wrong; Kenhub and C say lateral) and source C's clavicle
curvature wording. Labelled on the page as built from descriptions (no source states the rule): fibula, 5th metatarsal,
and the patella tipping test. Left out: 1st metatarsal (sources disagree on its base tubercle), carpals, navicular,
cuboid, cuneiforms.

**Other items** (`sources-local/facts/lower-limb-extra.md`; Europe PMC full texts, PubMed, Kenhub, TeachMeAnatomy,
IMAIOS; StatPearls and Radiopaedia via search excerpts):
- Neck of the fibula and the common fibular nerve, injury by fracture, tight plaster or bandage, leg crossing; foot drop
  (Int Orthop 2022 and Insights Imaging 2023 reviews, TeachMeAnatomy, Kenhub, StatPearls). "Lateral side of the neck"
  not stated by any source, so not used.
- Arch keystones: medial — head of the talus (StatPearls) vs navicular (several papers, incl. Commun Biol 2023), both
  given; lateral — cuboid (three papers); transverse — intermediate cuneiform vs 2nd metatarsal base, both given.
  Supports: fibularis longus, long and short plantar ligaments, transverse head of adductor hallucis (Kenhub's
  "adductor longus" is a slip, not copied).
- Lateral process of the talus and the snowboarder's fracture; lateral talocalcaneal ligament from its tip (EFORT Open
  Rev 2018, World J Clin Cases 2024, BMC Musculoskelet Disord 2019).
- Fibula: nutrient foramen directed downward, upper end the growing end; lower end appears and fuses first (three
  foramen studies, Kenhub). "Appears first fuses last" as the general rule rests on teaching sites only; the page states
  it as the contrast, without calling it a law.
- Distal femur ~36 weeks, proximal tibia ~38 weeks (two papers); forensic sign of a term infant (JIAFM 2024 case
  report — single source, worded "at autopsy").
- Pubic tubercle 2.5–3 cm from the symphysis (2026 review; 2015 cadaver study, 26 mm). Subpubic angle: male roughly
  50–70°, female 90° or more, given as a guide (Kenhub; Texas Tech teaching page; studies vary, PMC7118257).

## Second re-search (2026-11-15) — classic osteology and forensic texts

Fact sheets `sources-local/facts/side-determination-2.md` and `lower-limb-extra-2.md`; OCR texts (archive.org) in
`sources-local/classic/`, quotes checked by script against them.
- **Left or right, carpals and small foot bones** (scaphoid … hamate; navicular, cuboid, three cuneiforms, 1st
  metatarsal): Holden, *Human Osteology*, 6th ed. 1885 (`humanosteologyco00holdiala`) states a "Right or Left?" rule
  for each; Frazer, *Anatomy of the Human Skeleton*, 2nd ed. 1920 (`anatomyofhumansk00frazuoft`) states or supports
  them; Gray 1918 and Cunningham 1902 confirm each facet direction. 1st metatarsal: fibularis longus tubercle
  plantar-lateral, tibialis anterior medial (Holden, Frazer, Cunningham, Gray; Landfald et al. 2025,
  doi:10.3389/fcell.2025.1678965). Kenhub's "tuberosity medially" rejected (contradicts all). Lunate: palmar/dorsal
  size disagrees between sources, so not used.
- **Fibula, patella, 5th metatarsal side rules now stated in sources:** fibula — Cunningham 4th ed. 1914 p. 250,
  Wagstaffe *Student's Guide to Human Osteology* 1875 p. 121; patella (larger lateral facet) — Holden 3rd ed. 1861
  p. 184, Frazer 1920 p. 152; 5th metatarsal — Holden 1861 p. 204, Wagstaffe p. 150. The patella table-tipping test
  has no source and was removed.
- **Common fibular nerve round the lateral side of the fibular neck:** Cunningham 1914 p. 251; Gray 1918 p. 1342.
- **Order of epiphyseal union / growing end / nutrient canal "towards the elbow, from the knee"; fibula the
  exception:** Frazer p. 4, Holden p. 27 and p. 140, Cunningham p. 87, Wagstaffe p. 40; fibula: Holden p. 192,
  Wagstaffe p. 118. No source calls it a "law", so the page doesn't.
- **Knee centres at term:** lower femoral nucleus as the sign of maturity, ~36–37 weeks, ~5 mm at term (Glaister,
  *Text-book of Medical Jurisprudence* 3rd ed. 1915 p. 468; Taylor, *Principles and Practice of Medical
  Jurisprudence* 7th ed. 1920 vol. I p. 199; Lyon 1921 supports); upper tibial nucleus present in the mature newborn
  (Glaister p. 467 fig. 117; Morina et al. 2024; PMC7766077). Worded as maturity, not viability, and as a supporting
  sign (Taylor: "open to numerous exceptions").

## Modern open sources for the left/right rules (2026-11-15)

Fact sheet `sources-local/facts/side-determination-modern.md`; downloads in `sources-local/modern/`. No modern open
source contradicts any rule on the site; every disagreement found was an internal error in one source, corrected by
another. Sources: eForensics osteology pages (eforensics.info, 2017–19); Hall et al. 2010 (GVSU, CC BY-NC — has carpal
and tarsal notes, missed earlier); Bone Broke (J. Beck, CC BY-NC); Tallahassee CC handout (J. Steiner); Cuyamaca College
tutor tool; Robinson LibreTexts lab manual (CC BY 4.0); UW–Madison virtual femur lab; Landfald et al. 2025 (1st
metatarsal); Radiopaedia (excerpt). HALL, Bone Broke and eForensics follow White's *Human Bone Manual*, so for carpals
and tarsals they count as one tradition, independent of Holden/Frazer. Errors in those sources not followed: eForensics
clavicle (conoid tubercle), triquetrum and hamate (proximal/distal swapped); Robinson ulna (radial notch); Hall navicular
(contradicts itself) and lateral cuneiform (triangular facet is the front one, Gray). Added from them: pisiform siding
unreliable on some bones (White et al. via Bone Broke; eForensics); patella table test (Bone Broke; Radiopaedia
excerpt), same direction as the facet rule. 1st metatarsal: no modern full rule; the fact (lateral tubercle) agrees.

## Muscles of the Upper Limb — `upper-limb/muscles.html`

**Meshes:** bones = BodyParts3D 3.0 (95 %), as `upper-limb.json`, plus right-side ribs, costal cartilages, sternum,
vertebrae, sacrum, hip bone and occipital as context (coarse). Muscles, retinacula, palmar aponeurosis, interosseous
membrane and arm septa = **Z-Anatomy** (CC BY-SA 4.0; https://github.com/Z-Anatomy/Models-of-human-anatomy,
`Z-Anatomy.zip` → `Startup.blend`), read by `tools/zanat/export.py` and moved into the BodyParts3D frame with one
similarity transform fitted on 24 bones (`tools/zanat/z-to-bp3d.json`; median bone residual 0.3–1.1 mm; Z muscles that
BodyParts3D also has match it within 0.25–0.8 mm). Build: `tools/zanat/ul_muscles.py` → `configs/upper-limb-muscles.json`.
A muscle's heads/parts are merged into one part. Colours: `tools/zanat/muscle_colours.py` (Tol "muted"; touching muscles
never share). Palmaris brevis is not in Z-Anatomy (text only).

**Attachment areas** (`tools/zanat/areas.py`, spec `tools/zanat/ul-attach.json`): bone vertices within 3–6 mm of the
muscle **and** near the landmark (or part of the bone) the textbook names. Every area was checked by eye in contact
sheets (`tools/test/attach_sheet.py`, 2026-11-17). Left out because the model does not show them reliably (listed in the
spec's `_dropped`): palmar interossei (Z mesh incomplete), ED insertions, ECU/EPB/APB small areas, opponens pollicis
insertion (two blobs), FDS radial head, serratus anterior insertion (landed on the dorsal surface), levator scapulae
origins (laminae, not transverse processes), the axial origins of trapezius, latissimus dorsi and the rhomboids (the
mesh misses most spinous processes), anconeus origin.

**Sources:** fact sheets `sources-local/facts/ul-muscles-a.md` (pectoral, back, scapular, arm; 364 quotes) and
`ul-muscles-b.md` (forearm, hand, retinacula, thumb, clinical), each fact with two independent sources: Gray 1918
(bartleby.com/107 via web.archive.org, pages 120–126), StatPearls abstracts (Europe PMC), open-access papers (Europe PMC
full text) and Wikipedia (MediaWiki API; not counted where it copies Gray). Disagreements resolved as in the sheets:
modern wording for FDS heads (two), ECRB nerve (deep branch, variable), palmar interossei (three); root values only where
two sources agree; no supraspinatus angle; trapezius C3–C4 "mainly sensory; sources differ". Left out (single source):
supinator and extensor retinaculum attachments, FPB deep-head attachments, PAD/DAB, triangular space, triangle of
auscultation, "regimental badge" area, Poland syndrome, reflexes, subscapularis tests, FDS tendon pairs in the tunnel.

**Independent review (2026-11-17), 7 fixes:** subscapularis "guards the front of the joint" removed (single source);
teres major: triangular space removed; thumb opposition row reduced to opponens pollicis (APB helping = Wikipedia
only); pectoralis major "costal cartilages of the true ribs (upper six or seven)"; axillary nerve injury "fracture of
the upper humerus" (not "surgical neck"); biceps rupture "bulge in the front of the arm (Popeye sign)"; latissimus
"(climbing)" moved to the fixed-arm action.

## Muscle Tissue — `general/muscle.html`

Fact sheet `sources-local/facts/muscle-tissue.md` (255 quotes; Gray 1918 pages 102–104, 138, 183; StatPearls; open
reviews incl. PMC12130008, PMC5642817, PMC4748971, PMC5806676, PMC7248366, PMC11668723, PMC11212792; Wikipedia).
**Not on the page:** shunt and spurt muscles (AN3.3) — no open source defines them (MacConaill/Basmajian papers have no
open full text); fusiform example; cardiac/smooth cell sizes; smooth-muscle regeneration and T tubules; single- vs
multi-unit smooth muscle; Gray's 1918 theory of contraction (obsolete). Mammalian rule for T tubules noted (frog differs).
**Independent review (2026-11-17), 5 fixes:** H zone drawn lighter than the overlap part of the A band (was darker);
calcaneal tendon wording (the tendon starts as an aponeurosis); fixator definition without "proximal/distal"; "a modern
review" (one source) keeps synergist and fixator apart; T tubules "at the A–I junctions (in mammals)".

- Micrographs added 2026-11-18 (Wikimedia Commons, resized to 640 px; licences read from the Commons API):
  File:Musc_est_long_400.JPG (Ganímedes, CC BY-SA 3.0), File:Cardiocyte_(myocyte).jpg (Lazar.zenit, CC BY-SA 4.0),
  File:Musc_liso_400.JPG (Andrea Mazza, CC BY-SA 3.0); each states the tissue and H&E. Captions use features already
  verified in `muscle-tissue.md` E1–E4. Review (2026-11-18): skeletal caption reworded (fibre borders not visible).

## Connective Tissue — `general/connective-tissue.html`

Fact sheet `sources-local/facts/connective-tissue.md` (321 quotes; Gray 1918 pages 104–110; StatPearls; open papers
incl. PMC10486581, PMC9496548, PMC7824244, PMC8963043, PMC3445147, PMC11818326, PMC12914158, PMC8269293, PMC6070248,
PMC13160772; Wikipedia). Disagreements handled as the sheet advises: no parent group for adipose/reticular tissue;
ligamenta flava "mostly elastic (about 70 %)"; aortic lamellae "about 50–60"; articular cartilage nourished from synovial
fluid (Gray's older view noted); nasal cartilage = hyaline; "superficial fascia" in the classic sense, modern sense noted;
vascularity of deep fascia left out. **Not on the page:** deep fascia absent in the face, Alport syndrome, fibrocartilage
without perichondrium (one direct source: the table says so), sex differences in fat, infant brown-fat sites,
interosseous membranes as deep fascia, plasma-cell Golgi "hof", PAS for reticular fibres.
**Independent review (2026-11-17), 9 fixes:** elastic cartilage drawn with single cells (isogenous groups in elastic
cartilage = Wikipedia only); fibrocartilage figure says the perichondrium is not drawn because it is unconfirmed;
mast-cell granules get their own colour; removed "often lies along vessels" (mast cell), "basophilic cytoplasm" (plasma
cell → "abundant cytoplasm"), "oval nucleus"/"little cytoplasm" (fibroblast, now the quoted wording), "black" for
Verhoeff, vitreous body and nucleus pulposus for type II collagen, osteogenesis imperfecta (both quotes StatPearls = one
publisher), "rows of fibroblasts" in dense regular tissue; section retitled "Kinds of connective tissue" (no parent group
for adipose/reticular tissue).

- Additions (2026-11-18; fact sheet `sources-local/facts/fill-histo.md`, 62 quotes, script-checked; Gray 1918
  pp. 108, 111, 120, 149, 157, 227; StatPearls; PMC5291139, PMC11506611, PMC6406103, PMC10358300, PMC2224023,
  PMC5385471, PMC11642339, PMC8875079, PMC8963043, PMC12079772; Wikipedia, Gray copies excluded): gynoid vs android
  fat, buccal / ischioanal / orbital fat, investing layer and the pretracheal and prevertebral layers, carotid, axillary
  and femoral sheaths (Gray includes the axillary vein, Wikipedia not: both given; which layers form the carotid sheath
  varies), calf compartment drawing (pump, compartment syndrome), EM schematics of fibroblast, mast cell, plasma cell,
  macrophage, elastic fibre. Fibrocartilage perichondrium now "absent" (PMC8963043, PMC12079772).
- Cartilage micrographs: File:Cartilage01.JPG (Ganímedes, CC BY-SA 3.0, H&E, trachea), File:Cart_elastico_400.JPG
  (Ganímedes, CC BY-SA 3.0, stain not stated), File:Connective_Tissue_Fibrocartilage_(41140134634).jpg (Berkshire
  Community College Bioscience Image Library, CC0, stain not stated); chosen because the uploader names the tissue and
  the textbook features are visible (selection notes: `fill-histo.md` Part E).
- Left out (one source): visceral fat as harmful, oestrogen as cause, buttocks in gynoid fat, infrapatellar fat pad,
  compartment pressures and "opened"/nerves, plasma-cell Golgi. Review (2026-11-18) fixed captions (isogenous groups of
  two, four or more; fibrocartilage cells in short rows), the bone in the compartment drawing, sheath wording.

## Muscles of the Lower Limb — `lower-limb/muscles.html`

**Meshes:** bones = BodyParts3D 3.0 (as `lower-limb.json`) plus T12–L5 and the sacrum as context; 50 muscles, the
iliotibial tract, calcaneal tendon, ankle retinacula and plantar aponeurosis from Z-Anatomy, moved into the BodyParts3D
frame (`tools/zanat/ll_muscles.py` → `configs/lower-limb-muscles.json`; adductor minimus merged into adductor magnus,
the EDL tendon into EDL). Shared page logic: `assets/muscle-page.js` (also used by the upper-limb page).

**Attachment areas** (`tools/zanat/ll-attach.json`): 106 areas, each checked by eye (foot bones measured along the
front–back axis; gastrocnemius and soleus insertions measured from the calcaneal tendon mesh; sole areas viewed from
below). Left out (spec `_dropped`): EDL insertions, fibularis tertius, soleus tibial origin, tibialis posterior fibular
origin, abductor hallucis and abductor digiti minimi calcaneal origins, pectineus insertion, adductor brevis origin, TFL
origin, piriformis origin, gluteus minimus insertion.

**Sources:** fact sheets `sources-local/facts/ll-muscles-a.md` (hip and thigh; 412 quotes, 115 sources) and
`ll-muscles-b.md` (leg and foot; 349 quotes), each fact two independent sources: Gray 1918 (bartleby.com/107 pages
127–131, 157, 212–213, via web.archive.org), StatPearls abstracts (Europe PMC), open-access papers, Wikipedia (not
counted where it copies Gray). Root values only where two sources agree; fibularis tertius = deep fibular nerve (one
StatPearls abstract says superficial: logged as an error). Left out (single source or conflicting): actions of FDB and
flexor digiti minimi brevis, extensor retinaculum attachments, FHB's exact origin (sources differ — the page says so),
roots of the gemelli, obturator internus and quadratus femoris, knee-jerk roots, gluteus maximus lurch, perforating
openings in adductor magnus, the infant vastus lateralis injection site, "largest muscle", arch roles of adductor
hallucis, tibialis anterior and FHB, the lateral arch.
**Independent review (2026-11-17), 13 fixes:** removed single-source or gap items — soleus "main plantarflexor with the
knee bent", popliteus tendon "inside the capsule", calcaneal tendon rupture "commonest", age band and "push-off sport",
foot-drop causes "casts, fibular neck fracture" (→ habitual leg crossing, prolonged positioning), inferior fibular
retinaculum on the calcaneus (→ binds the fibular tendons, two sources), FL/TP tendons as the 4th layer (now "by
convention"), obturator externus "posterior branch", ITB syndrome "cyclists", fibularis tertius absence rates,
gluteus maximus "three-quarters", superior fibular retinaculum tear, the phrase "true hamstring" (criteria kept). FHB
origin reworded: the cuboid is agreed, the cuneiform differs.

- Additions (2026-11-18; fact sheet `sources-local/facts/fill-ll.md`, 510 quotes, script-checked; parts reused from
  the joints, ll-muscles-b and vessels sheets): extra-tab table "Vessels, nerves and lymph nodes in 3D" (femoral
  triangle, sheath and canal, adductor canal, under gluteus maximus, injections, calf pump, veins, perforators, lymph
  nodes, dermatomes). Parts load from body-vessels / body-nerves / body-lymph / ax-joints / ll-joints by byte range
  (whole file if the server ignores Range). Labels computed from the meshes, approximate. Lymph-node groups drawn
  three times enlarged about their centres; not shown in the femoral-triangle views (the model puts them in front of
  the femoral vein). Dermatome map schematic (maps differ).
- Disagreements shown: deep inguinal nodes 1–3 (Gray) vs 3–5 (Wikipedia); back wall of the femoral ring; nerve to
  vastus medialis in the adductor canal (disputed); L3 key point. Left out (one source): soleal venous sinuses, tight
  deep fascia in the pump, fascia lata attachments beyond the iliac crest and knee, popliteal/anterior tibial node
  details, nerve to quadratus femoris among the gluteal structures.
- Independent review (2026-11-18), fixed: injection wording (mainly the common fibular part), DVT start (deep calf
  vein; soleal veins in bedridden patients), trochanteric anastomosis "around" the neck and head, soleus wording,
  labels and framing in the gluteal and femoral views.
- Also from `fill-ll.md` (2026-11-18): `lower-limb.html` Arches tab "What holds them up, and what goes wrong" (factors,
  importance, flat foot, club foot, metatarsalgia, Morton's neuroma; stirrup = medial arch raised, lateral arch
  supported, one review; transverse arch from fibularis longus per Gray); `bones.html` "Joints it forms" per bone and
  the foot's "Muscle attachments, bone by bone" (rearranged checked facts; sacro-iliac classification contested).
  Left out: arches protecting plantar vessels and nerves (no source), plantar plate tears (one source),
  "osteochondrosis" for Freiberg disease (not in the sources).

## Muscles of the Back — `back/muscles.html`

**Meshes:** vertebral column, occipital and right temporal bones, right ribs and hip bone (BodyParts3D 3.0); 17 deep
back muscles and the three layers of the thoracolumbar fascia from Z-Anatomy (`tools/zanat/back_muscles.py`). Not in
the model: semispinalis capitis (absent from Z-Anatomy: text only) and levatores costarum (only their existence is
two-sourced, so they were removed). **Attachment areas** (`tools/zanat/back-attach.json`): 36, each checked by eye;
vertebral attachments limited to the spinous-process end (front–back axis). Left out: serratus posterior superior spinal
origins, splenius cervicis insertions, semispinalis insertions, multifidus sacral origin, quadratus lumborum
transverse-process insertions and iliac origin, rectus capitis posterior major occipital insertion (partial or sliver).

**Sources:** fact sheet `sources-local/facts/back-muscles.md` (329 quotes, 64 sources): Gray 1918 (bartleby.com/107
sections 115–118, 209), StatPearls abstracts, open-access papers (Zhang 2025, Hung 2024, Du 2025, Regan 2023, Homma
2023, Shuang 2015 and others), Wikipedia (not counted where it copies Gray). Left out (single source or disputed):
serratus posterior inferior origin levels and breathing role, spinalis levels and "inconstant" spinalis cervicis,
levatores costarum details, interspinales action, root values of the splenii and quadratus lumborum, quadratus
lumborum's action with both sides together, rotatores outside the thoracic region, semispinalis span in segments.
**Independent review (2026-11-17), 7 fixes:** intertransversarii supply "mixed, partly ventral, partly dorsal rami"
(the lumbar lateral/medial split is Gray only); longissimus capitis turning the face removed (Gray only); the
latissimus/serratus posterior inferior aponeuroses blend with the fascia as a whole, not the posterior layer; "the
posterior and middle layers fuse" laterally; low back pain wording (mechanical vs non-specific; days to weeks is for a
strain); occipital neuralgia "may be treated" with a nerve block; footer "better-supported wording".

## Muscles of the Trunk Wall — `thorax/wall-muscles.html`

**Meshes:** thoracic cage (both sides), lumbar spine, sacrum and both hip bones (BodyParts3D 3.0); the right
intercostals (three layers), transversus thoracis, abdominal muscles, pyramidalis and pelvic-diaphragm muscles, the
whole diaphragm, the inguinal ligament, linea alba and tendinous arch of levator ani from Z-Anatomy
(`tools/zanat/trunk_muscles.py`). Not separate in Z-Anatomy: subcostales, puborectalis. **Attachment areas**
(`tools/zanat/trunk-attach.json`): 25, each checked by eye. Not drawn: the intercostals (origin and insertion are the
facing borders of neighbouring ribs, which proximity cannot separate), the diaphragm's costal and xiphoid origins, the
pubococcygeus origin.

**Sources:** fact sheets `sources-local/facts/thorax-wall-muscles.md` (262 quotes; Gray 1918 sections 117, 210, 211;
StatPearls; 18 open-access papers incl. the 2024 ICS/NCCP pleural-procedure guideline, Formenti 2020, Park & Chang 2022)
and `abdominal-wall-muscles.md` (362 quotes, 85 sources; Gray 1918 sections 118–119; StatPearls; Kriener 2023, Mehta
2021, Wu 2022, Hori 2021, Salvador 2019, Roch 2021 and others; Wikipedia, not counted where it copies Gray). Disputes
as the sheets advise: the intercostals' roles (modern view; Gray's dissent noted), caval opening T8 (Gray: T8/9 disc),
left crus levels, costal origin of the diaphragm (lower six ribs), arcuate-line level, linea semilunaris (classic
definition), thoracocentesis site (guideline, no fixed space), coccygeus nerve. Left out (single source): subcostales
and transversus thoracis attachments, innermost intercostal fibres and extent, hiccups side, bilateral phrenic palsy
severity, traumatic diaphragmatic hernia, the triangle-of-safety boundaries, external oblique interdigitations,
cremasteric reflex arc, direct hernia in older people, incisional-hernia causes, coccygeus action.
**Independent review (2026-11-17), 5 fixes:** "levator plate" removed (gap item); pelvic nerve text separates levator
ani (S3–S4 + pudendal) from coccygeus (sacral plexus, S4–S5 in Gray); oesophageal opening "formed mainly by the right
crus"; referred shoulder pain limited to the central diaphragm, supraclavicular roots C3–C4; left crus "L1–L2; one
source L2–L3".

## Muscles of the Head and Neck — `head-neck/muscles.html`

**Meshes:** skull, hyoid, C1–C7, T1–T2, manubrium, first and second ribs and costal cartilage, clavicles and right
scapula (BodyParts3D 3.0); 57 right-side muscles, the thyroid, cricoid and arytenoid cartilages, the epiglottis, the right
eyeball (sclera, cornea), the epicranial aponeurosis and the investing layer of the deep cervical fascia from Z-Anatomy
(`tools/zanat/hn_muscles.py`; cartilages and eyeball exported by exact object name into `z-bp3d-extra.zip`). Not in
Z-Anatomy: tensor and levator veli palatini, palatoglossus, musculus uvulae, styloglossus, salpingopharyngeus, the
intrinsic tongue muscles (text only on the page). **Attachment areas** (`tools/zanat/hn_attach_spec.py` →
`hn-attach.json`): 54 on 32 muscles, each checked by eye (`tools/test/muscle_sheet.py`). Dropped, with reasons in the
spec's `_dropped`: the extraocular insertions (the muscles wrap the globe, so proximity marks far more than the
insertion) and orbital origins, occipitofrontalis, procerus, zygomaticus major, levator labii superioris alaeque nasi,
levator anguli oris, geniohyoid, genioglossus, longus capitis and colli, scalenus anterior, superior constrictor, lateral
and posterior cricoarytenoid, thyroarytenoid; the SCM insertion (its occipital part is empty), the omohyoid scapular
origin, the digastric fossa, sternohyoid and sternothyroid manubrial origins.

**Sources:** fact sheets `sources-local/facts/hn-face-mastication.md` (383 quotes, 98 sources: Gray 1918 sections
108–109 and the facial and trigeminal nerves; StatPearls; Wu 2022, Landfald 2025, Carré 2024, Okoń 2025/2026,
Triantafyllou 2025, Zöchmeister 2026, Lindor 2025, Miyanaga 2026 and others; Wikipedia, not counted where it copies
Gray), `hn-neck.md` (439 quotes, 88 sources: Gray 1918 sections 110–113, 145, 148, 210; StatPearls; Kikuta 2019, Feigl
2020, Phan 2022, Malkidou 2025, Pereira Boog 2025, Nito 2025, Shawky 2017 and others) and
`hn-eye-tongue-pharynx-larynx.md` (377 quotes: Gray 1918 orbit, tongue, palate, pharynx, larynx and cranial-nerve
sections; StatPearls; open-access papers on eye-muscle actions, palsies, the tongue, the palate, Zenker's diverticulum
and laryngeal nerve injury; Wikipedia). Disputes as the sheets advise: the facial-nerve branch for procerus, nasalis and
levator labii superioris ("facial nerve" only); which nuchal line for the occipital belly; scalene origin levels and
roots (roots left out); C1–C2 vs C1 for the superior root of the ansa (C1); the pharyngeal-plexus fibres (said to be
vagal); Wikipedia's extraocular "Examination" paragraph (reversed positions) excluded. Left out (single source): the
corneal reflex, the side of jaw deviation and the resistance tests for the pterygoids, an exaggerated jaw jerk, the
galea's bony attachments, the vagus' position in the carotid sheath, contents of the suprasternal space, the floor of
the subclavian triangle, rectus capitis lateralis action and roots, longus colli roots, UMN tongue deviation, Semon's
law, VI as a false localising sign, injury percentages.
**Independent review (2026-11-17), 4 fixes plus removals:** the phrenic nerve and sympathetic trunk are enclosed by the
prevertebral fascia (the nerve deep to it, on scalenus anterior), not "on" it; III-palsy ptosis has a large pupil only
when the pupil is involved; the pharyngeal muscles are called circular and longitudinal, without "outer/inner"; the
models line no longer says "the palate muscles" are absent (palatopharyngeus is in the model). Removed as Gray-only
(Wikipedia copies Gray): the eye-muscle angles (about 23°, 51–54°), the sternothyroid origin from the first costal
cartilage, the longus colli extent (atlas to T3), the longus capitis attachments, and the scalene origin levels and
tubercles.


## Anatomy home — whole body with muscles (`index.html`)

- No new facts: the Muscular system shows the muscles of the five regional muscle pages; tapping one selects its region
  and opens that page.
- Skeleton rebuilt from BodyParts3D 3.0 (was 4.0 at 99 %): checked 2026-11-17 that 4.0 bones sit up to 10–20 mm from the
  3.0 bones that the Z-Anatomy muscles were fitted to (e.g. clavicle +23 mm in z), which would leave muscles floating off
  or cutting into the bones. All 215 bones exist in 3.0 under the same FMA ids.
- Left muscles = right ones mirrored (Z-Anatomy does the same); the reflection, derived from `z-to-bp3d.json`, matches
  a least-squares fit to Z-Anatomy's own left meshes (gluteus maximus, temporalis) to 0.0001 mm. Checked by eye at the
  shoulders, knees, pelvis (back) and face that both sides sit on the bones.

- Heart and vessels layer (2026-11-18): no facts, only the model. Z-Anatomy vessels are Bezier curves with a radius;
  `tools/zanat/export_curves.py` sweeps a tube along each (radius = bevel depth × point radius, as Blender draws them);
  242 of 257 left curves are exact mirrors of the right ones and are mirrored by the page. Checked by eye: whole body
  front, heart and great vessels, neck, brain arteries from above, hands and feet; colour by kind (artery, vein,
  heart) from Z-Anatomy's collections ("Systemic arteries", "Pulmonary veins", ...).

- Nerves layer (2026-11-18): no facts. Z-Anatomy nerve curves swept into tubes like the vessels; spinal dura shown
  for the dural sac (no spinal cord in Z-Anatomy); no phrenic or inferior gluteal nerve in Z-Anatomy. Checked by eye:
  whole body front, with muscles, with vessels at the shoulder and the thigh.

- Lymph layer (2026-11-18): no facts; Z-Anatomy node groups (small blobs at their usual sites), tonsil, thymus,
  spleen. No lymphatic vessels or thoracic duct in Z-Anatomy.

## Joints — `general/joints.html`

- Fact sheet: `sources-local/facts/joints-general.md` (309 quotes, all script-checked against the downloads in
  `sources-local/modern/joints/`: Gray 1918 pages 68–96, StatPearls abstracts, Wikipedia extracts with revision ids,
  open-access papers). Wikipedia "Synovial joint", "Cartilaginous joint", "Syndesmosis" and "Synovial bursa" say they
  include OpenStax text and were not used. Wikipedia sentences copied from Gray were not counted as a second source.
- Hilton's law: not in Gray 1918; four independent wordings (Wikipedia; J Neurol 2020, PMC7914164; Edinburgh Med J 1925
  quoting Hilton, PMC5316670; Biomed Res Int 2022, PMC9173899). The page uses Hilton's own words and notes that the
  skin part is worded differently ("over the insertions" / "over the muscle" / "over the joint").
- Disagreements stated on the page: functional vs structural mapping (StatPearls 1:1; Gray and Wikipedia put
  syndesmoses among amphiarthroses, synchondroses among synarthroses); "permanent" first sternocostal synchondrosis
  (Wikipedia) vs all synchondroses temporary (Gray); knee = modified hinge (StatPearls, Wikipedia) vs two condyloid
  joints + patellofemoral (Gray 93); sternoclavicular = saddle (StatPearls, Wikipedia) vs double arthrodial (Gray);
  plane joints non-axial vs multiaxial (two Wikipedia articles); condyloid = ellipsoid (Gray, Wikipedia).
- Left out (one source or none): suture subtypes and which suture is which (Gray and Wikipedia conflict); forearm
  interosseous membrane as a syndesmosis (Wikipedia only); a separate condylar/bicondylar type for knee and TMJ (no
  downloaded source); close-packed/loose-packed positions; a general rule that every joint has an arterial
  anastomosis (only elbow and knee examples); named mechanoreceptor types; distal radio-ulnar as a pivot.
- Independent review (2026-11-17), fixed: menisci divide a joint only partly (only a complete disc makes two
  cavities); "cartilage is not in the model" -> articular cartilage (costal cartilages, discs and menisci are);
  synovium covers the non-cartilaginous surfaces; type B cells secrete the hyaluronan (the fluid is a plasma
  ultrafiltrate); "suggests" a reflex arc; anastomosis "around joints such as"; plane-joint axis wording attributed;
  manubriosternal "about a third of cases"; MCP joints "of the fingers"; thumb movement planes added (Gray 88 +
  Wikipedia "Carpometacarpal joint"); pronation example relabelled proximal radio-ulnar; palm-facing definition of
  pronation attributed to Wikipedia; Gray-only details removed or attributed (first costal cartilage continuity,
  facet joints as plane, "nearly half a sphere", head of humerus vs glenoid, Hilton on contracture, the condylar note).
- 3D: example joints from BodyParts3D 3.0 (bones, lower right teeth, costal cartilages, L4–L5 disc) and Z-Anatomy
  (menisci, interpubic disc), `tools/joints/general_config.py`. Pivots and axes fitted to the joint surfaces by
  `tools/joints/general_axes.py` (femoral head sphere r 23.3 mm; trochlea circle r 10.1 mm; knee condyle outline
  r 20.9 mm, 22.5 mm above the lowest point; dens: vertical line through its centre because it is too short to fit).
  Every movement direction was checked in screenshots at both ends of its arc, and again by the reviewer.

- Additions (2026-11-18; fact sheet `sources-local/facts/fill-ul.md`, 101 quotes, script-checked): triangle of
  auscultation, lumbar triangle, trapezius test, anatomical snuffbox (Gray 121/151, StatPearls 29489241, 30969656,
  30085536, 28846224, PMC6549589, 7815005, 12275635, 12900228, 10072784, 12246593, 13340701, 4481793, 11329012,
  9866992, 6221869, 8514418, 10692986, 10329327, Wikipedia). Snuffbox 3D: Z-Anatomy radial artery, cephalic vein and
  superficial branch of the radial nerve, read by byte range from the whole-body packs; labels approximate. Left out:
  latissimus dorsi bedside test (one vague source), ECRL/ECRB in the floor, "abducted" thumb, artery "crossed by EPL"
  (Gray only). Review (2026-11-18) fixed those wordings and "after an injury".
- Shared `assets/muscle-page.js`: "By bone" view (all five muscle pages) built from the existing checked attachment
  areas; no new facts.

## Joints of the Upper Limb — `upper-limb/joints.html`

- Fact sheets: `sources-local/facts/joints-shoulder.md` (349 quotes; SC, AC with coracoclavicular and coracoacromial
  ligaments, glenohumeral joint) and `sources-local/facts/joints-elbow-hand.md` (439 quotes; elbow and anastomosis,
  radio-ulnar joints, interosseous membrane, TFCC, wrist, carpus, CMC, MCP, IP). All quotes script-checked against the
  downloads in `sources-local/modern/joints-shoulder/` and `…/joints-elbow-hand/`. Key extra source: DePalma 1963
  (PMC2505212, the 2008 reprint).
- Contested, stated on the page: SC type (saddle vs Gray's double plane); main SC restraint (costoclavicular vs
  posterior capsule); supraspinatus starts abduction for 15° or 30°; timing of scapular rotation; transverse humeral
  ligament (ligament vs tendon fibres); humero-radial type; carrying angle values and sex difference; elbow nerves
  (radial absent from Gray); wrist cavity separate vs common with the midcarpal joint; 2nd–5th CMC type (plane vs
  condyloid); opposition muscles (opponens vs Gray's flexors and adductor); thumb-base OA by sex; quadrate ligament's
  existence.
- Left out (one source or none): blood supply of the AC joint (none found); radio-ulnar joints' vessels and nerves (none);
  named first CMC ligaments as fact (disputed); ranges of movement other than elbow and pronation–supination; the
  three-point relationship at the elbow (Wikipedia only); Neer's stages; frozen-shoulder stage durations; Rockwood V
  details; posterior shoulder dislocation from seizures; MCP collateral ligaments tight in flexion (not stated).
- Independent review (2026-11-17), fixed: SC dislocation "rare" dropped; SC restraint dispute added to the part card;
  shoulder-girdle muscles labelled as Gray's and as acting through the clavicle and scapula, clavicular head of SCM;
  teres major as extensor marked Gray; abduction/scapular-rhythm rows made consistent with the timing dispute; subacromial
  bursa opens "unless the tendon is torn right through"; Hilton's law "fits"; elbow extension limit removed (sources
  differ); middle collateral artery marked Gray; carrying-angle sex difference "not in all studies"; quadrate ligament
  disputed, not "thin"; oblique cord "sometimes" absent; palmaris longus and ECRB marked Gray; wrist ligament attachments
  marked Gray and modern bands mentioned, duplicate radiocapitate part removed, title "Wrist and carpus"; 2nd–5th CMC type
  attributed; thumb-base OA attributed; unrelated bursae (teres major, subcutaneous acromial, bicipitoradial) removed from
  the lists; "subscapular bursa is not in the 3D model".
- 3D: BodyParts3D 3.0 bones + 82 Z-Anatomy joint parts exported with their Blender Subsurf/Solidify modifiers applied
  (`tools/zanat/export_mod.py`). Pivots fitted (`tools/joints/ul_axes.py`): humeral head sphere r 19.1 mm, trochlea circle
  r 10.1 mm, 2nd metacarpal head sphere r 7.0 mm, PIP circle r 3.2 mm; SC and AC pivots at the facing surfaces. Every
  movement direction checked in screenshots at both ends of its arc, and by the reviewer.

- Additions (2026-11-18, `fill-ul.md` part C): distal radio-ulnar nerves (AIN, PIN, dorsal cutaneous branch of ulnar)
  and articular disc vessels; thumb CMC ligaments (main stabiliser disputed: anterior oblique vs dorsoradial, both
  stated) and nerves. Sources PMC12398336, 12209593, 11912921, 13668832, 12777731, 8817812, 11929737, 10843995,
  11682352, 12591505, 13065628, Wikipedia. Left out: proximal radio-ulnar joint nerves (one source) and arteries
  (none), DRUJ capsule arteries. Review fixed "mainly" (disc supply; one source) and removed a verification note from
  the page.

## Joints of the Lower Limb — `lower-limb/joints.html`

- Fact sheets: `sources-local/facts/joints-hip-knee.md` (483 quotes) and `sources-local/facts/joints-ankle-foot.md` (315
  quotes), all script-checked against `sources-local/modern/joints-hip-knee/` and `…/joints-ankle-foot/`.
- Source errors found and not used: StatPearls 32119474 (genicular arteries from the femoral); Wikipedia "Knee" (popliteus
  helps lock the knee); Wikipedia "Anterior cruciate ligament" (blends with the medial meniscus; Gray: lateral);
  StatPearls 32119497 (Chopart joint = talonavicular only).
- Contested, stated on the page: importance of the artery of the ligament of the head; iliopsoas as a rotator (left out of
  the rotator lists); unhappy-triad meniscus (classically medial, later lateral); talocalcaneonavicular type; spring
  ligament elasticity; deltoid ligament part names; ankle nerves; number of syndesmosis ligaments; foot-joint nerves
  (Gray only, attributed).
- Left out: hip ranges and the 350 kg ligament strength; DDH risk factors; neck-fracture limb posture; Lachman angle;
  "clergyman's knee"; circumflex fibular artery; posterior tibial recurrent artery; the quadriceps named as the locking
  muscle (Gray says only "continued muscular action"); ankle capsule attachments; blood supply of the foot joints.
- Independent review (2026-11-18), fixed: ligament-of-head artery importance attributed both ways; hip→knee referred pain
  attributed to a review; posterior dislocation "blow on the bent knee", "shortened" removed; popliteal artery depth and
  the knee muscle relations marked Gray; ACL tear mechanism removed, triad and meniscal mechanisms softened; meniscectomy
  "raises the risk" of OA; syndesmosis ligament count and transverse ligament wording; long plantar ligament attributed
  to Gray; acetabulum "about half (StatPearls ~40%)"; inversion "mainly at the subtalar and transverse tarsal joints";
  "commonest ankle sprain"; middle genicular removed from the anastomosis; distinct text for the lateral iliofemoral band.
- 3D: BodyParts3D 3.0 bones + Z-Anatomy joint parts with modifiers applied (`z-bp3d-joints-ll.zip`; pelvic ligaments,
  triradiate cartilage and hip retinacula left out). Pivots (`tools/joints/ll_axes.py`): femoral head sphere r 23.3 mm;
  knee condyle outline r 22.1 mm; talar dome outline r 27.8 mm (the facing surfaces alone gave r 8 mm, too small);
  1st metatarsal head sphere r 11.5 mm; the inversion–eversion axis is placed schematically (up, forward, medially). The
  patella stays still during knee flexion (moving it with the tibia left it floating). Directions checked in screenshots
  and by the reviewer.

## Joints of the Jaw, Spine and Pelvis — `back/joints.html`

- Fact sheets: `sources-local/facts/joints-tmj-cv.md` (297 quotes) and `sources-local/facts/joints-spine-pelvis.md`
  (322 quotes), script-checked against `sources-local/modern/joints-tmj-cv/` and `…/joints-spine-pelvis/`. Wikipedia
  articles citing OpenStax were excluded ("Condyloid joint", "Muscles of mastication", "Spinal column", "Cartilaginous
  joint"), as were sentences copied from Gray.
- Source errors not used: Wikipedia "Transverse ligament of atlas" (foramen "of the axis"); Wikipedia "Atlanto-axial
  joint" (thick capsules); Wikipedia "Facet joint" lead (recurrent meningeal nerves); PMC9249043 (notochord as endoderm);
  Wikipedia sacrotuberous attachment.
- Contested, stated on the page: SI joint classification and cartilage; strongest SI ligament (interosseous vs Gray's
  posterior); disc share of column length; ALL upper end; supraspinous lower end; which pubic ligament the abdominal
  aponeuroses join; tectorial membrane layers; share of neck rotation at C1–C2; atlanto-occipital type (Gray only,
  attributed).
- Left out: "condylar" as the TMJ type (no source); reduction of TMJ dislocation (one group of papers only); "yes/no"
  movement labels; ADI thresholds; degree values; cervical prolapse levels; L5–S1 → S1 example; SPD incidence.
- Independent review (2026-11-18), fixed: a dens fracture no longer said to leave the dens "unheld" (only failure of
  the transverse ligament does); **Z-Anatomy's "Lateral temporomandibular ligament.r" lies on the left side and ".l" on
  the right** — the right one (".l") is now used; lumbar arc flexion larger than extension; the jaw glide starts after
  the first 8° of opening (hinge first); RA wording; disc "attached all round to the capsule" (Gray only) removed;
  TMJ dislocation "usually" anterior; sciatica "low lumbar discs"; lateral atlanto-axial joints "upper articular facets
  of the axis"; L5 moves with the sacrum; ALL and pubic-aponeurosis disagreements stated; disc share attributed.
- 3D: BodyParts3D 3.0 skull bones, vertebrae, discs, sacrum, hip bones + Z-Anatomy parts with modifiers applied
  (`z-bp3d-joints-ax.zip`; Z-Anatomy has no ligaments of the atlas and axis, and its intertransverse ligaments have no
  faces). Pivots (`tools/joints/ax_axes.py`): TMJ through both condyles; atlanto-occipital and sacro-iliac pivots put on
  the midline; dens vertical line; L4–L5 disc centre.

## Blood Vessels — `general/blood-vessels.html`

- Fact sheet: `sources-local/facts/vessels-general.md` (289 quotes), script-checked against
  `sources-local/modern/vessels-general/` (downloads 2026-11-18). Gray 1918 Angiology pages, StatPearls, Wikipedia,
  open-access papers (arterial wall PMC11853455, PMC13604391; microcirculation PMC10164225; capillary types PMC9221661,
  PMC5725833; end arteries PMC3367227, PMC13204756; AV anastomoses PMC13678282; portal veins PMC9254532, PMC6011069;
  portal hypertension PMC13645364; venous valves PMC13212415). Excluded: Wikipedia "Tunica intima", "Tunica media",
  "Tunica externa" (OpenStax notice), "Vein" and "Circulatory system" (cite OpenStax); sentences copied from Gray.
- Contested, stated on the page: elastic vs muscular examples (Gray puts femoral and carotid with the lamellated
  arteries); arteriole size; liver sinusoids (discontinuous vs fenestrated); IMV ending; marginal artery
  (poorly developed in half, StatPearls, vs almost always present, Wikipedia); brain perforators (terminal, Gray, vs
  functional end arteries); existence of precapillary sphincters outside the mesentery and brain.
- Left out (one source): umbilical arteries, pulmonary vein count 3–5, no external elastic lamina in veins, arteries
  without valves, Gray's long list of valveless veins, actual/potential anastomoses, coronary arteries as functional
  end arteries, thoroughfare channels, renal "arterial portal" (Wikipedia contradicts itself), left gastro-omental vein
  ending, IMV percentages, blood share of arteries and capillaries, Allen test, aortic-to-capillary size ratio.
- Independent review (2026-11-18), fixed: portal drainage limit (lower anal canal, not the whole canal); middle
  cerebral artery no longer lit in the circle of Willis; microcirculation drawing redrawn so every capillary drains
  into the venule (the metarteriole no longer runs on to the venule: thoroughfare channels are single-source);
  size ratio removed; "another" portal system; collateral flow "partly"; artery wall "thicker media (muscle and
  elastic tissue)"; model name of the transverse cervical branch; orientation arteries in the portal view said so;
  schematic: basement membrane on the capillary, venous elastic network dashed, capillary lumen colour.
- 3D: the Anatomy home's heart and vessels model (`models/body-vessels`), no new build. Topics light vessels by their
  Z-Anatomy names; checked each in a screenshot (circle of Willis from below with the vessels outside the head hidden).
