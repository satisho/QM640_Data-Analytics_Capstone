# QM640 EQEPD Interim Capstone Repository

## Project title
**Evaluating the Business Impact of Artificial Intelligence Adoption Across the Quality Engineering Lifecycle**

**Student:** Satish Venugopal  
**Institution:** Walsh College  
**Course:** QM640: Data Analytics Capstone  
**Mentor:** Ms. Sanhita Karmakar  
**Term:** Summer 2026

## Purpose
This repository contains the reproducible analytical package supporting the QM640 interim report. It evaluates productivity improvement associated with Artificial Intelligence adoption across six Quality Engineering lifecycle phases:

1. Test Planning
2. Test Design
3. Automation Development
4. Test Execution
5. Regression Testing
6. Defect Management

The package preserves the distinction between statistical association, predictive usefulness, and causal evidence. The models are intended for directional decision support rather than autonomous investment decisions.

## Repository structure

```text
QM640_EQEPD_Interim_GitHub_Repository/
├── data/
│   ├── raw/
│   │   └── EQEPD_Dataset_v5.xlsx
│   └── processed/
│       ├── EQEPD_Cleaned_Project_Level.csv
│       └── EQEPD_Engineered_Phase_Level.csv
├── notebooks/
│   ├── QM640_EQEPD_Interim_Analysis.ipynb
│   └── QM640_EQEPD_Interim_Analysis.html
├── outputs/
│   ├── figures/
│   └── tables/
├── reports/
│   ├── QM640_EQEPD_Interim_Report_Satish_Venugopal.docx
│   └── Interim_Report_Figure_Guide.md
├── scripts/
│   ├── run_notebook.bat
│   └── run_notebook.sh
├── .gitignore
├── README.md
└── requirements.txt
```

## Headline reproducible results
The notebook is designed to reproduce the principal interim findings:

- Raw observations: **459**
- Exact duplicates removed: **2**
- Clean project/sprint observations: **457**
- Valid phase-level observations: **2,705**
- AI-assisted phase observations: **906**
- Traditional phase observations: **1,799**
- Mean AI-assisted productivity improvement: approximately **16.95%**
- Mean traditional productivity improvement: approximately **-4.63%**
- Highest AI-assisted mean improvement: **Regression Testing**, followed by **Test Design** and **Automation Development**
- Best grouped holdout model: **Random Forest**
- Random Forest holdout performance: MAE approximately **5.68**, RMSE approximately **7.29**, R² approximately **0.405**

## How to run

### 1. Create a Python environment

Windows:

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

### 2. Open and execute the notebook

```bash
jupyter notebook notebooks/QM640_EQEPD_Interim_Analysis.ipynb
```

Use **Kernel > Restart & Run All**. The notebook automatically writes processed datasets, tables, and figures into the repository folders.

A command-line execution option is also available:

Windows:

```powershell
scripts\run_notebook.bat
```

macOS/Linux:

```bash
bash scripts/run_notebook.sh
```

## Figures for the interim report
The figures whose numbering matches the interim report are stored under `outputs/figures/`:

- Figure 3: Dataset preview
- Figure 4: Missing values by variable
- Figure 5: AI adoption rate across years
- Figure 6: AI adoption rate by QE lifecycle phase
- Figure 7: AI-assisted versus traditional productivity
- Figure 8: AI-assisted productivity by phase
- Figure 9: AI adoption breadth and overall productivity
- Figure 10: Grouped holdout model comparison

Additional diagnostic figures are also provided for the appendix or final report.

## Uploading to GitHub
Create an empty GitHub repository, copy the contents of this folder into it, and run:

```bash
git init
git add .
git commit -m "Add QM640 EQEPD interim capstone package"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

After publication, replace the repository placeholder in the interim report with the active GitHub URL.

## Data and ethics note
The dataset is anonymised and aggregated for academic analysis. No client names, employee identifiers, source code, production data, or personally identifiable information are included. The study measures operational productivity through baseline and actual effort; it does not contain direct financial cost, AI licence cost, defect leakage, test coverage, AI tool identity, or AI-assistance intensity.
