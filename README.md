# ONYX V3.2 (Flux Edition)

**Système de surveillance acoustique autonome pour macOS (Apple Silicon).**
Architecture modulaire avec enregistrement audio rotatif, monitoring SPL (REW), surveillance météo et journalisation par Flags.

---

## 🚀 Fonctionnalités Clés

* **Audio Rotatif** : Enregistrement FLAC 24-bit/48kHz continu avec découpage horaire (sans perte de données).
* **Flux Edition** : Système de qualification rapide par "Flags" (Source Std, Source +, Source -, Résiduel) sans icônes superflues.
* **Intégration REW** : Récupération en temps réel des niveaux dBA/dBC et du spectre via l'API locale de Room EQ Wizard.
* **Météo Locale** : Injection automatique des données (Température, Vent, Pluie, Pression) dans les logs via Open-Meteo.
* **Sécurisation des Données** : Écriture sur SSD local + Délestage automatique vers clé USB dès qu'elle est détectée.
* **Interface "Pro Dark"** : UI sombre "Cockpit", optimisée pour réduire la fatigue visuelle et l'éblouissement nocturne.
* **Notifications** : Alertes de fonctionnement et rapports d'événements envoyés via Bot Telegram.

## 🛠️ Pré-requis Système

* **Machine** : Mac Mini / MacBook (Puce M1/M2/M3/M4 recommandée).
* **Système d'exploitation** : macOS Sonoma ou Sequoia.
* **Logiciel Tiers** : [REW (Room EQ Wizard)](https://www.roomeqwizard.com/) doit être installé.
    * *Configuration REW* : Allez dans `Preferences > API` et cochez **"Start Server"** (Port 4735).
* **Python** : Version 3.11 (gérée automatiquement par le script d'installation).

## 📦 Installation Rapide

1.  **Téléchargez** la dernière "Release" (fichier `.zip`) depuis la colonne de droite sur GitHub.
2.  **Décompressez** le dossier où vous le souhaitez.
3.  Ouvrez le **Terminal** dans ce dossier.
4.  Lancez l'installateur automatique :

```bash
sh install.sh
