import os
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from titan_memory import TitanMemory
from titan_intel import TitanIntel
from titan_web import TitanWeb
from titan_mail import TitanMail
from groq import Groq

console = Console()

class TitanBrain:
    def __init__(self):
        # API and Tool Initialization
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"
        self.memory = TitanMemory()
        self.intel = TitanIntel()
        self.web = TitanWeb()
        self.mail = TitanMail()

    def think(self, user_input):
        history_context = self.memory.get_context()
        
        # 1. Hardware Intel Logic
        if any(word in user_input.lower() for word in ["battery", "location", "status"]):
            user_input += f" (System Update: {self.intel.get_stats()})"

        # 2. Web Search Logic
        if "search" in user_input.lower():
            with console.status("[bold blue]Scanning the Web...", spinner="dots"):
                web_data = self.web.search(user_input)
                user_input += f" (Web Data: {web_data})"

        # 3. Mail Dispatch Logic
        if "email to" in user_input.lower():
            try:
                # Basic parsing: "email to example@gmail.com message body"
                parts = user_input.split("email to ")[1].split(" ", 1)
                target_email = parts[0]
                body_content = parts[1] if len(parts) > 1 else "No body provided."
                
                with console.status("[bold yellow]Sending Email...", spinner="envelope"):
                    mail_status = self.mail.send(target_email, "Titan OS Report", body_content)
                user_input += f" (Status: {mail_status})"
            except Exception as e:
                user_input += f" (Mail Parse Error: {e})"

        # 4. Processing via Groq
        messages = [
            {"role": "system", "content": "You are Kaida, a Titan OS assistant. Be concise and professional."},
            {"role": "assistant", "content": f"Context: {history_context}"},
            {"role": "user", "content": user_input}
        ]

        completion = self.client.chat.completions.create(messages=messages, model=self.model)
        response = completion.choices[0].message.content
        
        self.memory.save(user_input, response)
        return response

if __name__ == "__main__":
    brain = TitanBrain()
    console.print(Panel("[bold cyan]KAIDA ONLINE[/bold cyan]\n[dim]Intel, Web, & Mail Patched[/dim]", border_style="blue"))
    
    while True:
        try:
            u_in = console.input("[bold green]You:[/bold green] ")
            if u_in.lower() in ["exit", "quit"]:
                brain.memory.archive_session()
                break
            
            res = brain.think(u_in)
            console.print(Panel(Text(res, style="white"), title="[bold magenta]Kaida[/bold magenta]", border_style="cyan"))
        except KeyboardInterrupt:
            break
