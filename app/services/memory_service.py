from typing import Dict, List

class ConversationMemory:
    def __init__(self, max_history: int = 5):
        self.store: Dict[str, List[Dict[str, str]]] = {}
        self.max_history = max_history

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.store:
            self.store[session_id] = []

        self.store[session_id].append({
            "role": role,
            "content": content
        })

        # Keep only last N messages
        self.store[session_id] = self.store[session_id][-self.max_history:]

    def get_history(self, session_id: str):
        return self.store.get(session_id, [])

# Global memory instance
memory = ConversationMemory()