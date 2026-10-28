# Student Retention Early-Warning: a Synthetic Data Generator and What It Teaches (Philippine Higher Education)

> ⚠️ **Everything in this repository is synthetic.** It describes the behaviour of a generative model calibrated to cited *aggregate* statistics. It is **not** a measurement of any real Philippine student, institution or programme, and no number derived from it should be reported as an empirical finding.

**Author:** Matthew C. Batitay
**Project:** Eskwelabs Innovation Fellowship, Data Innovation Track

## The idea in one paragraph
Philippine higher-education records show what a student does (grades, attendance, financial-account status) but rarely why a student leaves, and the individual-level mechanisms behind published attrition figures are not present in any public dataset. Early-warning systems also tend to base support decisions on the same signals that predict dropout, so the effect of a support programme cannot be read off a naive comparison. I built a dataset to practise on that problem: a synthetic cohort in which a **hidden** state (structural vulnerability and acute shocks) drives both the recorded data and the dropouts, support is assigned from prior-term signals, and the true effect of support is known. Because the truth is known, I can test whether an analysis gets the right answer, not just whether it produces one.

## What is in the repository
| Folder | What it is | Start with |
|---|---|---|
| [`whitepaper/`](whitepaper/) | The specification: a two-layer generative model with every parameter tagged `LOCKED`, `CALIBRATED` or `ASSUMED`. | `student-retention-data-generator-model.pdf` |
| [`synthetic-data-generator/`](synthetic-data-generator/) | Deliverable 2: the generator (a notebook) and the dataset it produced: eight CSV tables, a validation scorecard, a parameter log and metadata. | `README.md`, then `output/` |
| [`results-and-discussion/`](results-and-discussion/) | Deliverable 3: an analysis of the dataset as a Student Success Analyst would do it, using the hidden truth only to grade the results. Notebook, executed HTML, and a slide deck. | `student-retention-results-slides.pdf` |

## Start here
* **I want the argument in ten minutes:** open the slide deck, `results-and-discussion/student-retention-results-slides.pdf` (17 slides and 2 backup slides).
* **I want the full results without running anything:** open `results-and-discussion/student-retention-analytics.html`.
* **I want the data:** `synthetic-data-generator/output/` holds the eight tables. The generator README describes each table, `output/README.md` lists the files, and `output/DATASET_NOTICE.txt` is the usage notice.
* **I want the specification and its justification:** the whitepaper PDF. Its folder README maps the sections and reconciles the Appendix A pilot with the released generator.

## What the analysis found (synthetic data)
* **The generator holds up** when its checks are re-derived from the CSV files: seven of seven comparable scorecard rows are identical, and the engine reproduces all eight tables bit for bit.
* **Early warning works, but only modestly.** Out-of-fold AUC is 0.655 for boosted trees against 0.567 for the signal-count rule. Even a predictor that knew every student's hidden vulnerability would reach only 0.683, and 19.4% of dropouts happen in term 1, before any prior record exists.
* **A good predictor cannot tell you whether support works.** The raw comparison says support *raises* dropout by 58%. Stratifying on the programme's own referral signals gives a 32.2% reduction (95% CI 24.3% to 39.3%) against a true 30%.
* **Estimator choice matters more than sample size.** Mantel–Haenszel and Poisson recover about 30% with a standard deviation of about 4 points over 20 populations. Inverse-probability weighting swings from −47% to +72% over the same populations.
* **Most dropouts happen where the programme is not looking.** 63.7% of dropout events fall in terms with a clean record and no support.
* **These conclusions survive what I varied:** eleven scenarios, each recalibrated to the same cited tier targets.

The recommendations and the full list of limitations are in the Deliverable 3 notebook (Sections 11 and 12).

## Reproduce it
```
pip install -r results-and-discussion/requirements.txt
```
1. **Regenerate the dataset (optional, about 30 to 50 seconds):** run `synthetic-data-generator/student-retention-data-generator.ipynb`. The committed dataset is already there.
2. **Re-run the analysis (about 10 to 15 minutes):** run `results-and-discussion/student-retention-analytics.ipynb`. It reads the committed CSV files, so step 1 is not required.
3. **Rebuild the PDFs (optional):** `pdflatex` in `results-and-discussion/` for the slides (run twice), and `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` in `whitepaper/` for the paper.

I tested with Python 3.12.3, numpy 2.4.4, pandas 3.0.2, scipy 1.17.1, statsmodels 0.15.0, matplotlib 3.10.8 and scikit-learn 1.8.0. Results are bitwise reproducible on the same platform and library versions, and statistically equivalent elsewhere. If a file hash check fails on your machine (often a line-ending effect on Windows), the notebooks say so and continue.

## Conventions used throughout
* **Provenance tags.** Every number that drives the model is tagged `LOCKED` (fixed by design), `CALIBRATED` (set to reproduce a cited statistic) or `ASSUMED` (a stated modelling choice). The generator logs all 60 of its parameters in `synthetic-data-generator/output/parameter_log.csv`, and Deliverable 3 logs the choices it adds.
* **Calibration is not validation.** Matching the two tier targets shows only that the calibration loop converged. The checks with independent content are the correlation structure, the confounding check and the recoverability check.
* **Open flags.** The limitations I know of are logged with a status (`OPEN`, `NOTED` or `RESOLVED`): flags OF-1 to OF-12 in the generator notebook, and DF-1 to DF-9 in the Deliverable 3 notebook.
* **No regional naming.** No individual-level table carries a region name; students carry only a two-tier label, `high` or `typical` (whitepaper Section 13.3).
* **Synthetic status is stated everywhere.** The dataset ships with a usage notice, the analysis notebook prints a synthetic-data banner with its results, every notebook figure title carries one, and so does the footer of every slide.

## A note on consistency across the documents
The whitepaper's Appendix A reports a **pilot** implementation, which gives different realised numbers from the released generator (for example the Mantel–Haenszel estimate and the held-out check). When describing the dataset, quote the generator's numbers. The reconciliation is in [`whitepaper/README.md`](whitepaper/README.md).
