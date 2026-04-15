import requests
import urllib3

from titan_brain import TitanBrain
from titan_reasoning import ReasoningEngine
from datetime import datetime
from bs4 import BeautifulSoup

# --- Setup ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TitanWeb:
    # ... (keep your existing TitanWeb class methods here) ...
    def __init__(self):
        self.agent_name = "Kaida"
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_weather(self, city="baltimore"):
        return requests.get(f"https://wttr.in/{city}?format=3", verify=False).text.strip()

    def search(self, query):
        # Simplification for this example
        return f"Search result for {query}: The weather is clear."

if __name__ == "__main__":
    # 1. Initialize
    web_tool = TitanWeb()
    brain_instance = TitanBrain(web_instance=web_tool)
    reasoner = ReasoningEngine(brain_instance=brain_instance)

    # 2. Define the goal
    user_query = "Summarize recent media releases for April 2026."
    print(f"--- Starting Task: {user_query} ---")
    
    # 3. Fetch web data
    # Use search() to actually get data, not just weather
    raw_web_data = web_tool.search(user_query) 
    
    # 4. Execute Reasoning
    final_output = reasoner.get_tot_response(
        prompt=user_query,
        search_context=raw_web_data
    )
    
    # 5. PRINT THE RESULT (The most important part!)
    print("\n" + "="*30)
    print("FINAL KAIDA OUTPUT:")
    print("="*30)
    print(final_output)
    print("="*30 + "\n")

    # 6. Archive and close
    brain_instance.memory.archive_session()

