import sqlite3
import os
from groq import Groq
from titan_sensors import get_system_vitals, get_directory_scan
# 1. Environment & Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'titan_memory.db')
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_chronological_context(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM titan_memory ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    # Reverse so Kaida sees the timeline from past to present
    return "\n".join([row[0] for row in reversed(rows)])

def save_to_engine(text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO titan_memory (category, content) VALUES ('history', ?)", (text,))
    conn.commit()
    conn.close()



def execute_reasoning(user_input):
    # 1. Gather Sensory Data (The "Pulse")
    vitals = get_system_vitals()
    
    # 2. Retrieve History
    past_context = get_chronological_context()
    
    # 3. Create the System Prompt with Sensory Awareness
    system_prompt = (
        "You are Kaida, a high-level systems architect. You are aware of your system vitals. "
        f"Your current body stats are: CPU Load: {vitals['cpu_load']}, RAM Usage: {vitals['ram_used']}, "
        f"Available Disk: {vitals['disk_free']}. Active Directory: {vitals['active_dir']}. "
        "When asked about your 'heart rate' or status, interpret it as your CPU/System Load. "
        "Be concise, technical, and partner-focused."
    )
    
    # 4. Groq API Call
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Chronological Context:\n{past_context}"},
            {"role": "user", "content": user_input}
        ],
        model="llama-3.3-70b-versatile",
    )
    
    return chat_completion.choices[0].message.content
    vitals = get_system_vitals()
    files = get_directory_scan()
    

if __name__ == "__main__":
    print("Kaida Chronological Brain (Groq-Powered): ONLINE")
    while True:
        user_msg = input("Larry: ")
        if user_msg.lower() in ['exit', 'quit']: break
        
        answer = execute_reasoning(user_msg)
        print(f"\nKaida: {answer}\n")
        
        # Save the interaction to the 12K Engine
        save_to_engine(f"Larry: {user_msg} | Kaida: {answer}")

