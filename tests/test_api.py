
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.models.schemas import ExcuseResponse


client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to ExcuseGPT API",
        "status": "running",
    }


def test_generate_rejects_empty_situation():
    response = client.post(
        "/generate",
        json={"situation": "   "},
    )

    assert response.status_code == 422


def test_generate_returns_three_excuses():
    mock_result = ExcuseResponse(
        excuses=[
            {
                "title": "Honest Approach",
                "text": (
                    "I forgot to complete the assignment, "
                    "and I take responsibility for that."
                ),
                "approach": "direct_acknowledgement",
            },
            {
                "title": "Alternative Perspective",
                "text": (
                    "I missed the assignment deadline, "
                    "and I understand the importance of submitting work on time."
                ),
                "approach": "alternative_framing",
            },
            {
                "title": "Taking Responsibility",
                "text": (
                    "I should have managed my time better, "
                    "and I accept responsibility for missing the deadline."
                ),
                "approach": "accountability_recovery",
            },
        ]
    )

    with patch("backend.main.generate_excuse", return_value=mock_result):
        response = client.post(
            "/generate",
            json={"situation": "I forgot to complete my assignment"},
        )

    assert response.status_code == 200
    assert len(response.json()["excuses"]) == 3
    assert all(
        "title" in excuse
        and "text" in excuse
        and "approach" in excuse
        for excuse in response.json()["excuses"]
    )


def test_refine_returns_refined_text():
    expected_text = (
        "I forgot to submit the assignment, and I take responsibility for that."
    )

    with patch(
        "backend.main.refine_excuse",
        return_value=expected_text,
    ) as mock_refine:
        response = client.post(
            "/refine",
            json={
                "situation": "I forgot to submit my assignment.",
                "original_response": "I forgot about it.",
                "refinement_instruction": "Make it more natural.",
            },
        )

    assert response.status_code == 200
    assert response.json() == {"refined_text": expected_text}
    mock_refine.assert_called_once()


def test_refine_rejects_empty_instruction():
    response = client.post(
        "/refine",
        json={
            "situation": "I forgot to submit my assignment.",
            "original_response": "I forgot about it.",
            "refinement_instruction": "   ",
        },
    )

    assert response.status_code == 422


def test_refine_handles_unexpected_service_error():
    with patch(
        "backend.main.refine_excuse",
        side_effect=RuntimeError("Simulated service failure"),
    ):
        response = client.post(
            "/refine",
            json={
                "situation": "I forgot to submit my assignment.",
                "original_response": "I forgot about it.",
                "refinement_instruction": "Make it more natural.",
            },
        )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "An unexpected error occurred while refining your response."
    )
