
import pytest
from pydantic import ValidationError

from backend.models.schemas import (
    ExcuseItem,
    ExcuseResponse,
    ExcuseRefinementRequest,
)


def create_valid_excuse(approach="light_humour"):
    return ExcuseItem(
        title="The Digital Disaster",
        text="I completely forgot, and that's on me.",
        approach=approach,
    )


def test_valid_excuse_creation():
    excuse = create_valid_excuse()

    assert excuse.title == "The Digital Disaster"
    assert excuse.approach == "light_humour"


def test_exactly_three_excuses():
    response = ExcuseResponse(
        excuses=[
            create_valid_excuse("direct_acknowledgement"),
            create_valid_excuse("alternative_framing"),
            create_valid_excuse("accountability_recovery"),
        ]
    )

    assert len(response.excuses) == 3


def test_invalid_excuse_count():
    with pytest.raises(ValidationError):
        ExcuseResponse(
            excuses=[
                create_valid_excuse("direct_acknowledgement"),
                create_valid_excuse("alternative_framing"),
            ]
        )


def test_duplicate_approaches_are_rejected():
    with pytest.raises(ValidationError):
        ExcuseResponse(
            excuses=[
                create_valid_excuse("direct_acknowledgement"),
                create_valid_excuse("direct_acknowledgement"),
                create_valid_excuse("accountability_recovery"),
            ]
        )


def test_invalid_approach_is_rejected():
    with pytest.raises(ValidationError):
        create_valid_excuse("invalid_approach")



def test_removed_score_fields_are_rejected():
    with pytest.raises(ValidationError):
        ExcuseItem.model_validate(
            {
                "title": "Old format",
                "text": "This uses the previous response structure.",
                "tone": "Funny",
                "creativity_score": 8,
                "formality_score": 3,
                "approach": "light_humour",
            }
        )



def test_valid_refinement_request():
    request = ExcuseRefinementRequest(
        situation="I forgot to submit my assignment.",
        original_response="I forgot to submit it, and that's on me.",
        refinement_instruction="Make it more natural.",
    )

    assert request.situation == "I forgot to submit my assignment."
    assert request.refinement_instruction == "Make it more natural."


def test_refinement_request_rejects_empty_situation():
    with pytest.raises(ValidationError):
        ExcuseRefinementRequest(
            situation="   ",
            original_response="I forgot to submit it.",
            refinement_instruction="Make it natural.",
        )


def test_refinement_request_rejects_empty_original_response():
    with pytest.raises(ValidationError):
        ExcuseRefinementRequest(
            situation="I forgot to submit my assignment.",
            original_response="   ",
            refinement_instruction="Make it natural.",
        )


def test_refinement_request_rejects_empty_instruction():
    with pytest.raises(ValidationError):
        ExcuseRefinementRequest(
            situation="I forgot to submit my assignment.",
            original_response="I forgot to submit it.",
            refinement_instruction="   ",
        )
