#!/bin/bash
# SCRIPT DE COMPILATION/DISTRIBUTION ONYX
# Nettoie et Zippe le projet pour distribution

VERSION="V2.16"
DIR_NAME="ONYX_RELEASE_$VERSION"

echo "🚧 PRÉPARATION DE LA VERSION $VERSION..."

# 1. Création dossier temporaire
mkdir -p "$DIR_NAME"

# 2. Copie des fichiers essentiels (Pas le venv, pas les logs !)
cp onyx_*.py "$DIR_NAME/"
cp requirements.txt "$DIR_NAME/"
cp README_TECH.md "$DIR_NAME/"
cp install_onyx.sh "$DIR_NAME/"

# 3. Nettoyage (Au cas où des fichiers cachés traînent)
rm -rf "$DIR_NAME/__pycache__"
rm -rf "$DIR_NAME/*.csv"
rm -rf "$DIR_NAME/*.flac"

# 4. Compression
echo "📦 Compression en cours..."
zip -r "${DIR_NAME}.zip" "$DIR_NAME"

# 5. Nettoyage dossier temp
rm -rf "$DIR_NAME"

echo "✅ ARCHIVE PRÊTE : ${DIR_NAME}.zip"
echo "👉 Vous pouvez distribuer ce fichier zip."
