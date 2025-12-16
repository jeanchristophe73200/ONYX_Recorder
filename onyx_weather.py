import requests
import threading
import time

class WeatherEngine:
    def __init__(self):
        self.lat = 45.68039
        self.lon = 6.40926
        self.data = {
            "temp": "--.-", "hum": "--", "wind": "--", "press": "----", "rain": "0.0 mm"
        }
        self.running = False

    def update_coords(self, lat_str, lon_str):
        try:
            self.lat = float(lat_str.strip())
            self.lon = float(lon_str.strip())
            self.fetch_data()
        except: pass

    def start_monitoring(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.running:
            self.fetch_data()
            time.sleep(900)

    def fetch_data(self):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,precipitation&timezone=auto"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                js = r.json()['current']
                self.data["temp"] = f"{js['temperature_2m']} °C"
                self.data["hum"] = f"Hum: {js['relative_humidity_2m']} %"
                self.data["wind"] = f"Vent: {js['wind_speed_10m']} km/h"
                self.data["press"] = f"Pres: {int(js['surface_pressure'])} hPa"
                self.data["rain"] = f"Pluie: {js['precipitation']} mm"
            else: print("Erreur API Météo")
        except: pass

    def get_data(self): return self.data
