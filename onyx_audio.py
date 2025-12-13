import pyaudio
import numpy as np
import soundfile as sf
import os
import shutil
import threading
import time
from datetime import datetime
import onyx_settings as config

class AudioEngine:
    def __init__(self):
        self.chunk = config.CHUNK_SIZE
        self.rate = config.SAMPLE_RATE
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.is_running = False
        self.is_recording = False
        self.frames = []
        self.current_hour = -1
        self.current_filename = ""
        self.device_index = config.AUDIO_DEVICE_INDEX

    def start_stream(self):
        try:
            # EXACTEMENT COMME LE TESTEUR
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index=self.device_index,
                                      frames_per_buffer=self.chunk)
            self.is_running = True
            print(f"--- MOTEUR AUDIO DÉMARRÉ ({self.rate}Hz) ---")
            
            # On lance la boucle de lecture DANS UN THREAD DÉDIÉ (Comme le testeur)
            threading.Thread(target=self._audio_loop, daemon=True).start()
            
        except Exception as e:
            print(f"!!! ERREUR AUDIO START : {e}")

    def _audio_loop(self):
        """Boucle de lecture calquée sur le testeur"""
        print(">>> BOUCLE AUDIO ACTIVE")
        while self.is_running:
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                
                # Gestion Enregistrement
                if self.is_recording:
                    self.frames.append(data)
                    self._check_hourly_rotation()
                
                # On stocke le dernier chunk pour le VU-mètre (lecture externe)
                self.last_chunk = data
                
            except: pass

    def get_audio_data(self):
        """Récupère le dernier chunk pour l'affichage"""
        if hasattr(self, 'last_chunk'):
            return np.frombuffer(self.last_chunk, dtype=np.int16)
        return None

    def stop_stream(self):
        self.is_running = False
        time.sleep(0.5) # On laisse le temps au thread de finir
        final = self.stop_recording()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        return final

    def start_recording(self):
        self.frames = []
        self.current_hour = datetime.now().hour
        self.current_filename = self._get_filename()
        self.is_recording = True # On active l'enregistrement
        print(f">>> REC START : {self.current_filename}")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            print(f"Arrêt REC. {len(self.frames)} frames capturées.")
            if self.frames:
                return self._save_worker(self.frames, self.current_filename)
        return None

    def _get_filename(self):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%Hh00")
        
        # MODIFICATION V2.03 : Utilisation directe du dossier tampon défini dans settings
        # On utilise config.RECORD_DIR au lieu de créer un dossier local relatif
        return os.path.join(config.RECORD_DIR, f"{timestamp}_Audio.flac")

    def _check_hourly_rotation(self):
        now = datetime.now()
        if now.hour != self.current_hour:
            old_frames = list(self.frames)
            old_filename = self.current_filename
            self.frames = []
            self.current_hour = now.hour
            self.current_filename = self._get_filename()
            threading.Thread(target=self._save_worker, args=(old_frames, old_filename)).start()

    def _save_worker(self, frames_to_save, filename):
        if not frames_to_save: return None
        try:
            raw_data = b''.join(frames_to_save)
            audio_array = np.frombuffer(raw_data, dtype=np.int16)
            
            # Vérif silence
            if np.max(np.abs(audio_array)) == 0:
                print("⚠️ ALERTE : FICHIER SILENCIEUX")
            
            sf.write(filename, audio_array, self.rate)
            final_path = filename
            
            # Gestion du transfert vers USB (si configuré)
            if config.USB_PATH and os.path.exists(config.USB_PATH):
                usb_dir = os.path.join(config.USB_PATH, "Sauvegardes_ONYX")
                if not os.path.exists(usb_dir): 
                    try: os.makedirs(usb_dir)
                    except: pass
                if os.path.exists(usb_dir):
                    dest = os.path.join(usb_dir, os.path.basename(filename))
                    shutil.move(filename, dest)
                    final_path = dest
            
            print(f"Sauvegarde OK : {final_path}")
            return final_path
        except Exception as e:
            print(f"Save Error: {e}")
            return None
