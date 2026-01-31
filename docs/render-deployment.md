# Render Deployment

This project can be deployed as a Render Web Service using the included `render.yaml` Blueprint.

## Deploy From GitHub

1. Push the latest code to GitHub.
2. Open the Render Dashboard.
3. Select **New** and choose **Blueprint**.
4. Connect the GitHub repository.
5. Render detects `render.yaml` and creates the web service.
6. After deployment, open the generated `onrender.com` URL.

## Manual Web Service Settings

If creating the service manually instead of using the Blueprint:

- Runtime: `Python 3`
- Build command: `python -m pip install --upgrade pip && python -m pip install .`
- Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/api/v1/health`

## URLs

- Dashboard: `/`
- API docs: `/docs`
- Health check: `/api/v1/health`
- Metrics: `/api/v1/metrics`
