import sqlite3
import pytest
from backend.services import storage_service


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Provide an isolated temporary SQLite database for testing."""
    test_db_path = tmp_path / "test_excusegpt.db"
    monkeypatch.setattr(storage_service, "DATA_DIR", tmp_path)
    monkeypatch.setattr(storage_service, "DATABASE_PATH", test_db_path)
    return test_db_path


def test_initialize_database_creates_table(temp_db):
    storage_service.initialize_database()

    assert temp_db.exists()

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='app_state'"
        )
        assert cursor.fetchone() is not None


def test_load_app_state_returns_default_structure(temp_db):
    state = storage_service.load_app_state()

    assert "generation_history" in state
    assert "saved_excuses" in state
    assert "refined_responses" in state
    assert state["generation_history"] == []
    assert state["saved_excuses"] == []
    assert state["refined_responses"] == {}


def test_save_and_load_app_state(temp_db):
    mock_history = [
        {
            "id": "1",
            "situation": "Missed a meeting due to a deadline.",
            "preferences": {"category": "Work", "tone": "Professional"},
            "excuses": [
                {
                    "title": "Direct Admission",
                    "text": "I missed the meeting because of a conflicting deadline.",
                    "approach": "direct_acknowledgement",
                }
            ],
        }
    ]
    mock_saved = [
        {
            "situation": "Missed a meeting due to a deadline.",
            "title": "Direct Admission",
            "text": "I missed the meeting because of a conflicting deadline.",
            "approach": "direct_acknowledgement",
        }
    ]
    mock_refined = {"1_0": "I sincerely apologize for missing the meeting."}

    storage_service.save_app_state(
        generation_history=mock_history,
        saved_excuses=mock_saved,
        refined_responses=mock_refined,
    )

    loaded_state = storage_service.load_app_state()

    assert loaded_state["generation_history"] == mock_history
    assert loaded_state["saved_excuses"] == mock_saved
    assert loaded_state["refined_responses"] == mock_refined


def test_save_app_state_overwrites_previous(temp_db):
    storage_service.save_app_state(
        generation_history=[{"id": "1"}],
        saved_excuses=[],
        refined_responses={},
    )

    storage_service.save_app_state(
        generation_history=[{"id": "2"}],
        saved_excuses=[{"title": "Test"}],
        refined_responses={"2_0": "Refined"},
    )

    loaded = storage_service.load_app_state()
    assert len(loaded["generation_history"]) == 1
    assert loaded["generation_history"][0]["id"] == "2"
    assert len(loaded["saved_excuses"]) == 1
    assert loaded["refined_responses"] == {"2_0": "Refined"}
