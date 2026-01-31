# AI-Native Microservice Platform

AI-Native Microservice Platform is a cloud-ready FastAPI service for intelligent document processing. It accepts text, PDF, and image workloads, routes each request to the best AI provider profile, returns structured JSON, and exposes operational telemetry for cost, latency, and service health.

## Highlights

- Async FastAPI API with 15+ endpoints across health, document processing, provider routing, telemetry, and operations.
- AI provider routing profiles for reasoning, vision, long-context, economy, and balanced workloads.
- Dark operations dashboard for routing demos, service health, and metrics snapshots.
- Prometheus instrumentation for request counts, latency, provider cost, and model selections.
- Docker runtime, Kubernetes manifests, Helm chart, Terraform AWS/EKS infrastructure, and GitHub Actions CI/CD.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open the dashboard at `http://127.0.0.1:8000/` or the API schema at `http://127.0.0.1:8000/docs`.

## Test

```bash
pytest
```

## Run With Docker

```bash
docker compose up --build
```

## Deploy To Render

The repository includes a `render.yaml` Blueprint for Render Web Services.

```bash
git push origin main
```

Then create a Render Blueprint from the GitHub repository. Deployment details are in [docs/render-deployment.md](docs/render-deployment.md).

## Architecture

- API docs: `http://127.0.0.1:8000/docs`
- Dark dashboard: `http://127.0.0.1:8000/`
- Prometheus metrics: `http://127.0.0.1:8000/api/v1/metrics`
- Full design notes: [docs/architecture.md](docs/architecture.md)

## Infrastructure

- `Dockerfile` and `docker-compose.yml` package the service for local and containerized execution.
- `k8s/` contains Kubernetes manifests for deployment, service discovery, config, service account, and HPA autoscaling.
- `helm/` provides a reusable Helm chart for Kubernetes deployments.
- `terraform/` provisions the AWS/EKS resource shape for the platform.
- `.github/workflows/` validates tests, linting, container builds, and Terraform checks.
