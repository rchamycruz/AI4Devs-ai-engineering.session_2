from datetime import datetime, timezone

import anthropic
import openai
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.config import Settings, get_settings
from app.services.llm_service import LLMConfigurationError, generate_estimation

router = APIRouter(tags=["estimations"])


class EstimationRequest(BaseModel):
    transcription: str = Field(
        ...,
        min_length=20,
        description="Texto de la transcripción de la reunión con el cliente",
        examples=["En la reunión con el cliente se discutió la necesidad de una landing page..."],
    )


class EstimationResponse(BaseModel):
    estimation: str = Field(..., description="Estimación generada en formato Markdown")
    model: str
    provider: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    created_at: datetime


@router.post("/estimate", response_model=EstimationResponse)
async def estimate(request: EstimationRequest, settings: Settings = Depends(get_settings)) -> EstimationResponse:
    try:
        result = await generate_estimation(request.transcription, settings)
    except LLMConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except (anthropic.APIError, openai.APIError) as exc:
        raise HTTPException(status_code=502, detail=f"Error del proveedor LLM: {exc}") from exc

    return EstimationResponse(
        estimation=result.estimation,
        model=result.model,
        provider=result.provider,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        created_at=datetime.now(timezone.utc),
    )
