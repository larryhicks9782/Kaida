import sqlite3
import json
import os

# Get the directory where THIS script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'titan_memory.db')
JSON_PATH = os.path.join(BASE_DIR, 'titan_memory.json')

def migrate_memory():
    # 1. Connect to the High-Speed Engine
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 2. Check if the JSON file exists before trying to read it
    if not os.path.exists(JSON_PATH):
        print(f"Alert: {JSON_PATH} not found. Starting with a fresh engine.")
        return

    # 3. Load the old memory data
    with open(JSON_PATH, 'r') as f:
        old_memory = json.load(f)

    # 4. Pour data into the new pathways
    # This assumes your JSON is a list of entries or a dict
    for entry in old_memory:
        # We use 'get' to prevent crashes if a field is missing
        category = entry.get('category', 'general')
        content = entry.get('content', str(entry))
        importance = entry.get('importance', 0.5)
        
        cursor.execute('''
            INSERT INTO titan_memory (category, content, importance)
            VALUES (?, ?, ?)
        ''', (category, content, importance))

    conn.commit()
    conn.close()
    print(f"Migration Complete: Data moved to {DB_PATH}")

if __name__ == "__main__":
    migrate_memory()

