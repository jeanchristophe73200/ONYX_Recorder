import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import os
import time
from datetime import datetime, timedelta
import onyx_settings as config

class AudioEngine:
    def __init__(self, callback_file_completed=None):
        self.q = queue.Queue()
        self.stream = None
        self.is_recording = False
        self.device_idx = config.AUDIO_DEVICE_INDEX
        self.samplerate = 48000
        self.channels = 1
        self.subtype = 'PCM_24'
        
        # Gestion des fichiers
        self.current_filename = None  # Le fichier principal (pour le CSV)
        self.callback_file_completed = callback_file_completed # Pour prévenir le Main qu'un fichier est fini

    def callback(self, indata, frames, time_info, status):
        if status:
            print(f"Audio Status: {status}")
        self.q.put(indata.copy())

    def start_stream(self):
        if self.stream is not None: return
        try:
            self.stream = sd.InputStream(
                device=self.device_idx,
                channels=self.channels,
                samplerate=self.samplerate,
                callback=self.callback
            )
            self.stream.start()
            print(f"--- MOTEUR AUDIO V2.19 (ROTATION) DÉMARRÉ ---")
        except Exception as e:
            print(f"!!! ERREUR AUDIO START: {e}")

    def start_recording(self):
        if self.is_recording: return
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._rotation_record_loop)
        self.recording_thread.start()

    def _get_next_hour_timestamp(self, offset_seconds=0):
        """Calcule le timestamp de la prochaine heure pile + offset"""
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        return next_hour.timestamp() + offset_seconds

    def _generate_filename(self):
        """Génère un nom de fichier basé sur l'heure actuelle"""
        return os.path.join(config.RECORD_DIR, datetime.now().strftime("%Y-%m-%d_%Hh%M_Audio.flac"))

    def _rotation_record_loop(self):
        print(">>> BOUCLE DE ROTATION ACTIVE")
        
        # --- ETAT INITIAL ---
        file_A = None # Fichier Courant
        file_B = None # Fichier Suivant (pour le tuilage)
        path_A = self._generate_filename()
        path_B = None
        
        # On ouvre le premier fichier immédiatement
        try:
            file_A = sf.SoundFile(path_A, mode='w', samplerate=self.samplerate, channels=self.channels, subtype=self.subtype)
            self.current_filename = path_A
            print(f">>> REC START : {os.path.basename(path_A)}")
        except Exception as e:
            print(f"!!! ERREUR INIT FILE A: {e}")
            self.is_recording = False
            return

        # On calcule les prochains points de bascule
        # Tuilage START : 1 seconde AVANT l'heure pile (HH:59:59)
        # Tuilage STOP  : 1 seconde APRÈS l'heure pile (HH:00:01)
        next_rotation_ts = self._get_next_hour_timestamp(0) 
        overlap_start_ts = next_rotation_ts - 1.0 
        overlap_stop_ts  = next_rotation_ts + 1.0

        while self.is_recording:
            try:
                # 1. Récupération du Buffer (Timeout court pour ne pas bloquer)
                data = self.q.get(timeout=0.5)
                now = time.time()

                # 2. Gestion Fichier A (Le fichier courant)
                if file_A:
                    file_A.write(data)
                    # Si on dépasse le temps d'arrêt (HH:00:01), on ferme A
                    if now >= overlap_stop_ts:
                        print(f">>> CLOSING FILE A : {os.path.basename(path_A)}")
                        file_A.close()
                        file_A = None
                        # SIGNALER AU MAIN DE DÉPLACER CE FICHIER
                        if self.callback_file_completed:
                            self.callback_file_completed(path_A)
                        
                        # Rotation complète : B devient A
                        if file_B:
                            file_A = file_B
                            path_A = path_B
                            file_B = None
                            path_B = None
                            self.current_filename = path_A # Mise à jour pour le CSV
                            
                            # Recalcul des prochains horaires pour la nouvelle heure
                            next_rotation_ts = self._get_next_hour_timestamp(0)
                            overlap_start_ts = next_rotation_ts - 1.0
                            overlap_stop_ts  = next_rotation_ts + 1.0
                            print(f">>> ROTATION TERMINÉE. Nouveau cycle jusqu'à {datetime.fromtimestamp(next_rotation_ts).strftime('%H:%M:%S')}")

                # 3. Gestion Fichier B (Le fichier suivant - Anticipation)
                # Si on atteint HH:59:59, on ouvre B
                if now >= overlap_start_ts and file_B is None:
                    # On force le nommage de l'heure suivante pour éviter les doublons si démarrage tardif
                    # Astuce : On prend le timestamp de rotation pour nommer le fichier
                    next_dt = datetime.fromtimestamp(next_rotation_ts)
                    fname = next_dt.strftime("%Y-%m-%d_%Hh%M_Audio.flac")
                    path_B = os.path.join(config.RECORD_DIR, fname)
                    
                    try:
                        print(f">>> OPENING FILE B (Overlap) : {fname}")
                        file_B = sf.SoundFile(path_B, mode='w', samplerate=self.samplerate, channels=self.channels, subtype=self.subtype)
                    except Exception as e:
                        print(f"!!! ERREUR OPEN FILE B: {e}")

                # 4. Écriture dans B si ouvert (C'est ici que se fait le tuilage A+B)
                if file_B:
                    file_B.write(data)

            except queue.Empty:
                continue
            except Exception as e:
                print(f"!!! CRASH LOOP: {e}")
                break

        # --- NETTOYAGE FINAL ---
        # Si on arrête manuellement, on ferme tout proprement
        if file_A:
            file_A.close()
            # On demande aussi le délestage du dernier fichier partiel
            if self.callback_file_completed:
                self.callback_file_completed(path_A)
        if file_B:
            file_B.close() # B était à peine ouvert, on le supprime ou on le garde ? On le garde par sécurité.
            if self.callback_file_completed:
                self.callback_file_completed(path_B)

        self.is_recording = False
        print("Arrêt Thread Audio.")

    def stop_stream(self):
        self.is_recording = False
        # On attend un peu que le thread finisse
        time.sleep(1)
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        return None # Plus de retour de fichier unique, c'est géré par callback

    def get_audio_data(self):
        if not self.q.empty():
            try: return self.q.queue[-1] 
            except: return None
        return None
