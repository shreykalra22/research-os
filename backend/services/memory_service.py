from collections import defaultdict
from typing import Dict, List


class MemoryService:
    """
    Simple in-memory conversation memory.

    Stores:
    session_id -> conversation messages
    """

    def __init__(self):

        self.sessions: Dict[str, List[dict]] = defaultdict(list)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_history(
        self,
        session_id: str,
    ) -> List[dict]:

        return self.sessions.get(
            session_id,
            [],
        )

    def clear_history(
        self,
        session_id: str,
    ):

        self.sessions[session_id] = []