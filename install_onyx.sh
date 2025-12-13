#!/bin/bash
# INSTALLATEUR AUTOMATIQUE ONYX V2.16
# Pour macOS

echo "========================================"
echo "      INSTALLATION ONYX V2.16"
echo "========================================"

# 1. Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERREUR : Python 3 n'est pas installé."
    echo "👉 Veuillez installer Python depuis python.org"
    exit 1
fi

echo "✅ Python 3 détecté."

# 2. Création de l'environnement virtuel (isolé)
echo "📦 Création de l'environnement virtuel..."
cd "$(dirname "$0")"
python3 -m venv venv

# 3. Activation et Installation des dépendances
echo "⬇️  Téléchargement des bibliothèques..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Création du lanceur rapide (Double-clic)
echo "🔨 Création du raccourci de lancement..."
cat << EOF > LANCER_ONYX.command
#!/bin/bash
cd "\$(dirname "\$0")"
source venv/bin/activate
python3 onyx_main.py
EOF

chmod +x LANCER_ONYX.command

echo "========================================"
echo "✅ INSTALLATION TERMINÉE AVEC SUCCÈS !"
echo "👉 Double-cliquez sur 'LANCER_ONYX.command' pour démarrer."
echo "========================================"
