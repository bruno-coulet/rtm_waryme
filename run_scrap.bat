@echo off
REM ===============================
REM Wrapper pour exécuter scrap.py
REM ===============================

REM Chemin complet vers Python (ou utilise python si dans PATH)
SET PYTHON=C:\Users\coule\anaconda3\python.exe

REM Dossier du script
SET SCRIPT_DIR=C:\Users\coule\Documents\projets\rtm_waryme
CD /D %SCRIPT_DIR%

REM Lancer le script et rediriger stdout/stderr vers un log
%PYTHON% scrap.py >> scraper_run.log 2>&1

REM Vérifier si le script a échoué (code retour != 0)
IF ERRORLEVEL 1 (
    echo Erreur détectée, vérifier scraper_run.log
)
