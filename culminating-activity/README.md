# Culminating Activity: EIF Final Culmination (Portfolio, Reflection and Story)

> ⚠️ **Everything numerical in this folder is synthetic.** The numbers describe the behaviour of a generative model calibrated to cited *aggregate* statistics. None of them measures any real Philippine student or institution, and none should be reported as an empirical finding.

**Author:** Matthew C. Batitay
**Project:** Eskwelabs Innovation Fellowship, Data Innovation Track
**Covers:** my Synthetic Dataset project and its three deliverables, in [`../whitepaper/`](../whitepaper/), [`../synthetic-data-generator/`](../synthetic-data-generator/) and [`../results-and-discussion/`](../results-and-discussion/)

## What this is
The EIF Final Culmination is not a new project. It is a portfolio of my EIF work, a reflection on my growth, and a way to present my contributions, built around one question: *what did I do, and what does it say about me?* `eif-final-culmination.pdf` is that story as a **38-slide deck** (16:9). It has five parts, each opened by a divider slide:

| Part | What it contains |
|---|---|
| 1. About Me | Who I am, how I work, and a skills snapshot that points to where each skill can be checked in the repository. |
| 2. My EIF Journey | The track and its three deliverables, how I met the programme's definition of done, the path through the work, and "the good, the bad, the old, the new". |
| 3. Project Portfolio | The project at a glance, then each deliverable on its own slides with **Problem / Context**, **Role and Contributions**, **Output** (links and figures) and **Skills Demonstrated**. |
| 4. Reflection | What I learned, what challenged me, what I am proud of, and what I would improve. |
| 5. What Is Next | How I would finish this project, extend it, and what real use would require, plus a table of where everything is. |

The deck opens with a short orientation and a synthetic-data notice, closes with a summary slide, and ends with the sources it cites.

## Files
```
culminating-activity/
├── README.md
├── .gitignore                       # tracks only the deliverables (same allow-list approach as the other folders)
├── eif-final-culmination.tex        # Beamer source of the deck
├── eif-final-culmination.pdf        # the rendered deck (38 slides, 16:9)
└── references.bib                   # the sources the deck cites (entries copied from ../whitepaper/references.bib)
```
There is no `figures/` folder on purpose. The deck reuses three figures that already exist in this repository and loads them by relative path, so there is one copy of each and nothing to keep in sync:

| Slide | Figure | File it loads |
|---|---|---|
| 18 | Generation pipeline | `../whitepaper/figures/fig1_pipeline.png` |
| 22 | Generator diagnostics | `../synthetic-data-generator/output/diagnostics.png` |
| 26 | The actionability gap | `../results-and-discussion/figures/fig3_actionability_gap.png` |

The journey diagram and the provenance-tag chips are drawn in TikZ inside the `.tex`, so they need no image files.

## Design
The deck is built on a Beamer template with a section tab in the header, a three-part footer, a rounded key-box and a shadowed title block, restyled with the Eskwelabs gradient: sage-mint at the top, through teal and deep teal, to a muted indigo. The gradient fills the title, divider and closing slides, and a slim strip of it runs across the top of every content slide. Brand orange marks alerts and brand blue marks key results. All colours are defined once, near the top of the `.tex`.

## Rebuilding the PDF
From this folder, with a standard TeX Live or MiKTeX installation and **the repository layout intact** (the three figures above are loaded from the sibling folders):
```
pdflatex eif-final-culmination.tex
bibtex   eif-final-culmination
pdflatex eif-final-culmination.tex
pdflatex eif-final-culmination.tex
```
It needs the packages `beamer`, `lmodern`, `tcolorbox`, `tikz`, `natbib`, `microtype`, `booktabs` and `array`, all of which ship with a standard installation. The third run is needed so the "n / N" slide counter and the gradient strips settle.

## How it follows the Final Culmination guidelines
| Guideline | Where it is met |
|---|---|
| Include About You, EIF Journey, Project Portfolio, Reflection, What's Next | Parts 1 to 5 above. |
| For each project: Problem / Context, Role and Contributions, Output, Skills Demonstrated | Part 3, once for each of the three deliverables. |
| Reflection prompts: learn, challenged, proud of, improve | Part 4, one slide for each. |
| List all EIF projects and include them all | My EIF work is one project with three deliverables, and all three are included. If I add another project, copy a deliverable's slides in Part 3 of the `.tex`. |
| Highlight the good, the bad, the old, the new | Part 2, the slides "The good and the bad" and "The old and the new". |
| Add reflection last; clarity, not perfection | The reflection is built from what the earlier slides show, and the limitations that remain are stated rather than hidden. |

## Conventions
* **Synthetic status is stated on every slide**, in the footer, and in a notice near the start of the deck.
* **Provenance tags** (`LOCKED`, `CALIBRATED`, `ASSUMED`) are used wherever a model parameter is quoted, as in the rest of the repository.
* **Numbers are the released generator's (v1.0.1, seed 193), not the whitepaper pilot's.** The pilot appears only where it is described as the pilot. See [`../whitepaper/README.md`](../whitepaper/README.md) for the reconciliation.
* **Links** in the PDF point to files on the `main` branch of this repository.
