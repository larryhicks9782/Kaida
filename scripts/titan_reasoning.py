import random

class ReasoningEngine:
    def __init__(self, brain_instance):
        # self.brain is the TitanBrain instance passed from the main script
        self.brain = brain_instance

    def get_tot_response(self, prompt, search_context=None, branches=3, depth=2):
        """
        One single version of the method that handles everything.
        """
        print(f"\n[ToT System]: Analyzing {branches} branches with live data...")
        
        # Level 1: Initial thoughts grounded in search context
        context_str = search_context if search_context else "No extra context."
        thoughts = [f"Plan {i+1} using context ({context_str[:50]}...): {prompt}" for i in range(branches)]
        
        for d in range(depth):
            print(f"[ToT System]: Expanding depth {d+1}...")
            new_thoughts = []
            for thought in thoughts:
                # Use the brain to think about the expansion
                expansion = self.brain.think(f"Context: {context_str}\nExpand this idea: {thought}")
                new_thoughts.append(expansion)
            
            # Keep only the best branches
            thoughts = random.sample(new_thoughts, min(len(new_thoughts), branches))

        return thoughts[0]
