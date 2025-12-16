import requests
import base64
import struct
import onyx_settings as config
import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)

class RewEngine:
    def __init__(self):
        # ADRESSES API REW (unit=SPL pour avoir les décibels corrects)
        self.url_levels = "http://127.0.0.1:4735/rta/levels"
        self.url_data = "http://127.0.0.1:4735/rta/captured-data?unit=SPL"
        
        self.session = requests.Session()
        self.session.trust_env = False 
        self.connected = False

    def get_full_data(self):
        result = {
            "dba": 0.0,
            "dbc": 0.0,
            "spectrum": {k: "" for k in config.FREQS}
        }
        
        try:
            # 1. RÉCUPÉRATION NIVEAUX GLOBAUX
            r1 = self.session.get(self.url_levels, timeout=0.2)
            
            if r1.status_code == 200:
                self.connected = True
                d = r1.json()
                val = d[0] if isinstance(d, list) and len(d) > 0 else d
                
                if isinstance(val, dict):
                    if 'rmsLevelAWeighted' in val: 
                        result["dba"] = val['rmsLevelAWeighted'].get('value', 0.0)
                    elif 'rmsLevel' in val: 
                        result["dba"] = val['rmsLevel'].get('value', 0.0)
                    
                    if 'rmsLevelCWeighted' in val: 
                        result["dbc"] = val['rmsLevelCWeighted'].get('value', 0.0)
            else:
                self.connected = False

            # 2. RÉCUPÉRATION DU SPECTRE (BASE64)
            if self.connected:
                try:
                    r2 = self.session.get(self.url_data, timeout=0.2)
                    if r2.status_code == 200:
                        d = r2.json()
                        raw_mag = d.get('magnitude', '')
                        
                        if raw_mag:
                            # A. Décodage Base64
                            decoded_bytes = base64.b64decode(raw_mag)
                            count = len(decoded_bytes) // 4
                            # B. Conversion en liste de nombres (dB)
                            values = struct.unpack(f'>{count}f', decoded_bytes)
                            
                            # C. Mapping des fréquences
                            # On récupère le point de départ
                            start_freq = d.get('startFreq', 0)
                            
                            # REW en RTA envoie souvent les données en "Points par Octave" (PPO)
                            # Si on ne trouve pas 'ppo', on suppose un step linéaire ou on tente de deviner
                            ppo = d.get('ppo', 0) 
                            freq_step = d.get('freqStep', 0)

                            if len(values) > 0:
                                # On parcourt chaque valeur reçue de REW
                                for i, db_val in enumerate(values):
                                    # Calcul de la fréquence correspondante à ce point 'i'
                                    if ppo > 0:
                                        # Formule Logarithmique (Standard RTA)
                                        current_freq = start_freq * (2 ** (i / ppo))
                                    elif freq_step > 0:
                                        # Formule Linéaire (Rare en RTA mais possible)
                                        current_freq = start_freq + (i * freq_step)
                                    else:
                                        continue

                                    # On regarde si cette fréquence correspond à une de nos cibles (20Hz, 25Hz...)
                                    for target_str in config.FREQS:
                                        try:
                                            target = float(target_str)
                                            # Tolérance large (10%) pour "attraper" la valeur la plus proche
                                            if abs(current_freq - target) < (target * 0.10):
                                                # On prend la valeur (arrondie à 1 décimale)
                                                result["spectrum"][target_str] = round(db_val, 1)
                                        except: pass

                except Exception as e: 
                    # print(f"Erreur spectre: {e}") # Debug silencieux
                    pass

            return result

        except Exception:
            self.connected = False
            return None
