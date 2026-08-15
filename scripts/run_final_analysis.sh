#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python scripts/final_analysis.py
python scripts/generate_final_figures.py
python scripts/generate_report_diagrams.py
