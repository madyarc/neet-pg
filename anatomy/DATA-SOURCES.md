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
