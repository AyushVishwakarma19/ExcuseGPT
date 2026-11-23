
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
    field_validator,
)


ApproachType = Literal[
    "direct_acknowledgement",
    "alternative_framing",
    "accountability_recovery",
    "light_humour",
    "emotional_expression",
]

class ExcuseRequest(BaseModel):
    """Validates user input for excuse generation."""

    model_config = ConfigDict(extra="forbid")

    situation: str = Field(min_length=1, max_length=3000)
    category: str = Field(default="General", min_length=1, max_length=50)
    tone: str = Field(default="Funny", min_length=1, max_length=50)

    creativity: Literal["Low", "Medium", "High"] = "Medium"
    formality: Literal["Casual", "Balanced", "Formal"] = "Casual"
    length: Literal["Short", "Medium", "Long"] = "Medium"

    @field_validator("situation", "category", "tone")
    @classmethod
    def validate_text_fields(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty or whitespace.")

        return value


class ExcuseItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    text: str = Field(min_length=1)
    approach: ApproachType


class ExcuseResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    excuses: list[ExcuseItem]

    @model_validator(mode="after")
    def validate_excuse_count(self):
        if len(self.excuses) != 3:
            raise ValueError("Exactly three excuses are required")

        approaches = [excuse.approach for excuse in self.excuses]

        if len(set(approaches)) != 3:
            raise ValueError("All three excuses must use different approaches")

        return self

class ExcuseRefinementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situation: str = Field(min_length=1, max_length=3000)
    original_response: str = Field(min_length=1, max_length=2000)
    refinement_instruction: str = Field(min_length=1, max_length=500)

    @field_validator(
        "situation",
        "original_response",
        "refinement_instruction",
    )
    @classmethod
    def validate_text_fields(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty or whitespace.")

        return value