# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

AI4Devs course exercise (session 2): `estimador-cag`, a FastAPI service that turns a meeting transcription into a software estimate using an LLM. The spec, including the verification checklist, is `docs/instructions.md` (in Spanish). Prompts, examples and user-facing strings are in Spanish.

The architecture is **CAG (Context-Augmented Generation)**: static reference data is injected into the system prompt on every call. There is no database, no retrieval and no persistence. Later course modules evolve this into RAG, so keep the context source (`app/context/examples.py`) easy to swap out.

## Commands

```bash
uv sync                                   # install deps
uv run uvicorn app.main:app --reload      # dev server on :8000; Swagger at /docs
curl localhost:8000/health
curl -X POST localhost:8000/api/v1/estimate -H "Content-Type: application/json" -d '{"transcription": "..."}'
```

No tests or linter are configured.

## Architecture

Request flow: `routers/estimations.py` → `services/llm_service.generate_estimation()` → the provider SDK (async clients).

- `config.py`: `Settings` (pydantic-settings) loaded from `.env`, cached through `get_settings()` and injected into routes with `Depends`. `env_ignore_empty=True`, so blank variables fall back to the defaults. `LLM_PROVIDER` (`anthropic` | `openai`) picks the provider; the defaults are `claude-haiku-4-5` and `gpt-4o-mini`.
- `services/llm_service.py`: `build_system_prompt()` joins the instructions with every `ESTIMATION_EXAMPLES` entry, wrapped in XML-style tags. That is the CAG injection. The transcription is sent as the only user message. Each provider has its own `_call_*` function, and both return an `EstimationResult` that includes token usage.
- The project uses the `anthropic` SDK 1.x, which removed `temperature`/`top_p`/`top_k` from `messages.create()`; passing them raises a `TypeError`. Send `temperature` through `extra_body`, which `claude-haiku-4-5` still accepts. Opus 4.7+ models reject it with a 400.
- Error mapping in the router: a missing API key raises `LLMConfigurationError` and returns 500. SDK `APIError`s return 502.
- Response: `{estimation, model, provider, input_tokens, output_tokens, created_at}`.

When adding config variables, update `.env.example` (names only, no values) and the table in `README.md`. `.env` is gitignored.
