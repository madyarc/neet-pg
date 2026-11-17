# NEET-PG

**🌐 Website: [madyarc.github.io/neet-pg](https://madyarc.github.io/neet-pg/)**

Revision for NEET-PG you can see and handle, organised by the official MBBS curriculum. Plain static HTML, no build
step. Sister project of [jee-materials](https://github.com/madyarc/jee-materials).

## Modules

### Anatomy — [`anatomy/`](anatomy/index.html)

| # | Module | Branch | What it does |
|---|---|---|---|
| — | [Anatomy home](anatomy/index.html) | Whole body | The whole skeleton in 3D; system filters; tap a bone to open its page |
| 01 | [The Skull](anatomy/head-neck/skull.html) | Head and neck | 22 bones assembled and colour-coded; sutures and meeting points (bregma, lambda, pterion, asterion, nasion); inside the cranial cavity: the three fossae; foramina of the cranial floor and what passes through them |
| 02 | [Bones of the Skull](anatomy/head-neck/skull-bones.html) | Head and neck | Each skull bone and the hyoid alone at near-full detail: parts, 110 landmarks and foramina, the bones it joins (contact areas from the model), ossification |
| 03 | [The Vertebral Column](anatomy/back/vertebral-column.html) | Back | 24 vertebrae, sacrum, coccyx and 23 discs assembled; regions; the four curves; discs |
| 04 | [The Vertebrae](anatomy/back/vertebrae.html) | Back | Atlas, axis, typical cervical, C7, thoracic, lumbar, sacrum and coccyx in detail: landmarks, how to recognise each, ossification |
| 05 | [The Thoracic Cage](anatomy/thorax/thoracic-cage.html) | Thorax | Ribs (true, false, floating), costal cartilages, sternum, thoracic vertebrae assembled; joints; openings |
| 06 | [Ribs and Sternum](anatomy/thorax/ribs.html) | Thorax | Typical, first, second and twelfth ribs and the sternum in detail |
| 07 | [The Upper Limb](anatomy/upper-limb/upper-limb.html) | Upper limb | Shoulder girdle, humerus, radius and ulna, hand assembled; nerves on the humerus; carpal tunnel |
| 08 | [Bones of the Upper Limb](anatomy/upper-limb/bones.html) | Upper limb | Clavicle, scapula, humerus, ulna, radius and hand bones in detail |
| 09 | [The Lower Limb](anatomy/lower-limb/lower-limb.html) | Lower limb | Hip bone, femur and patella, tibia and fibula, foot assembled; the joints between them; arches of the foot |
| 10 | [Bones of the Lower Limb](anatomy/lower-limb/bones.html) | Lower limb | Hip bone (with the pelvis), femur, patella, tibia, fibula and foot bones in detail: 88 landmarks, how to recognise each, ossification |
| 11 | [The Femur: attachments and side](anatomy/lower-limb/femur.html) | Lower limb | 3D bone: 18 landmarks; left or right; 30 muscle and ligament attachments; neck fracture and blood supply; five ossification centres |
| 12 | [Muscle Tissue](anatomy/general/muscle.html) | General / histology | Skeletal vs cardiac vs smooth; a sarcomere you can contract (I band and H zone shorten); triads vs dyads; fibre architecture; tendon vs aponeurosis; endo-, peri-, epimysium; fibre types |
| 13 | [Connective Tissue](anatomy/general/connective-tissue.html) | General / histology | Cells and fibres; loose, dense, elastic, reticular, adipose tissue; collagen types and 67 nm banding; hyaline, elastic, fibrocartilage; tendon, aponeurosis, ligament; superficial and deep fascia |
| 14 | [Muscles of the Upper Limb](anatomy/upper-limb/muscles.html) | Upper limb | 49 muscles in 3D on the bones (Z-Anatomy meshes): origin and insertion areas on the bone, nerve, action, clinical notes; colour by nerve supply; retinacula, carpal tunnel, extensor compartments, thumb movements |

### Ophthalmology — [`ophthalmology/`](ophthalmology/index.html)

| # | Module | Branch | What it does |
|---|---|---|---|
| 01 | [The Visual Pathway and Field Defects](ophthalmology/neuro-ophthalmology/visual-pathway.html) | Neuro-ophthalmology | 11 lesion sites from optic nerve to visual cortex, either side; fibres coloured by the half of the view they carry; both eyes' fields with the loss shaded (junctional scotoma, bitemporal, early pituitary/craniopharyngioma patterns, quadrantanopias, macular sparing) |
| 02 | [Pupil Reflexes](ophthalmology/neuro-ophthalmology/pupil-reflexes.html) | Neuro-ophthalmology | Light-reflex pathway (afferent and efferent limbs coloured); light in either eye, swinging light, near object; normal, optic nerve lesion, RAPD, oculomotor palsy, Argyll Robertson, Adie; comparison table |
| 03 | [Refractive Errors](ophthalmology/refraction/refractive-errors.html) | Refraction | Ray diagram in a schematic eye: myopia, hypermetropia (latent part shown with cycloplegia), astigmatism (types named live), presbyopia by age; correcting lens, pinhole, a letter blurred to match; accommodation, amblyopia, refractive surgery |

## Syllabus

[`SYLLABUS.md`](SYLLABUS.md) indexes all 19 subjects; each `<subject>/SYLLABUS.md` lists every NMC CBME 2024 topic and
competency with its code (401 topics, 2626 competencies), ticked as modules cover them.

## Layout

```
index.html                  hub: links to each subject
SYLLABUS.md                 index of the NMC topic lists
<subject>/SYLLABUS.md       per-subject checklist
anatomy/                    index.html, DATA-SOURCES.md, lower-limb/femur.html
tools/syllabus/             generates the SYLLABUS files from the NMC PDF
anatomy/assets/             shared 3D viewer (viewer.js) and styles (atlas.css)
anatomy/models/             simplified BodyParts3D meshes (skeleton overview; skull, spine, thorax, upper-limb, lower-limb, each with a -detail set + landmarks)
tools/bones-rs/             Rust mesh pipeline: BodyParts3D OBJ -> simplified binaries + contacts
tools/bones/                Python helpers: femur build, skull sutures/points, bone colours, landmarks/ (hand-placed points)
tools/test/                 headless-browser checks; bone_views.py places landmarks
tools/<region>/landmarks/   hand-placed landmark sources per region (spine, thorax, upper-limb, lower-limb)
```

## Run locally

```bash
python3 -m http.server 8000   # then open http://localhost:8000/
```

The anatomy pages load model files, which browsers block when a page is opened straight from disk.

## Credits

3D bones: BodyParts3D, © The Database Center for Life Science, licensed under CC Attribution-Share Alike 2.1 Japan.
The simplified meshes embedded in the pages are shared under the same licence.

## Adding to it

Read [`CLAUDE.md`](CLAUDE.md) first: content, verification and design rules, and the steps for adding a module.
