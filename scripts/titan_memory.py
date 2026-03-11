import os
import datetime

class MemoryManager:
    def __init__(self):
        self.mem_dir = os.path.expanduser("~/titan/ai/memory")
        os.makedirs(os.path.join(self.mem_dir, "long_term"), exist_ok=True)
        os.makedirs(os.path.join(self.mem_dir, "short_term"), exist_ok=True)

    def save_long_term(self, name, content):
        filepath = os.path.join(self.mem_dir, "long_term", f"{name}.txt")
        with open(filepath, "w") as f:
            f.write(content)

    def get_context(self):
        lt_path = os.path.join(self.mem_dir, "long_term")
        memories = []
        for filename in os.listdir(lt_path):
            if filename.endswith(".txt"):
                with open(os.path.join(lt_path, filename), "r") as f:
                    memories.append(f.read())
        return "\n".join(memories)

    # THIS IS THE MISSING FUNCTION
    def archive_session(self, history, client, model):
        if not history:
            return
        
        print("\nKaida is reflecting on our conversation...")
        summary_prompt = "Briefly list key facts about the user and their interests from this chat for long-term memory."
        messages = history + [{"role": "user", "content": summary_prompt}]
        
        try:
            completion = client.chat.completions.create(messages=messages, model=model)
            summary = completion.choices[0].message.content
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.save_long_term(f"session_{ts}", summary)
            print(f"--- Memory Archived: session_{ts}.txt ---")
        except Exception as e:
            print(f"Failed to archive memory: {e}")

