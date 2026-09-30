# Estimador CAG

Servicio FastAPI que recibe la transcripción de una reunión con un cliente y devuelve una estimación de proyecto de software generada por un LLM (OpenAI o Anthropic).

Usa arquitectura **CAG**: los ejemplos de estimaciones previas (`app/context/examples.py`) se inyectan en el system prompt en cada llamada. No hay base de datos, retrieval ni persistencia.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- API key de OpenAI y/o Anthropic

## Configuración

```bash
uv sync
cp .env.example .env   # y completa los valores
```

| Variable | Descripción | Por defecto |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` u `openai` | `anthropic` |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` | API key del proveedor elegido | — |
| `ANTHROPIC_MODEL` / `OPENAI_MODEL` | Modelo a usar | `claude-haiku-4-5` / `gpt-4o-mini` |
| `MAX_TOKENS` | Máximo de tokens de salida | `4096` |
| `TEMPERATURE` | Temperatura de muestreo | `0.3` |

Las variables vacías usan el valor por defecto.

## Ejecución

```bash
uv run uvicorn app.main:app --reload
```

- Swagger UI: http://localhost:8000/docs
- Health: `GET http://localhost:8000/health`

```bash
curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d '{"transcription": "En la reunión con el equipo de marketing, el cliente explicó que necesita una landing page con formulario de contacto, integración con su CRM actual (HubSpot), y una sección de blog con editor WYSIWYG. El plazo ideal sería tenerlo listo en 4 semanas. El diseño ya existe en Figma."}'
```

Respuesta:

```json
{
  "estimation": "## Estimación: ...",
  "model": "claude-haiku-4-5",
  "provider": "anthropic",
  "input_tokens": 1234,
  "output_tokens": 567,
  "created_at": "2026-09-29T12:00:00Z"
}
```

## Estructura

```
app/
├── main.py                  # App FastAPI, /health, router con prefijo /api/v1
├── config.py                # Settings (pydantic-settings) desde .env
├── routers/estimations.py   # POST /api/v1/estimate + schemas
├── services/llm_service.py  # Construcción del prompt CAG y llamada al LLM
└── context/examples.py      # Estimaciones históricas (few-shot)
```
