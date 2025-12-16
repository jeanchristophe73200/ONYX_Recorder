import os
import platform

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

# --- CONFIGURATION UNIVERSELLE (PUBLIC RELEASE) ---
# Détecte le dossier utilisateur courant (ex: /Users/Jean... ou /Users/Paul...)
USER_HOME = os.path.expanduser("~")
RECORD_DIR = os.path.join(USER_HOME, "ONYX_Records")

if not os.path.exists(RECORD_DIR): os.makedirs(RECORD_DIR)

FREQS = ["20","25","31.5","40","50","63","80","100","125","160","200","250","315","400","500","630","800","1000","1250","1600","2000","2500","3150","4000"]
DURATIONS = ["Continu (Infini)", "Cycle 24 Heures", "Cycle 48 Heures", "Cycle 72 Heures"]

# --- PALETTE macOS DARK PRO (V3.2) ---
COLOR_BG = "#1e1e1e"
COLOR_PANEL = "#2c2c2c"
COLOR_TEXT_STD = "#e0e0e0"
COLOR_TEXT_GRAY = "#a0a0a0"
COLOR_ACCENT = "#3a3a3a"
COLOR_HOVER = "#4a4a4a"
COLOR_SUCCESS = "#32d74b"
COLOR_WARNING = "#ff9f0a"
COLOR_ERROR = "#ff453a"
COLOR_STOP_BTN = "#FF3B30"
COLOR_TEMP = "#e0e0e0"
COLOR_DATA_VAL = "#d0d0d0"

# --- CONFIGURATION FLAGS (SANS ICÔNES) ---
BUTTONS_LAYOUT = [
    ("Source Std", ""),
    ("Source +", ""),
    ("Source -", ""),
    ("Résiduel", "")
]

APP_VERSION = "ONYX V3.2 (Pro Dark UI)"
