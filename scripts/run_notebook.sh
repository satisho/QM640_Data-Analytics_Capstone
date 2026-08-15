#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
jupyter notebook notebooks/QM640_EQEPD_Final_Analysis.ipynb
