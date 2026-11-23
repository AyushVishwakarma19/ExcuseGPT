
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from backend.models.schemas import ExcuseResponse
from backend.prompts.prompt_builder import (
    build_excuse_prompt,
    build_refinement_prompt,
)


# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

if not MODEL_NAME:
    raise ValueError("GEMINI_MODEL is missing from .env")


# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def get_gemini_schema():
    """Prepare the Pydantic schema for Gemini structured output."""

    schema = ExcuseResponse.model_json_schema()

    def remove_unsupported_fields(obj):
        if isinstance(obj, dict):
            obj.pop("additionalProperties", None)

            for value in obj.values():
                remove_unsupported_fields(value)

        elif isinstance(obj, list):
            for item in obj:
                remove_unsupported_fields(item)

    remove_unsupported_fields(schema)

    return schema


def generate_excuse(
    situation: str,
    category: str = "General",
    tone: str = "Funny",
    creativity: str = "Medium",
    formality: str = "Casual",
    length: str = "Medium",
) -> ExcuseResponse:

    # Build prompts
    messages = build_excuse_prompt(
        situation=situation,
        category=category,
        tone=tone,
        creativity=creativity,
        formality=formality,
        length=length,
    )

    system_instruction = messages[0]["content"]
    user_prompt = messages[1]["content"]

    # Generate structured response using Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.6,
            max_output_tokens=1200,
            response_mime_type="application/json",
            response_schema=get_gemini_schema(),
        ),
    )

    # Extract and validate response
    if response.parsed is not None:
        return ExcuseResponse.model_validate(response.parsed)

    raw_content = response.text

    if not raw_content:
        raise ValueError("Gemini returned an empty response.")

    parsed_data = json.loads(raw_content)

    return ExcuseResponse.model_validate(parsed_data)


def refine_excuse(
    situation: str,
    original_response: str,
    refinement_instruction: str,
) -> str:
    """Refine an existing excuse while preserving its facts."""

    system_instruction, user_prompt = build_refinement_prompt(
        situation=situation,
        original_response=original_response,
        refinement_instruction=refinement_instruction,
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.5,
            max_output_tokens=500,
        ),
    )

    refined_text = response.text

    if not refined_text or not refined_text.strip():
        raise ValueError("Gemini returned an empty refined response.")

    return refined_text.strip()
