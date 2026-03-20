import requests
from bs4 import BeautifulSoup
class TitanWeb:
    def search(self, query):
        try:
            res = requests.get(f"https://duckduckgo.com/html/?q={query}", headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            results = [r.get_text() for r in soup.find_all('a', class_='result__snippet', limit=2)]
            return " | ".join(results) if results else "No web data found."
        except:
            return "Web search failed."
