# QM640 EQEPD Final Capstone Repository

## Project title
**Evaluating the Business Impact of Artificial Intelligence Adoption Across the Quality Engineering Lifecycle**

**Student:** Satish Venugopal  
**Institution:** Walsh College  
**Course:** QM640: Data Analytics Capstone  
**Mentor:** Dr. Sanhita Karmakar  
**Term:** Summer 2026  
**Final submission date:** 13-August-2026  
**Repository URL:** https://github.com/satisho/QM640_Data-Analytics_Capstone

## Purpose
This repository contains the complete final capstone submission package. The study evaluates productivity improvement associated with Artificial Intelligence (AI) adoption across six Quality Engineering (QE) lifecycle phases: Test Planning, Test Design, Automation Development, Test Execution, Regression Testing, and Defect Management.

The final submission is cumulative. It retains the data preparation, exploratory analysis, hypothesis testing, and baseline modelling established for the interim milestone and extends them with final sensitivity analyses, model-stability checks, business-value interpretation, implementation guidance, limitations, and reproducibility evidence.

## Headline final results
- Raw project/sprint observations: **459**
- Exact duplicates removed: **2**
- Clean project/sprint observations: **457**
- Valid phase-level observations: **2,705**
- AI-assisted phase observations: **906**
- Traditional phase observations: **1,799**
- Mean AI-assisted productivity improvement: **16.95%**
- Mean traditional productivity improvement: **-4.63%**
- Mean difference: **21.58 percentage points**
- RQ1 Mann-Whitney U: **1,392,443, p < .001**
- RQ1 Cohen's d: **1.16**
- RQ2 Kruskal-Wallis: **H = 92.72, p < .001, epsilon-squared = .097**
- Strongest AI-assisted phases by mean improvement: **Regression Testing, Test Design, Automation Development**
- Primary RQ3 AI coefficient after controls: **+16.69 percentage points, p < .001**
- Best canonical predictive model: **Random Forest**
- Random Forest sprint-grouped holdout: **MAE 5.69, RMSE 7.29, R-squared .405**
- Random Forest grouped five-fold CV: **mean R-squared .471**
- Repeated grouped holdouts: Random Forest achieved best R-squared in **7 of 10** splits
- AI-assisted total effort saved: approximately **4,417.63 hours**
- Regression Testing, Test Design, and Automation Development account for approximately **94.5%** of positive AI-assisted hours saved.

## Final interpretation
The results support a **phase-specific, governed adoption strategy**, not uniform AI deployment. The strongest evidence supports scaling proven use cases in Regression Testing, Test Design, and Automation Development; Defect Management is suitable for controlled expansion; Test Planning and Test Execution remain targeted-pilot areas until stronger evidence is available.

The analysis is observational. The study therefore distinguishes statistical association, predictive usefulness, causal evidence, and complete financial return on investment. The predictive model is intended for directional portfolio screening and should not be used for precise budgets, individual performance assessment, or autonomous investment decisions.

## Repository structure
```text
QM640/
├── data/
│   ├── raw/
│   │   └── EQEPD_Dataset_v5.xlsx
│   └── processed/
│       ├── EQEPD_Cleaned_Project_Level.csv
│       └── EQEPD_Engineered_Phase_Level.csv
├── notebooks/
│   ├── QM640_EQEPD_Final_Analysis.ipynb
│   ├── QM640_EQEPD_Final_Analysis.html
│   └── archive/
├── outputs/
│   ├── figures/
│   └── tables/
├── reports/
│   ├── QM640_Final_Capstone_Report_Satish_Venugopal.docx
│   ├── QM640_Final_Capstone_Report_Satish_Venugopal.pdf
│   ├── FINAL_SUBMISSION_CHECKLIST.md
│   ├── Final_Report_Figure_Guide.md
│   └── archive/
├── scripts/
│   ├── final_analysis.py
│   ├── generate_final_figures.py
│   ├── generate_report_diagrams.py
│   ├── run_final_analysis.bat
│   ├── run_final_analysis.sh
│   ├── run_notebook.bat
│   └── run_notebook.sh
├── environment_versions.txt
├── repository_tree.txt
├── requirements.txt
└── README.md
```

## How to reproduce
### 1. Create a Python environment
Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Review the executed final evidence notebook
```bash
jupyter notebook notebooks/QM640_EQEPD_Final_Analysis.ipynb
```
The supplied notebook is already executed and provides a compact verification of the final evidence tables and figures.

### 3. Regenerate the full final analytical outputs
Windows:
```powershell
scripts\run_final_analysis.bat
```

macOS/Linux:
```bash
bash scripts/run_final_analysis.sh
```
The full workflow performs the statistical sensitivity checks, sprint-clustered regression specifications, grouped model comparison, grouped cross-validation, repeated grouped holdouts, feature-importance stability, error segmentation, adoption-roadmap generation, and final figure regeneration. Full model regeneration can take several minutes depending on CPU resources.

## Important final output files
### Final statistical and model evidence
- `outputs/tables/Final_RQ1_Sensitivity_Analysis.csv`
- `outputs/tables/Final_Minimum_Sample_Size_Power_Check.csv`
- `outputs/tables/Final_RQ2_Sensitivity_Analysis.csv`
- `outputs/tables/Final_RQ3_Regression_Stability.csv`
- `outputs/tables/Final_Model_Performance_Seed42.csv`
- `outputs/tables/Final_Grouped_Cross_Validation.csv`
- `outputs/tables/Final_Repeated_Grouped_Holdout_Summary.csv`
- `outputs/tables/Final_Permutation_Importance_Stability.csv`
- `outputs/tables/Final_Random_Forest_Error_by_Segment.csv`
- `outputs/tables/Final_Phase_Priority_and_Business_Value.csv`
- `outputs/tables/Final_AI_Adoption_Roadmap.csv`

### Final report figures
Figures 1-14 are available in `outputs/figures/`. The final report also retains selected appendix diagnostics from the interim analytical work. See `reports/Final_Report_Figure_Guide.md` for the exact figure mapping.

## Data and ethics note
The EQEPD is anonymised and aggregated for academic analysis. The package does not contain client names, employee identifiers, source code, production data, or personally identifiable information. Direct labour cost, AI licence cost, defect leakage, test coverage, automation coverage, AI tool identity, assistance intensity, and human-review effort are not available, so productivity improvement is not presented as a complete financial ROI measure.
