# Synthetic Student-Retention Dataset (Philippine Higher Education)

> ⚠️ **All data produced here is synthetic.** It describes the behaviour of a generative model calibrated to cited *aggregate* statistics. It is **not** a measurement of any real student or population. Do not report any number derived from it as an empirical finding.

**Project:** Eskwelabs Innovation Fellowship, Data Innovation Track
**Implements:** *A Two-Layer Synthetic Data Generator for Studying Student Retention Early-Warning Systems in Philippine Higher Education* (whitepaper v17, Appendix A reference instantiation)
**Generator version:** 1.0.0

## What this is
A generator for a synthetic student cohort in which a **hidden** state (baseline vulnerability + per-term acute shocks) drives both the **recorded** institutional data (grades, attendance, financial holds, support) and the eventual dropout — mirroring what a Student Success Analyst can and cannot see. Support is assigned using prior-term records only, so a naive treated-vs-untreated comparison is **confounded**; the true support effect is fixed by design (30 % relative hazard reduction) so analyses can be scored against a known answer.

## Quick start
1. `pip install numpy pandas scipy statsmodels matplotlib jupyter`
2. Open `student-retention-data-generator.ipynb`, edit the `CONFIG` cell (`N_STUDENTS`, `MASTER_SEED`, …), and **Run All**.
3. ≈ 50 s at N = 50,000 (≈ 10 s with `RECALIBRATE=False`). Outputs land in `output/`.

| Setting | Meaning |
|---|---|
| `N_STUDENTS` | Students generated (default 50,000 → ≈ 298k rows per panel table). Tolerances were designed at 50,000; small N widens sampling noise. |
| `MASTER_SEED` | One integer seed; independent named streams per variable. |
| `RECALIBRATE` | Re-fit the hazard intercept γ₀ and tier shift δ for this N/seed, or reuse `FROZEN_CALIBRATION`. |
| `WRITE_AUDIT_LATENT` | Leave `False`. The latent state is never exported; `True` writes a *private* audit copy. |

## The eight tables
Panel tables have one row per student per term, for terms 1…Tᵢ only (no rows after dropout).

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

Other outputs: `metadata.json` (seed, versions, row counts, SHA-256 of every table), `parameter_log.csv` (every parameter with its tag), `validation_scorecard.csv`, `diagnostics.png`, `DATASET_NOTICE.txt`.

**Deliberately absent:** baseline vulnerability, shock indicators, the hazard. Region *names* are never exported — only the two-tier label (whitepaper §13.3).

## What you can analyze
1. **Dropout prediction** — classify the per-term `dropout_flag`; observables only reveal the hidden state noisily, so there is a ceiling on achievable accuracy.
2. **Discrete-time survival / hazard modelling** on the person-period panel, with right-censoring at term 8.
3. **Causal effect of support under confounding** — compare naive vs adjusted estimators against the known 30 % truth. Estimate the **risk ratio**; the odds ratio drifts away from it.
4. **Targeting audits** — who is flagged, who is missed (shock-driven dropouts with clean records), who is flagged unnecessarily.
5. **Positivity / estimator-choice exercises** — assignment is near-deterministic when 0 or ≥ 2 of 3 prior-term signals fire, so only the k = 1 and k = 2 cells contain both arms.

## Validation snapshot (N = 50,000, seed 193 — numbers describe the model, not reality)
| Check (whitepaper Table 5) | Result |
|---|---|
| Tier attrition, high / typical (calibrated) | 67.1 % / 45.9 % → PASS (this is calibration-until-convergence, not validation) |
| Pooled attrition (derived blend) | 49.1 % → PASS |
| Held-out Class-of-2023 tier ratio, band [1.2, 1.7] | 1.673 → **PASS (fragile)**: over 20 replicate populations 1.69 ± 0.03, only ≈ 60 % inside the band |
| Confounding presence | naive estimate −57.7 % (CI −64.6 % to −50.6 %) excludes the true 30 % → PASS |
| Recoverability | Mantel–Haenszel 32.2 % (CI 24.3–39.3 %); cluster-robust Poisson 33.6 % (CI 25.1–41.2 %) → PASS; window ±8.6 pp is wide (estimator SD ≈ 4.3 pp across runs) |
| Edge cases from the mechanism | 2,937 unflagged shock-driven dropouts; 774 falsely flagged → PASS |
| Parameter traceability | 56 parameters: 47 ASSUMED, 6 CALIBRATED, 3 LOCKED → PASS |

## Known limitations (full list: notebook §10)
* **Realized targeting does not match the §8 design targets — decided, not re-fitted.** Only ≈ 6 % of student-terms are supported, so sensitivity is ≈ 16 % (capped near 21 % at a 30 % "high-vulnerability" prevalence), not 70 %. A scan (notebook §7.4) shows the 70 %/25 % pair is not jointly reachable here, so re-fitting would be ill-posed. Appendix A defaults are kept; weaker-targeting settings are reserved for Deliverable-3 sensitivity analysis.
* **The held-out check is fragile** and the structural reason is spec-level (OF-2).
* **IPW is unreliable here**: four reasonable variants give −14 % to +74 % on identical data (OF-12).
* The 47 `ASSUMED` parameters — including all non-core attribute forms — are not empirically grounded; they are the candidate list for sensitivity analysis.
* The 29.4 % national figure is read as a Class of 2023 value from table layout (OF-7). "Attrition" here includes temporary leave, so rates are an upper bound on permanent dropout.
* Single shock type, single undifferentiated intervention, fixed (not heterogeneous) effect, two regional tiers; gender, disability and indigenous status are not modelled.
* Bitwise reproducibility only on the same platform and library versions.

## Citations used by the generator's calibration
CPBRD (2025) *CHED Agency Budget Notes FY 2026* (regional attrition table); EDCOM II (2025) *Year Two Report*; CHED (2025) FY2026 budget presentation. See whitepaper §10 for the full provenance trace and cohort reasoning. Methods: Law (2015); Gelman, Hill & Vehtari (2020); Peters, Janzing & Schölkopf (2017); McElreath (2020).
