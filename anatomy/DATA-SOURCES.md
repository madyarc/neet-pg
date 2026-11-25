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

- Additions (2026-11-18/20; fact sheet `sources-local/facts/fill-skull.md`, 206 quotes, script-checked against
  `sources-local/modern/fill-skull/`; Gray 1918 pp. 13, 17, 18, 31–47, 49, 144, 171, 193, 200, 202, 204; StatPearls
  (basilar fractures, Battle sign, dural sinuses, cavernous sinus, tentorium, falx, MMA, greater petrosal nerve, CN V,
  jugular foramen, ossification); open-access papers PMC10080110, PMC10080008, PMC6168052, PMC6050782, PMC6837784,
  PMC10462404, PMC3353710, PMC5913417, PMC11831567, PMC6959958, PMC13384707, PMC5111326, PMC11807260, PMC10971245,
  PMC6108977, PMC11176318, PMC13613290, PMC12649854; Wikipedia, Gray copies not counted; "Cranial cavity" excluded
  (cites OpenStax)): falx and tentorium compartments with the dural sinuses in 3D, middle meningeal artery, further
  floor foramina, related structures and fracture signs per fossa, a "Base, from below" view, jugular foramen schemes,
  a "How the bones form" tab; "formed in" line per bone on `skull-bones.html`. 3D vessels and nerves from the home
  layers, loaded on demand; points placed on the mesh from the textbook wording, approximate.
- Disagreements shown: Battle's sign fossa; Gray's 3 vs the modern 2-part jugular foramen; clavicle membrane vs mixed;
  sphenoid membrane parts (Gray 35 vs Gray 17, same wording on both pages); fontanelle closure incl. the lateral
  fontanelles (Gray vs Wikipedia); chorda tympani canal. Attributed (one source): foramen caecum vein, posterior
  ethmoidal nerve, inferior concha in cartilage, fate of Meckel's cartilage (Gray; Wikipedia copies him). Left out:
  venous plexus of the carotid canal, hypoglossal canal artery and plexus, falx cerebelli on the occipital crest.
- Independent review (2026-11-20), fixed: tentorium borders (free → anterior clinoid, attached → posterior clinoid);
  mandible "mostly in membrane"; straight sinus second source PMC6168052; inferior petrosal sinus in the pars nervosa;
  label and marker positions in the MMA and posterior-fossa views. The home vessels model now mirrors the cavernous
  sinus (`tools/zanat/body_vessels.py`).
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

- Additions (2026-11-18; `fill-trunk.md` Part G): "Deformities and defects" tab: scoliosis (3D S-bend, Cobb angle),
  hyperlordosis, spondylolysis/spondylolisthesis (3D slip, L5 pars marked approximately: L5 vertices nearest
  [±19, −55, 940] mm, checked in three views; Meyerding grades), spina bifida types (drawings). Gray p. 25; StatPearls
  28613518, 28722876, 30020705, 30855876, 31424775, 29763083, 32644691, 32965845, 31536302; PMC13585927,
  PMC12558799; Wikipedia. Bends and slips are schematic rigid transforms. Review fixed: scoliosis drawing was mirrored;
  myelomeningocele "commonest of the open forms"; AFP in the open forms; isthmic "commonest" attributed to Wikipedia.
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

- Additions (2026-11-18; `sources-local/facts/fill-trunk.md` Parts A–D, H; 276 quotes, script-checked): inlet,
  cavity and mediastinum (schematic + 3D sternal-angle line), structures through the inlet lit in 3D, thoracic outlet
  syndrome (forms, cervical rib, three spaces lit in 3D), all thoracic joints incl. xiphisternal, costochondral,
  interchondral, breathing (pump-handle, bucket-handle, diaphragm; animated). Gray pp. 26–28, 76–78, 117, 237–240;
  StatPearls 30969641, 30085590, 30137860, 31334942, 32491382, 31082045, 30422526, 29262242, 30855912, 31082185,
  29083651; PMC13205449, PMC13681301, PMC5154401, PMC13750572, PMC12464809, PMC13385665, PMC12160079, PMC13491613,
  PMC11706305, PMC11727880; Wikipedia. TOS percentages: neurogenic 80–95 %+ (sources differ), arterial <1 %; venous
  2–3 % (PMC13205449) vs 4–20 % (Wikipedia) not shown.
- Wikipedia "Rib cage" cites OpenStax and is excluded: the statements it supported in the older sheet (`thorax.md` G6)
  are re-sourced with StatPearls, attributed to Gray ("vertebrosternal", "vertebrochondral", "vertebral ribs",
  intra-articular ligament) or removed (Part H). Rib 10 meeting one vertebra: Gray always, StatPearls a variant.
- Independent review (2026-11-18), fixed: mediastinum drawing line at T4/T5; single-source TOS space details
  removed; brachiocephalic trunk added to the inlet; bucket-handle ribs 7–10.
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

- Additions (2026-11-18; `fill-trunk.md` Parts E–F): anterior abdominal wall layers (Camper, Scarpa with attachments
  and continuity, transversalis fascia, extraperitoneal fat), wall arteries in 3D (right side of the body-vessels pack;
  the superficial circumflex iliac artery is not in the model), diaphragm development, Bochdalek/Morgagni, sliding vs
  rolling hiatal hernia (types I–IV), eventration, traumatic rupture. Gray pp. 117, 118, 135, 148, 156, 157;
  StatPearls 31985930, 30247850, 29939686, 30725841, 32965871, 32310536, 32809332, 29262087; PMC12213017,
  PMC13509838, PMC13179270, PMC13448060; Wikipedia (Gray copies not counted). Left out: "sternocostal triangle" (in no
  source read), hiatal type II "rarest" (one source).
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


- Additions (2026-11-18; fact sheet `sources-local/facts/fill-hn.md`, 257 quotes, script-checked; Gray 1918 sections
  144, 168, 177, 202, 204, 205, 216, 236, 242–244, 279–280; 26 StatPearls abstracts; 18 open-access papers incl.
  PMC10884764 (facial palsy task force), PMC5398733 (Horner), PMC8356106 (tonsil), PMC11857515, PMC13346026 (deep neck
  spaces), PMC1766559 (tongue lymph), PMC10052824 (external jugular); Wikipedia, Gray copies excluded): last tab rows
  for the facial nerve course and lesion levels, Horner pathway, squint types, neck spaces, pharynx, larynx and tongue
  supply, pulse points and vertebral levels. 3D from the whole-body nerve, vessel and lymph layers (right side, loaded
  on demand); pulse and level markers computed from the meshes, approximate. Not in the model: greater petrosal nerve,
  nerve to stapedius, tonsillar, ascending palatine, lingual, superior thyroid and laryngeal arteries.
- Disagreements shown: superior cervical ganglion level (Gray C2–C3, StatPearls C3–C4); hyoid level (C4 Gray and
  StatPearls, C3 Wikipedia); Gray's wider "vestibule" of the larynx. Left out (one source): primary vs secondary
  deviation definition, external jugular surface line to mid-clavicle, laryngeal epithelium, V2 to the nasopharynx and
  tonsil, referred ear pain after tonsillectomy, molar roots below the mylohyoid line, maxillary pharyngeal branch,
  Ramsay Hunt tinnitus, retropharyngeal abscess age.
- Independent review (2026-11-18), fixed: those single-source sentences; tongue schematic (IX area follows the sulcus
  terminalis); verification notes moved off the page; carotid and temporal pulse markers and labels.
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

## Nerves, Vessels and Lymph Nodes of the Upper Limb — `upper-limb/nerves-vessels.html`

- Fact sheet `sources-local/facts/fill-ulnv.md` (764 quotes, script-checked against `sources-local/modern/fill-ulnv/`,
  downloads 2026-11-20): Gray 1918 pages 122–126, 148–152, 172, 178, 209–211, 289–290; StatPearls; Wikipedia; open
  papers (axilla review PMC11909697; brachial plexus PMC8695258, PMC10793125, PMC10982913; deltoid injection
  PMC13208304, PMC11379345; hand of benediction PMC9616636; epitrochlear nodes PMC6823563; dermatomes PMC12097171;
  others in the sheet). Excluded: Wikipedia sentences copied from or credited to Gray.
- Contested, stated on the page: ribs of the medial wall (4 or 5); brachial vein ending; median nerve roots (C6–T1 or
  C5–T1, C5 dashed in the diagram); axillary nerve level and injection site; middle finger in the hand of benediction;
  radial branch completing the superficial arch; posterior interosseous artery course; superficial arch level (Gray vs
  Kaplan's line); dermatome maps.
- Left out (one source): what passes through the axillary apex, Erb's point, wrist flexion in the waiter's tip, prefixed
  and postfixed rates, "75 % of breast lymph", Guyon zones, brachial blood pressure, lateral thoracic artery supply,
  ASIA use of the Foerster map.
- Model `models/ul-nv` (`tools/upper-limb/nv_config.py`): right upper-limb bones, muscles (glass), Z-Anatomy vessels,
  nerves and nodes, keys and `error_mm` as the whole-body configs; 852 KB pack. Z-Anatomy's apical and "lateral
  axillary" nodes are misplaced and hidden; it has no lateral or medial cord and no superior thoracic artery (said on
  the page). The model's palmar arches lie further apart than the surface marking: approximate.
- Independent review (2026-11-20), fixed: venepuncture wording ("receives a communicating branch"), Klumpke Horner
  "when T1 is involved", muscles-glass toggle bug in injury views, arch distance note, T1/T2 dermatome bands, median
  roots in the diagram, cubital fossa labels, deltoid-injection note, phone hint for the plexus diagram.

## Nerves, Vessels and Lymph Nodes of the Lower Limb — `lower-limb/nerves-vessels.html`

- Fact sheet `sources-local/facts/fill-llnv.md` (636 quotes, script-checked against `sources-local/modern/fill-llnv/`
  and the folders of the reused fill-ll, joints-hip-knee and ll-muscles-b sections; downloads 2026-11-21): Gray 1918
  pages 127, 155–162, 173, 179, 212, 213, 291, 292; StatPearls (about 30 chapters); Wikipedia; open papers (lumbar
  plexus ultrasound and disorders 2026, profunda femoris 2025, femoral vein landmarks 2025, saphenofemoral junction
  2026, sciatic division meta-analysis 2026, psoas abscess reviews, Japanese Hernia Society groin hernia guideline 2024,
  corona mortis 2025, popliteal aneurysm reviews, femoral neck fracture vascular consensus 2026, incompetent
  perforators 2024, obturator neuropathy PMC13463367, inguinal node metastases 2026). Excluded: Wikipedia sentences
  copied from or credited to Gray; no OpenStax notice in any article used.
- Contested, stated on the page: sciatic roots (L4–S3, one StatPearls chapter L4–S4); extent of the sacral plexus
  (Gray to S3 with a separate pudendal plexus from parts of S2–S3, S4–S5 and coccygeal); profunda origin 2–5 cm below
  the inguinal ligament; direction in which the popliteal vein crosses the artery (Gray followed).
- Single source, attributed on the page: anterior tibial pulse at the front of the ankle (Gray 291); order of structures
  behind the medial malleolus (Gray 162).
- Left out (one source): Hunterian perforator, Virchow's triad, Trendelenburg test, the "superficial femoral" misnomer,
  testis drainage, node size cut-offs, corona mortis frequencies, tarsal and arcuate branches, number of popliteal nodes,
  femoral pulse depth, prone position for the popliteal pulse, risk factors for varicose veins.
- Model `models/ll-nv` (`tools/lower-limb/nv_config.py`): right lower-limb bones with hip bone, sacrum and L5, muscles
  (glass), Z-Anatomy vessels, nerves and nodes, keys and `error_mm` as the whole-body configs; 209 parts, 865 KB pack.
  Z-Anatomy lacks the inferior gluteal nerve, lumbosacral trunk, plexus roots, superficial circumflex iliac vessels,
  descending genicular artery and medial calcaneal nerve (said on the page).
- Independent review (2026-11-21), fixed: popliteal fossa and femoral hernia views (muscles as glass, hidden labels),
  "four pulses plus the anterior tibial (Gray)", Cloquet's node at the femoral ring, popliteal node numbers removed,
  causes of obturator neuropathy, eleven single-source statements sourced twice, attributed or cut, division of the
  posterior tibial artery and tibial nerve in the sole, tarsal tunnel wording, Gray's pudendal plexus roots, nerve
  contrast on bone, row highlighting.

## The Heart — `thorax/heart.html`

- Fact sheet `sources-local/facts/fill-heart.md` (398 quotes, script-checked against `sources-local/modern/fill-heart/`,
  downloads 2026-11-21): Gray 1918 pages 137, 138, 142, 166, 210, 284; StatPearls; Wikipedia; open papers PMC12175212,
  PMC12060931, PMC11179863, PMC13363422, PMC4743947, PMC3537199, PMC11775805, PMC12861964, PMC13329930, PMC7330354,
  PMC7712333, PMC11602569, PMC12789789, PMC9579841, PMC6221866, PMC8008978, PMC9848245, PMC6524010.
- Excluded: Wikipedia "Heart" and "Cardiac conduction system" (OpenStax notice) and "Coronary circulation" (cites an
  OpenStax author); Wikipedia sentences copied from Gray.
- Contested, stated on the page: coronary dominance frequencies (six series); SA nodal artery from the RCA (60–68 %) or
  the circumflex; AV nodal artery from the RCA (72 % to about 90 %); supply of the posteromedial papillary muscle;
  coronary sinus length; two (Gray) or three right-ventricular papillary muscles; whether the coronary arteries
  anastomose; arteries of the pericardium (Gray vs Wikipedia).
- Left out (one source): vagal and sympathetic nerves and aortic branches to the pericardium, limbus of the fossa ovalis,
  left fascicles, Beck's triad.
- Surface points: Gray 284 applied to the model's own ribs, second source PMC8008978.
- Model `models/heart` (`tools/thorax/heart_config.py`): Z-Anatomy chambers, valve cusps (with chordae), papillary
  muscles, coronary arteries, cardiac veins, great-vessel roots; BodyParts3D sternum, ribs and cartilages 1–7; 73 parts,
  522 KB pack. Z-Anatomy has no pericardium, fibrous skeleton or conducting tissue: schematics instead; the SA and AV
  node points are approximate. Chambers are cut open with the viewer's clip plane.
- Independent review (2026-11-21), fixed: fibrous-skeleton and right-atrium schematics were mirrored (now match the 3D
  views); posteromedial papillary muscle supply; pericardial arteries attributed; territory labels; SA nodal artery
  "most often" behind the SVC; heart position on the chest; single-source details attributed or cut; mitral point and
  text agree; infarct wording.

## Nerves, Vessels and Lymphatics of the Thorax — `thorax/nerves-vessels.html`

- Fact sheet `sources-local/facts/fill-thnv.md` (402 quotes, script-checked against `sources-local/modern/fill-thnv/`,
  downloads 2026-11-21): Gray 1918 pages 142, 148, 153, 172, 176, 181, 205, 210, 211, 217, 239; 26 StatPearls
  abstracts; open papers (ICS/NCCP pleural procedures guideline 2024, azygos system review 2025, PMC13624812 on the
  thoracoabdominal nerves, PMC11409315 on coarctation collaterals, others in the sheet); Wikipedia. Excluded as Gray
  copies (Part N): Costocervical trunk, Subcostal arteries and nerve, Parasternal and Thoracic lymph nodes, parts of
  Hemiazygos, Thoracic aorta, Intercostal nerves and arteries, Mediastinum, Accessory hemiazygos. No OpenStax.
- Contested, stated on the page: thoracic duct start (L2 or T12) and arch height; right lymphatic duct ending (Gray vs
  Wikipedia); internal thoracic artery distance from the sternum; posterior mediastinum level; hemiazygos (T8/T9) and
  accessory hemiazygos (T7/T8) crossing levels; lesser splanchnic roots; intercostal muscle layer of the bundle.
- Single source, attributed: typical 3rd–6th nerves (Gray); arch behind the 2nd right sternocostal joint (Gray).
- Left out (one source): tributaries of the thoracic duct beyond the cisterna chyli, hemiazygos origin, subcostal artery
  course, oesophageal relations of the aorta, drainage of each node group, transverse cervical collateral.
- Model `models/thorax-nv` (`tools/thorax/nv_config.py`): 136 parts, 887 KB pack, left side mirrored. Z-Anatomy has no
  thoracic duct and no phrenic nerve: approximate lines (`fill-thnv-scripts/paths.py`), checked in screenshots. Its
  "superior intercostal vein" parts are all the intercostal veins of a side, and its thoracic/abdominal aorta split is
  at about T10 (said on the page).
- Independent review (2026-11-21), fixed: right lymphatic duct ending, atypical nerves second source, rib notching
  second source, hemiazygos origin removed from the levels chart, needle path in the intercostal schematic, bronchial
  arteries, labels on hidden parts, phrenic sensory wording, six single-source statements cut, visuals.

## Nerves and Vessels of the Abdomen and Pelvis — `abdomen-pelvis/nerves-vessels.html`

- Fact sheet `sources-local/facts/fill-abnv.md` (651 quotes, script-checked against `sources-local/modern/fill-abnv/`,
  downloads 2026-11-21; reuses fill-llnv sections with their files copied): Gray 1918 pages 154–156, 173, 174, 180, 212,
  213, 218–220; 36 StatPearls abstracts; 13 open papers; 99 Wikipedia articles (none with an OpenStax notice or Betts
  citation). Excluded as Gray copies: Abdominal aorta relations, Lumbar arteries, Celiac ganglia, Abdominal aortic
  plexus, Ganglion impar, Internal iliac relations and collaterals, Internal iliac length.
- Contested, stated on the page: common iliac length (Gray 5 cm, Wikipedia 4 cm); share of the transverse colon from
  the SMA (half or two-thirds); sacral plexus to S3 or S4; IMA origin level (about 60 % at L3).
- Single source, attributed: variceal bleeding as the commonest fatal complication of cirrhosis (StatPearls); far-lateral
  disc mimicking a plexus lesion (2026 review); lumbar artery origins (Gray).
- Left out (one source): AAA "85 % infrarenal" and smoking, portal vein valves, cisterna chyli level, IVC tributary
  levels, coeliac bifurcation rate, Wilkie's name, pudendal block in labour, secondary autonomic plexuses, internal
  iliac relations and collaterals, portal vein free-edge relation, gonadal vein angles, prolonged sitting in pudendal
  entrapment.
- Model `models/abd-nv` (`tools/abdomen-pelvis/nv_config.py`): 171 parts, 860 KB pack, 51 left parts mirrored in the
  page. Z-Anatomy has no autonomic plexuses and its sympathetic trunk stops at L1: plexus markers approximate.
- Independent review (2026-11-21), fixed: AAA and popliteal aneurysm direction, aortic plexus position, six unsourced
  statements sourced or cut, five single-source statements attributed or cut, "paired visceral" wording, iliac
  arteries drawn in front of the IVC, table row highlighting, portal and IVC labels.
- Home page: `tools/home/region_pages.py` writes `models/region-pages.json`, so "Trunk" parts open the thorax, abdomen,
  upper-limb or lower-limb page whose model contains them. The sigmoid veins are now tagged portal in
  `models/body-vessels/vessels.json` (Gray 173, Wikipedia "Inferior mesenteric vein").


## Nerves, Vessels and Lymph Nodes of the Head and Neck — `head-neck/nerves-vessels.html`

- Fact sheet `sources-local/facts/fill-hnnv.md` (610 quotes, script-checked against `sources-local/modern/fill-hnnv/`,
  downloads 2026-11-21): Gray 1918; StatPearls abstracts; open-access papers (scalp innervation, facial vein
  dissections, carotid bifurcation CT, vertebral artery, subclavian imaging, interscalene triangle, neurogenic and
  cervical-rib thoracic outlet syndrome, recurrent laryngeal nerve variants, bilateral vocal fold paralysis,
  hypoglossal palsy, accessory nerve injury, three on neck node levels, a transradial angiography trial); 105
  Wikipedia articles (none with an OpenStax notice or Betts citation). Excluded as Gray copies: the whole Subclavian
  artery and Facial artery articles and parts of about 15 others (listed in the sheet header). Node levels: AAO 2002.
- Contested, stated on the page: facial vein valves (Gray none, dissections in most); cervical rib frequency
  (0.5–1 % StatPearls, 0.2–0.5 % Wikipedia); internal carotid on the medial wall of or through the cavernous sinus;
  carotid division level by CT (C3 in 44 %, C4 in 27 % of sides).
- Single source, attributed: external carotid position at its start, condylar and foramen-caecum emissary links,
  submandibular, mastoid, preauricular and retropharyngeal node details (Gray); cavernous sinus thrombosis eye signs,
  sinus valves, cervical-rib vascular signs, accessory palsy signs (Wikipedia); cervical-rib numbness and hypoglossal
  palsy causes (2026 review).
- Left out (one source): scalp wound bleeding and gaping, the surgical plane of the scalp, third occipital nerve, ICA
  segments C1–C7, lacrimal artery course, retinal artery emboli, grey rami, subclavian artery surface line,
  Erb's 90 % and waiter's tip, supraclavicular nodes in lung and breast cancer, and others (sheet part S).
- Model `models/hn-nv` (`tools/head-neck/nv_config.py`): 204 parts, 884 KB pack, 137 left parts mirrored in the page.
  Z-Anatomy has no cervical plexus, phrenic nerve, pterygoid plexus or deep facial vein: the plexus marker is
  approximate; the superior cervical ganglion ends lower than in textbooks; one thin glossopharyngeal strand runs
  down to about C7 (noted on the page).
- Independent review (2026-11-21), fixed: 3D node levels III–V lit the wrong groups; subclavian schematic (cervical rib
  in front of the artery, common carotid medial, subclavian vein ending on an artery, label overlaps); about 30
  single-source statements attributed or cut; hidden and dropped 3D labels; accessory nerve sentence; level
  highlight and tongue colours; wrong link targets.
- Home page: head and neck vessels, nerves and nodes open this page; the common facial vein (filed under Trunk) via
  `models/region-pages.json`.

## Lungs, Pleura and Trachea — `thorax/lungs.html`

- Fact sheet `sources-local/facts/fill-lung.md` (372 quotes, script-checked against `sources-local/modern/fill-lung/`,
  downloads 2026-11-21): Gray 1918 pages 181, 237, 238, 240, 245, 284; StatPearls abstracts; 29 open-access papers and
  chapters (lung dissection series, CT of the bronchi and a foreign-body study, bronchial-artery reviews, IASLC node map
  review, segment and aspiration sources, a 2021 topography paper, chest X-ray reviews, an oesophagogram review, the
  ICS/NCCP 2024 pleural guideline); Wikipedia ("Lung" excluded: it cites OpenStax; Gray copies excluded).
- Contested, stated on the page: carina level (T4 or T4–5, Gray upper T5); start of the oblique fissure (T2 Gray, T3–T4);
  left pleura to the 6th or 7th cartilage; main bronchus lengths (Gray and CT); azygos lobe 0.3 % or 1 %; whether
  bronchus shape predicts the side of a foreign body.
- Single source, attributed: midclavicular levels of lung and pleura and the 8th costochondral point (Gray); carina
  widening from nodes and pulmonary vein count (Wikipedia); bronchial artery levels (2020 CT review); left atrium and
  dysphagia (2026 case report); oesophagus ending at T11 (StatPearls); no lymphatics in alveolar walls (Gray); spread
  through incomplete fissures (one dissection study).
- Left out (one source): incisor distances of the oesophageal narrowings, the decompression site for tension
  pneumothorax, cough sensitivity of the carina, the 8th–10th space for pleural tap (would fall below the pleura).
- Surface lines are computed on the model's ribs from the written levels (`fill-lung-scripts/surface_lines.py`).
- Model `models/lung` (`tools/thorax/lung_config.py`; Z-Anatomy exports `z-bp3d-lung*.zip`): 168 parts, 798 KB pack,
  nothing mirrored. Z-Anatomy has no separate visceral and parietal pleura, recesses, pulmonary ligament, bronchial
  vessels, phrenic nerve or pulmonary plexus (schematics); its pleura overlaps itself, so faint mottling shows.
- Images: Mikael Häggström, "Normal posteroanterior (PA) chest radiograph (X-ray).jpg", CC0 (resized); Ptrump16,
  "Fluoroscopy of normal barium swallow.gif", frame 60, cropped and resized, CC BY-SA 4.0; licences checked on
  Wikimedia Commons 2026-11-21.
- Independent review (2026-11-21), fixed: a pleural-tap level that fell below the pleura (removed), dropped and faint 3D
  labels (now none dropped on desktop or phone), side labels in the aspiration view, solid fissure lines, colour
  clashes (pleura line with phrenic nerve, segment colours with airway, nerve and vein), nine one-source statements,
  two overstatements, pleura schematic contrast, X-ray label size on phones, barium credit.
- Home page: the lobar and segmental pulmonary vessels open this page (`tools/home/region_pages.py`).

## The Abdominal Cavity: Peritoneum and Organs — `abdomen-pelvis/organs.html`

- Fact sheet `sources-local/facts/fill-abdo.md` (582 quotes, script-checked against `sources-local/modern/fill-abdo/`,
  downloads 2026-11-21): Gray 1918 pages 246–251, 253, 254, 277, 278, 285, 286; StatPearls abstracts; open-access papers
  (WSES 2023 laparotomy guideline, two peritoneal-space imaging reviews, stomach blood supply, liver anatomy,
  cholecystectomy anatomy and the critical view of safety, liver biopsy studies, pancreaticobiliary junction, abdominal
  pain, appendicitis, a Meckel's meta-analysis, splenic rupture and accessory spleens, adrenal veins); Wikipedia
  (Stomach, Kehr's sign and Adrenal gland excluded for citing OpenStax; Gray copies excluded).
- Contested, stated on the page: vertical region lines (Gray's halfway ASIS–symphysis or midclavicular); subcostal
  plane at the upper or lower border of L3; SMA origin at or 2 cm above the transpyloric plane; McBurney's point as
  tenderness or appendix position; side of subphrenic abscess; Calot's triangle original and modern upper boundary;
  lowest point of the cavity (Morison's pouch lying flat, rectouterine pouch).
- Single source, attributed: lengths, hilum order and colon relations (Gray); SMA syndrome, kidney length (Wikipedia);
  ERCP (StatPearls); McBurney incision and incisional hernia (a 2025 history review); nerves at risk in incisions
  (PMC13198815, PMC11324006); selective vagotomy (PMC12083144). Liver biopsy site has two sources (PMC11272270,
  PMC5670258).
- Left out (one source): the clinical use of the splenic notch, Spigelian hernia, the classic seven subphrenic spaces.
- Planes are computed on the model's bones (`fill-abdo-scripts/planes.py`), approximate; the model's iliac tubercle is
  closer to the ASIS than Gray's 5 cm.
- Model `models/abdo` (`tools/abdomen-pelvis/organs_config.py`): 100 parts, 664 KB pack, nothing mirrored. BodyParts3D
  bones, stomach, duodenum, jejunum, ileum, rectum, ureters; Z-Anatomy liver segments, biliary tree, pancreas, colon,
  appendix, omenta, mesocolon, suprarenals, spleen, vessels. Kidneys and renal pelves: "Kidney" by Lissie Cowley as
  included in Z-Anatomy, CC BY-NC 4.0, chosen for its fit to the renal vessels and suprarenals and its separate pelvis.
  Missing (schematics): separate caecum, hepatic and cystic ducts, mesentery, parietal peritoneum, liver and spleen
  ligaments, lesser sac, anterior abdominal wall. The model's SMA and SMV pass through the 3rd part of the duodenum
  and its epiploic-foramen vessels only approximate the textbook arrangement (said on the page).
- Independent review (2026-11-21), fixed: liver biopsy needle wording, linea alba colour, dropped and faint 3D labels
  (now none on desktop or phone), foramen and duodenum caveats, peritonitis and lowest-point wording, subphrenic,
  Calot, horizontal and sagittal schematics, about ten one-source statements, jejunum position, colour clashes, dark
  contrast, incision nerves, selective vagotomy, keyboard access.
- Home page: the spleen (lymph layer) opens this page.

## Face and Neck: Regions and Glands — `head-neck/regions.html`

- Fact sheet `sources-local/facts/fill-hnreg.md` (531 quotes, script-checked against `sources-local/modern/fill-hnreg/`,
  downloads 2026-11-21): Gray 1918 pages 46, 111–116, 121, 144–148, 200–210, 242, 272–273, 280; StatPearls; about 100
  Wikipedia articles (none with an OpenStax notice; Gray copies excluded); open-access papers (sialolithiasis,
  submandibular ganglion, thyroid arteries, external laryngeal nerve, RLN and inferior thyroid artery, parathyroids,
  thyroglossal cysts, Frey's syndrome, parotid duct landmarks, posterior triangle sonoanatomy, neck muscles, pterion,
  great auricular nerve, salivary tumours).
- Contested, stated on the page: thyroid weight (25 or 30 g), lower pole level, isthmus rings, pyramidal lobe frequency,
  pterion distance behind the frontozygomatic suture, parotid duct length and surface line (Gray's or tragus to mouth
  corner), one-side action of semispinalis, splenius nerve roots, accessory parotid "usually" or "sometimes".
- Single source, attributed: scalene levels, pterygomaxillary fissure, infratemporal walls (Gray); maxillary artery and
  lateral pterygoid (StatPearls); nerves to protect in stone surgery (one source each).
- Left out (one source or none): where to tie the thyroid arteries, the prevertebral fascia as the posterior triangle
  floor's covering.
- Model `models/hn-reg` (`tools/head-neck/regions_config.py`; Z-Anatomy glands and ducts exported with modifiers
  applied, `z-bp3d-hnreg*.zip`): 141 parts, 636 KB pack, 94 left parts mirrored in the page. Z-Anatomy's thyroid and
  parathyroids sit about 2 cm high: the page draws the textbook outline from Gray's levels and says so. The model's
  lingual and hypoglossal nerves don't show the textbook relation to the duct (schematic instead). Missing: otic and
  submandibular ganglia, auriculotemporal nerve, cervical plexus, laryngeal nerves, superior thyroid and lingual
  arteries, middle and inferior thyroid veins, pyramidal lobe, semispinalis capitis (schematics).
- Independent review (2026-11-21), fixed: face sensory map (lips, nose tip, great auricular area, duct line), parotid
  section orientation, carotid sheath contents, model caveats for parathyroids and the lingual nerve, swallow
  animation, RLN crossing the inferior thyroid artery, faint labels (now none), about eight one-source statements,
  colours; added the accessory nerve surface line.

## Mouth, Pharynx, Nose and Larynx — `head-neck/mouth-pharynx-nose.html`

- Fact sheet `sources-local/facts/fill-oro.md` (430 quotes, script-checked against `sources-local/modern/fill-oro/`,
  downloads 2026-11-21): Gray 1918 pages 223, 236, 242–244; StatPearls; Wikipedia (no OpenStax notices; about 40
  articles carry Gray text and the copied sentences are not counted); open-access papers (tonsils and adenoids,
  adenotonsillectomy, soft palate, Killian's triangle, pyriform sinus, hypopharyngeal cancer, epistaxis, sinonasal CT,
  rhinosinusitis 2024, sinonasal tumours, maxillary carcinoma, ICA distance in tonsillectomy).
- Contested, stated on the page: palate muscle nerve (accessory or vagus), tonsil crypt count, four or five arteries
  at Kiesselbach's plexus, back wall of the retropharyngeal space (alar or prevertebral fascia), adenoid peak age, croup
  peak age, timing of secondary haemorrhage.
- Single source, attributed: sinus functions (Wikipedia, debated), adenoid facies, uvula deviation, quinsy as the
  commonest deep neck infection (StatPearls), aspiration or incision (Wikipedia), pyriform foreign-body removal and
  nerve block (one paper each), molar roots and nasal branch areas (Gray), the "about half" pyriform cancer figure.
- Left out (one source): supratonsillar fossa, the paratonsillar vein as the bleeding source, the RLN under the pyriform
  mucosa, ear pain after tonsillectomy.
- Model `models/oro` (`tools/head-neck/oro_config.py`; Z-Anatomy soft tissues exported with modifiers applied,
  `z-bp3d-oro*.zip`): 107 parts, 653 KB pack, 57 left parts mirrored in the page; midline topics use a clip plane. No
  maxillary sinus mesh in either source: markers placed inside the model's maxilla. Adenoid, tubal and lingual
  tonsils, Little's area, Killian's dehiscence, pyriform fossa, aryepiglottic fold and retropharyngeal nodes are
  hand-placed and labelled approximate. The model's quadrangular membrane and retropharyngeal nodes sit wrongly, its
  glossopharyngeal nerve and septal arteries stop short (said on the page). Missing: levator and tensor veli palatini,
  palatoglossus, vocal folds, tonsillar and lingual arteries, palatine and laryngeal nerves.
- Independent review (2026-11-22), fixed: pyriform fold drawn lateral to the fossa, maxillary nerve cut away by the
  clip, maxillary markers off-canvas, model caveats, quinsy, epistaxis and pyriform sourcing, laryngeal epithelium,
  label collisions, dark contrast, colours, accessibility.

## The Ear and the Eye — `head-neck/ear-eye.html`

- Fact sheet `sources-local/facts/fill-eareye.md` (522 quotes, script-checked against `sources-local/modern/fill-eareye/`,
  downloads 2026-11-22): Gray 1918 pages 35, 146, 197–203, 224–232, 275; 31 StatPearls abstracts; 94 Wikipedia
  articles (no OpenStax notices; Tympanic cavity, Outer ear and Petrous part not used as they copy Gray; other copied
  sentences not counted); open-access papers PMC9647717, PMC9360827, PMC12746166 (tympanostomy site), PMC13230221
  (temporal bone CT), PMC10294180 (jugular bulb), PMC12122612, PMC13720400, PMC12801116 (auditory tube), PMC12752107
  (CRAO).
- Contested, stated on the page: cornea layers (five, Gray four); greater petrosal nerve (parasympathetic, Gray mainly
  sensory); narrowest point of the meatus (Gray in the bony part, StatPearls at the junction).
- Single source, attributed: cone of light (Wikipedia), pain sign in otitis externa and spread of necrotising otitis
  externa (StatPearls), round window, carotid relation, central retinal artery course, lateral canal at the aditus,
  lacrimal fossa (Gray), child tube length (2025 review), jugular bulb dehiscence (2023 CT study), Edinger–Westphal
  and superior salivatory nuclei, uveoscleral route, intraocular lens, hyperacusis, macroadenoma size (Wikipedia).
- Left out (one source): cochlear tonotopy, ion values, the eardrum's tilt, nasolacrimal duct length, number of
  lacrimal ducts; AN31.5's "secondary deviation larger than primary" (searched again 2026-11-22).
- Model `models/eareye` (`tools/head-neck/eareye_config.py`; `z-bp3d-eareye.zip`): 83 parts, 631 KB pack, left eyeball
  mirrored in the page. Bones, optic pathway and pituitary: BodyParts3D. Temporal bone, ossicles, eardrum, auricle,
  eye, lacrimal parts, muscles, vessels, nerves: Z-Anatomy (its temporal bone fits its inner ear far better).
  Cochlea and vestibule: Z-Anatomy after University of Dundee "Anatomy of the Inner Ear", CC BY-NC-SA 4.0. The
  model's chorda tympani lies outside the middle ear, its auditory tube is nearly horizontal, and its chiasm is
  about 2 mm above the pituitary (said on the page). Missing: tensor tympani, stapedius, choroid, ciliary body,
  labyrinthine artery (schematics).
- Image: Michael Hawke MD, "TM RIGHT NORMAL.jpg", Wikimedia Commons, CC BY-SA 4.0 (checked 2026-11-22), resized and
  labelled → `head-neck/img/tm-right-normal.jpg`.
- Independent review (2026-11-22), fixed: canal, tragus and lobule labels on the wrong spots, model notes for the
  chorda and tube, cone of light and isthmus sourcing, seven one-source statements, pituitary visual-field layout,
  eye schematic cut labels and Schlemm's canal, dark contrast, colours (extraocular muscles now muscle red).

## Pelvic Viscera; Perineum and Male External Genitalia — `abdomen-pelvis/pelvis.html`, `abdomen-pelvis/perineum.html`

- Fact sheet `sources-local/facts/fill-pelv.md` (796 quotes, script-checked against `sources-local/modern/fill-pelv/`,
  downloads 2026-11-22): Gray 1918 pages 118–120, 155, 180, 249, 252, 255–270, 287–288; 47 StatPearls abstracts; about
  20 open-access papers (internal iliac ligation 2023, urethral injury, prostate zones, haemorrhoids, fistula, tears,
  episiotomy, descent); Wikipedia (Ovary and Uterus excluded for citing OpenStax; Gray copies not counted).
- Contested, stated on the page: which testis hangs lower; time of descent; artery to the ductus; seminal vesicle
  length; prostate zone shares; tubal share of ectopic pregnancy; symptoms of retroversion; the urogenital diaphragm.
- Single source, attributed: pectinate-line table rows (Wikipedia; arteries also Gray), phimosis resolution, uterine
  body and vaginal lymph and ovarian fossa (Gray), extravasation "not into the thigh" (Gray), ilio-inguinal nerve
  outside the cord and cervix nerves (Wikipedia), sympathetic levels of the bladder (StatPearls).
- Left out (one source): Goodsall's rule, anteversion angles, bony landmarks per rectum or vagina, the part of the tube
  used for ligation, why fissures are posterior, urine spreading into the deep pouch, the "autonomous bladder" term.
- Model `models/pelv` (`tools/abdomen-pelvis/pelvis_config.py`; `z-bp3d-pelv*.zip`): 77 parts, 391 KB pack, 33 left
  parts mirrored in the page. BodyParts3D organs and bones; Z-Anatomy pelvic floor, ligaments, ducts, vessels, nerves,
  nodes. Male only: neither source has female pelvic organs (schematics). The model's ductus ends at the tip of the
  seminal vesicle, its pudendal nerve lies medial to the vessels, its right testicular vein ends short of the IVC (said
  on the page).
- Independent review (2026-11-22), fixed: palpable vs relation per rectum, extravasation of urine added, one-source
  table rows, phimosis wording, cryptorchidism side, episiotomy wording, model caveats, testis caption, lesion dimming,
  colours, schematic layers and label collisions, sourcing of levels and nerves.
- AN48.3: internal iliac relations completed with PMC10801552.

## Anatomy home: Joints and ligaments, and Organs layers — `index.html`

- Joints and ligaments (`models/body-joints`, 236 parts, 1.09 MB; `tools/home/body_layers.py`): the ligaments,
  capsules, discs, menisci, labra, bursae, interosseous membranes and fat pad of the regional joint models. Z-Anatomy
  (CC BY-SA 4.0, from BodyParts3D), modifiers applied, in the BodyParts3D frame; intervertebral discs from BodyParts3D
  (CC BY-SA 2.1 Japan). Same keys as the regional models, the thinnest parts slightly coarser; right side mirrored to
  the left. A second tap opens the regional joints page.
- Organs (`models/body-organs`, 102 parts, 0.63 MB): organs of the lung, abdominal, pelvic, neck-gland,
  mouth-pharynx and ear-eye models, with the same sources (the kidney is Z-Anatomy's CC BY-NC 4.0 model, as on the
  abdominal page). Each organ is coloured as on its own page and a second tap opens that page. Heart chambers are in
  the vessel layer; spleen and tonsil in the lymph layer; the pelvis is male, as in the model.

## Meninges, CSF and the Spinal Cord; Brainstem and Cerebellum — `neuro/meninges-cord.html`, `neuro/brainstem.html`

- Fact sheet `sources-local/facts/fill-neuro1.md` (609 quotes, script-checked against `sources-local/modern/fill-neuro1/`,
  downloads 2026-11-22): Gray 1918 pages 185, 187, 188, 191, 193, 194, 198–201, 204; StatPearls (cord, tracts, lesion
  and brainstem syndrome chapters); Wikipedia (Gray copies not counted); a 2022 lumbar puncture review (PMC10295920),
  a 2025 spinal anaesthesia review, reviews PMC7710193 and PMC12721976, case reports.
- Contested, stated on the page: share of pyramidal fibres crossing (Gray two-thirds, Wikipedia 75–90 %), enlargement
  levels, cord end at birth, Tuffier's line, cerebellar cortex layers, trochlear nucleus level, mesencephalic root of
  V, Millard–Gubler with or without VI, Foville, pontine haemorrhage share.
- Single source, attributed: Brown-Séquard level, spinothalamic crossing within 1–2 segments, segments higher than
  vertebrae, ALS and syringomyelia details (Wikipedia); fifth-month cord level and fissure depth (Gray); III through
  the red nucleus (StatPearls); cruciate paralysis for "crossed diplegia" (AN58.4, one case report with review).
- Left out (one source or none): which ventricles enlarge in each type of hydrocephalus, cauda equina paraplegia,
  taste in the upper solitary nucleus, the paravermis as vestibulocerebellum.
- Model `models/neuro1` (`tools/neuro/neuro1_config.py`; `z-bp3d-neuro1*.zip`): 121 parts, 810 KB pack. Brainstem,
  cerebellum and ventricles: BodyParts3D (CC BY-SA 2.1 Japan). Cord (rebuilt by `export_cord.py`, faces flipped by
  `flip_cord.py`), olive, pyramid, nuclei, dura, nerves and vessels: Z-Anatomy (CC BY-SA 4.0). No Brainder or
  White-matter meshes. The model's dural sac ends at L2 (the page gives the real level, S2).
- Independent review (2026-11-22), fixed: anterior spinal artery lesion area, fourth ventricle position, Millard–Gubler
  overlay and facial loop, V root label, about a dozen one-source statements, cerebellum caption and paravermis aside,
  colours (white-matter bundles token), keyboard focus, unused model parts, dark 3D cord sections.

## Cerebrum, Ventricles and Sensory Pathways; Nervous System — `neuro/cerebrum.html`, `general/nervous-system.html`

- Fact sheet `sources-local/facts/fill-neuro2.md` (621 quotes, script-checked against `sources-local/modern/fill-neuro2/`,
  downloads 2026-11-22): Gray 1918 pages 146, 148, 183, 189–191, 194, 196, 197, 208, 209, 214, 233; StatPearls; open
  papers PMC13189687, PMC7710193, PMC11318184, PMC10991002, PMC13657594, PMC10960742, PMC10710919, PMC4518744,
  PMC11074696, PMC4280388, PMC11767383 (central facial palsy, 2025). Wikipedia articles citing OpenStax excluded
  (Neuron, Chemical synapse, Diencephalon, White and Gray ramus communicans, Lateralization of brain function,
  Ventricular system, Motor unit, Precentral gyrus, Brodmann area); Gray copies not counted.
- Contested, stated on the page: "unipolar" (Gray) vs pseudounipolar; taste ending in the solitary nucleus (Gray
  unsure); language on the left in about 95 %; upper-face sparing in central facial palsy (mild weakness reported).
- Single source, attributed: taste via VPM and the VL relay, internal capsule blood-supply split, electrical synapse
  details, fibrillations, alpha/gamma motor neurons, microglia, homunculus layout, Meyer's loop, corpus callosum
  length, Huntington's onset, Parkinson's cell loss, thalamic syndrome details (Wikipedia or StatPearls); Golgi types
  and motor unit (Wikipedia).
- Left out (one source): order of the nucleus columns, tongue in genu lesions, satellite-cell ring difference, motor
  unit size rule, left-hander language figures.
- Model `models/neuro2` (`tools/neuro/neuro2_config.py`): 123 parts, 998 KB pack, 23 arteries mirrored in the page.
  Brain meshes and skull: BodyParts3D 3.0 (CC BY-SA 2.1 Japan), two relabelled by position ("accessory short gyrus"
  as the inferior frontal gyrus; "anterior limb of internal capsule" as the whole capsule). Arteries: Z-Anatomy (CC
  BY-SA 4.0), sitting only approximately on the BodyParts3D brain; lenticulostriate arteries stop short (said on the
  page).
- Independent review (2026-11-22), fixed: genu lesion (lower face only), internal capsule caption side, nucleus
  column order, attributions, wording, colours, 3D labels, schematic clipping, keyboard access, swipe hints, contrast.

## Histology I: Epithelium and Glands; Nervous Tissue and Blood Vessels; Lymphoid Organs, Bone and Skin — `histology/`

- Fact sheet `sources-local/facts/fill-histo1.md` (414 quotes, script-checked against `sources-local/modern/fill-histo1/`,
  built from `fill-histo1-scripts/spec-*.md`, downloads 2026-11-22): Gray 1918 pages 18, 133, 175, 183, 234, 237, 242,
  243, 245, 247, 248, 255, 272, 274, 278; StatPearls histology chapters; open papers PMC12525432, PMC1995455,
  PMC11132765, PMC9599896, PMC10704243, PMC9705259, PMC11965237, PMC11924920, PMC10416754, PMC12956672, PMC13762532,
  PMC12188952, PMC13246397 and the vessel papers; Wikipedia. Excluded for OpenStax notices: Wikipedia Neuron, Chemical
  synapse, Bone, Skin, Epidermis, Stratum basale, Stratum spinosum. Gray copies not counted.
- Contested, stated on the page: tracheal epithelium (Gray "stratified", modern pseudostratified); sublingual gland
  mucous or seromucous; four or five epidermal layers; serous demilunes partly a fixation artefact; apocrine
  mechanism; liver sinusoids sinusoidal or fenestrated.
- Single source, attributed: stereocilia, cement line, Volkmann's canals, medullary cords, spiral sweat duct, one-way
  synapse, nucleolus (Gray); spleen zones and cords, connexons, capillary sites, eccrine merocrine (Wikipedia);
  Langerhans cells to nodes (PMC13246397).
- Left out (one source or none): woven vs lamellar bone (only source OpenStax-derived), satellite-cell ring
  difference, thymus without follicles, tonsil without afferent lymphatics, lamina lucida and densa, microvillus size.
- Micrographs (Wikimedia Commons; licences read from the Commons API 2026-11-22; all resized and labelled, labels
  approximate): Berkshire Community College Bioscience Image Library, CC0 (simple cuboidal, simple columnar,
  pseudostratified, stratified squamous, transitional epithelium; motor neuron; nerve bundles; compact bone);
  Wbensmith, "WVSOM Parotid Gland1.JPG", CC BY 3.0; CoRus13, oesophageal submucosal glands, CC BY-SA 4.0 (cropped);
  Heihaheihaha, "Serous demilunes of submandibular gland section.png", CC BY-SA 4.0; M-J-G, "Spinalganglion.jpg",
  CC BY-SA 4.0 (cropped); Lord of Konrad, "Artery.png", CC0; Ed Uthman, "Normal Lymph Node.jpg", CC BY-SA 2.0; Alexander
  Klepnev, spleen and thymus, CC BY 4.0 (cropped); Nephron, "Thymic corpuscle.jpg", CC BY-SA 3.0 (cropped); Bhavya
  akula, "Histology of thick skin.jpg", CC BY-SA 4.0 (cropped); Mikael Häggström, skin collagen, CC0 (cropped);
  SGnanadeep, "Thin skin histology.jpg", CC BY-SA 4.0 (cropped). Elastic artery and vein micrographs could not be
  downloaded (Commons rate limit): drawings instead.
- Independent review (2026-11-22), fixed: seven micrograph labels on the neighbouring structure (internal elastic
  lamina, media, sebaceous gland, epidermis, lymph-node capsule, cilia, goblet cell, demilune, glial nuclei,
  lamellae), schematic layers (demilune inside the basement membrane, paracortex, septa, basal layer), one-source
  statements, dark bone figure, phone label size, keyboard access.

## General Embryology — `embryology/early-development.html`, `embryology/membranes-placenta.html`

- Fact sheet `sources-local/facts/fill-embryo1.md` (753 quotes, script-checked against `sources-local/modern/fill-embryo1/`,
  downloads 2026-11-22): Gray 1918 (embryology chapter and pages 255, 266, 268); StatPearls; about 45 open-access papers
  (Europe PMC); Wikipedia. Excluded: Wikipedia "Human embryonic development" and "Neural tube" (OpenStax/Betts) and
  sentences shared with them; Wikipedia sentences copying Gray; Gray's chromosome number of 24.
- Contested, stated on the page (as tables): implantation day, day the uterus is reached, neuropore closure days, twin
  split days and chorionicity, CVS weeks, amniocentesis and CVS loss rates, viability (22–24 vs the traditional 28),
  trimester cut-off, ectopic and ampullary shares, oocyte counts, spermatogenesis duration, cycle length, placenta
  and cord sizes, somite number, origin of extra-embryonic mesoderm and of sacrococcygeal teratoma, decidual reaction
  timing, teratogenic period, polyspermy outcome.
- Single source, attributed: hatching day, LH surge to ovulation, TTTS share, thalidomide windows, endoderm to the
  middle ear (Gray), surrogacy law 2021 (Cureus 2023), lambda and T signs (StatPearls), Gray's fetal-age table.
- Left out (one source): somite formation rate, cotyledon number, battledore definition, the sex-selection law
  (PCPNDT), morula cell range.
- Schematics only; hormone curves are schematic shapes. Germ-layer colour tokens (--ecto, --meso, --endo, --epi,
  --hypo, --tropho, --endom, --noto, --crest, --jelly) are for reuse on later embryology pages.
- Independent review (2026-11-22), fixed: yolk sac drawn inside the amnion and the sac crossing the uterine wall, the
  amniocentesis needle through the placenta and the CVS catheter in the wall, germ-layer colours too close to artery,
  nerve and vein colours, life-chart bars misaligned, uterus without a lumen, dates and attributions, drawing slips,
  accessibility of the flow button and steppers.

## Histology II: Respiratory and Digestive Organs; Urinary and Reproductive Organs; Endocrine Glands, Senses and CNS — `histology/respiratory-digestive.html`, `histology/urinary-reproductive.html`, `histology/endocrine-senses-cns.html`

- Fact sheet `sources-local/facts/fill-histo2.md` (528 quotes, script-checked against `sources-local/modern/fill-histo2/`,
  built from `fill-histo2-scripts/spec-*.md` with `assemble.sh`, downloads 2026-11-22): Gray 1918 pages 3, 12, 185, 187,
  189, 197, 223, 225, 227, 232, 236, 237, 240, 242, 245, 247–251, 253–255, 258, 259, 262, 263, 266–268, 272, 273, 275–277;
  StatPearls (24 chapters); open papers PMC10024030, PMC11188711, PMC12481553, PMC12721976, PMC12776365, PMC13093675,
  PMC13297954, PMC13400080, PMC13745872, PMC4736353, PMC4908136, PMC59567, PMC6895843, PMC7384063, PMC7496161,
  PMC7764992, PMC7961977, PMC8071372, PMC8948418; Wikipedia, including the hormone table of "Anterior pituitary"
  (rebuilt from the wikitext). Excluded for OpenStax notices: Wikipedia Lung, Stomach, Gastric glands, Ovary, Uterus,
  Adrenal gland. Wikipedia sentences copying Gray (villus circulation) counted as Gray only.
- Contested, stated on the page: tracheal epithelium (Gray "stratified"); both convoluted tubules alike (Gray) vs a brush
  border on the proximal tubule; ureter muscle order (Gray external longitudinal first) and the extra outer layer in
  the lower part; vas deferens three muscle layers (Wikipedia) vs two for most of its length (Gray); epididymis
  "ciliated" (Gray) vs stereocilia; posterior pituitary "no nerve fibers" (Gray) vs hypothalamic axons; cornea four
  (Gray) vs five layers; cerebral cortex four cell layers (Gray) vs six; vallate papillae 8–12 (Gray) vs 10–14;
  outer hair-cell rows; what chromophobes are (degranulated hormone cells vs hormone-negative stem cells).
- Single source, attributed: pyloric mucous and G cells, scattered parietal cells, Z-line, Brunner's glands' alkaline
  mucus, Rokitansky–Aschoff sinuses, no muscularis mucosae in the gall bladder, macula densa, squamocolumnar junction,
  Herring bodies, C cells larger, paler and inside the basement membrane (Wikipedia); pale islets, labial glands,
  complete longitudinal muscle of the appendix, colloid eosin-stained, substantia gelatinosa (Gray); corpus luteum
  stops within 14 days (StatPearls); layer II and IV cell types (Wikipedia; PMC8948418).
- Left out (one source or none): "densest" cortical layer, cardiac glands mucous (only OpenStax-flagged source), the
  widest adrenal zone, unmyelinated posterior-pituitary axons, the kind of labial glands, a separate statement that the
  gall bladder has no submucosa (neither source states it; the page says neither lists one).
- Micrographs (Wikimedia Commons; licences read from the Commons API 2026-11-22; all resized to 720 px and labelled,
  labels approximate and each checked on the image): Jpogi, public domain (lung, gastro-oesophageal junction, fundus
  and parietal cells — both cropped to remove the uploader's pointer, pylorus, duodenum, liver sinusoid, kidney cortex
  — cropped likewise, kidney medulla, ureter, testis, epididymis, vas deferens, ovarian follicle, corpus albicans,
  endometrium, uterine tube, placenta, adrenal gland; the other uploader pointers are explained in the captions);
  Abdulrazakca, "Oesophagus09.jpg", public domain (cropped); Urkiurmo, "Trakearen ebaketa histologikoa.png",
  CC BY-SA 4.0; CoRus13, "Colon, low mag.jpg", CC BY-SA 4.0 (cropped); Andrjusgeo, "KirmėlinėAtauga.JPG" (appendix),
  CC BY-SA 3.0 (cropped); Netha Hussain, jejunum, gall bladder (contrast raised), umbilical cord (cropped), thyroid
  and parathyroid (cropped, contrast raised), CC BY-SA 3.0; Polarlys, islet of Langerhans and bladder urothelium,
  CC BY 2.5; Ed Uthman, "Renal corpuscle.jpg", CC BY-SA 2.0, and the cervix squamocolumnar junction, CC BY 2.0;
  Mikael Häggström, normal prostate and anterior pituitary, CC0; Nephron, "Corpora amylacea intermed mag.jpg",
  CC BY-SA 3.0; Berkshire Community College Bioscience Image Library, thyroid, cerebellum and Purkinje cells, CC0;
  Iceclanl, olfactory epithelium, CC BY-SA 3.0 (cropped); Librepath, "Optic nerve -- low mag.jpg", CC BY-SA 3.0.
  No usable open micrograph (drawings only): bronchus, lip, tongue (vallate papilla), epiglottis, ileum (Peyer's
  patch), penis, normal corpus luteum, posterior pituitary, pineal, eyelid, limbus, cornea, retina, cochlea, organ of
  Corti, whole spinal cord, cerebral cortex, Leydig cells, separate adrenal zones, portal triad.
- Independent review (2026-11-22), fixed: pituitary cell types misread from one source (now three sources, and the
  chromophobe disagreement shown); umbilical-cord image height; six micrograph labels on the neighbouring layer; lung
  airway labelled respiratory bronchiole / alveolar duct; blurred appendix image replaced; colour clashes (grey and
  white matter now the neuro pages' tokens, receptor cells and macrophages given their own colours, capillary walls
  drawn as endothelium, not artery, one colour for eosin-stained cells, unmyelinated retinal fibres not drawn as
  myelin); thyroid C cells inside the basement membrane; one-source statements attributed; uploader pointers
  explained or cropped; page code (missing micrographs, observers released, drawing labels for screen readers).

## Systemic Embryology — `embryology/heart-vessels.html`, `embryology/gut-urogenital.html`, `embryology/head-neck-cns.html`

- Fact sheet `sources-local/facts/fill-embryo2.md` (777 quotes, script-checked against `sources-local/modern/fill-embryo2/`,
  downloads 2026-11-22): Gray 1918 (13–15, 135, 139, 142, 184–189, 224, 235, 241, 250–252, 255, 258, 266, 272, 275);
  StatPearls abstracts; about 30 open-access papers (Europe PMC / NCBI BioC), among them PMC12372156 (interatrial
  septum), PMC11241401, PMC10328954, PMC9592245, PMC9556351, PMC7557825 (arch arteries), PMC6893009, PMC10788309,
  PMC12693601 (great veins), PMC11658130, PMC10011220 (VSD), PMC13514265 (left SVC), PMC12499430 (TEF), PMC11195428
  (lung), PMC2908440, PMC4546136, PMC6014125 (midgut), PMC12840228 (gastroschisis), PMC7155797, PMC11593116,
  PMC6084689, PMC12599990 (urogenital), PMC10521768, PMC13200892, PMC12519008, PMC13603011, PMC5618146, PMC12538268
  (head and neck); Wikipedia.
- Excluded: Wikipedia "Heart development", "Tubular heart", "Lung", "Diencephalon", "Myelencephalon" and "Ventricular
  system" (they cite OpenStax/Betts); Wikipedia sentences that copy Gray (wpcopy2 list in the sheet); PMC13332512
  (survey, no facts) and PMC6440433 (built on a licensed textbook). The slips in PMC10521768 (superior constrictor under
  arch 3, cricothyroid under arch 6) are not used.
- Contested, shown on the page: the segment of the adult arch formed by the left 4th arch (Gray vs StatPearls); IVC
  infrarenal segment (supracardinal, modern sources, vs Gray's cardinal vein); ductus closure (12–24 h / 2–3 weeks vs
  Gray's 4–10 days); commonest VSD type (perimembranous vs newer data for muscular, Wikipedia); ASD secundum share
  (70% vs 75%); lung stage weeks; midgut return (weeks 9–12) and the 270° rotation as a descriptive model; kidney ascent
  timing; palatal fusion starting at the front (Gray) or the centre (2026 review); posterior tongue from the copula
  (Gray) or the hypopharyngeal eminence; ultimobranchial body in the 4th pouch (Gray: 5th); hyaloid artery regression
  (week 10, Wikipedia, vs the ninth month, Gray); which part of the pancreas each bud forms.
- Single source, attributed: bulbus → RV infundibulum and primitive ventricle → LV (Gray); ostium primum share (review);
  TGA aorta in front and to the right, Fallot right arch 20–25%, truncus single valve, gastroschisis 10% anomalies and
  AFP, horseshoe malrotation, Dandy–Walker hydrocephalus, craniopharyngioma extent, bilious vomiting in volvulus
  (StatPearls); AVSD with Down syndrome, pancreas divisum, spleen from mesoderm, superior vesical arteries, SRY on the
  short arm, hypospadias rates, epispadias in every exstrophy, genital tubercle at week 4, metanephric blastema →
  nephrons, branchial cyst details, alar plate → sensory nuclei, lingual thyroid symptoms, hyoid removal, rachischisis,
  coloboma field defect, cleft feeding and voice (Wikipedia); olive, colliculi, flocculus first, mantle/marginal layers
  (Gray); TEF types A and D and the H-type share, reversed rotation, corniculate from arch 6 (reviews).
- Left out (no second source): tongue muscles from occipital somites, the pectinate line as the junction, arterial
  shifts during kidney ascent, rubella cataract, the "machinery" murmur, left vagus turning anterior, lobe-branching
  weeks, day numbers for looping.
- Schematics only. Germ-layer tokens as on the module 39 pages; organ tokens reused with their meanings (--gut, --colon,
  --stom, --liver, --panc, --bile, --kidney, --duct, --uter, --vag, --gonad, --thyroid, --parathy, --pit, --lens,
  --retina, --medulla, --pons, --midb, --cblm, --dien, --s-csf, --pleura, --airway). New: --telen (telencephalon and
  cerebral hemispheres) #f606a6 / dark #ff5cc8, checked with fill-histo2-scripts/colcheck3.py. Pharyngeal arches,
  facial prominences and external genital primordia are told apart by hatch patterns, not colours.
- Independent review (2026-11-22), fixed: the IVC drawn into the right ventricle in the fetal circulation (now enters
  the floor of the right atrium); the arch-artery adult step (right dorsal aorta, 7th intersegmentals moved above
  arch 6 so the coarctation lies beyond the left subclavian, truncus and descending aorta separated, aberrant right
  subclavian overlay); patent ductus drawn on the newborn state; pulmonary trunk drawn as an artery; shunt arrows per
  defect (right to left in Fallot); brain flexures (the pontine flexure bends the opposite way) and the order of the
  vesicles; malrotation and reversed rotation drawn; annular pancreas round the 2nd part; IMA in front of the kidneys;
  optic cup layers swapped; mandibular prominence hatch; --telen too close to --parathy; unquoted and one-source
  statements quoted, attributed or cut; overlapping and clipped labels; small figures fit phone width.

## Genetics — `genetics/chromosomes-karyotype.html`, `genetics/inheritance-pedigrees.html`, `genetics/aberrations-clinical.html`

- Fact sheet `sources-local/facts/fill-genetics.md` (712 quotes, script-checked against `sources-local/modern/fill-genetics/`,
  downloads 2026-11-22): StatPearls (25 abstracts); GeneReviews abstracts (achondroplasia, X-linked hypophosphataemia);
  MedlinePlus Genetics (public-domain summaries; "Courtesy of MedlinePlus from the National Library of Medicine");
  open-access papers PMC8022097, PMC1084335, PMC8198510, PMC3983585, PMC5023040, PMC4215412, PMC12941462, PMC12801557,
  PMC13258534, PMC12176624, PMC13484737, PMC3991414, PMC3769083, PMC7658086, PMC10084876, PMC12898306, PMC12712970,
  PMC13341453, PMC3781639, PMC12050259, PMC12469938, PMC13745948, PMC13178452, PMC2853554, PMC6060985, PMC4629947,
  PMC13538617, PMC13072683, PMC13627043, PMC13419904, PMC13740504; Wikipedia (Centromere tables rebuilt from wikitext).
  Gray 1918 not used.
- Not independent (10-word shingle check): Wikipedia "Chromosome 21", "Uniparental disomy", "Leber hereditary optic
  neuropathy", "Mutation", "Myotonic dystrophy", "Patau syndrome", "XYY syndrome" and part of "CFTR" copy MedlinePlus;
  "Achondroplasia" copies the GeneReviews abstract; the Wikipedia Denver-group table copies an IOP paper. None is counted
  as a second source. No quoted article cites OpenStax ("Betts" in "Achondroplasia" is James Betts, a consensus co-author).
- Contested, shown on the page: X and Y in groups C and G vs a separate "group H"; Down syndrome types (about 94% free
  trisomy, 4% vs 5.6% translocation, 1–2% mosaic) and two maternal-age series plotted separately; Edwards 5% mosaic vs
  5% translocation; Klinefelter frequency and mosaic share; F508del share; alkaline phosphatase in XLH; heart disease in
  Down syndrome (about 40% vs about half); horseshoe kidney in Turner syndrome (10% vs 14–20%).
- Single source, attributed on the page: pedigree carrier and numbering conventions; chromosome sizes for the to-scale
  drawing; the Barr-body "X minus one" rule and 47,XXX; knight's move; repeat ranges; the threshold model; cleft lip and
  NTD recurrence; paternal expansion in Huntington disease and congenital myotonic dystrophy from the mother; the 1%
  polymorphism cut-off; sickle Glu6Val; PCR temperatures; ddNTP chemistry; non-directive counselling; father-carrier
  risk under 5%; rocker-bottom feet, cutis aplasia, cubitus valgus; meiosis II errors being rarer; AVSD and duodenal
  atresia in Down syndrome (linked to the embryology pages).
- Left out (no second source): ambiguous genitalia as a karyotype indication; the Carter effect and pyloric stenosis;
  sweat-test cut-offs; transplant and micro-chimerism; the fate of the 45 line after a mitotic error; "does not respond
  to vitamin D".
- Images (Wikimedia Commons, licences read 2026-11-22): NHGRI karyogram, public domain (resized, group labels added);
  Reischig metaphase spread, CC BY-SA 3.0 (cropped, resized, 2 labels); Dietzel Barr body / X-territory painting,
  CC BY-SA 3.0 (recompressed); DOE trisomy 21 karyotype, public domain (converted to JPEG); Serra Amoros trisomy 18,
  CC BY-SA 4.0 (recompressed); Saideekshit et al. 46,X,i(Xq) from a mosaic Turner case, CC BY 4.0 (recompressed).
  "47,XXY.jpg" and "45,X.jpg" not used (no author); Trisomy13.jpg not obtained. No patient photographs.
- New colour tokens: `--mat` (maternal), `--pat` (paternal), `--mut` (variant or moved segment), `--probe` (FISH signal),
  checked with colcheck3 against atlas.css and every page.
- Independent review 2026-11-22, fixed: Punnett titles upper-casing genotypes; missing CFTR 7q31.2 and splice-site
  variants; Wikipedia copies counted as second sources; over-claims and mis-credits; colour meanings (`--mat`, `--pat`,
  `--mut`, `--clin`) and dark-theme contrast; mitotic non-disjunction, frameshift and ΔF508 drawings; pedigree layout and
  the consanguinity line; label collisions; XLH flow arrows; image credits; phone layouts.

## General Anatomy: Terms, Bone, Skin and Lymphatics — `general/terminology-bone.html`, `general/skin-lymphatics.html`, additions to `general/blood-vessels.html`

- Fact sheet `sources-local/facts/fill-general2.md` (309 quotes, script-checked against `sources-local/modern/fill-general2/`,
  downloads 2026-11-22): Gray 1918 (pages 1, 17, 18, 50, 59, 60, 62, 71, 85, 95, 96, 133, 141, 165, 175, 176, 234);
  StatPearls abstracts; open-access papers PMC4917311, PMC11759331, PMC11083575, PMC12097171, PMC12714326, PMC2107348,
  PMC9892216, PMC12631335, PMC12411914, PMC9767978, PMC11763355, PMC12827920, PMC13577710, PMC7375305; Wikipedia.
- Excluded: Wikipedia "Anatomical terms of motion", "Lymph capillary" and "Circulatory system" (OpenStax). Not counted
  where they copy Gray 1918 (6- and 7-word checks): Coracoid process, Flat bone, Greater trochanter, Irregular bone,
  Nutrient artery (its lead copies Gray, so the nutrient artery's branching is Gray only), Nutrient canal, Right
  lymphatic duct, Sesamoid bone, Supraclavicular nodes. Wikipedia "Dermatome" and PMC12097171 share the
  international-standard key-point wording; Wikipedia "Pseudoaneurysm" shares the clot-wall phrase with StatPearls.
- Contested, shown on the page: bone classes (four, Gray, vs five, StatPearls); adult red-marrow sites; Langer's lines
  (cut along them, Wikipedia, vs a 2025 review calling them cadaver artefacts and favouring relaxed skin tension lines);
  lymphatics in the CNS (Gray vs StatPearls); the lungs in the right-duct territory; lymphatics "open" vs a "closed
  system"; who proposed Virchow's triad; the wall of a false aneurysm (two StatPearls chapters); cisterna chyli level
  (StatPearls chapters differ); the right lymphatic duct's ending is variable.
- Single source, attributed on the page: Gray only — the epiphysis that appears first unites last (fibula exception),
  branching of the nutrient artery, one-epiphysis bones, nail parts, bone-type features, lymph valves closer than in
  veins; Wikipedia only — ipsilateral/contralateral, the aberrant epiphysis and epiphysis examples, epiphyseal arteries,
  upper tibial centre, the 20/17/3 litre and 25/8 mm Hg figures, hypoxic vasoconstriction, white vs red infarcts,
  saccular aneurysm, dissecting aneurysm; StatPearls only — the ≥150% aneurysm definition, elephantiasis sites. The
  "to the elbow I go, from the knee I flee" mnemonic is shown only as a memory aid.
- Left out (no second source): pneumatic bones, sesamoid "no periosteum" features, traction epiphyses ossifying later,
  pitting vs non-pitting lymphoedema, a general "carcinoma spreads by lymph" rule, metaphyseal arteries, the fabella.
  AN3.3 (shunt and spurt muscles) is not covered: the only sources are 1959–1979 J Anat papers available as scans only,
  and one 2024 paper (PMC11395053) uses the terms the other way round.
- No images; every figure is a data-drawn schematic (Commons dermatome maps were Gray's or OpenStax).
- New colour tokens: `--redmarrow` #730d14 / #cf1723 and `--clot` #541244 / #bd2898, one hue in both themes, at least
  ΔE 24 from every atlas token (including `--n-*`); infarcts are hatched, not coloured.
- Independent review 2026-11-22, fixed: aneurysm wall layers drawn in the wrong order; ipsilateral/contralateral sides
  swapped; the nutrient-artery Wikipedia copy counted as a second source; the S1 dermatome band; colour hues and clashes;
  lymph-territory encoding aligned with the thorax page; attribution slips; label clipping.

## Bony Pelvis; Imaging the Abdomen; Surface Marking and Sections — `abdomen-pelvis/bony-pelvis.html`, `abdomen-pelvis/imaging-abdomen.html`, `abdomen-pelvis/surface-sections.html`

- Fact sheet `sources-local/facts/fill-abdo2.md` (511 quotes, script-checked against `sources-local/modern/fill-abdo2/`,
  downloads 2026-11-22): Gray 1918; StatPearls; Wikipedia; open-access papers on pelvimetry and pelvic types, subpubic
  angle, sciatic notch, inlet shape, sex estimation, lumbosacral transitional vertebrae, the abdominal radiograph,
  pneumoperitoneum, volvulus, barium studies, HSG, MRCP vs ERCP, CT vs IVU, ultrasound, PET, MRI basics (2021),
  Hounsfield values (2024, 2026), renal angle, McBurney terminology, pancreas (2024).
- Excluded: Wikipedia "Pelvis" (cites OpenStax); Wikipedia sentences copying Gray (Coccyx, Thoracic diaphragm, Aortic
  hiatus, Pelvic brim, Pelvic inlet, Pelvic outlet); "Transpyloric plane" not counted for the halfway definition (Gray
  template); Wikipedia's pelvic-type text copies the StatPearls Pelvic Inlet chapter.
- Contested, shown on the page: subpubic angle in four studies; sacral curvature; pelvic diameters and outlet cut-offs;
  "true" conjugate (Gray's anteroposterior diameter vs the obstetric "true" conjugate); pelvic-type frequencies;
  McBurney's point (one-third vs halfway); deep ring position; SMA origin; caval opening (T8 vs T8/9 disc); HSG day;
  air-fluid levels (erect only vs supine and erect); Hounsfield ranges for fat and bone.
- Single source, attributed: Gray's surface outlines (liver, Morris's parallelogram, ureter, spleen axis) and the
  transpyloric halfway definition; DSA mask, cathode and anode (StatPearls); 1 mL of free gas (one review); metal as
  densest (Wikipedia); Murphy's-sign manoeuvre; coccydynia figures; Castellvi classes (2026 review).
- Left out (no second source): hip-bone muscle list, sentinel loop, "3-6-9" as a name, control film, thoracic duct in
  the hiatus, embolisation, pelvic tumours on MRI.
- Sections are cut from the lung and abdo models (z 1203 T8/9, 1159 T10, 1075 L1 mm) with `fill-abdo2-scripts/slice.py`;
  pelvis landmarks from points.py; both approximate and labelled so. Label points are checked to lie on their part.
- Images (Wikimedia Commons, licences read 2026-11-22; resized, labelled): Heilman small-bowel obstruction CC BY-SA 3.0;
  Hellerhoff Rigler sign CC BY-SA 3.0 (cropped); small-bowel follow-through public domain (R marker kept); Jmarchn HSG
  CC BY-SA 3.0; Guntau ERCP CC BY-SA 3.0; Ptrump16 MRCP CC BY-SA 4.0; UCSD pelvis AP public domain. Barium swallow,
  double-contrast enema, IVU and CT images not obtained (Commons rate limits): drawings instead.
- New colour tokens on bony-pelvis.html: `--inlet`, `--outlet` (outlet and midpelvis), `--sx-f`, `--sx-m` (one hue in
  both themes; sex labels drawn in ink).
- Independent review 2026-11-22, fixed: T10 cut through T11 (no oesophagus); section labels on the wrong organs;
  "true" conjugate naming; pubic-arch drawing; 3D zoom on phone and clip notes; about ten unsourced or misattributed
  claims; T1/T2, Hounsfield and density order added; colour rules and contrast; Rigler and fluid drawing; label clashes;
  image crop. lower-limb/bones.html: the subpubic-angle line no longer rests on the OpenStax-citing "Pelvis" article.

## Limb leftovers: Breast; Landmarks and Radiographs; Development of the Limbs; scaphoid, hand spaces, osteoarthritis — `upper-limb/breast.html`, `upper-limb/radiographs-landmarks.html`, `lower-limb/radiographs-landmarks.html`, `embryology/limb-development.html`, additions to `upper-limb/bones.html`, `upper-limb/muscles.html`, `lower-limb/joints.html`

- Fact sheet `sources-local/facts/fill-limbs3.md` (421 quotes, script-checked against `sources-local/modern/fill-limbs3/`,
  downloads 2026-11-22). Sources by topic:
  - Scaphoid: StatPearls (Scaphoid Wrist Fracture, Snuff Box); PMC7672797; PMC12404867 (2025 MRI study questioning the
    retrograde-supply explanation); Wikipedia.
  - Breast: Gray 1918 (148, 149, 181, 271, 283); StatPearls (Breast, Mammary Gland, Breast Lymphatics, Axillary Lymph
    Nodes, Poland syndrome); PMC11909697 (axillary levels), PMC12647528 (breast fascia), accessory and ectopic breast,
    amastia and Poland reports; Wikipedia.
  - Sheaths, spaces, extensor expansion: Gray 125, 126, 290; StatPearls (pyogenic flexor tenosynovitis, felon, ulnar
    bursa, lumbricals, mallet, boutonnière, swan-neck); Flevas 2019; Malizos group 2012/2020 (counted as one source);
    2024–2026 hand papers; Wikipedia.
  - Osteoarthritis: StatPearls ×3; PMC13322087, PMC13150102, PMC13150380; Wikipedia (Osteophyte, Heberden's and
    Bouchard's nodes, Hyaline cartilage).
  - Landmarks and radiographs: Gray 26, 282, 284, 289–292; Wikipedia; PMC6806572, PMC5063483, PMC4916809, PMC6635173,
    PMC6283718; acromial-angle studies PMC13179215, PMC11191861; elbow reviews PMC12818852, PMC13217208, PMC13287200,
    PMC5782864; StatPearls (Bone Age, Elbow Fractures).
  - Limb development: Gray 13, 15, 51, 53, 59; StatPearls (Embryology Hand, Bone Ossification); PMC13349005,
    PMC13139040 (C5–T1), PMC10153723; PMC8428198 (thalidomide, 2021, also on early-development.html); Wikipedia.
- Excluded: Wikipedia "Osteoarthritis" and "Tendon sheath" (OpenStax). Counted as Gray only where Wikipedia copies
  Gray: Ulnar bursa, Spine of scapula, Posterior superior iliac spine, Malleolus, Fibula, Calcaneus, Fifth metatarsal,
  Acromion, the interossei articles, and the Breast sentence on nerves.
- Contested, shown on the page: sternal angle T4–5 (Wikipedia) vs T5 (Gray); CRITOE ages (three schemes, with the
  StatPearls sex exception); limb-bud timing (3rd vs 5th week); lactiferous duct count; share of breast lymph not going
  to the axilla; meaning of "acromial angle"; iliac tubercle at the L5 body or spine; intercristal line at L4 spine,
  body or L4–5; Kanavel 3 vs 4 signs; ossification of the shafts (6th–7th vs 7th–8th week).
- Single source, attributed: scaphoid waist and necrosis percentages and the 7–10-day repeat film; breast veins,
  nerves and thoracoacromial branches (Gray); involution; Poland syndrome ratios; ectopic breast diseases; Parona 80%;
  collar-button abscess; felon necrosis; space walls (Flevas); swan-neck causes and mallet-to-swan-neck; thenar drainage;
  Heberden's and Bouchard's nodes; standing films (Lin et al.); upper limb bud first and FGF10 (Wikipedia); Gray's 1918
  segment counts (C4–T2, T12–S4) shown beside modern C5–T1.
- Left out (no second source): level of the nipple, accessory-nipple prevalence, diaphysis sparing in felon, Klein's
  line, ankle joint-line level, a day-26–28 limb-bud date, radial vs ulnar styloid height.
- Model checks (3D skeleton, landmark points placed by hand, levels computed on the model): jugular notch T3, sternal
  angle T4–T5 disc, spine of scapula T3, inferior angle T7, iliac crest top L4; the hand-placed iliac tubercle point lies
  level with L4 on this model (said on the page); PSIS shown as a line only.
- Images (Wikimedia Commons, licences read 2026-11-22; resized, labels added and checked): Mikael Häggström, CC0 —
  shoulder (cropped), elbow AP (side marker cropped), elbow lateral, wrist PA, ankle AP and lateral, knee lateral (marker
  cropped); James Heilman, CC BY-SA 3.0 — osteoarthritic knee (cropped, contrast, author's arrow kept). Not obtained
  (Commons HTTP 429 on two days): knee AP, foot, child knee and hand, scaphoid fracture. Breast and hand are schematics.
- Colours: the breast's glandular tissue uses the existing `--gland`; no new tokens.
- Independent review 2026-11-22, fixed: limb rotation redrawn as cross-sections; child elbow side; ankle and wrist
  labels; pectoralis minor orientation and depth; OA alt text; 3D level notes and disc naming; web-space, dorsal
  ectoderm and ossification drawings; about 20 unsourced or single-source sentences; colour meanings (`--clin`, `--musc`,
  `--mamm`); label clipping and faint 3D labels.

- 2026-11-25 correction (skull.html): Wikipedia "Fontanelle" cites a Boundless text and is excluded; its closure
  figures (posterior 6–8 weeks, sphenoidal ~6 months, mastoid 6–18 months, anterior palpable to 18 months) were removed.
  Fontanelle closure now rests on Gray 1918 and StatPearls.
