@echo off
cd /d "%~dp0\.."
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 notebooks\QM640_EQEPD_Interim_Analysis.ipynb
if errorlevel 1 (
  echo Notebook execution failed.
  exit /b 1
)
echo Notebook execution completed. Review outputs\figures and outputs\tables.
