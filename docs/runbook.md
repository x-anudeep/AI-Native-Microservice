# Operations Runbook

## Start Locally

```bash
make install
make run
```

## Container Runtime

```bash
make docker-build
make docker-up
```

## Health Checks

- Liveness: `GET /api/v1/health`
- Readiness: `GET /api/v1/ready`
- Runtime version: `GET /api/v1/version`

## Deployment Notes

- The service follows 12-factor configuration through environment variables.
- Upload size and latency SLOs are configurable without rebuilding the image.
- The Docker image runs as a non-root user and uses a multi-stage build.
