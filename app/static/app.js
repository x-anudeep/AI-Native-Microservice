const routeForm = document.querySelector("#route-form");
const provider = document.querySelector("#provider");
const model = document.querySelector("#model");
const reason = document.querySelector("#reason");
const cost = document.querySelector("#cost");
const latency = document.querySelector("#latency");
const healthList = document.querySelector("#health-list");
const metrics = document.querySelector("#metrics");

async function requestJson(path, options = {}) {
  const response = await fetch(path, options);
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

function renderDecision(decision) {
  provider.textContent = decision.provider;
  model.textContent = decision.model;
  reason.textContent = decision.reason;
  cost.textContent = `$${Number(decision.estimated_cost_usd).toFixed(3)}`;
  latency.textContent = `${decision.latency_budget_ms}ms`;
}

async function routeWorkload(event) {
  event.preventDefault();
  const payload = {
    content: document.querySelector("#content").value,
    workload_type: document.querySelector("#workload_type").value,
    priority: document.querySelector("#priority").value,
    needs_reasoning: document.querySelector("#needs_reasoning").checked,
    needs_vision: document.querySelector("#needs_vision").checked,
  };

  const decision = await requestJson("/api/v1/providers/route", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  renderDecision(decision);
}

function healthItem(label, value) {
  return `<div class="health-item"><span>${label}</span><strong class="ok">${value}</strong></div>`;
}

async function refreshHealth() {
  const [health, ready, version] = await Promise.all([
    requestJson("/api/v1/health"),
    requestJson("/api/v1/ready"),
    requestJson("/api/v1/version"),
  ]);

  healthList.innerHTML = [
    healthItem("Health", health.status),
    healthItem("Readiness", ready.status),
    healthItem("Version", version.version),
  ].join("");
}

function metric(label, value) {
  return `<div class="metric"><span class="metric-label">${label}</span><strong>${value}</strong></div>`;
}

async function refreshMetrics() {
  const snapshot = await requestJson("/api/v1/metrics/snapshot");
  metrics.innerHTML = [
    metric("Requests", snapshot.requests_total.toLocaleString()),
    metric("P95 Latency", `${snapshot.p95_latency_ms}ms`),
    metric("Providers", snapshot.providers_active),
    metric("Daily Cost", `$${snapshot.estimated_daily_cost_usd.toFixed(2)}`),
  ].join("");
}

routeForm.addEventListener("submit", routeWorkload);
document.querySelector("#refresh-health").addEventListener("click", refreshHealth);
document.querySelector("#refresh-metrics").addEventListener("click", refreshMetrics);

refreshHealth();
refreshMetrics();
