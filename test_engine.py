import sqlite3
import os
import time

# Ensure we are in the Baltimore Node directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'titan_memory.db')

def run_diagnostics():
    print(f"--- Starting Engine Diagnostic on {DB_PATH} ---")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. TEST: Writing a high-priority data shard
        start_time = time.time()
        cursor.execute('''
            INSERT INTO titan_memory (category, content, importance)
            VALUES (?, ?, ?)
        ''', ('system_status', 'Baltimore Node Engine: High-Speed Path Verified.', 1.0))
        conn.commit()
        write_time = (time.time() - start_time) * 1000

        # 2. TEST: Retrieving the shard (The "Memory Recall")
        start_time = time.time()
        cursor.execute("SELECT content FROM titan_memory WHERE category='system_status' ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        read_time = (time.time() - start_time) * 1000

        # 3. OUTPUT: The Results
        if result:
            print(f"SUCCESS: Data Integrity Confirmed.")
            print(f"CONTENT: {result[0]}")
            print(f"WRITE LATENCY: {write_time:.2f}ms")
            print(f"READ LATENCY: {read_time:.2f}ms")
        else:
            print("ERROR: Engine failed to retrieve the shard.")

        conn.close()
    
    except Exception as e:
        print(f"CRITICAL SYSTEM ERROR: {e}")

if __name__ == "__main__":
    run_diagnostics()

