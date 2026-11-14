# Syllabus generator

Builds `../../SYLLABUS.md` and every `<subject>/SYLLABUS.md` from the NMC CBME 2024 PDF.

Source PDF: NMC, *Guidelines for Competency Based Medical Education (CBME) Curriculum 2024*, notice
D-11011/500/2024-AcademicCell, 12-09-2024 (466 pages). Copy used: https://medicaldialogues.in/pdf_upload/cbme-2024-guidelines-252294.pdf
Not stored in the repo.

```bash
W=$(mktemp -d)            # work folder outside the repo
curl -sSL -o $W/cbme.pdf https://medicaldialogues.in/pdf_upload/cbme-2024-guidelines-252294.pdf
pdftotext -layout $W/cbme.pdf $W/cbme.txt
cd $W
python3 -I <repo>/tools/syllabus/parse_cbme.py cbme.txt .      # -> cbme.json
python3 -I <repo>/tools/syllabus/patch_cbme.py                 # hand fixes, checked against the PDF
python3 -I <repo>/tools/syllabus/fill_domain.py cbme.txt       # K/S/A/C domains printed beside the code
python3 -I <repo>/tools/syllabus/write_syllabus.py cbme.json hub-sections.txt <repo>
```

`hub-sections.txt` is the Revision Hub outline (subject / chapter / section headings), extracted from
`source/NEET-PG-2026_Revision-Hub.html`. Regenerating overwrites any ticks in the subject files, so
only rerun it before ticking starts.
