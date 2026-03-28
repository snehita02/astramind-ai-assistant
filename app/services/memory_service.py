# from typing import Dict, List

# class ConversationMemory:
#     def __init__(self, max_history: int = 5):
#         self.store: Dict[str, List[Dict[str, str]]] = {}
#         self.max_history = max_history

#     def add_message(self, session_id: str, role: str, content: str):
#         if session_id not in self.store:
#             self.store[session_id] = []

#         self.store[session_id].append({
#             "role": role,
#             "content": content
#         })

#         # Keep only last N messages
#         self.store[session_id] = self.store[session_id][-self.max_history:]

#     def get_history(self, session_id: str):
#         return self.store.get(session_id, [])

# # Global memory instance
# memory = ConversationMemory()













# from typing import Dict, List

# class ConversationMemory:

#     def __init__(self, max_history: int = 6):
#         self.store: Dict[str, List[Dict[str, str]]] = {}
#         self.max_history = max_history

#     def add_message(self, session_id: str, role: str, content: str):

#         if session_id not in self.store:
#             self.store[session_id] = []

#         self.store[session_id].append({
#             "role": role,
#             "content": content
#         })

#         self.store[session_id] = self.store[session_id][-self.max_history:]


#     def get_history(self, session_id: str):

#         history = self.store.get(session_id)

#         if history:
#             return history

#         # Memory fallback
#         return []


# memory = ConversationMemory()















from typing import Dict, List


class ConversationMemory:

    def __init__(self, max_history: int = 6):
        self.store: Dict[str, List[Dict[str, str]]] = {}
        self.max_history = max_history

    def add_message(self, session_id: str, role: str, content: str):

        if session_id not in self.store:
            self.store[session_id] = []

        self.store[session_id].append({
            "role": role,
            "content": content
        })

        self.store[session_id] = self.store[session_id][-self.max_history:]

    def get_history(self, session_id: str) -> List[Dict[str, str]]:

        # 1️⃣ Try in-memory first (works locally)
        history = self.store.get(session_id)
        if history:
            return history

        # 2️⃣ Fallback to DB (works on Render across processes)
        try:
            from app.database.chat_database import get_chat_history
            rows = get_chat_history(session_id)
            history = [
                {"role": r["role"], "content": r["content"]}
                for r in rows
                if r.get("role") and r.get("content")
            ]
            if history:
                # repopulate in-memory so subsequent calls in same process are fast
                self.store[session_id] = history[-self.max_history:]
                return self.store[session_id]
        except Exception:
            pass

        return []


memory = ConversationMemory()