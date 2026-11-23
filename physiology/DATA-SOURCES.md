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
