import tkinter as tk
import numpy as np
import threading
import requests
import csv
import os
import shutil
import time
import sounddevice as sd
import subprocess
import sys
import platform
from datetime import datetime, timedelta

import onyx_gui
import onyx_audio
import onyx_weather
import onyx_rew
import onyx_telegram
import onyx_log 
import onyx_settings as config

# --- ACTIVATION SURVEILLANCE V3.2 (Patch Cosmétique) ---
onyx_log.start_surveillance(config.RECORD_DIR)
# -------------------------------------

MEMORY_FILE = "onyx_memory.txt"
MIN_DISK_SPACE_GB = 5

class OnyxController:
    def __init__(self):
        self.view = onyx_gui.OnyxApp()
        self.view.after(3000, self.minimize_terminal)
        
        self.rew = onyx_rew.RewEngine()
        self.weather = onyx_weather.WeatherEngine()
        self.telegram = onyx_telegram.TelegramEngine(callback_gui=self.trigger_event)
        
        self.usb_drives = self.scan_usb()
        self.mics = self.scan_mics()
        
        self.view.btn_open_rew.configure(command=self.open_rew_app)
        self.view.show_setup_screen(self.usb_drives, self.mics, self.launch_setup)
        try:
            self.view.combo_dur.configure(values=config.DURATIONS)
        except: pass

        self.load_usb_memory()
        
        self.setup_running = True
        threading.Thread(target=self.monitor_rew_startup, daemon=True).start()
        
        self.weather_count = 0
        self.last_event_time = 0
        self.stop_target_time = None
        self.stop_mode = None
        self.running = False
        self.waiting_start = False 
        
        self.view.mainloop()

    def minimize_terminal(self):
        try:
            subprocess.Popen("osascript -e 'tell application \"Terminal\" to set miniaturized of window 1 to true'", shell=True)
        except: pass

    def restore_terminal(self):
        try:
            subprocess.Popen("osascript -e 'tell application \"Terminal\" to set miniaturized of window 1 to false'", shell=True)
        except: pass

    def monitor_rew_startup(self):
        while self.setup_running:
            d = self.rew.get_full_data()
            if d and d['dba'] > 1.0:
                self.view.after(0, lambda: self.view.lbl_rew_state.configure(text="REW CONNECTÉ", text_color=config.COLOR_SUCCESS))
            else:
                self.view.after(0, lambda: self.view.lbl_rew_state.configure(text="REW DÉCONNECTÉ", text_color=config.COLOR_ERROR))
            time.sleep(1.0)

    def launch_setup(self):
        self.setup_running = False
        sel_usb = self.view.combo_usb.get()
        sel_mic = self.view.combo_mic.get()
        sel_dur = self.view.combo_dur.get()
        sel_gps = self.view.entry_setup_gps.get()

        self.save_usb_memory(sel_usb)

        if len(sel_gps) < 5: return 
        if "," in sel_gps:
            pts = sel_gps.split(",")
            self.weather.update_coords(pts[0], pts[1])

        config.USB_PATH = sel_usb if "Disque Local" not in sel_usb else ""
        try: 
            config.AUDIO_DEVICE_INDEX = int(sel_mic.split(":")[0])
            config.AUDIO_DEVICE_NAME = sel_mic
        except: 
            config.AUDIO_DEVICE_INDEX = 0
            config.AUDIO_DEVICE_NAME = "Unknown"
        
        if "Continu" in sel_dur:
            config.DURATION_MODE = "continu"
            self.target_start_time = datetime.now()
        else:
            hours = int(sel_dur.replace("h", ""))
            if "24" in sel_dur: config.DURATION_MODE = "24h"
            elif "48" in sel_dur: config.DURATION_MODE = "48h"
            elif "72" in sel_dur: config.DURATION_MODE = "72h"
            
            now = datetime.now()
            today_07 = now.replace(hour=7, minute=0, second=0, microsecond=0)
            today_22 = now.replace(hour=22, minute=0, second=0, microsecond=0)
            
            if now < today_07: self.target_start_time = today_07
            elif now < today_22: self.target_start_time = today_22
            else: self.target_start_time = today_07 + timedelta(days=1)

        self.view.show_live_screen()
        self.view.set_recap(
            "Local" if not config.USB_PATH else os.path.basename(config.USB_PATH),
            config.AUDIO_DEVICE_NAME,
            config.DURATION_MODE
        )
        
        if (self.target_start_time - datetime.now()).total_seconds() < 10:
            self.start_cascade_sequence()
        else:
            self.waiting_start = True
            self.view.lbl_rec_status.configure(text="ATTENTE LANCEMENT...", text_color=config.COLOR_WARNING)
            self.view.btn_stop.configure(text="ANNULER LANCEMENT", fg_color=config.COLOR_WARNING, state="normal", command=self.cancel_start)
            self.view.btn_open_rew.configure(state="normal")
            self.start_countdown_loop()

    def start_countdown_loop(self):
        if self.waiting_start:
            now = datetime.now()
            remaining = self.target_start_time - now
            if remaining.total_seconds() <= 0:
                self.waiting_start = False
                self.start_cascade_sequence()
            else:
                rem_str = str(remaining).split('.')[0]
                self.view.lbl_rec_status.configure(text=f"LANCEMENT DANS : {rem_str}", text_color=config.COLOR_TEMP)
                self.view.after(1000, self.start_countdown_loop)

    def cancel_start(self):
        self.waiting_start = False
        self.view.destroy()

    def offload_file_worker(self, filepath):
        filename = os.path.basename(filepath)
        if config.USB_PATH and os.path.exists(config.USB_PATH):
            usb_dir = os.path.join(config.USB_PATH, "Sauvegardes_ONYX")
            if not os.path.exists(usb_dir): os.makedirs(usb_dir)
            dest_path = os.path.join(usb_dir, filename)
            self.view.after(0, lambda: self.view.write_flac(f"[USB] DEPLACEMENT EN COURS : {filename}"))
            try:
                shutil.move(filepath, dest_path)
                self.view.after(0, lambda: self.view.write_flac(f"[OK] DELESTAGE REUSSI : {filename}"))
            except Exception as e:
                self.view.after(0, lambda: self.view.write_flac(f"[ERREUR] ECHEC COPIE : {e}"))
        else:
            self.view.after(0, lambda: self.view.write_flac(f"[INFO] STOCKAGE LOCAL : {filename}"))

    def on_audio_file_completed(self, filepath):
        threading.Thread(target=self.offload_file_worker, args=(filepath,), daemon=True).start()

    def start_cascade_sequence(self):
        self.view.btn_stop.configure(command=self.open_stop_popup, state="normal", text="ARRÊTER LA MISSION", fg_color=config.COLOR_STOP_BTN)
        if config.DURATION_MODE != "continu":
            hours = int(config.DURATION_MODE.replace("h", ""))
            self.stop_target_time = datetime.now() + timedelta(hours=hours)
            self.stop_mode = f"FIN {hours}H"
        
        # CONFIGURATION DES 4 FLAGS
        for t, i in config.BUTTONS_LAYOUT:
            if t in self.view.event_buttons:
                # i est vide maintenant, on envoie juste le texte
                self.view.event_buttons[t].configure(command=lambda m=f"{t}": self.trigger_event(m))
        
        self.view.btn_restart.configure(command=self.restart_system)
        
        self.telegram.update_keyboard()
        self.telegram.start_listening()
        
        self.view.lbl_rec_status.configure(text="[1/3] VÉRIFICATION SYSTÈME...", text_color=config.COLOR_WARNING)
        self.model = onyx_audio.AudioEngine(callback_file_completed=self.on_audio_file_completed)
        
        try:
            total, used, free = shutil.disk_usage(config.RECORD_DIR)
            free_gb = free / (1024**3)
            if free_gb < MIN_DISK_SPACE_GB:
                self.view.lbl_rec_status.configure(text=f"[ERREUR] ESPACE DISQUE FAIBLE ({free_gb:.1f} Go)", text_color=config.COLOR_ERROR)
                return
        except: pass

        self.view.after(1500, self.cascade_startup_2)

    def cascade_startup_2(self):
        self.view.lbl_rec_status.configure(text="[2/3] RADAR MÉTÉO...", text_color=config.COLOR_TEMP)
        self.weather.start_monitoring()
        self.view.after(1500, self.cascade_startup_3)

    def cascade_startup_3(self):
        self.view.lbl_rec_status.configure(text="[3/3] MOTEUR AUDIO...", text_color=config.COLOR_WARNING)
        
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_file = f"{config.RECORD_DIR}/enrg_{now_str}.csv"
        self.init_csv()
        
        self.model.start_stream()
        self.model.start_recording()
        self.mission_start_time = time.time()
        
        self.running = True 
        
        self.update_rew_display()
        self.update_weather_loop()
        self.update_footer_loop()
        self.heartbeat_loop()
        
        threading.Thread(target=self.data_logger_loop, daemon=True).start()
        
        start_msg = f"DÉMARRAGE SYSTÈME - {datetime.now().strftime('%H:%M:%S')}"
        self.view.write_flac(start_msg)
        
        # CORRECTION DU DOUBLON : On retire les préfixes "Hum:", "Vent:", etc.
        w = self.weather.get_data()
        w_msg = f"MÉTÉO DÉPART: {w['temp']} | {w['hum']} | {w['wind']} | {w['press']}"
        self.view.write_flac(w_msg)

        self.view.lbl_rec_status.configure(text="ENREGISTREMENT ACTIF", text_color=config.COLOR_ERROR)

    def start_stop_sequence(self):
        self.running = False 
        self.view.lbl_rec_status.configure(text="[1/3] STABILISATION...", text_color=config.COLOR_WARNING)
        self.view.after(1500, self.stop_cascade_2)

    def stop_cascade_2(self):
        self.view.lbl_rec_status.configure(text="[2/3] FINALISATION AUDIO...", text_color=config.COLOR_WARNING)
        self.model.stop_stream()
        
        # CORRECTION DU DOUBLON : On retire les préfixes ici aussi
        w = self.weather.get_data()
        w_msg = f"MÉTÉO ARRIVÉE: {w['temp']} | {w['hum']} | {w['wind']} | {w['press']}"
        self.view.write_flac(w_msg)
        
        et = datetime.now().strftime('%H:%M:%S')
        self.view.write_rew(f"--- FIN MONITORING : {et} ---")
        self.view.write_note(f"--- CLOTURE JOURNAL : {et} ---")
        
        self.view.after(1500, self.stop_cascade_3)

    def stop_cascade_3(self):
        self.view.lbl_rec_status.configure(text="[3/3] SÉCURISATION USB...", text_color=config.COLOR_TEMP)
        self.view.update()
        
        if config.USB_PATH and os.path.exists(config.USB_PATH):
            try:
                td = os.path.join(config.USB_PATH, "Sauvegardes_ONYX")
                if not os.path.exists(td): os.makedirs(td)
                shutil.copy2(self.csv_file, os.path.join(td, os.path.basename(self.csv_file)))
                self.view.write_rew("[OK] CSV COPIÉ SUR USB")
            except Exception as e: 
                self.view.write_rew(f"[ERREUR] USB: {e}")
            
        et = datetime.now().strftime('%H:%M:%S')
        self.telegram.send_message(f"[STOP] MISSION STOPPÉE À {et}")
        self.telegram.stop()
        
        self.view.lbl_rec_status.configure(text="CYCLE TERMINÉ", text_color="gray")
        self.view.btn_stop.configure(text="FERMER ONYX", command=self.on_close, fg_color=config.COLOR_ERROR)
        self.view.btn_restart.pack(pady=5, padx=20, fill="x")

    def heartbeat_loop(self):
        if self.running:
            current = self.view.lbl_rec_status.cget("text_color")
            # Clignotement Rouge Vif / Rouge Sombre
            nex = config.COLOR_ERROR if current != config.COLOR_ERROR else "#880000"
            if "ACTIF" in self.view.lbl_rec_status.cget("text"):
                self.view.lbl_rec_status.configure(text_color=nex)
            self.view.after(1000, self.heartbeat_loop)

    def update_footer_loop(self):
        if self.running:
            el = int(time.time() - self.mission_start_time)
            h, r = divmod(el, 3600); m, s = divmod(r, 60)
            dur = f"{h:02}h {m:02}m {s:02}s"
            usb = f"USB: {os.path.basename(config.USB_PATH)}" if config.USB_PATH else "LOCAL"
            self.view.lbl_footer_info.configure(text=f"{usb} | {config.AUDIO_DEVICE_NAME} | DURÉE: {dur}")
            if self.stop_target_time:
                rem = self.stop_target_time - datetime.now()
                if rem.total_seconds() > 0:
                    rem_str = str(rem).split('.')[0]
                    self.view.lbl_rec_status.configure(text=f"ARRÊT AUTO ({self.stop_mode}): {rem_str}", text_color=config.COLOR_WARNING)
                else:
                    self.start_stop_sequence()
            self.view.after(1000, self.update_footer_loop)

    def load_usb_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    last = f.read().strip()
                if last in self.usb_drives:
                    self.view.combo_usb.set(last)
            except: pass

    def save_usb_memory(self, usb):
        try:
            with open(MEMORY_FILE, "w") as f: f.write(usb)
        except: pass

    def scan_usb(self):
        drives = ["Disque Local"]
        if os.path.exists("/Volumes"):
            for d in os.listdir("/Volumes"):
                if d not in ["Macintosh HD", "com.apple.TimeMachine.localsnapshots"] and not d.startswith("."):
                    drives.insert(0, os.path.join("/Volumes", d))
        return drives

    def scan_mics(self):
        devs = []
        try:
            for i, d in enumerate(sd.query_devices()):
                if d['max_input_channels'] > 0: devs.append(f"{i}: {d['name']}")
        except: pass
        return devs

    def open_rew_app(self):
        apps = ["REW", "Roomeqwizard", "Room EQ Wizard"]
        for a in apps:
            try: subprocess.run(["open", "-a", a]); return
            except: pass

    def restart_system(self):
        self.view.btn_restart.pack_forget()
        self.view.btn_stop.configure(state="normal", text="ARRÊTER LA MISSION", command=self.open_stop_popup, fg_color=config.COLOR_STOP_BTN)
        self.view.lbl_rec_status.configure(text="REDÉMARRAGE...", text_color=config.COLOR_WARNING)
        self.start_cascade_sequence()

    def open_stop_popup(self):
        onyx_gui.StopPopup(self.view, self.handle_stop_choice)

    def handle_stop_choice(self, mode):
        if mode == "now": 
            self.start_stop_sequence()
        elif mode == "hour":
            start_ts = self.mission_start_time
            now_ts = time.time()
            elapsed = now_ts - start_ts
            next_hour_cycle = (int(elapsed // 3600) + 1) * 3600
            target_ts = start_ts + next_hour_cycle
            self.stop_target_time = datetime.fromtimestamp(target_ts)
            rem_minutes = int((target_ts - now_ts) / 60)
            self.stop_mode = "HEURE PLEINE"
            self.view.lbl_rec_status.configure(text=f"ARRÊT PRÉVU: DANS {rem_minutes} MIN (HEURE PLEINE)", text_color=config.COLOR_WARNING)

    def init_csv(self):
        cols = ["ts", "h", "dBA", "dBC"] + [f"{f}Hz" for f in config.FREQS] + ["tmp", "hum", "vent", "pres", "pluie", "note", "Audio_Ref"]
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([f"# ONYX V3.2 | MACHINE: {platform.node()} | DATE: {datetime.now()}"])
                writer.writerow(cols)

    def data_logger_loop(self):
        while self.running:
            st = time.time()
            now = datetime.now()
            rew = self.rew.get_full_data()
            if rew is None: rew = {"dba": 0, "dbc": 0, "spectrum": {}}
            w = self.weather.get_data()
            t = w['temp'].replace(" °C", "C")
            
            spec = rew.get('spectrum', {})
            def g(k): return str(spec.get(k, '--')).split('.')[0]
            
            log_msg = (f"{now.strftime('%H:%M:%S')}   "
                       f"A: {rew['dba']:.1f}   C: {rew['dbc']:.1f}   |   "
                       f"63Hz: {g('63'):<3}   80Hz: {g('80'):<3}   100Hz: {g('100'):<3}   125Hz: {g('125'):<3}   |   "
                       f"T: {t}")
            
            if self.running: self.view.after(0, lambda: self.view.write_rew(log_msg))

            current_audio_path = self.model.current_filename
            if current_audio_path:
                short = os.path.basename(current_audio_path)
                self.view.lbl_current_file.configure(text=f"Fichier : {short}")
            else:
                short = "Buffer..."

            row = [f"{now.timestamp():.3f}", now.strftime("%H:%M:%S"), 
                   f"{rew['dba']:.1f}".replace('.',','), f"{rew['dbc']:.1f}".replace('.',',')]
            for f in config.FREQS: row.append(f"{rew['spectrum'].get(f, '')}".replace('.',','))
            
            row.append(w['temp'].replace(" °C", ""))
            row.append(w['hum'].replace("Hum: ", "").replace(" %", ""))
            row.append(w['wind'].replace("Vent: ", "").replace(" km/h", ""))
            row.append(w['press'].replace("Pres: ", "").replace(" hPa", ""))
            row.append(w.get('rain', "0").replace("Pluie: ", "").replace(" mm", ""))
            
            note = getattr(self, 'current_note', "")
            row.append(note)
            if note: self.current_note = ""
            
            row.append(short)
            
            try:
                with open(self.csv_file, 'a', newline='', encoding='utf-8-sig') as f:
                    csv.writer(f, delimiter=';').writerow(row)
            except: pass
            
            if config.USB_PATH and now.minute==0 and now.second<5 and getattr(self, 'last_bu', -1)!=now.hour:
                try: 
                    td = os.path.join(config.USB_PATH, "Sauvegardes_ONYX")
                    if not os.path.exists(td): os.makedirs(td)
                    shutil.copy2(self.csv_file, os.path.join(td, os.path.basename(self.csv_file)))
                    self.view.after(0, lambda: self.view.write_rew("[BACKUP] SAUVEGARDE CSV USB OK"))
                except: pass
                self.last_bu = now.hour
            time.sleep(max(0, 3.0 - (time.time() - st)))

    def update_rew_display(self):
        d = self.rew.get_full_data()
        if d and d["dba"] > 10:
            self.view.lbl_dba.configure(text=f"{d['dba']:.1f} dBA", text_color=config.COLOR_ERROR)
            self.view.lbl_dbc.configure(text=f"{d['dbc']:.1f} dBC")
            spec = d.get('spectrum', {})
            def get_f(target):
                for k in [target, str(target), f"{target}.0", str(int(target))]:
                    if k in spec and spec[k] != "": return spec[k]
                return "--"
            self.view.lbl_63hz.configure(text=f"63Hz: {get_f(63)} dB")
            self.view.lbl_80hz.configure(text=f"80Hz: {get_f(80)} dB")
            self.view.lbl_100hz.configure(text=f"100Hz: {get_f(100)} dB")
            self.view.lbl_125hz.configure(text=f"125Hz: {get_f(125)} dB")
            self.view.lbl_rew_state.configure(text="REW CONNECTÉ", text_color=config.COLOR_SUCCESS)
        else:
            self.view.lbl_dba.configure(text="NO SIGNAL", text_color=config.COLOR_ERROR)
            self.view.lbl_rew_state.configure(text="REW DÉCONNECTÉ", text_color=config.COLOR_ERROR)
        if self.running: self.view.after(500, self.update_rew_display)

    def update_weather_loop(self):
        d = self.weather.get_data()
        self.weather_count += 1
        self.view.lbl_temp.configure(text=d["temp"])
        try: self.view.lbl_rain.configure(text=d["rain"])
        except: pass
        self.view.lbl_hum.configure(text=d["hum"])
        self.view.lbl_wind.configure(text=d["wind"])
        self.view.lbl_pressure.configure(text=d["press"])
        self.view.lbl_weather_time.configure(text=f"MAJ ({self.weather_count}): {datetime.now().strftime('%H:%M')}")
        if self.running: self.view.after(5000, self.update_weather_loop)
    
    def trigger_event(self, msg, from_telegram=False):
        self.current_note = msg
        self.last_event_time = time.time()
        ts = datetime.now().strftime("%H:%M:%S")
        src = "[MOBILE]" if from_telegram else "[SYSTEM]"
        self.view.write_note(f"{ts} {src} | {msg}")
        if not from_telegram: self.telegram.send_message(f"[NOTE] {msg}")
    
    def on_close(self):
        self.setup_running = False 
        self.restore_terminal()
        self.running = False
        self.telegram.stop()
        if hasattr(self, 'model'): self.model.stop_stream()
        self.view.destroy()
        print("--- Fin de session ONYX ---")

if __name__ == "__main__":
    OnyxController()
