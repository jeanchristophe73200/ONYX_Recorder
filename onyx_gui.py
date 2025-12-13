import customtkinter as ctk
import onyx_settings as config

# --- VERSION V2.08 : INTERFACE + FREQUENCES ---
try:
    ctk.deactivate_automatic_dpi_awareness()
except Exception:
    pass
# ----------------------------------------------

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class StopPopup(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("ARRÊT MISSION")
        self.geometry("400x320")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text="CHOISIR LE TYPE D'ARRÊT", font=("Arial", 16, "bold")).pack(pady=(20, 15))

        ctk.CTkButton(self, text="ARRÊT IMMÉDIAT", fg_color=config.COLOR_ERROR, height=45, 
                      font=("Arial", 13, "bold"), command=lambda: self.confirm("now")).pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(self, text="ARRÊT HEURE PLEINE", fg_color=config.COLOR_WARNING, height=45, 
                      font=("Arial", 13, "bold"), command=lambda: self.confirm("hour")).pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self, text="", height=15).pack()

        ctk.CTkButton(self, text="RETOUR / ANNULER", fg_color="transparent", border_width=2, border_color="gray", 
                      height=50, font=("Arial", 14), text_color="white", command=self.destroy).pack(pady=10, padx=30, fill="x")

    def confirm(self, mode): 
        self.callback(mode)
        self.destroy()

class OnyxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("--- [LOG GUI] Démarrage Interface V2.08 ---")
        self.title(f"ONYX - {config.APP_VERSION}")
        self.geometry("1400x950") # Un peu plus haut pour les fréquences
        self.configure(fg_color=config.COLOR_BG)
        self.grid_columnconfigure(0, weight=0, minsize=280)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=260)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize=30)

        # GAUCHE
        self.frame_left = ctk.CTkFrame(self, corner_radius=0, fg_color=config.COLOR_PANEL)
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.frame_left, text="ONYX SYSTEM", font=("Roboto Medium", 22, "bold")).pack(pady=(20, 5))

        self.frame_recap = ctk.CTkFrame(self.frame_left, fg_color="#222")
        self.frame_recap.pack(padx=10, pady=5, fill="x")
        self.lbl_recap_usb = ctk.CTkLabel(self.frame_recap, text="USB: --", font=("Arial", 11), text_color="gray")
        self.lbl_recap_usb.pack(fill="x")
        self.lbl_recap_mic = ctk.CTkLabel(self.frame_recap, text="MIC: --", font=("Arial", 11), text_color="gray")
        self.lbl_recap_mic.pack(fill="x")
        self.lbl_recap_dur = ctk.CTkLabel(self.frame_recap, text="MODE: --", font=("Arial", 11), text_color="gray")
        self.lbl_recap_dur.pack(fill="x")

        # ZONE SPL (dBA / dBC)
        self.frame_spl = ctk.CTkFrame(self.frame_left, fg_color="#222", corner_radius=6)
        self.frame_spl.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(self.frame_spl, text="MONITEUR SPL (REW)", font=("Arial", 11, "bold"), text_color="gray").pack(pady=(5, 0))
        self.lbl_dba = ctk.CTkLabel(self.frame_spl, text="--.- dBA", font=("DSA", 32, "bold"), text_color="#ff4444")
        self.lbl_dba.pack(pady=2)
        self.lbl_dbc = ctk.CTkLabel(self.frame_spl, text="--.- dBC", font=("Arial", 16), text_color="#ffbb33")
        self.lbl_dbc.pack(pady=(0, 5))

        # --- NOUVEAU : ZOOM BASSES FRÉQUENCES ---
        self.frame_bass = ctk.CTkFrame(self.frame_left, fg_color="#1a1a1a", corner_radius=6)
        self.frame_bass.pack(padx=10, pady=(0, 10), fill="x")
        ctk.CTkLabel(self.frame_bass, text="BASSES (dB)", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(2,2))

        # Grille 2x2 pour 63, 80, 100, 125 Hz
        self.frame_bass_grid = ctk.CTkFrame(self.frame_bass, fg_color="transparent")
        self.frame_bass_grid.pack(fill="x", padx=5, pady=2)

        self.lbl_63hz = ctk.CTkLabel(self.frame_bass_grid, text="63Hz: --", font=("Consolas", 12), text_color="#33b5e5")
        self.lbl_63hz.grid(row=0, column=0, padx=5, pady=1, sticky="w")
        self.lbl_80hz = ctk.CTkLabel(self.frame_bass_grid, text="80Hz: --", font=("Consolas", 12), text_color="#33b5e5")
        self.lbl_80hz.grid(row=0, column=1, padx=5, pady=1, sticky="e")
        self.lbl_100hz = ctk.CTkLabel(self.frame_bass_grid, text="100Hz: --", font=("Consolas", 12), text_color="#33b5e5")
        self.lbl_100hz.grid(row=1, column=0, padx=5, pady=1, sticky="w")
        self.lbl_125hz = ctk.CTkLabel(self.frame_bass_grid, text="125Hz: --", font=("Consolas", 12), text_color="#33b5e5")
        self.lbl_125hz.grid(row=1, column=1, padx=5, pady=1, sticky="e")

        self.frame_bass_grid.grid_columnconfigure(0, weight=1)
        self.frame_bass_grid.grid_columnconfigure(1, weight=1)
        # ----------------------------------------

        # STATUS REC
        self.lbl_rec_status = ctk.CTkLabel(self.frame_left, text="", font=("Arial", 12, "bold"), text_color="gray")
        self.lbl_rec_status.pack(pady=(5, 0))

        # BOUTONS
        self.btn_stop = ctk.CTkButton(self.frame_left, text="⏹ STOP", fg_color=config.COLOR_STOP_BTN, state="disabled", font=("Arial", 14, "bold"), height=45)
        self.btn_stop.pack(pady=(5, 5), padx=20, fill="x")
        self.btn_restart = ctk.CTkButton(self.frame_left, text="🔄 RELANCER UN CYCLE", fg_color="#2ecc71", font=("Arial", 14, "bold"), height=45)
        self.lbl_stop_target = ctk.CTkLabel(self.frame_left, text="", font=("Arial", 11), text_color="orange")
        self.lbl_stop_target.pack(pady=(5, 0))

        ctk.CTkLabel(self.frame_left, text="__________________", text_color="gray").pack(pady=5)

        # MÉTÉO
        self.lbl_temp = ctk.CTkLabel(self.frame_left, text="--.- °C", font=("Arial", 26, "bold"), text_color=config.COLOR_TEMP)
        self.lbl_temp.pack(pady=2)
        self.lbl_rain = ctk.CTkLabel(self.frame_left, text="Pluie: --", font=("Arial", 14, "bold"), text_color="#33b5e5")
        self.lbl_rain.pack(pady=2)
        self.frame_w_det = ctk.CTkFrame(self.frame_left, fg_color="transparent")
        self.frame_w_det.pack(fill="x")
        self.lbl_hum = ctk.CTkLabel(self.frame_w_det, text="Hum: -- %", font=("Arial", 12), text_color=config.COLOR_HUM)
        self.lbl_hum.pack()
        self.lbl_wind = ctk.CTkLabel(self.frame_w_det, text="Vent: -- km/h", font=("Arial", 12), text_color=config.COLOR_WIND)
        self.lbl_wind.pack()
        self.lbl_pressure = ctk.CTkLabel(self.frame_w_det, text="Pres: ---- hPa", font=("Arial", 12), text_color="gray")
        self.lbl_pressure.pack()
        self.lbl_weather_time = ctk.CTkLabel(self.frame_left, text="MAJ: --:--", font=("Arial", 10), text_color="gray")
        self.lbl_weather_time.pack(pady=5)

        # REW ET VU-METRE
        self.lbl_rew_state = ctk.CTkLabel(self.frame_left, text="🔴 REW OFF", font=("Arial", 12, "bold"), text_color="red", fg_color="#222", corner_radius=5)
        self.lbl_rew_state.pack(pady=(10, 0), padx=20, fill="x")

        self.lbl_vu = ctk.CTkLabel(self.frame_left, text="NIVEAU MICRO (FLAC)", font=("Arial", 9, "bold"), text_color="gray")
        self.lbl_vu.pack(pady=(5, 0))
        self.bar_vu = ctk.CTkProgressBar(self.frame_left, height=12, progress_color="#2ecc71")
        self.bar_vu.pack(pady=(2, 10), padx=20, fill="x")
        self.bar_vu.set(0)

        self.btn_open_rew = ctk.CTkButton(self.frame_left, text="🚀 Démarrer REW", fg_color="#555", font=("Arial", 12), height=30)
        self.btn_open_rew.pack(pady=(0, 10), padx=20, fill="x")

        # CENTRE & DROITE
        self.frame_center = ctk.CTkFrame(self, fg_color=config.COLOR_BG)
        self.frame_center.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.frame_center.grid_columnconfigure(0, weight=1) 

        self.frame_right = ctk.CTkFrame(self, corner_radius=0, fg_color=config.COLOR_PANEL)
        self.frame_right.grid(row=0, column=2, sticky="nsew")
        ctk.CTkLabel(self.frame_right, text="MARQUEURS", font=("Roboto Medium", 16)).pack(pady=20)

        self.event_buttons = {} 
        for btn_text, btn_icon in config.BUTTONS_LAYOUT:
            btn = ctk.CTkButton(self.frame_right, text=f"{btn_icon}  {btn_text}", fg_color=config.COLOR_ACCENT, hover_color=config.COLOR_HOVER, height=40, anchor="w", state="disabled")
            btn.pack(pady=4, padx=20, fill="x")
            self.event_buttons[btn_text] = btn

        self.btn_correction = ctk.CTkButton(self.frame_right, text=f"↩ {config.BTN_CORRECTION}", fg_color="#555", height=40, state="disabled")
        self.btn_correction.pack(pady=10, padx=20, fill="x")

        self.frame_pac = ctk.CTkFrame(self.frame_right, fg_color="transparent")
        self.frame_pac.pack(pady=10, padx=20, fill="x")
        self.btn_pac_on = ctk.CTkButton(self.frame_pac, text=config.BTN_PAC_ON, fg_color="#444", width=90, height=40)
        self.btn_pac_on.pack(side="left", padx=5)
        self.btn_pac_off = ctk.CTkButton(self.frame_pac, text=config.BTN_PAC_OFF, fg_color="#444", width=90, height=40)
        self.btn_pac_off.pack(side="right", padx=5)

        self.btn_ongoing = ctk.CTkButton(self.frame_right, text=config.BTN_ONGOING, fg_color="#555", height=40, state="disabled")
        self.btn_ongoing.pack(pady=(20, 5), padx=20, fill="x")

        # FOOTER
        self.frame_footer = ctk.CTkFrame(self, height=30, corner_radius=0, fg_color="#2e2e2e")
        self.frame_footer.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.lbl_footer_info = ctk.CTkLabel(self.frame_footer, text="Système Prêt.", font=("Consolas", 11), text_color="white")
        self.lbl_footer_info.pack(side="left", padx=20)

    def show_setup_screen(self, drives, mics, callback_launch):
        self.setup_frame = ctk.CTkFrame(self.frame_center, fg_color="#222", corner_radius=10)
        self.setup_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.7)
        ctk.CTkLabel(self.setup_frame, text="CONFIGURATION DU VOL", font=("Roboto", 24, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self.setup_frame, text="1. Disque de Sauvegarde", font=("Arial", 12)).pack(pady=2)
        self.combo_usb = ctk.CTkComboBox(self.setup_frame, values=drives, width=350)
        self.combo_usb.pack(pady=5)
        ctk.CTkLabel(self.setup_frame, text="2. Source Audio (Micro)", font=("Arial", 12)).pack(pady=2)
        self.combo_mic = ctk.CTkComboBox(self.setup_frame, values=mics, width=350)
        self.combo_mic.pack(pady=5)
        ctk.CTkLabel(self.setup_frame, text="3. GPS (Requis)", font=("Arial", 12)).pack(pady=2)
        self.entry_setup_gps = ctk.CTkEntry(self.setup_frame, placeholder_text="ex: 45.680, 6.409", width=350)
        self.entry_setup_gps.pack(pady=5)
        self.entry_setup_gps.insert(0, "45.68039, 6.40926")
        ctk.CTkLabel(self.setup_frame, text="4. Durée", font=("Arial", 12)).pack(pady=2)
        self.combo_dur = ctk.CTkComboBox(self.setup_frame, values=["Continu (Infini)", "24 Heures", "48 Heures"], width=350)
        self.combo_dur.pack(pady=5)

        self.btn_launch = ctk.CTkButton(self.setup_frame, text="✅ START", font=("Arial", 16, "bold"), fg_color="#2ecc71", height=45, command=self.on_launch_click)
        self.btn_launch.pack(pady=30)

        self.lbl_status_setup = ctk.CTkLabel(self.setup_frame, text="", text_color="#ff6b6b")
        self.lbl_status_setup.pack()
        self.callback_launch_ref = callback_launch

    def on_launch_click(self):
        if self.callback_launch_ref: self.callback_launch_ref()

    def show_live_screen(self):
        self.setup_frame.destroy()
        self.frame_center.grid_rowconfigure(0, weight=4) 
        self.frame_center.grid_rowconfigure(1, weight=1) 
        self.frame_center.grid_rowconfigure(2, weight=2) 

        # ZONES
        self.frame_rew = ctk.CTkFrame(self.frame_center, fg_color="#1a1a1a")
        self.frame_rew.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0,5))
        ctk.CTkLabel(self.frame_rew, text="DONNÉES ACOUSTIQUES (REW)", text_color="gray", font=("Arial", 10)).pack(anchor="w", padx=5)
        self.log_rew = ctk.CTkTextbox(self.frame_rew, fg_color="#121212", text_color="#00ff00", font=("Consolas", 12))
        self.log_rew.pack(fill="both", expand=True)

        self.frame_flac = ctk.CTkFrame(self.frame_center, fg_color="#1a1a1a")
        self.frame_flac.grid(row=1, column=0, sticky="nsew", padx=0, pady=5)
        self.frame_flac_head = ctk.CTkFrame(self.frame_flac, fg_color="transparent")
        self.frame_flac_head.pack(fill="x")
        ctk.CTkLabel(self.frame_flac_head, text="ENREGISTREMENT AUDIO (FLAC)", text_color="gray", font=("Arial", 10)).pack(side="left", padx=5)
        self.lbl_current_file = ctk.CTkLabel(self.frame_flac, text="En attente...", text_color="#33b5e5", font=("Arial", 12))
        self.lbl_current_file.pack(anchor="w", padx=10, pady=0)
        self.log_flac = ctk.CTkTextbox(self.frame_flac, fg_color="#121212", text_color="#33b5e5", font=("Consolas", 12))
        self.log_flac.pack(fill="both", expand=True)

        self.frame_notes = ctk.CTkFrame(self.frame_center, fg_color="#1a1a1a")
        self.frame_notes.grid(row=2, column=0, sticky="nsew", padx=0, pady=(5,0))
        ctk.CTkLabel(self.frame_notes, text="JOURNAL D'ÉVÉNEMENTS", text_color="gray", font=("Arial", 10)).pack(anchor="w", padx=5)
        self.log_notes = ctk.CTkTextbox(self.frame_notes, fg_color="#121212", text_color="white", font=("Consolas", 12))
        self.log_notes.pack(fill="both", expand=True)

        for btn in self.event_buttons.values(): btn.configure(state="normal")
        self.btn_ongoing.configure(state="normal")

    def set_recap(self, usb, mic, dur):
        self.lbl_recap_usb.configure(text=f"💾 {usb}")
        self.lbl_recap_mic.configure(text=f"🎤 {mic}")
        self.lbl_recap_dur.configure(text=f"⏱️ {dur}")

    def write_rew(self, txt): self.log_rew.insert("end", txt + "\n"); self.log_rew.see("end")
    def write_flac(self, txt): self.log_flac.insert("end", txt + "\n"); self.log_flac.see("end")
    def write_note(self, txt): self.log_notes.insert("end", txt + "\n"); self.log_notes.see("end")

if __name__ == "__main__":
    app = OnyxApp()
    app.mainloop()
