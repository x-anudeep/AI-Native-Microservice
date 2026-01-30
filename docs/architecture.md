# Architecture

## Request Flow

1. Client uploads a PDF, image, or text payload.
2. FastAPI validates the request and records HTTP telemetry.
3. The provider router selects the best model for the workload:
   - Claude for reasoning-heavy tasks.
   - GPT-4o for vision workloads.
   - Gemini for long-context documents.
   - Local inference for economy requests.
4. The processor returns structured JSON and records provider cost metrics.
5. Prometheus scrapes `/api/v1/metrics`; Grafana visualizes request rate, cost, and latency.

## Endpoint Inventory

- `GET /api/v1/health`
- `GET /api/v1/ready`
- `GET /api/v1/version`
- `POST /api/v1/documents/process`
- `POST /api/v1/documents/upload`
- `GET /api/v1/documents/jobs/{job_id}`
- `GET /api/v1/providers`
- `GET /api/v1/providers/{provider_name}`
- `POST /api/v1/providers/route`
- `GET /api/v1/metrics`
- `GET /api/v1/metrics/snapshot`
- `GET /api/v1/ops/config`
- `GET /api/v1/ops/slo`
- `POST /api/v1/ops/deployments/blue-green`
- `GET /api/v1/cost/estimate`
- `GET /api/v1/audit/requests/{request_id}`

## 12-Factor Alignment

- Config is provided by environment variables.
- Dependencies are declared in `pyproject.toml`.
- The Docker image is disposable and runs one process.
- Logs and metrics are emitted to stdout and Prometheus endpoints.
- CI validates tests, linting, image builds, and Terraform syntax.

## Platform Capabilities

- Containerized API service: Dockerfile, compose, and CI image build.
- 15+ endpoints: API inventory above.
- 4 AI models: Claude, GPT-4o, Gemini, and local Llama route profiles.
- Terraform with 10+ AWS resources: VPC, subnets, IGW, route table, routes, security group, IAM, EKS, and node group.
- Kubernetes autoscaling: HPA from 2 to 6 pods.
- Observability: Prometheus counters/histograms, alert rules, and Grafana starter dashboard.
