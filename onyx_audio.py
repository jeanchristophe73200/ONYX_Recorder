import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import os
import time
from datetime import datetime
import onyx_settings as config

class AudioEngine:
    def __init__(self):
        self.q = queue.Queue()
        self.stream = None
        self.is_recording = False
        self.current_filename = None
        self.file = None
        self.start_time = None
        self.device_idx = config.AUDIO_DEVICE_INDEX
        self.samplerate = 48000
        self.channels = 1
        self.subtype = 'PCM_24'

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
            print(f"--- MOTEUR AUDIO DÉMARRÉ ({self.samplerate}Hz) ---")
        except Exception as e:
            print(f"!!! ERREUR AUDIO START: {e}")

    def start_recording(self):
        if self.is_recording: return
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._record_loop)
        self.recording_thread.start()

    def _record_loop(self):
        print(">>> BOUCLE AUDIO ACTIVE")
        while self.is_recording:
            # --- MODIFICATION V2.17 : TIMESTAMP PRÉCIS (HHhMMmSS) ---
            now = datetime.now()
            # Format précis à la seconde : 14h32m15_Audio.flac
            fname = now.strftime("%Y-%m-%d_%Hh%Mm%S_Audio.flac")
            self.current_filename = os.path.join(config.RECORD_DIR, fname)
            
            try:
                with sf.SoundFile(self.current_filename, mode='w', samplerate=self.samplerate, 
                                channels=self.channels, subtype=self.subtype) as file:
                    print(f">>> REC START : {self.current_filename}")
                    self.start_time = time.time()
                    
                    # On enregistre jusqu'à la prochaine heure pleine (ou arrêt manuel)
                    # Ex: Si départ 14:32:15, on coupe à 15:00:00
                    next_hour = (now.replace(minute=0, second=0, microsecond=0) + 
                               type(now - now)(3600)).timestamp()
                    
                    while self.is_recording and time.time() < next_hour:
                        try:
                            data = self.q.get(timeout=1)
                            file.write(data)
                        except queue.Empty:
                            continue
            except Exception as e:
                print(f"!!! ERREUR ECRITURE FLAC: {e}")
                time.sleep(1)

        print(f"Arrêt REC.")
        self.current_filename = None

    def stop_stream(self):
        last_file = self.current_filename
        self.is_recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        return last_file

    def get_audio_data(self):
        if not self.q.empty():
            # On retourne un échantillon pour le VU-mètre sans le consommer (peek)
            # Simplification : on ne fait que vider un peu pour la visu
            try:
                return self.q.queue[-1] 
            except:
                return None
        return None
