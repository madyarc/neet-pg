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
