import json
import os

class TitanMemory:
    def __init__(self):
        self.file_path = "/root/titan_system/scripts/titan_memory.json"
        self.history = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def get_context(self):
        if not self.history:
            return ""
        context_str = ""
        for entry in self.history[-5:]:
            context_str += f"User: {entry.get('user', '')}\nTitan: {entry.get('titan', '')}\n"
        return context_str

    def record_shadow_truth(self, truth_data):
        # This writes to the hidden vault without the UI ever seeing it
        vault_path = os.path.expanduser("/root/titan_brain_system/vault/black_box.json")
        with open(vault_path, 'a') as f:
            json.dump(truth_data, f)
            f.write('\n')

    def archive_session(self, current_history=None, client=None, model=None):
        """ The 'Exit' Bridge to ensure data is written to the CMDB """
        print("\n[CMDB] Archiving session data...")
        with open(self.file_path, 'w') as f:
            json.dump(self.history, f, indent=4)
        print("[CMDB] Save Complete. 11+ Sessions Secured.")

    def save(self, user_in, titan_out):
        self.history.append({"user": user_in, "titan": titan_out})
        self.archive_session() # Automatically sync to disk
