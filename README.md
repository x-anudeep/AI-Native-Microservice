# AI-Native Microservice Platform

Production-style FastAPI platform for intelligent document processing. The API accepts text, PDF, and image workloads, selects an AI provider based on request characteristics, returns structured JSON, and exposes telemetry for cost, latency, and request quality.

## Highlights

- Async FastAPI service with 15 endpoints across health, documents, providers, telemetry, and operations.
- Provider router for reasoning, vision, long-context, economy, and balanced workloads.
- Background job simulation for uploaded document/image processing.
- Prometheus metrics for request counts, latency, provider cost, model selections, and failures.
- Docker, Kubernetes, Helm, Terraform, and GitHub Actions support.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API schema.

## Test

```bash
pytest
```

## Architecture

- API docs: `http://127.0.0.1:8000/docs`
- Dark dashboard: `http://127.0.0.1:8000/`
- Prometheus metrics: `http://127.0.0.1:8000/api/v1/metrics`
- Full design notes: [docs/architecture.md](docs/architecture.md)

## Phases

The implementation is organized into four delivery phases in [docs/phases.md](docs/phases.md).
