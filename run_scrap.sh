#!/bin/bash
# ===============================
# Wrapper pour exécuter scrap.py
# ===============================

# Dossier du script
SCRIPT_DIR="/home/username/projets/rtm_waryme"
cd "$SCRIPT_DIR" || exit 1

# Python à utiliser (ou python3 si dans PATH)
PYTHON="/usr/bin/python3"

# Lancer le script et capturer logs
$PYTHON scrap.py >> scraper_run.log 2>&1

# Vérifier code retour
if [ $? -ne 0 ]; then
    echo "❌ Erreur détectée, vérifier scraper_run.log"
fi
