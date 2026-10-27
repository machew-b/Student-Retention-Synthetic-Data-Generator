# Results and Discussion: Student Retention Analytics (Deliverable 3)

> ⚠️ **Everything here is synthetic.** Every number describes the behaviour of a generative model calibrated to cited *aggregate* statistics. None of it measures any real Philippine student or institution, and none of it says what any real institution should do.

**Project:** Eskwelabs Innovation Fellowship, Data Innovation Track
**Builds on:** my whitepaper, *A Two-Layer Synthetic Data Generator for Studying Student Retention Early-Warning Systems in Philippine Higher Education* (v17), and the dataset from Deliverable 2 (`../synthetic-data-generator/`, generator v1.0.1)

## What this is
I use the Deliverable 2 dataset the way a Student Success Analyst would, and I use the hidden ground truth only to grade the analysis. Because I know the support programme cuts the dropout hazard by exactly 30 %, I can say whether each method gets the right answer, not just whether it produces an answer. The notebook covers six questions:

| § | Question | Headline (synthetic data) |
|---|---|---|
| 4 | Is the generator valid? | Re-derived from the CSVs, 7 of 7 comparable scorecard rows are identical to the generator's own. |
| 5 | What does the data show? | Cumulative attrition 67.1 % (high tier) and 45.9 % (typical tier); attrition is highest among low-income working students. |
| 6 | Can attrition be predicted before it happens? | Out-of-fold AUC 0.655 for boosted trees against 0.567 for the signal-count rule. A predictor that knew every student's hidden baseline vulnerability would reach 0.683, and one that knew the true hazard 0.722. 19.4 % of dropouts occur in term 1, before any prior record exists. |
| 7 | Does a good predictor tell me whether support works? | No. The raw comparison says support *raises* dropout by 58 %; stratifying on the model's risk score gives +7 % (misses the truth); stratifying on the assignment signals gives +32.2 % (CI 24.3 % to 39.3 %) against a true 30 %. |
| 8 | Does the support programme work? | Mantel–Haenszel and cluster-robust Poisson recover about 30 % (SD about 4 points over 20 populations). Inverse-probability weighting swings from −47 % to +72 % over the same populations. Adjusting for only some of the referral signals fails. |
| 9 | Who is flagged, who is missed, what do false flags cost? | 63.7 % of dropout events occur in terms with a clean record and no support. At equal capacity a model-ranked list would avert an expected 18 % more dropouts than the actual rule, and still only 66 % of an unattainable oracle. |
| 10 | How robust is this? | Eleven recalibrated scenarios. Mantel–Haenszel stays near 30 %. IPW only stabilises once all signal cells contain both arms. The predictable part of dropout is capped by baseline vulnerability, not by shocks. |

The slide deck in `slides/` presents the same chain of evidence in 17 slides (plus two backup slides). Its figures are redrawn at slide size from the executed notebook, and its tables are generated from the notebook's outputs.

Section 11 turns this into eight recommendations about how to build and evaluate a retention programme. Section 12 lists every limitation and open flag.

## Folder layout
```
results-and-discussion/
├── README.md
├── requirements.txt                       # library versions I tested with
├── student-retention-analytics.ipynb      # the analysis (committed with outputs cleared; run it to regenerate everything)
├── student-retention-analytics.html       # an executed copy, so the results can be read without running anything
├── slides/
│   ├── student-retention-results-slides.tex   # Beamer source (pdflatex, run twice)
│   ├── student-retention-results-slides.pdf   # the 17-slide deck plus 2 backup slides
│   └── figures/                               # vector figures and generated tables used by the slides
└── figures/
    └── fig1_descriptive.png … fig7_sensitivity.png
```

## Quick start
1. Install the packages with `pip install -r requirements.txt`.
2. Open `student-retention-analytics.ipynb` from the repository root or from this folder, and **Run All**. It reads the exported CSV files in `../synthetic-data-generator/output/`, so Deliverable 2 does not need to be re-run first.
3. A full run takes about 10 to 15 minutes. Two switches in the first code cell help: `FAST_MODE` for a quick smoke test (not comparable with the scorecard) and `RUN_SENSITIVITY = False` to skip §10.

I tested with Python 3.12.3, numpy 2.4.4, pandas 3.0.2, scipy 1.17.1, statsmodels 0.15.0, matplotlib 3.10.8 and scikit-learn 1.8.0 (pinned in `requirements.txt`). Other versions are untested.

## How it is built
* **The analysis sees only what an analyst would see.** Sections 5 to 9.1 use the exported tables only. The hidden state (baseline vulnerability, shocks, hazard) is used in three groups of clearly labelled places, always to *grade* the analysis: the validation checks (§4.4, §4.6), the prediction ceilings and policy values (§6.4, §9.2), and the new-population sensitivity runs (§10).
* **The generator engine is copied unchanged** into §3, and the notebook proves the copy is faithful: it regenerates all eight tables with SHA-256 hashes equal to `metadata.json`, and its calibration loop returns the recorded (δ, γ0). If the hash check fails on your platform, the notebook says so and skips only the steps that need exact row alignment.
* **No leakage.** A feature for student *i* in term *t* uses only entry attributes and records from terms 1 to *t*−1. A guard in the code rejects outcome columns, current-term columns and the regional tier. The one model that breaks the rule (a labelled "leaky contrast") is only there to show how much apparent skill current-term data would add.
* **Validation is grouped by student** (5-fold), with the same folds for every model, fixed hyperparameters and no tuning on the evaluation data.
* **Every choice I add carries a tag** (`LOCKED`, `CALIBRATED` or `ASSUMED`) in a small D3 registry that mirrors the generator's, and §12 prints it.
* **Every output carries a synthetic-data banner**, including each figure title.

## Key limitations (full list: notebook §12)
* All conclusions are properties of the generator: the predictability ceilings, the homogeneous 30 % effect and the form of the confounding are assumptions, not measurements.
* The policy value in §9.2 assumes a homogeneous effect, so ranking by risk is optimal by construction. A head-to-head pilot would be needed with real effects.
* The generator has no carry-over (support never changes later grades) and no unmeasured assignment confounders, so the causal problem here is easier than a real one.
* The IPW results are a best case, since the analyst is given the true propensity.
* Sensitivity is one parameter at a time with 10 replicates per scenario. The held-out check from Deliverable 2 is fragile (OF-2) and I did not re-run it.
* Bitwise reproducibility holds only on the same platform and library versions.

## Citations
Methods: Law (2015); James, Witten, Hastie & Tibshirani (2013); Gelman, Hill & Vehtari (2020); Peters, Janzing & Schölkopf (2017). Practitioner framing for prediction as decision support: Lopez-Muñoz, Gonzalez Serrano & Sanchez-Ferreira (2026), *Journal of Information Technology Education: Research* 25, https://doi.org/10.28945/5776 (confirmed by web search while writing the notebook). The generator's calibration sources are listed in `../synthetic-data-generator/README.md` and whitepaper §10.
