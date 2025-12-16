import requests
import base64
import struct
import json

# URL de base selon votre doc
BASE_URL = "http://localhost:4735"

def decode_base64_floats(b64_string):
    """Décode une chaîne Base64 en liste de nombres décimaux (floats)"""
    try:
        # 1. Décodage Base64 en bytes
        decoded_bytes = base64.b64decode(b64_string)
        # 2. Conversion bytes -> floats (Big Endian standard pour l'audio réseau)
        # '>f' signifie Big-Endian Float (4 bytes)
        count = len(decoded_bytes) // 4
        floats = struct.unpack(f'>{count}f', decoded_bytes)
        return floats
    except Exception as e:
        return f"Erreur décodage: {e}"

def run_test():
    print(f"--- TEST API REW : {BASE_URL} ---")

    # 1. VÉRIFICATION DU STATUT RTA
    try:
        r_status = requests.get(f"{BASE_URL}/rta/status", timeout=1)
        print(f"1. RTA STATUS: {r_status.text}")
    except:
        print("❌ REW non accessible (vérifiez que le serveur API est coché dans les préférences REW)")
        return

    # 2. VÉRIFICATION DES NIVEAUX (Ce qui marche déjà)
    try:
        r_levels = requests.get(f"{BASE_URL}/rta/levels", timeout=1)
        print(f"2. NIVEAUX (dBA/dBC): {r_levels.text}")
    except:
        print("❌ Erreur Niveaux")

    # 3. RÉCUPÉRATION DU SPECTRE (Ce qui échoue)
    print("\n3. ANALYSE DU SPECTRE (/rta/captured-data)...")
    try:
        # On demande explicitement l'unité SPL comme indiqué dans la doc
        r_data = requests.get(f"{BASE_URL}/rta/captured-data?unit=SPL", timeout=2)
        
        if r_data.status_code == 200:
            data = r_data.json()
            keys = data.keys()
            print(f"   🔑 Clés reçues : {list(keys)}")
            
            if 'magnitude' in data:
                raw_mag = data['magnitude']
                print(f"   📦 Format 'magnitude' : {type(raw_mag)}")
                print(f"   📄 Début des données brutes : {str(raw_mag)[:50]}...")
                
                # TENTATIVE DE DÉCODAGE
                values = decode_base64_floats(raw_mag)
                if isinstance(values, tuple) and len(values) > 0:
                    print(f"   ✅ DÉCODAGE RÉUSSI !")
                    print(f"   📊 Nombre de points de fréquence : {len(values)}")
                    print(f"   🔎 5 premières valeurs (dB) : {[round(v, 1) for v in values[:5]]}")
                    
                    # Récupération des infos de fréquence pour comprendre l'échelle
                    start_freq = data.get('startFreq', 0)
                    freq_step = data.get('freqStep', 1)
                    print(f"   📏 Start: {start_freq}Hz | Step: {freq_step}Hz")
                else:
                    print(f"   ❌ Echec décodage : {values}")
            else:
                print("   ❌ Pas de clé 'magnitude' trouvée.")
        else:
            print(f"   ❌ Erreur HTTP : {r_data.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur requête : {e}")

if __name__ == "__main__":
    run_test()
