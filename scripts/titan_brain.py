import os
from groq import Groq
from titan_memory import MemoryManager # Importing your new separate file
from titan_ui import TitanUI
from rich.prompt import Prompt

class TitanBrain:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.memory = MemoryManager()
        self.history = []
        self.ui = TitanUI()
        self.modes = {
            "default": "You are Kaida. Be helpful, concise, and friendly.",
            "serious": "You are Kaida, the analytical assistant. Be direct, factual, and strictly objective.",
            "creative": "You are Kaida, the creative muse. Use metaphors and be imaginative.",
            "humorous": "You are Kaida, the witty companion. Use humor and playful banter."
        }
        self.current_mode = "default"

    def think(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        if len(self.history) > 10: self.history.pop(0)

        if user_input.startswith("/mode "):
            mode = user_input.split(" ")[1]
            if mode in brain.modes:
                brain.current_mode = mode
                brain.ui.show_response(f"Personality switched to {mode}.")
            else:
                brain.ui.show_response("Available modes: default, serious, creative, humorous.")

        context = self.memory.get_context()
        messages = [{"role": "system", "content": f"You are Kaida. Info: {context}"}] + self.history
        system_content = f"{self.modes[self.current_mode]} Info: {context}"
        messages = [{"role": "system", "content": system_content}] + self.history
        completion = self.client.chat.completions.create(messages=messages, model=self.model)
        response = completion.choices[0].message.content

        self.history.append({"role": "assistant", "content": response})
        return response

if __name__ == "__main__":
    brain = TitanBrain()
    # Use your UI design for the header
    brain.ui.show_header() 
    
    while True:
        # Using standard input but then passing it to the UI
        user_input = Prompt.ask("[bold green]You[/bold green]")
        
        if user_input.lower() == 'quit':
            brain.memory.archive_session(brain.history, brain.client, brain.model)
            break
        
        # This is where the magic happens:
        # 1. Show the status animation
        with brain.ui.show_status():
            response = brain.think(user_input)
            
        # 2. Show the fancy panel response
        brain.ui.show_response(response)


