# Synthetic Student-Retention Dataset (Philippine Higher Education)

> ⚠️ **All data produced here is synthetic.** It describes the behaviour of a generative model calibrated to cited *aggregate* statistics. It is **not** a measurement of any real student or population. Do not report any number derived from it as an empirical finding.

**Project:** Eskwelabs Innovation Fellowship, Data Innovation Track
**Implements:** my whitepaper, *A Two-Layer Synthetic Data Generator for Studying Student Retention Early-Warning Systems in Philippine Higher Education* (v17, Appendix A reference instantiation)
**Generator version:** 1.0.1

## What this is
I built a generator for a synthetic student cohort in which a **hidden** state (baseline vulnerability plus per-term acute shocks) drives both the **recorded** institutional data (grades, attendance, financial holds, support) and the eventual dropout. This mirrors what a Student Success Analyst can and cannot see. Support is assigned using prior-term records only, so a naive comparison of treated and untreated students is **confounded**. I fixed the true support effect by design (a 30 % relative hazard reduction) so that any analysis can be scored against a known answer.

## Folder layout
```
synthetic-data-generator/
├── README.md
├── requirements.txt                         # library versions I tested with
├── student-retention-data-generator.ipynb   # the generator: run this
└── output/                                  # everything the notebook writes
    ├── Regions.csv … PersistenceOutcomes.csv    # the eight tables
    ├── metadata.json  parameter_log.csv  validation_scorecard.csv
    ├── diagnostics.png
    └── DATASET_NOTICE.txt
```

## Quick start
1. Install the packages with `pip install -r requirements.txt` (or `pip install numpy pandas scipy statsmodels matplotlib jupyter`).
2. Open `student-retention-data-generator.ipynb`, edit the `CONFIG` cell (`N_STUDENTS`, `MASTER_SEED`, …), and **Run All**.
3. A full run takes about 30–50 s at N = 50,000 (about 15–30 s with `RECALIBRATE=False`), depending on hardware. Outputs are written to `output/` inside this folder (`synthetic-data-generator/output/`), even if Jupyter is launched from the repository root.

I tested with Python 3.12.3, numpy 2.4.4, pandas 3.0.2, scipy 1.17.1, statsmodels 0.15.0 and matplotlib 3.10.8, which are the versions pinned in `requirements.txt`. Other versions are untested.

| Setting | Meaning |
|---|---|
| `N_STUDENTS` | Students generated (default 50,000, which gives about 298k rows per panel table). The tolerances were designed at 50,000, and a small N widens the sampling noise. |
| `MASTER_SEED` | One integer seed, with independent named streams per variable. |
| `RECALIBRATE` | Re-fit the hazard intercept γ₀ and tier shift δ for this N and seed, or reuse `FROZEN_CALIBRATION` (full-precision values fitted at N = 50,000, seed 193, which reproduce the default dataset exactly on the same platform and library versions). |
| `WRITE_AUDIT_LATENT` | Leave this `False`. The latent state is never exported, and `True` writes a *private* audit copy. |
| `OUTPUT_DIR` | Name of the folder the notebook writes to (default `output`). |

## The eight tables
Panel tables have one row per student per term, for terms 1…Tᵢ only (no rows after dropout). The field-level types are in Appendix B of the whitepaper (Table 8).

| Table | Grain | Key contents |
|---|---|---|
| `Regions` | per tier | tier share, calibration target, source |
| `Students` | per student | `region_tier` (high/typical), entry year, programme, income bracket 1–5, working-student, distance, subsidy at entry |
| `Enrollments` | student × term | `enrollment_status`, `censored` (true only on term 8 for never-withdrawn students) |
| `CourseGrades` | student × term | `term_avg_score` (0–100), units attempted/passed |
| `AttendanceRecords` | student × term | `attendance_rate` (0–1) |
| `FinancialHolds` | student × term | `hold_flag`, `overdue_amount` (PHP), `subsidy_status` |
| `SupportInterventions` | student × term | `risk_score` (null in term 1), `intervention` (always false in term 1) |
| `PersistenceOutcomes` | student × term | `dropout_flag`, `attrition_flag` (rolled-up) |

Other outputs: `metadata.json` (seed, versions, row counts, SHA-256 of every table), `parameter_log.csv` (every parameter with its tag), `validation_scorecard.csv`, `diagnostics.png` and `DATASET_NOTICE.txt`.

**Deliberately absent:** I never export baseline vulnerability, shock indicators or the hazard. No individual-level table carries a region name, only the two-tier label (whitepaper Sec. 13.3). The `Regions` table names the source regions only inside its `target_source` citation text.

## What you can analyze
1. **Dropout prediction.** Classify the per-term `dropout_flag`. The observables only reveal the hidden state noisily, so there is a ceiling on achievable accuracy.
2. **Discrete-time survival / hazard modelling** on the person-period panel, with right-censoring at term 8.
3. **Causal effect of support under confounding.** Compare naive and adjusted estimators against the known 30 % truth. Estimate the **risk ratio**, because the odds ratio drifts away from it.
4. **Targeting audits.** Who is flagged, who is missed (shock-driven dropouts with clean records), and who is flagged unnecessarily.
5. **Positivity and estimator-choice exercises.** Assignment is near-deterministic when 0 or at least 2 of the 3 prior-term signals fire, so only the k = 1 and k = 2 cells contain both arms.

## Validation snapshot (N = 50,000, seed 193; these numbers describe the model, not reality)
| Check (whitepaper Table 5) | Result |
|---|---|
| Tier attrition, high / typical (calibrated) | 67.1 % / 45.9 % → PASS (this is calibration until convergence, not validation) |
| Pooled attrition (derived blend) | 49.1 % → PASS |
| Held-out Class-of-2023 tier ratio, band [1.2, 1.7] | 1.673 → **PASS (fragile)**: over 20 replicate populations the ratio is 1.69 ± 0.03, and only about 60 % of runs fall inside the band |
| Confounding presence | the naive estimate is −57.7 % (CI −64.6 % to −50.6 %), which excludes the true 30 % → PASS |
| Recoverability | Mantel–Haenszel 32.2 % (CI 24.3–39.3 %) and cluster-robust Poisson 33.6 % (CI 25.1–41.2 %) → PASS. The window of ±8.6 pp is wide (estimator SD about 4.3 pp across runs) |
| Edge cases from the mechanism | 2,937 unflagged shock-driven dropouts and 774 falsely flagged students → PASS |
| Parameter traceability | 60 parameters: 51 ASSUMED, 6 CALIBRATED, 3 LOCKED → PASS |

## Known limitations (full list: notebook Sec. 10)
* **Realized targeting does not match the Sec. 8 design targets, and I decided not to re-fit.** Only about 6 % of student-terms are supported, so sensitivity is about 16 % (capped near 21 % at a 30 % "high-vulnerability" prevalence), not 70 %. My scan (notebook Sec. 7.4) shows that the 70 % / 25 % pair is not jointly reachable here, so re-fitting would be ill-posed. I kept the Appendix A defaults and reserve weaker-targeting settings for the sensitivity analysis in Deliverable 3.
* **The held-out check is fragile**, and the structural reason lies in the specification itself (OF-2).
* **IPW is unreliable here.** Four reasonable variants give −14 % to +74 % on identical data (OF-12).
* The 51 `ASSUMED` parameters, including all non-core attribute forms, are not empirically grounded. They are my candidate list for sensitivity analysis.
* The 29.4 % national figure is read as a Class of 2023 value from the table layout (OF-7). "Attrition" here includes temporary leave, so the rates are an upper bound on permanent dropout.
* The model has a single shock type, a single undifferentiated intervention, a fixed (not heterogeneous) effect and two regional tiers. Gender, disability and indigenous status are not modelled.
* Bitwise reproducibility holds only on the same platform and library versions.

## Citations used by the generator's calibration
CPBRD (2025) *CHED Agency Budget Notes FY 2026* (regional attrition table); EDCOM II (2025) *Year Two Report*; CHED (2025) FY2026 budget presentation. See whitepaper Sec. 10 for the full provenance trace and cohort reasoning. Methods: Law (2015); Gelman, Hill & Vehtari (2020); Peters, Janzing & Schölkopf (2017); McElreath (2020).
