# Delivery Phases

## Phase 1: Application Core

- FastAPI app factory, settings, schemas, routing, provider decision engine, and processor service.
- Health, readiness, version, document processing, provider, metrics snapshot, operations, cost, and audit endpoints.
- Initial API tests for health and model routing behavior.

## Phase 2: Containerization and Runtime Quality

- Docker multi-stage build and local compose stack.
- Linting, environment examples, and operational runbook.
- Expanded test coverage for jobs and cost estimation.

## Phase 3: Kubernetes, Helm, and Observability

- Kubernetes manifests and Helm chart for deployment, service, HPA, config, and service account.
- Prometheus metrics endpoint and custom request/cost/latency instrumentation.
- Grafana dashboard starter and alert rules.

## Phase 4: Terraform, CI/CD, and Production Hardening

- Terraform modules for AWS network, EKS skeleton, IAM, and observability namespaces.
- GitHub Actions pipeline for tests, image build, IaC checks, and deployment gates.
- Final documentation covering architecture, 12-factor principles, and operating model.

## Commit Structure

Each phase is represented by three focused commits:

- Phase 1: scaffold, API/provider logic, tests/docs.
- Phase 2: container runtime, operations workflow, runtime tests.
- Phase 3: telemetry, Kubernetes/monitoring assets, Helm chart.
- Phase 4: Terraform, CI/CD scripts, final architecture docs.
