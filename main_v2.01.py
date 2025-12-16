import sys

def main():
    print("--- Démarrage du système V2.01 (Python) ---")

    # ---------------------------------------------------------
    # ÉTAPE 1 : Nettoyage (Initialisation d'une liste vide)
    # ---------------------------------------------------------
    markers = []

    # ---------------------------------------------------------
    # ÉTAPE 2 : Création des Nouveaux Marqueurs
    # ---------------------------------------------------------
    
    # Marqueur 1
    markers.append({
        "Name": "Point Alpha",
        "Lat":  45.67,
        "Lng":  6.39
    })

    # Marqueur 2
    markers.append({
        "Name": "Point Beta",
        "Lat":  48.85,
        "Lng":  2.35
    })

    # Marqueur 3
    markers.append({
        "Name": "Point Gamma",
        "Lat":  43.70,
        "Lng":  7.26
    })

    # ---------------------------------------------------------
    # Vérification du contenu
    # ---------------------------------------------------------
    print(f"Nettoyage terminé. {len(markers)} nouveaux marqueurs prêts :")
    
    for i, m in enumerate(markers):
        print(f" [{i+1}] {m['Name']} : Latitude {m['Lat']} / Longitude {m['Lng']}")

if __name__ == "__main__":
    main()
