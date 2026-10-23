# output/

Everything `../student-retention-data-generator.ipynb` writes is stored in this folder (default run: N = 50,000 students, seed 193).

> ⚠️ **All data here is synthetic.** It describes the behaviour of a generative model, not any real student or population.

| File | Contents |
|---|---|
| `Regions.csv` | Two regional tiers: share, calibration target, source |
| `Students.csv` | One row per student (50,000) |
| `Enrollments.csv`, `CourseGrades.csv`, `AttendanceRecords.csv`, `FinancialHolds.csv`, `SupportInterventions.csv`, `PersistenceOutcomes.csv` | Student × term panels (297,739 rows each) |
| `metadata.json` | Seed, calibrated parameters, library versions, row counts and the SHA-256 of every table |
| `parameter_log.csv` | Every model parameter with its `LOCKED` / `CALIBRATED` / `ASSUMED` tag |
| `validation_scorecard.csv` | The validation scorecard (whitepaper Table 5) |
| `diagnostics.png` | Diagnostic figure |
| `DATASET_NOTICE.txt` | Synthetic-data notice |

To regenerate, run the notebook; the table hashes in `metadata.json` let you check that a regenerated copy is identical (same platform and library versions).
