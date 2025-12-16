# ONYX V3.2 (Flux Edition)

Système de surveillance acoustique autonome pour macOS (Apple Silicon).
Architecture modulaire avec enregistrement audio rotatif, monitoring SPL (REW), surveillance météo et journalisation par Flags.

## 🚀 Fonctionnalités Clés

* **Audio Rotatif** : Enregistrement FLAC 24-bit/48kHz continu avec découpage horaire (sans perte).
* **Flux Edition** : Système de qualification rapide par "Flags" (Source Std, Source +, Source -, Résiduel).
* **Intégration REW** : Récupération temps réel des niveaux dBA/dBC et du spectre via l'API locale de Room EQ Wizard.
* **Météo Locale** : Injection automatique des données (Temp, Vent, Pluie) dans les logs via Open-Meteo.
* **Sécurisation** : Écriture sur SSD local + Délestage automatique vers clé USB si détectée.
* **Interface Pro** : UI sombre "Cockpit", optimisée pour réduire la fatigue visuelle.
* **Notifications** : Alertes de fonctionnement via Bot Telegram.

## 🛠️ Pré-requis Système

* **Machine** : Mac Mini / MacBook (Puce M1/M2/M3 recommandée).
* **OS** : macOS Sonoma ou Sequoia.
* **Logiciel Tiers** : [REW (Room EQ Wizard)](https://www.roomeqwizard.com/) doit être installé et lancé (API serveur active sur port 4735).
* **Python** : Version 3.11 (via Homebrew).

## 📦 Installation

Ouvrez votre Terminal et exécutez les commandes suivantes ligne par ligne :

```bash
# 1. Installation de Python et PortAudio (Moteur Son)
brew install python@3.11 portaudio

# 2. Clonage du projet (ou téléchargement du ZIP)
git clone https://github.com/VOTRE_NOM/ONYX_V3.git
cd ONYX_V3

# 3. Création de l'environnement virtuel (Isolation)
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate

# 4. Installation des dépendances (Versions strictes)
pip install -r requirements.txt
```

## ▶️ Utilisation

1.  **Lancer REW** et activer le serveur API (Preferences > API > Start Server).
2.  **Lancer ONYX** :
    ```bash
    source venv/bin/activate
    python onyx_main.py
    ```
3.  **Configuration** : Au démarrage, choisissez le disque de sauvegarde USB, le micro et le mode de durée.
4.  **En vol** : Utilisez les boutons de droite pour qualifier les sources sonores.
5.  **Arrêt** : Cliquez sur "ARRÊTER LA MISSION". Le système finalisera le fichier audio, copiera le CSV sur la clé USB et enverra un rapport Telegram.

## 📂 Architecture des fichiers

* `onyx_main.py` : Orchestrateur et logique principale.
* `onyx_audio.py` : Moteur d'enregistrement (Thread haute priorité).
* `onyx_gui.py` : Interface utilisateur (CustomTkinter).
* `onyx_rew.py` : Pont API vers REW.
* `onyx_settings.py` : Configuration globale.

---
*Version 3.2 (Pro Dark UI) - 2025*
