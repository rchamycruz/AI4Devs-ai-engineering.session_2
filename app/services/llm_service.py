"""Lógica de negocio: construye el prompt CAG y llama al proveedor LLM configurado."""

from dataclasses import dataclass

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from app.config import Settings
from app.context.examples import ESTIMATION_EXAMPLES


class LLMConfigurationError(Exception):
    """El proveedor seleccionado no tiene API key configurada."""


@dataclass
class EstimationResult:
    estimation: str
    model: str
    provider: str
    input_tokens: int | None = None
    output_tokens: int | None = None


SYSTEM_INSTRUCTIONS = """Eres un estimador de proyectos de software experto. Tu tarea es leer la \
transcripción de una reunión con un cliente y generar una estimación de esfuerzo realista.

Basa tu estimación en las estimaciones históricas de referencia que aparecen más abajo: úsalas \
para calibrar las horas por tipo de tarea y mantén exactamente el mismo formato Markdown \
(título, supuestos, desglose de tareas con horas, total, equipo recomendado, duración y riesgos).

Reglas:
- Responde en español.
- Si la transcripción omite información relevante, decláralo en la sección de supuestos.
- Considera las restricciones que mencione el cliente (plazos, diseño existente, integraciones).
- Responde únicamente con la estimación, sin texto adicional antes ni después."""


def build_system_prompt() -> str:
    """Instrucciones + ejemplos de contexto estático (el corazón de CAG)."""
    examples = "\n\n".join(
        f"<ejemplo numero=\"{i}\">\n"
        f"<resumen_reunion>\n{example['meeting_summary']}\n</resumen_reunion>\n"
        f"<estimacion>\n{example['estimation'].strip()}\n</estimacion>\n"
        f"</ejemplo>"
        for i, example in enumerate(ESTIMATION_EXAMPLES, start=1)
    )
    return f"{SYSTEM_INSTRUCTIONS}\n\n## Estimaciones históricas de referencia\n\n{examples}"


async def generate_estimation(transcription: str, settings: Settings) -> EstimationResult:
    system_prompt = build_system_prompt()
    if settings.llm_provider == "openai":
        return await _call_openai(system_prompt, transcription, settings)
    return await _call_anthropic(system_prompt, transcription, settings)


async def _call_openai(system_prompt: str, transcription: str, settings: Settings) -> EstimationResult:
    if not settings.openai_api_key:
        raise LLMConfigurationError("OPENAI_API_KEY no está configurada")
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model=settings.openai_model,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcription},
        ],
    )
    return EstimationResult(
        estimation=response.choices[0].message.content or "",
        model=response.model,
        provider="openai",
        input_tokens=response.usage.prompt_tokens if response.usage else None,
        output_tokens=response.usage.completion_tokens if response.usage else None,
    )


async def _call_anthropic(system_prompt: str, transcription: str, settings: Settings) -> EstimationResult:
    if not settings.anthropic_api_key:
        raise LLMConfigurationError("ANTHROPIC_API_KEY no está configurada")
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    response = await client.messages.create(
        model=settings.anthropic_model,
        max_tokens=settings.max_tokens,
        # El SDK 1.x eliminó `temperature` de la firma; claude-haiku-4-5 aún lo acepta en la API.
        extra_body={"temperature": settings.temperature},
        system=system_prompt,
        messages=[{"role": "user", "content": transcription}],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    return EstimationResult(
        estimation=text,
        model=response.model,
        provider="anthropic",
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
    )
