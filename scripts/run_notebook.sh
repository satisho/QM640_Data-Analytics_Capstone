#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 notebooks/QM640_EQEPD_Interim_Analysis.ipynb
echo "Notebook execution completed. Review outputs/figures and outputs/tables."
