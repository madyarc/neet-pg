# NEET-PG

**🌐 Website: [madyarc.github.io/neet-pg](https://madyarc.github.io/neet-pg/)**

Revision for NEET-PG you can see and handle, organised by the official MBBS curriculum. Plain static HTML, no build
step. Sister project of [jee-materials](https://github.com/madyarc/jee-materials).

## Modules

### Anatomy — [`anatomy/`](anatomy/index.html)

| # | Module | Branch | What it does |
|---|---|---|---|
| 01 | [The Femur](anatomy/lower-limb/femur.html) | Lower limb | 3D bone: 18 landmarks with a find-it quiz; left or right?; 30 muscle and ligament attachments; neck fracture and blood supply; five ossification centres |

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
tools/bones/                builds 3D bone data from BodyParts3D
tools/test/                 headless-browser checks
```

## Run locally

Open `index.html` in a browser.

## Credits

3D bones: BodyParts3D, © The Database Center for Life Science, licensed under CC Attribution-Share Alike 2.1 Japan.
The simplified meshes embedded in the pages are shared under the same licence.

## Adding to it

Read [`CLAUDE.md`](CLAUDE.md) first: content, verification and design rules, and the steps for adding a module.
