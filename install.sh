#!/bin/bash
echo "--- INSTALLATION ONYX V3.2 ---"

if ! command -v brew &> /dev/null; then
    echo "ERREUR: Homebrew n'est pas installé."
    exit 1
fi

echo "[1/3] Installation des composants système..."
brew install python@3.11 portaudio

echo "[2/3] Création de l'environnement virtuel..."
rm -rf venv
/opt/homebrew/bin/python3.11 -m venv venv

echo "[3/3] Installation des librairies Python..."
source venv/bin/activate
pip install -r requirements.txt

echo "--- INSTALLATION TERMINÉE ---"
echo "Pour lancer : source venv/bin/activate && python onyx_main.py"
