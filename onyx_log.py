import sys
import os
from datetime import datetime

# PALETTE DE COULEURS (ANSI)
C_RED = "\033[91m"      # Pour les Erreurs / Crashs
C_GREEN = "\033[92m"    # Pour les succès / Démarrages
C_YELLOW = "\033[93m"   # Pour les Avertissements
C_BLUE = "\033[94m"     # Pour les infos Système
C_MAGENTA = "\033[95m"  # Pour l'Interface Graphique (GUI)
C_CYAN = "\033[96m"     # Pour les infos générales
C_RESET = "\033[0m"     # Retour à la normale

class DualLogger:
    """
    Logger Intelligent V2.10 :
    - Écrit en BRUT dans le fichier (pour lecture facile).
    - Écrit en COULEUR dans le terminal (pour monitoring temps réel).
    """
    def __init__(self, filepath, original_stream, is_error_stream=False):
        self.terminal = original_stream
        self.log = open(filepath, "a", encoding="utf-8")
        self.is_error = is_error_stream

    def write(self, message):
        # 1. ÉCRITURE FICHIER (Toujours propre)
        try:
            self.log.write(message)
            self.log.flush()
        except: pass

        # 2. ÉCRITURE TERMINAL (Avec Couleurs)
        if message.strip(): # Si ce n'est pas juste un saut de ligne
            color = ""
            msg_up = message.upper()
            
            # Détection intelligente du contexte
            if self.is_error or "ERROR" in msg_up or "EXCEPTION" in msg_up or "TRACEBACK" in msg_up:
                color = C_RED
            elif "---" in message: # Séparateurs système
                color = C_CYAN
            elif ">>>" in message: # Actions importantes
                color = C_GREEN
            elif "[LOG GUI]" in message: # Activité Interface
                color = C_MAGENTA
            elif "⚠️" in message or "ALERTE" in message or "WARNING" in msg_up:
                color = C_YELLOW
            elif "✅" in message:
                color = C_GREEN
            elif "❌" in message:
                color = C_RED
            
            # Application de la couleur si nécessaire
            if color:
                # On ajoute le RESET à la fin pour ne pas colorier tout le terminal
                self.terminal.write(color + message + C_RESET)
            else:
                self.terminal.write(message)
        else:
            self.terminal.write(message) # Saut de ligne standard

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def start_surveillance(record_dir):
    """Active la surveillance active colorée"""
    log_file = os.path.join(record_dir, "system_debug.log")
    
    # Redirection vers notre logger intelligent
    sys.stdout = DualLogger(log_file, sys.stdout, is_error_stream=False)
    sys.stderr = DualLogger(log_file, sys.stderr, is_error_stream=True)
    
    print(f"--- SURVEILLANCE ACTIVE V2.10 (COLOR MODE) : {datetime.now()} ---")
    print(f"--- JOURNAL : {log_file} ---")
