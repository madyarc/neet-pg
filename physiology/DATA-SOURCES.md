# Physiology — data sources and verification log

Open sources only: Gray 1918 (public domain), StatPearls abstracts (one source), MedlinePlus Genetics (public domain),
CC open-access papers via Europe PMC, Wikipedia (wikitext checked). Every fact needs two independent open sources;
where only one source has it, the page names that source.

## 01 General physiology, nerve and muscle — `general/cell-transport-fluids.html`, `nerve-muscle/membrane-potentials.html`, `nerve-muscle/nerve-nmj.html`, `nerve-muscle/muscle.html`

- Fact sheet `sources-local/facts/fill-physio1.md` (680 quotes, script-checked against `sources-local/modern/fill-physio1/`,
  downloads 2026-11-22).
- Excluded: Wikipedia articles citing OpenStax or cnx — Acid–base homeostasis, Active transport, Passive transport,
  Buffer solution, Cell (biology), Homeostasis, Hydrogen ion, Ion channel, Motor unit, Motor unit recruitment, Muscle
  tone, Neuron, Paracrine signaling, Positive feedback, Sarcomere, Skeletal muscle, Smooth muscle, Tetanic contraction,
  Troponin; as a precaution, Fluid compartments and Cytosol (they cite a CUNY OER that could not be checked);
  PMC13074981 (cites OpenStax in its references). PMC10416754 (Cureus 2023) reuses Wikipedia wording and is not counted
  as independent of it.
- 01a Cell, transport, fluids: organelles MedlinePlus, PMC10416754, Gray; signalling StatPearls, Wikipedia; gap
  junctions PMC3804956, PMC4151093. Homeostasis StatPearls, PMC5459253, PMC12989328, PMC13126257; Ferguson reflex
  PMC8578887, PMC6688382; LH surge PMC4063702 (attributed). Apoptosis PMC11592877, StatPearls, Wikipedia. Transport
  StatPearls, Wikipedia, PMC3299169 (3:2 pump), PMC9478590 and PMC3325487 (NCX). Body water PMC10255140, PMC3964340,
  PMC3183532, PMC12849772; plasma and interstitial split StatPearls (attributed); D₂O PMC12849772 and Wikipedia Body
  water. Darrow–Yannet rules PMC4178546, PMC3183532, PMC10255140 (dehydration types); the simulator is an
  ideal-osmometer calculation, marked schematic. Ions PMC3964340, PMC2945073 (plasma Na 140, K 5, Cl 100, HCO₃ 24),
  Wikipedia Na⁺/K⁺ pump, PMC3061004, PMC3325487, StatPearls. pH and buffers StatPearls, PMC11048434, PMC12653126;
  Henderson–Hasselbalch constants Wikipedia.
- 01b Membrane potentials: RMP −70/−90 mV Wikipedia (attributed; StatPearls ≈ −60 shown); K⁺ permeability
  PMC12658365 and Wikipedia; refractory periods PMC9826316 and Wikipedia (durations one review); K⁺ disorders
  PMC6892421, PMC5881435; GHK PMC6994931; strength–duration PMC13549163, PMC3401985, PMC4506053; fibre diameters
  Wikipedia and PMC7858112 (speeds Wikipedia only); myelin PMC6772175, StatPearls; block order shown as a disagreement
  (Wikipedia: B first; PMC3774755: C most susceptible; PMC4669927: smaller fibres more susceptible); pressure block
  PMC7844252; the "hypoxia blocks B first" rule has no open source and is left out.
- 01c Nerve and NMJ: neuron, Nissl, Wallerian degeneration, end plate Gray 1918 and Wikipedia; axonal transport
  PMC6696875; glia PMC3627983, PMC2799634, PMC6772175 (types are on the anatomy pages); neurotrophins PMC5372564. Injury
  PMC10484240, StatPearls, Wikipedia. NMJ PMC7744297; myasthenia gravis PMC8196750, PMC12888114; Lambert–Eaton
  PMC6524763, PMC9792103; blockers StatPearls, PMC6292224, Wikipedia.
- 01d Muscle: sliding filament and length–tension PMC5642817, PMC2234572, PMC2228549; EC coupling PMC9478590; smooth
  muscle PMC13102872, PMC4819215; fibre types PMC11212792 and Wikipedia (Henneman); energy PMC3005844; motor units
  PMC10952757; fatigue PMC5668469; myopathies StatPearls, PMC4789806, PMC8583847, Wikipedia. The twitch and tetanus
  trace, the cross-bridge drawing and the left limb of the length–tension curve are schematic.
- Contested, shown on the page: neuron RMP (−60 vs −70 mV); upper limits of plasma K⁺ and osmolality; body water 60%
  vs 65%; how much myelin speeds conduction; C and Aδ diameters; Seddon's year; Sunderland-to-Seddon mapping;
  regeneration rate; NGF co-discoverer; LEMS tumour rate; AChE anchoring; length–tension plateau; fibre block order.
- Colour tokens: ions `--na` (one hue in both themes), `--k`, `--cl`, `--ca`, `--ach`; `--gate` (Na⁺ inactivation
  gate); reused anatomy tokens keep their meaning (`--fluid`, `--collagen` for nerve sheaths, `--nerve`, `--myelin`,
  `--musc` …). Ion names in text are ink with a coloured swatch.
- Independent review 2026-11-22, fixed: cross-bridge drawing; fibre block order as a disagreement; Wikipedia reuse in
  PMC10416754; an OpenStax-citing paper; axon protein wording; Ca²⁺ arrows at the NMJ; all-or-none stimulus bar; colour
  meanings and ion-token contrast; HCO₃⁻ range; Darrow–Yannet losses; units; death-receptor position; duplication with
  the anatomy pages (now linked).

## 02 Haematology and immunity — `blood/blood-cells.html`, `blood/haemoglobin-anaemia.html`, `blood/haemostasis-blood-groups.html`, `blood/immunity.html`

- Fact sheet `sources-local/facts/fill-physio2.md` (800 quotes, script-checked against `sources-local/modern/fill-physio2/`,
  downloads 2026-11-22).
- Excluded: Wikipedia Blood plasma, Coagulation, Thrombopoiesis (cite OpenStax); PMC5767294 (its references include
  Lumen's Boundless A&P, an OpenStax remix, and its wording echoes it). Not counted as independent: PMC8490160 repeats
  Wikipedia's reticulocyte range; Wikipedia Eosinophil shares a sentence with PMC6156898; PMC8977343's MCH formula is a
  misprint and is not used.
- WHO Guideline on haemoglobin cutoffs (2024, IRIS, CC BY-NC-SA 3.0 IGO) for the anaemia cut-offs by age (filed under
  the MLP- key in the sheet); StatPearls' merged 2–11-year row is not used.
- Sources: Gray 1918 "The Blood"; StatPearls; Wikipedia; EPO PMC3191152, PMC7503180; erythropoiesis PMC3904103,
  PMC6016880, PMC5288342; haem synthesis PMC9505951, PMC9267699, PMC8705723; bilirubin PMC3678498, PMC11896460,
  PMC9486497, PMC4706896; coagulation and tests PMC10305031, PMC3176495, PMC8068903, PMC4715843, PMC3654192,
  PMC9600347, PMC2913942; vWD PMC5406777, PMC3224412; DIC PMC4267589, PMC6710154; transfusion PMC9144124, PMC3999321,
  PMC4997901, PMC7371205; immunity PMC6156898, PMC6963682, PMC4267263; index formulas PMC9057813; reference intervals
  PMC6056383 (Korea, ages 3–99, shown with age bands).
- Contested, shown: each source's normal ranges, HbA2 share, neutrophil life, urobilinogen reabsorption, MCH range,
  platelet lifespan, hepatic urobilinogen (variable).
- Images (Commons, licences read 2026-11-22; resized, labelled): SEM blood cells (public domain, NCI); Ed Uthman smears
  (eosinophils, iron deficiency, sickle cell, spherocytes CC BY 2.0; reticulocytes CC BY 3.0); megakaryocyte (Erhabor
  Osaro, CC BY-SA 4.0, cropped to remove a wrong scale bar).
- Colour tokens: `--rbc`, `--platelet` (new, in phys.css); `--clot` (fibrin), `--eosin`, `--baso`, `--fluid` (plasma)
  reused with their meanings.
- Independent review 2026-11-22, fixed: undefined `--ok`; WHO children's cut-offs; PMC5767294 exclusion; lab-table
  starring; about 40 attributions; DIC and LMWH readouts; vWD screening wording; ESR preset; keyboard focus and grid
  arrow keys; antibody, IgA, haem-synthesis and red-cell drawings; colour meanings.

## 03 Cardiovascular physiology — `cvs/cardiac-electrophysiology.html`, `cvs/cardiac-cycle-output.html`, `cvs/haemodynamics-bp-regulation.html`

- Fact sheet `sources-local/facts/fill-physio3.md` (576 quotes, script-checked against `sources-local/modern/fill-physio3/`,
  downloads 2026-11-22).
- Excluded (cite OpenStax or cnx): Wikipedia Cardiac conduction system, Stroke volume, Cardiac output, Heart rate,
  Coronary circulation. Wikipedia Sinus arrhythmia copies StatPearls (counted once).
- 03a electrophysiology: phases PMC8424989, PMC4823581, Wikipedia; If PMC3387723, PMC4346881; rates PMC4823581,
  PMC4179748; AV delay 0.09 s (Wikipedia) vs 0.13 s (PMC8424989); ECG PMC5875041, PMC4040880, PMC11508899, StatPearls;
  blocks PMC8142363, PMC11390567, PMC3232542; STEMI PMC5388060, PMC13179089, PMC8142368; K⁺ PMC11041971, PMC11215665,
  PMC3043756.
- 03b cycle and output: PMC5018161, PMC7333110, PMC2805814, PMC4070490, PMC7700364, PMC9595280, StatPearls, Wikipedia
  (Jugular venous pressure for the a, c, v waves). Wiggers curves hand-set, valve states computed from them (schematic).
- 03c haemodynamics: PMC6842957, PMC7512016, PMC9917827, PMC4164098, PMC3959699, PMC2906723, PMC3144666, PMC8056939,
  PMC5073467, PMC6617132, PMC5018168, PMC2590178, PMC5523632, PMC10382122, PMC4239778 (ESICM 2014), PMC3672555,
  PMC6520577, PMC6507212, PMC8541346, PMC7252783, PMC4220427, PMC8126502, PMC10704008.
- Contested, shown: AV delay; upper limit of the normal axis (+90 vs +105); QRS and QTc limits; bradycardia and VT
  thresholds; ventricular RMP; the share of If in setting the rate; classic Starling vs the glycocalyx revision.
- Not shown for want of an open source: S4 as a stiff ventricle, why inspiratory S2 splitting widens, filling pressures
  and SVR in most shock types, EF 55–70% (the page gives 50–65% and ≥50% preserved), BP guideline thresholds.
- No new colour tokens: `--conduct`, `--valve` (from anatomy heart.html), `--heart`, `--vein`, `--artery`, `--nerve`,
  `--fluid` with their meanings; all figures are data-drawn schematics.
- Independent review 2026-11-22, fixed: stepper keyboard handler in phys.js; shock claims without a source removed;
  systolic-failure preset (EF 39%); tetanus, sinus-tachycardia and escape-rhythm wording; a, c, v waves labelled; LV
  pressure rise after the R wave; colour meanings; MAP slider limit; label collisions; a note that the 20/17/3 L figures
  are the classic model.
