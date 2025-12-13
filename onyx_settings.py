import os

# --- VARIABLES DYNAMIQUES ---
USB_PATH = ""
AUDIO_DEVICE_INDEX = 0
AUDIO_DEVICE_NAME = ""
DURATION_MODE = "continu"

# --- CONSTANTES ---
TELEGRAM_TOKEN = "8586948145:AAG4XPgoBdC3OD0XGe0Za8zkPbMbsnqoejY"
TELEGRAM_CHAT_ID = "8522453915"

SAMPLE_RATE = 48000 
CHUNK_SIZE = 1024

# MODIFICATION V2.01 : CHEMIN DU BUFFER LOCAL
RECORD_DIR = "/Users/jeanchristophefinantz/ONYX_Local_Buffer V2"

if not os.path.exists(RECORD_DIR): os.makedirs(RECORD_DIR)

FREQS = ["20","25","31.5","40","50","63","80","100","125","160","200","250","315","400","500","630","800","1000","1250","1600","2000","2500","3150","4000"]

# OPTIONS DE DURÉE (Avec le 72h)
DURATIONS = ["Continu (Infini)", "Cycle 24 Heures", "Cycle 48 Heures", "Cycle 72 Heures"]

COLOR_BG = "#2b2b2b"
COLOR_PANEL = "#363636"
COLOR_TEXT_STD = "#ececec"
COLOR_ACCENT = "#454545"
COLOR_HOVER = "#5a5a5a"
COLOR_SUCCESS = "#1dd1a1"
COLOR_WARNING = "#ffbb33"
COLOR_ERROR = "#ff6b6b"
COLOR_TEMP = "#33b5e5"
COLOR_HUM = "#99cc00"
COLOR_WIND = "#ffbb33"
COLOR_STOP_BTN = "#c0392b"

BUTTONS_LAYOUT = [
    ("Tracteur / Agri", "🚜"), ("Voiture bruyante", "🚗"), ("Moto / Scooter", "🏍️"),
    ("Bruit voisinage", "🔊"), ("Orage / Tonnerre", "⛈️"), ("Pluie Forte", "🌧️"),
    ("Travaux / BTP", "🏗️"), ("Avion de ligne", "✈️"), ("Camion / PL", "🚛"),
    ("Tronçonneuse", "🪚")
]

BTN_CORRECTION = "Correction (-1 min)"
BTN_ONGOING = "Toujours en cours ⏳"
BTN_PAC_ON = "PAC ON 🟢"
BTN_PAC_OFF = "PAC OFF 🔴"

# MISE A JOUR V2.04
APP_VERSION = "ONYX V2.04 (Buffer Active)"
