import sqlite3
from pathlib import Path


class ChatDBService:

    def __init__(self):

        self.db_path = "chat_history.db"

        self._initialize_database()

    def _initialize_database(self):

        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()

        conn.close()

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages
            (
                session_id,
                role,
                content
            )
            VALUES (?, ?, ?)
            """,
            (
                session_id,
                role,
                content,
            ),
        )

        conn.commit()

        conn.close()

    def get_history(
        self,
        session_id: str,
        limit: int = 20,
    ):

        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role, content
            FROM messages
            WHERE session_id=?
            ORDER BY id ASC
            LIMIT ?
            """,
            (
                session_id,
                limit,
            ),
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            {
                "role": row[0],
                "content": row[1],
            }
            for row in rows
        ]

    def clear_session(
        self,
        session_id: str,
    ):

        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM messages
            WHERE session_id=?
            """,
            (session_id,),
        )

        conn.commit()

        conn.close()