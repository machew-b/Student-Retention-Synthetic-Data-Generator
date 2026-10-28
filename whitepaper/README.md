# Whitepaper: A Two-Layer Synthetic Data Generator for Studying Student Retention Early-Warning Systems in Philippine Higher Education

> ⚠️ **This paper specifies a synthetic data model.** Nothing in it, and nothing in the dataset built from it, measures any real Philippine student or institution.

**Author:** Matthew C. Batitay
**Project:** Eskwelabs Innovation Fellowship, Data Innovation Track
**Cited as:** "whitepaper v17" in the generator and Deliverable 3 documents. The PDF itself does not print a version number.

## What this is
The paper specifies a **two-layer generative model** for student retention. A hidden state (a student's structural vulnerability and exposure to acute shocks) drives both the observed institutional record (grades, attendance, financial holds, support) and the eventual dropout, and no downstream analyst can see it. Support is assigned from the same prior-term signals that predict dropout, so the effect of a support programme cannot be read off a naive comparison. Every generative parameter is tagged `LOCKED`, `CALIBRATED` (against cited Philippine statistics) or `ASSUMED`, and Section 11 says how the model is checked, including the difference between calibration and validation.

The model is implemented in [`../synthetic-data-generator/`](../synthetic-data-generator/) and analysed in [`../results-and-discussion/`](../results-and-discussion/).

## Files
```
whitepaper/
├── README.md
├── student-retention-data-generator-model.tex   # the paper (LaTeX source)
├── student-retention-data-generator-model.pdf   # the rendered paper (29 pages)
├── references.bib                               # bibliography
└── figures/
    ├── fig1_pipeline.png   fig1_pipeline.py     # Figure 1 and the script that draws it
    └── fig2_dag.png        fig2_dag.py          # Figure 2 and the script that draws it
```

## Section guide
The generator and Deliverable 3 documents cite the paper by section, so here is the map.

| § | Title | | § | Title |
|---|---|---|---|---|
| 1 | Introduction | | 10 | Calibration Parameter Design (sources, Table 4) |
| 2 | Related Work and Theoretical Foundation | | 11 | Validation Measures and Success Benchmarks (Table 5) |
| 3 | Design Principles | | 12 | Deliberate Edge Cases |
| 4 | System Architecture and End-to-End Pipeline | | 13 | Ethical and Responsible-Use Considerations (13.3 Regional Framing) |
| 5 | Phase 1: Cohort and Region Initialization | | 14 | Limitations and Scope |
| 6 | Phase 2: Latent State Assignment | | 15 | Conclusion |
| 7 | Phase 3: Term-by-Term Observable Generation | | App. A | Reference Instantiation and Pilot Check |
| 8 | Phase 4: Confounded Intervention Assignment (Eqs. 1 and 2) | | App. B | Field-Level Schema (Table 8), Integrity Rules, Reproducibility Policy |
| 9 | Phase 5: Outcome Generation and Validation (Eq. 3) | | | |

## Rebuilding the PDF
From this folder, with a standard TeX Live or MiKTeX installation:
```
pdflatex student-retention-data-generator-model.tex
bibtex   student-retention-data-generator-model
pdflatex student-retention-data-generator-model.tex
pdflatex student-retention-data-generator-model.tex
```
I rebuilt it this way from the committed source and got a 29-page PDF with the same text as the committed one. The two figures are regenerated with `python fig1_pipeline.py` and `python fig2_dag.py` from inside `figures/` (matplotlib only). Both reproduce the committed PNGs byte for byte.

## Appendix A (pilot) versus the production generator
Appendix A reports a **pilot implementation** of one admissible instantiation of the specification. The paper is explicit that the pilot "is a feasibility check of the specification, not the production generator", and that it implements only the core mechanism (Phases 1 to 5) and omits the non-core attributes of Appendix B. The released dataset comes from the **production generator** (`synthetic-data-generator/`, version 1.0.1, seed 193), which implements the full schema. The two share the same forms and parameters, but they are separate runs, so their realised numbers differ.

| Quantity | Appendix A pilot | Production generator v1.0.1 |
|---|---|---|
| Calibrated (δ, γ0) | (1.06, −2.67) | (1.033, −2.673) |
| Tier attrition, high / typical / pooled | 67.1% / 45.9% / 49.1% | 67.1% / 45.9% / 49.1% |
| Naive estimate, 1 − RR (95% CI) | −57.6% (−64.1% to −50.8%) | −57.7% (−64.6% to −50.6%) |
| Mantel–Haenszel | 25.5% | 32.2% (24.3% to 39.3%) |
| Poisson | 25.5% (16.6% to 33.5%) | 33.6% (25.1% to 41.2%) |
| Mantel–Haenszel over 20 populations | mean 28.4%, SD 4.4, range 21.0% to 35.4% | mean 28.9%, SD 4.3, range 20.4% to 36.0% |
| IPW with the true propensity | 75.6% untrimmed, −17.8% trimmed (not recovered) | Hajek 39.1% and Horvitz–Thompson 32.7% untrimmed; −13.7% and +73.7% clipped (unreliable: SD about 37 to 38 points over 20 populations) |
| Held-out Class-of-2023 tier ratio (band 1.2 to 1.7) | 1.72, **not passed**; over 8 populations 1.71 ± 0.04, 12% in band | 1.673, **pass (fragile)**; over 20 populations 1.692 ± 0.025, 60% in band |
| Student-terms by prior signal count k = 0 / 1 / 2 / 3 | 186,580 / 47,341 / 11,407 / 2,168 | 186,653 / 47,528 / 11,321 / 2,237 |
| Of which supported, k = 0 / 1 / 2 / 3 | 19 / 2,258 / 10,880 / 2,167 | 26 / 2,237 / 10,793 / 2,237 |

**What agrees.** Both calibrate to the same two tier targets. In both, the naive comparison is badly confounded and excludes the true 30%. In both, estimators that assume a constant risk ratio (Mantel–Haenszel, Poisson) recover the effect while inverse-probability weighting does not. In both, the assignment is near-deterministic at k = 0 and k ≥ 2, so only the one-signal and two-signal cells contain both arms.

**What differs, and how to read it.** The point estimates differ by amounts of the size that run-to-run variation produces: the Mantel–Haenszel estimate of the pilot (25.5%) and of the production run (32.2%) are about 1.5 standard deviations apart, where the SD across populations is about 4.4 points in both. The held-out verdict differs because the ratio sits at the edge of the pre-specified band: 1.72 is just outside it and 1.673 just inside, which is the fragility that the generator notebook records as open flag OF-2. I did not trace the exact source of the differences between the two runs, because the pilot script is not in this repository.

**Which numbers to quote.**
* When describing the released dataset, the generator, or Deliverable 3, quote the **production** numbers. They are in `../synthetic-data-generator/output/validation_scorecard.csv` and are re-derived from the CSV files in `../results-and-discussion/`.
* Quote the Appendix A numbers only when describing the pilot.

**One item that is not in the repository.** Appendix A says "a script reproducing the results accompanies this paper". That pilot script is not included here. The production generator notebook is the implementation to run.

## Consistency with the generator
I checked the paper against the released dataset. The Appendix B Table 8 schema matches the exported CSV headers exactly, and the dataset satisfies every Appendix B.2 integrity rule (unique keys, contiguous terms, no rows after dropout, risk score empty only in term 1, no support in term 1, valid value ranges, no region names). Citations in the generator and Deliverable 3 documents to Section 10 (calibration), Section 11 (validation), Section 12 (edge cases), Section 13.3 (regional framing), Table 4, Table 5, Table 8 and Appendix B.3 point to the right places.

## Citation sources behind the calibration
CPBRD (2025), EDCOM II (2024, 2025) and CHED (2025) are traced in Section 10 and listed in `references.bib`. The generator README lists the sources it uses directly.
