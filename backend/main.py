
import traceback

from fastapi import FastAPI, HTTPException
from google.genai.errors import APIError

from backend.models.schemas import (
    ExcuseRequest,
    ExcuseResponse,
    ExcuseRefinementRequest,
)
from backend.services.llm_service import generate_excuse, refine_excuse


app = FastAPI(
    title="ExcuseGPT API",
    description="An AI-powered, context-aware excuse generation API.",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {
        "message": "Welcome to ExcuseGPT API",
        "status": "running",
    }


@app.post("/generate", response_model=ExcuseResponse)
def generate_excuses(request: ExcuseRequest):
    try:
        result = generate_excuse(
            situation=request.situation,
            category=request.category,
            tone=request.tone,
            creativity=request.creativity,
            formality=request.formality,
            length=request.length,
        )

        return result

    except APIError as error:
        print(f"GEMINI API ERROR: {error}")

        status_code = getattr(error, "code", None)

        if status_code == 503:
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable. Please try again later.",
            )

        raise HTTPException(
            status_code=502,
            detail="The AI service could not process your request. Please try again later.",
        )

    except ValueError as error:
        print(f"GENERATION VALIDATION ERROR: {error}")

        raise HTTPException(
            status_code=422,
            detail="We couldn't generate a suitable response. Please try again.",
        )

    except Exception as error:
        print(f"UNEXPECTED GENERATION ERROR: {error}")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while generating excuses.",
        )


@app.post("/refine")
def refine_generated_excuse(request: ExcuseRefinementRequest):
    try:
        refined_text = refine_excuse(
            situation=request.situation,
            original_response=request.original_response,
            refinement_instruction=request.refinement_instruction,
        )

        return {"refined_text": refined_text}

    except APIError as error:
        print(f"GEMINI API ERROR DURING REFINEMENT: {error}")

        status_code = getattr(error, "code", None)

        if status_code == 503:
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable. Please try again later.",
            )

        raise HTTPException(
            status_code=502,
            detail="The AI service could not refine your response. Please try again later.",
        )

    except ValueError as error:
        print(f"REFINEMENT VALIDATION ERROR: {error}")

        raise HTTPException(
            status_code=422,
            detail="We couldn't refine this response. Please try again.",
        )

    except Exception as error:
        print(f"UNEXPECTED REFINEMENT ERROR: {error}")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while refining your response.",
        )
