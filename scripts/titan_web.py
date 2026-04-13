import requests
import urllib3
from datetime import datetime

# 1. Silences the InsecureRequestWarning for you
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TitanWeb:
    def __init__(self):
        self.agent_name = "Kaida"

    def get_weather(self, city="baltimore"):
        try:
            # Short timeout so it doesn't hang forever
            response = requests.get(f"https://wttr.in/{city}?format=3", verify=False, timeout=5)
            return response.text.strip()
        except Exception as e:
            self.log_rejection("Weather Fetch Failure", str(e))
            return "Weather unavailable"
    def search(self, query):
        try:
            # This is where you connect her to a real Search API
            # For now, let's at least log that she's TRYING to see 2026
            print(f"Searching for: {query}...")
            # actual_data = your_search_api_call(query)
            return "Search logic pending implementation"
        except Exception as e:
            self.log_rejection("Search Failure", str(e))
            return "Search unavailable"

    def log_rejection(self, error_type, detail):
        # This keeps track of her "rejections" and errors in a simple file
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("rejection_log.txt", "a") as f:
            f.write(f"[{timestamp}] {self.agent_name} - {error_type}: {detail}\n")

    def run_task(self):
        try:
            # Insert your main logic here
            print(f"Executing Task... Current Weather: {self.get_weather()}")
            
            # --- YOUR SCRAPING LOGIC GOES HERE ---
            # If line 49 was failing, it's because this block wasn't closed.
            pass 

        except Exception as e:
            # This catches the "delusional" behavior or syntax bypasses
            self.log_rejection("Protocol Bypass Attempt", str(e))
            print(f"Critial Deviation Caught: {e}")

# This is now at zero-indentation (line 49 fix)
if __name__ == "__main__":
    titan = TitanWeb()
    titan.run_task()

