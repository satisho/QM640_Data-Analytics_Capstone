@echo off
setlocal
cd /d "%~dp0\.."
python scripts\final_analysis.py
if errorlevel 1 exit /b %errorlevel%
python scripts\generate_final_figures.py
if errorlevel 1 exit /b %errorlevel%
python scripts\generate_report_diagrams.py
if errorlevel 1 exit /b %errorlevel%
endlocal
