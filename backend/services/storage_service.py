
import json
import sqlite3
from pathlib import Path


# Store the database in the project's data directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "excusegpt.db"


def get_connection():
    """Create a connection to the SQLite database."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the application state table if it does not exist."""

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS app_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                generation_history TEXT NOT NULL DEFAULT '[]',
                saved_excuses TEXT NOT NULL DEFAULT '[]',
                refined_responses TEXT NOT NULL DEFAULT '{}'
            )
            """
        )

        connection.execute(
            """
            INSERT OR IGNORE INTO app_state (id)
            VALUES (1)
            """
        )


def load_app_state():
    """Load previously saved application data."""

    initialize_database()

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                generation_history,
                saved_excuses,
                refined_responses
            FROM app_state
            WHERE id = 1
            """
        ).fetchone()

    return {
        "generation_history": json.loads(row["generation_history"]),
        "saved_excuses": json.loads(row["saved_excuses"]),
        "refined_responses": json.loads(row["refined_responses"]),
    }


def save_app_state(
    generation_history,
    saved_excuses,
    refined_responses,
):
    """Persist all application data in one database transaction."""

    initialize_database()

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE app_state
            SET
                generation_history = ?,
                saved_excuses = ?,
                refined_responses = ?
            WHERE id = 1
            """,
            (
                json.dumps(generation_history, ensure_ascii=False),
                json.dumps(saved_excuses, ensure_ascii=False),
                json.dumps(refined_responses, ensure_ascii=False),
            ),
        )
