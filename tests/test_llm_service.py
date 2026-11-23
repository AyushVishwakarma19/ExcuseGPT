
import json
from unittest.mock import patch, MagicMock

import pytest
from pydantic import ValidationError

from backend.services.llm_service import generate_excuse, refine_excuse


def create_valid_response():
    return {
        "excuses": [
            {
                "title": "Calendar Confusion",
                "text": (
                    "I completely forgot about the meeting, and that's on me. "
                    "My calendar and I clearly need a serious conversation after this."
                ),
                "approach": "direct_acknowledgement",
            },
            {
                "title": "A Different Perspective",
                "text": (
                    "The meeting happened, and I wasn't there; that's the simple truth. "
                    "I should have managed my schedule more carefully, and I apologize."
                ),
                "approach": "alternative_framing",
            },
            {
                "title": "Owning the Mistake",
                "text": (
                    "I missed the meeting, and I take responsibility for that. "
                    "I apologize for my absence."
                ),
                "approach": "accountability_recovery",
            },
        ]
    }


def test_generate_excuse_accepts_structured_response():
    mock_response = MagicMock()
    mock_response.parsed = create_valid_response()

    with patch(
        "backend.services.llm_service.client.models.generate_content",
        return_value=mock_response,
    ):
        result = generate_excuse(
            situation="I missed an office meeting."
        )

    assert len(result.excuses) == 3
    assert result.excuses[0].title == "Calendar Confusion"
    assert result.excuses[0].approach == "direct_acknowledgement"


def test_generate_excuse_parses_json_fallback():
    mock_response = MagicMock()
    mock_response.parsed = None
    mock_response.text = json.dumps(create_valid_response())

    with patch(
        "backend.services.llm_service.client.models.generate_content",
        return_value=mock_response,
    ):
        result = generate_excuse(
            situation="I missed an office meeting."
        )

    assert len(result.excuses) == 3


def test_generate_excuse_rejects_invalid_response():
    invalid_response = create_valid_response()
    invalid_response["excuses"].pop()

    mock_response = MagicMock()
    mock_response.parsed = invalid_response

    with patch(
        "backend.services.llm_service.client.models.generate_content",
        return_value=mock_response,
    ):
        with pytest.raises(ValidationError):
            generate_excuse(
                situation="I missed an office meeting."
            )


def test_refine_excuse_returns_refined_text():
    mock_response = MagicMock()
    mock_response.text = (
        "I forgot to submit the assignment, and I take responsibility for that."
    )

    with patch(
        "backend.services.llm_service.client.models.generate_content",
        return_value=mock_response,
    ) as mock_generate:

        result = refine_excuse(
            situation="I forgot to submit my assignment.",
            original_response="I forgot about it.",
            refinement_instruction="Make it more natural.",
        )

    assert result == (
        "I forgot to submit the assignment, and I take responsibility for that."
    )
    mock_generate.assert_called_once()


def test_refine_excuse_rejects_empty_response():
    mock_response = MagicMock()
    mock_response.text = "   "

    with patch(
        "backend.services.llm_service.client.models.generate_content",
        return_value=mock_response,
    ):
        with pytest.raises(
            ValueError,
            match="Gemini returned an empty refined response.",
        ):
            refine_excuse(
                situation="I forgot to submit my assignment.",
                original_response="I forgot about it.",
                refinement_instruction="Make it more natural.",
            )
