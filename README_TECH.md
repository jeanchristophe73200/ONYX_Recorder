# ONYX V2.16 - SYSTEME DE PREUVE ACOUSTIQUE

## 📋 PRÉREQUIS MACHINE
* **Ordinateur :** Apple Mac (Mac mini, MacBook Air/Pro, iMac).
* **Système OS :** macOS 10.15 (Catalina) ou supérieur recommandé.
  *(Fonctionne techniquement sur 10.13 High Sierra mais nécessite des certificats SSL à jour).*
* **Logiciel Tiers :** REW (Room EQ Wizard) doit être installé et ouvert pour le monitoring SPL.
* **Microphone :** Interface USB (ex: UMIK-1) ou micro interne calibré.

## 🚀 INSTALLATION (Première fois)
1. Décompressez le dossier `ONYX_V2.16`.
2. Ouvrez le Terminal.
3. Glissez le fichier `install_onyx.sh` dans le terminal et appuyez sur Entrée.
   *(Ou tapez `sh install_onyx.sh` si vous êtes dans le dossier).*
4. Attendez la fin de l'installation des bibliothèques.

##  ▶️ DÉMARRAGE
Double-cliquez simplement sur le fichier **`LANCER_ONYX.command`** qui a été créé dans le dossier.

## 🕹️ UTILISATION
### 1. Configuration (Écran Jaune)
* **USB :** Sélectionnez votre clé USB pour la sauvegarde (ou "Disque Local").
* **Micro :** Choisissez votre source audio (ex: "UMIK-1").
* **Durée :**
    * *Continu :* Enregistrement infini (boucle).
    * *24h/48h/72h :* Cycles légaux (démarrent et finissent à 07h00).
* **GPS :** Entrez vos coordonnées (Lat, Lon) pour la météo locale.

### 2. Monitoring (Interface Principale)
* **Start :** Lance la séquence en cascade (Check Disque -> Météo -> Audio).
* **Indicateur de Vie :** Le texte "ENREGISTREMENT ACTIF" clignote (rouge vif/sombre).
* **Boutons Événements :** Cliquez pour noter un événement (Passage Train, Voisin, Avion...).
* **Correction :** Si vous avez oublié de cliquer, utilisez "Correction (-1 min)".

### 3. Arrêt & Récupération
* Cliquez sur **STOP**.
* Choisissez :
    * **ARRÊT IMMÉDIAT :** Coupe tout proprement en 3 secondes.
    * **ARRÊT HEURE PLEINE :** Attend la fin du cycle de 60min en cours (ex: arrêt à 10h55 si lancé à 09h55).
* **Fichiers :** Retrouvez les preuves (CSV + FLAC) dans le dossier `Sauvegardes_ONYX` sur votre clé USB.

## ⚖️ VALIDITÉ LÉGALE
Les fichiers générés (FLAC et CSV) contiennent :
* Signature numérique de la machine.
* Horodatage précis.
* Données météorologiques complètes (Temp, Vent, Pluie, Pression).
* Calibration SPL (via REW).

---
*Développé pour Jean-Christophe Finantz - 2025*
