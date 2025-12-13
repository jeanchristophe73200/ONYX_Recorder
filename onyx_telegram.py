import requests
import threading
import time
import json
import onyx_settings as config

class TelegramEngine:
    def __init__(self, callback_gui):
        self.token = config.TELEGRAM_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.callback_gui = callback_gui
        self.running = False
        self.last_update_id = 0

    def send_message(self, text):
        try:
            requests.post(f"{self.base_url}/sendMessage", data={"chat_id": self.chat_id, "text": text}, timeout=5)
        except: pass

    def update_keyboard(self):
        keyboard = []
        row = []
        for i, (text, icon) in enumerate(config.BUTTONS_LAYOUT):
            row.append({"text": f"{icon} {text}"})
            if len(row) == 2:
                keyboard.append(row); row = []
        if row: keyboard.append(row)
        keyboard.append([{"text": config.BTN_PAC_ON}, {"text": config.BTN_PAC_OFF}])
        keyboard.append([{"text": config.BTN_ONGOING}])
        try:
            requests.post(f"{self.base_url}/sendMessage", data={"chat_id": self.chat_id, "text": "🎛️ SYSTEME ARME", "reply_markup": json.dumps({"keyboard": keyboard, "resize_keyboard": True})}, timeout=5)
        except: pass

    def start_listening(self):
        self.running = True
        threading.Thread(target=self._poll_updates, daemon=True).start()

    def _poll_updates(self):
        self._get_updates(offset=-1)
        while self.running:
            updates = self._get_updates(offset=self.last_update_id + 1)
            if updates:
                for u in updates:
                    self.last_update_id = u["update_id"]
                    if "message" in u and "text" in u["message"]:
                        self.callback_gui(u["message"]["text"], from_telegram=True)
            time.sleep(1.5)

    def _get_updates(self, offset=None):
        try:
            r = requests.get(f"{self.base_url}/getUpdates", params={"timeout": 1, "offset": offset}, timeout=2)
            if r.status_code == 200: return r.json().get("result", [])
        except: pass
        return []

    def stop(self): self.running = False
