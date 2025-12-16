import customtkinter as ctk
import onyx_settings as config

try:
    ctk.deactivate_automatic_dpi_awareness()
except Exception:
    pass

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class StopPopup(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("CONFIRMATION D'ARRÊT")
        self.geometry("400x320")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color=config.COLOR_BG)

        ctk.CTkLabel(self, text="MODE D'ARRÊT", font=("Arial", 14, "bold"), text_color=config.COLOR_TEXT_STD).pack(pady=(25, 15))

        # BOUTON ROUGE FRANC (URGENCE)
        ctk.CTkButton(self, text="ARRÊT IMMÉDIAT", fg_color=config.COLOR_STOP_BTN, height=50, 
                      font=("Arial", 13, "bold"), hover_color="#ff6b6b",
                      command=lambda: self.confirm("now")).pack(pady=5, padx=30, fill="x")

        # BOUTON ORANGE (OPERATIONNEL)
        ctk.CTkButton(self, text="FINIR L'HEURE EN COURS", fg_color=config.COLOR_WARNING, height=50, 
                      font=("Arial", 13, "bold"), text_color="#1e1e1e",
                      command=lambda: self.confirm("hour")).pack(pady=5, padx=30, fill="x")

        ctk.CTkLabel(self, text="", height=10).pack()

        ctk.CTkButton(self, text="ANNULER", fg_color="transparent", border_width=1, border_color=config.COLOR_TEXT_GRAY, 
                      height=40, font=("Arial", 12), text_color=config.COLOR_TEXT_STD, command=self.destroy).pack(pady=15, padx=60, fill="x")

    def confirm(self, mode): 
        self.callback(mode)
        self.destroy()

class OnyxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("--- [GUI] CHARGEMENT INTERFACE PRO DARK V3.2 ---")
        self.title(f"ONYX SYSTEM - {config.APP_VERSION}")
        self.geometry("1400x950")
        self.configure(fg_color=config.COLOR_BG)
        
        # Grille principale
        self.grid_columnconfigure(0, weight=0, minsize=300) # Panneau Gauche un peu plus large
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=280) # Panneau Droite
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize=25) # Footer fin

        # --- PANNEAU GAUCHE (INFO & CONTROLE) ---
        self.frame_left = ctk.CTkFrame(self, corner_radius=0, fg_color=config.COLOR_PANEL)
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        
        # TITRE
        ctk.CTkLabel(self.frame_left, text="ONYX CONTROL", font=("Helvetica", 20, "bold"), text_color=config.COLOR_TEXT_STD).pack(pady=(25, 10))

        # RECAP SETUP (Style "Carte")
        self.frame_recap = ctk.CTkFrame(self.frame_left, fg_color=config.COLOR_ACCENT, corner_radius=4)
        self.frame_recap.pack(padx=15, pady=10, fill="x")
        self.lbl_recap_usb = ctk.CTkLabel(self.frame_recap, text="STOCKAGE : --", font=("Arial", 11), text_color=config.COLOR_TEXT_GRAY)
        self.lbl_recap_usb.pack(fill="x", pady=(5,0))
        self.lbl_recap_mic = ctk.CTkLabel(self.frame_recap, text="ENTRÉE : --", font=("Arial", 11), text_color=config.COLOR_TEXT_GRAY)
        self.lbl_recap_mic.pack(fill="x")
        self.lbl_recap_dur = ctk.CTkLabel(self.frame_recap, text="CYCLE : --", font=("Arial", 11), text_color=config.COLOR_TEXT_GRAY)
        self.lbl_recap_dur.pack(fill="x", pady=(0,5))

        # MONITORING SPL
        self.frame_spl = ctk.CTkFrame(self.frame_left, fg_color=config.COLOR_ACCENT, corner_radius=4)
        self.frame_spl.pack(padx=15, pady=10, fill="x")
        ctk.CTkLabel(self.frame_spl, text="PRESSION ACOUSTIQUE", font=("Arial", 10, "bold"), text_color=config.COLOR_TEXT_GRAY).pack(pady=(8, 0))
        self.lbl_dba = ctk.CTkLabel(self.frame_spl, text="--.- dBA", font=("Helvetica", 36, "bold"), text_color=config.COLOR_ERROR)
        self.lbl_dba.pack(pady=0)
        self.lbl_dbc = ctk.CTkLabel(self.frame_spl, text="--.- dBC", font=("Arial", 14), text_color=config.COLOR_WARNING)
        self.lbl_dbc.pack(pady=(0, 8))

        # ZOOM BASSES
        self.frame_bass = ctk.CTkFrame(self.frame_left, fg_color="#252525", corner_radius=4)
        self.frame_bass.pack(padx=15, pady=5, fill="x")
        ctk.CTkLabel(self.frame_bass, text="BASSES FREQUENCES", font=("Arial", 9, "bold"), text_color=config.COLOR_TEXT_GRAY).pack(pady=(4,2))

        self.frame_bass_grid = ctk.CTkFrame(self.frame_bass, fg_color="transparent")
        self.frame_bass_grid.pack(fill="x", padx=5, pady=2)
        # 63Hz / 80Hz
        self.lbl_63hz = ctk.CTkLabel(self.frame_bass_grid, text="63: --", font=("Consolas", 12), text_color=config.COLOR_TEMP)
        self.lbl_63hz.grid(row=0, column=0, padx=5, sticky="w")
        self.lbl_80hz = ctk.CTkLabel(self.frame_bass_grid, text="80: --", font=("Consolas", 12), text_color=config.COLOR_TEMP)
        self.lbl_80hz.grid(row=0, column=1, padx=5, sticky="e")
        # 100Hz / 125Hz
        self.lbl_100hz = ctk.CTkLabel(self.frame_bass_grid, text="100: --", font=("Consolas", 12), text_color=config.COLOR_TEMP)
        self.lbl_100hz.grid(row=1, column=0, padx=5, sticky="w")
        self.lbl_125hz = ctk.CTkLabel(self.frame_bass_grid, text="125: --", font=("Consolas", 12), text_color=config.COLOR_TEMP)
        self.lbl_125hz.grid(row=1, column=1, padx=5, sticky="e")
        self.frame_bass_grid.grid_columnconfigure(0, weight=1)
        self.frame_bass_grid.grid_columnconfigure(1, weight=1)

        # ETAT SYSTEME & BOUTONS
        self.lbl_rec_status = ctk.CTkLabel(self.frame_left, text="PRÊT", font=("Arial", 12, "bold"), text_color=config.COLOR_TEXT_GRAY)
        self.lbl_rec_status.pack(pady=(20, 5))

        self.btn_stop = ctk.CTkButton(self.frame_left, text="ARRÊTER LA MISSION", fg_color=config.COLOR_STOP_BTN, 
                                      state="disabled", font=("Arial", 13, "bold"), height=45, hover_color="#ff6b6b")
        self.btn_stop.pack(pady=5, padx=20, fill="x")

        self.btn_restart = ctk.CTkButton(self.frame_left, text="RELANCER", fg_color=config.COLOR_SUCCESS, 
                                         font=("Arial", 13, "bold"), height=45, text_color="#1e1e1e") # Texte sombre sur vert
        
        self.lbl_stop_target = ctk.CTkLabel(self.frame_left, text="", font=("Arial", 11), text_color=config.COLOR_WARNING)
        self.lbl_stop_target.pack(pady=(2, 0))

        ctk.CTkLabel(self.frame_left, text="__________________", text_color="#444").pack(pady=10)

        # METEO
        self.lbl_temp = ctk.CTkLabel(self.frame_left, text="--°C", font=("Arial", 28), text_color=config.COLOR_TEXT_STD)
        self.lbl_temp.pack(pady=0)
        
        self.frame_w_det = ctk.CTkFrame(self.frame_left, fg_color="transparent")
        self.frame_w_det.pack(fill="x")
        self.lbl_hum = ctk.CTkLabel(self.frame_w_det, text="Hum: --%", font=("Arial", 12), text_color=config.COLOR_TEXT_GRAY)
        self.lbl_hum.pack()
        self.lbl_wind = ctk.CTkLabel(self.frame_w_det, text="Vent: --", font=("Arial", 12), text_color=config.COLOR_TEXT_GRAY)
        self.lbl_wind.pack()
        self.lbl_rain = ctk.CTkLabel(self.frame_w_det, text="Pluie: --", font=("Arial", 12), text_color=config.COLOR_TEMP)
        self.lbl_rain.pack()
        self.lbl_pressure = ctk.CTkLabel(self.frame_w_det, text="Pres: --", font=("Arial", 12), text_color="#666")
        self.lbl_pressure.pack()
        
        self.lbl_weather_time = ctk.CTkLabel(self.frame_left, text="MAJ: --:--", font=("Arial", 9), text_color="#555")
        self.lbl_weather_time.pack(pady=5)

        # ETAT REW (Sans icône, texte pur)
        self.lbl_rew_state = ctk.CTkLabel(self.frame_left, text="REW NON DÉTECTÉ", font=("Arial", 10, "bold"), text_color=config.COLOR_ERROR)
        self.lbl_rew_state.pack(pady=(15, 0))

        self.btn_open_rew = ctk.CTkButton(self.frame_left, text="Lancer REW", fg_color="#333", 
                                          font=("Arial", 11), height=25, hover_color="#444")
        self.btn_open_rew.pack(pady=(5, 10), padx=40, fill="x")


        # --- CENTRE (VISUALISATION DONNEES) ---
        self.frame_center = ctk.CTkFrame(self, fg_color=config.COLOR_BG)
        self.frame_center.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.frame_center.grid_columnconfigure(0, weight=1) 
        # Configuration des lignes faite dynamiquement dans show_live_screen

        # --- DROITE (FLAGS) ---
        self.frame_right = ctk.CTkFrame(self, corner_radius=0, fg_color=config.COLOR_PANEL)
        self.frame_right.grid(row=0, column=2, sticky="nsew")
        
        ctk.CTkLabel(self.frame_right, text="MARQUEURS", font=("Helvetica", 14, "bold"), text_color=config.COLOR_TEXT_STD).pack(pady=(30, 20))

        self.event_buttons = {} 
        # Génération des boutons sans icônes
        for btn_text, _ in config.BUTTONS_LAYOUT:
            btn = ctk.CTkButton(self.frame_right, text=btn_text, 
                                fg_color=config.COLOR_ACCENT, 
                                hover_color=config.COLOR_HOVER, 
                                height=45, 
                                font=("Arial", 13), 
                                state="disabled")
            btn.pack(pady=8, padx=20, fill="x")
            self.event_buttons[btn_text] = btn


        # --- FOOTER (BARRE D'ETAT) ---
        self.frame_footer = ctk.CTkFrame(self, height=25, corner_radius=0, fg_color="#181818")
        self.frame_footer.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.lbl_footer_info = ctk.CTkLabel(self.frame_footer, text="Initialisation...", font=("Menlo", 10), text_color="#777")
        self.lbl_footer_info.pack(side="left", padx=15)

    def show_setup_screen(self, drives, mics, callback_launch):
        self.setup_frame = ctk.CTkFrame(self.frame_center, fg_color=config.COLOR_PANEL, corner_radius=8, border_width=1, border_color="#333")
        self.setup_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.6)
        
        ctk.CTkLabel(self.setup_frame, text="CONFIGURATION MISSION", font=("Helvetica", 18, "bold"), text_color=config.COLOR_TEXT_STD).pack(pady=(30, 20))
        
        # Style des options
        def lbl(t): ctk.CTkLabel(self.setup_frame, text=t, font=("Arial", 12), text_color=config.COLOR_TEXT_GRAY).pack(pady=(10, 2))
        
        lbl("Disque de Destination")
        self.combo_usb = ctk.CTkComboBox(self.setup_frame, values=drives, width=300, fg_color=config.COLOR_ACCENT, border_color="#444")
        self.combo_usb.pack()
        
        lbl("Entrée Audio")
        self.combo_mic = ctk.CTkComboBox(self.setup_frame, values=mics, width=300, fg_color=config.COLOR_ACCENT, border_color="#444")
        self.combo_mic.pack()
        
        lbl("Coordonnées GPS")
        self.entry_setup_gps = ctk.CTkEntry(self.setup_frame, placeholder_text="lat, lon", width=300, fg_color=config.COLOR_ACCENT, border_color="#444")
        self.entry_setup_gps.pack()
        self.entry_setup_gps.insert(0, "45.68039, 6.40926")
        
        lbl("Durée de surveillance")
        self.combo_dur = ctk.CTkComboBox(self.setup_frame, values=["Continu", "24 Heures"], width=300, fg_color=config.COLOR_ACCENT, border_color="#444")
        self.combo_dur.pack()

        self.btn_launch = ctk.CTkButton(self.setup_frame, text="DÉMARRER LE SYSTÈME", font=("Arial", 14, "bold"), 
                                        fg_color=config.COLOR_SUCCESS, text_color="#1e1e1e", height=50, width=300,
                                        command=self.on_launch_click)
        self.btn_launch.pack(pady=35)
        
        self.callback_launch_ref = callback_launch

    def on_launch_click(self):
        if self.callback_launch_ref: self.callback_launch_ref()

    def show_live_screen(self):
        self.setup_frame.destroy()
        
        # Division de l'écran central en 3 blocs horizontaux
        self.frame_center.grid_rowconfigure(0, weight=1) # REW
        self.frame_center.grid_rowconfigure(1, weight=1) # FLAC
        self.frame_center.grid_rowconfigure(2, weight=1) # LOGS

        # 1. REW LOGS
        self.frame_rew = ctk.CTkFrame(self.frame_center, fg_color="#121212", corner_radius=0, border_width=1, border_color="#222")
        self.frame_rew.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        ctk.CTkLabel(self.frame_rew, text="FLUX ACOUSTIQUE (REW)", text_color="#555", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=(5,0))
        self.log_rew = ctk.CTkTextbox(self.frame_rew, fg_color="transparent", text_color=config.COLOR_SUCCESS, font=("Menlo", 11), activate_scrollbars=False)
        self.log_rew.pack(fill="both", expand=True, padx=5, pady=5)

        # 2. FLAC LOGS
        self.frame_flac = ctk.CTkFrame(self.frame_center, fg_color="#121212", corner_radius=0, border_width=1, border_color="#222")
        self.frame_flac.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        
        # Header FLAC avec nom du fichier
        h = ctk.CTkFrame(self.frame_flac, fg_color="transparent", height=20)
        h.pack(fill="x", padx=10, pady=(5,0))
        ctk.CTkLabel(h, text="MOTEUR AUDIO (FLAC)", text_color="#555", font=("Arial", 9, "bold")).pack(side="left")
        self.lbl_current_file = ctk.CTkLabel(h, text="En attente...", text_color=config.COLOR_TEMP, font=("Arial", 10))
        self.lbl_current_file.pack(side="right")
        
        self.log_flac = ctk.CTkTextbox(self.frame_flac, fg_color="transparent", text_color=config.COLOR_TEMP, font=("Menlo", 11))
        self.log_flac.pack(fill="both", expand=True, padx=5, pady=5)

        # 3. NOTES LOGS
        self.frame_notes = ctk.CTkFrame(self.frame_center, fg_color="#121212", corner_radius=0, border_width=1, border_color="#222")
        self.frame_notes.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        ctk.CTkLabel(self.frame_notes, text="HISTORIQUE ÉVÉNEMENTS", text_color="#555", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=(5,0))
        self.log_notes = ctk.CTkTextbox(self.frame_notes, fg_color="transparent", text_color=config.COLOR_TEXT_STD, font=("Menlo", 11))
        self.log_notes.pack(fill="both", expand=True, padx=5, pady=5)

        # Activation des boutons
        for btn in self.event_buttons.values(): btn.configure(state="normal")

    def set_recap(self, usb, mic, dur):
        self.lbl_recap_usb.configure(text=f"STOCKAGE : {usb}")
        self.lbl_recap_mic.configure(text=f"ENTRÉE : {mic}")
        self.lbl_recap_dur.configure(text=f"CYCLE : {dur}")

    def write_rew(self, txt): self.log_rew.insert("end", txt + "\n"); self.log_rew.see("end")
    def write_flac(self, txt): self.log_flac.insert("end", txt + "\n"); self.log_flac.see("end")
    def write_note(self, txt): self.log_notes.insert("end", txt + "\n"); self.log_notes.see("end")

if __name__ == "__main__":
    app = OnyxApp()
    app.mainloop()
