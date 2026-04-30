# LangFuse — institutional observability

LLM-call observability (prompts, completions, traces, evals, costs) for any
NeutronOS / Axiom node that wants to report into a shared dashboard.

This release packages the upstream `langfuse/langfuse-k8s` Helm chart with
our institutional values. It's the *bridge* until LangFuse is wrapped as a
proper AEOS observability extension in the post-Prague queue.

## Where this lives in the architecture

- **Service** runs on **Server-tier** node (Rascal first; TACC later).
- **Edge-tier** nodes (instructor / student laptops) run *no LangFuse server*;
  they ship the LangFuse SDK and report HTTPS traces to a configured
  institutional endpoint.
- **Cross-institution federation** does NOT share a LangFuse — each
  institution keeps its own (privacy + EC).

## First-time install (Rascal, K3S)

Prereqs: `k3s` running, `helm` 3.x present, `kubectl` pointed at the K3S cluster.

```bash
export KUBECONFIG=~/.kube/config-rascal

# 1. Namespace
kubectl create namespace langfuse

# 2. Out-of-band secrets (don't commit these values).
#    The chart's bundled subcharts (PG, Valkey, ClickHouse) require
#    pre-set passwords, so we create one Secret with all six keys.
kubectl -n langfuse create secret generic langfuse-secrets \
  --from-literal=salt="$(openssl rand -base64 32)" \
  --from-literal=nextauth-secret="$(openssl rand -base64 32)" \
  --from-literal=encryption-key="$(openssl rand -hex 32)" \
  --from-literal=postgres-password="$(openssl rand -base64 24 | tr -d /=+)" \
  --from-literal=redis-password="$(openssl rand -base64 24 | tr -d /=+)" \
  --from-literal=clickhouse-password="$(openssl rand -base64 24 | tr -d /=+)"

# 3. Install
helm repo add langfuse https://langfuse.github.io/langfuse-k8s
helm repo update
helm install langfuse langfuse/langfuse \
  --namespace langfuse \
  --version 1.5.28 \
  --values values.yaml \
  --wait --timeout 10m

# 4. Verify
kubectl -n langfuse get pods
```

## Access

- Web UI: `http://rascal.austin.utexas.edu:30030` (UT network / UT VPN)
- API ingest: same host, `/api/public/ingestion` (used by SDKs)

## Wiring a workstation to report traces

Each LangFuse **project** has its own API key pair. Operators keep one env file
per project under `~/.config/axiom/`, mode 600, never committed:

```
~/.config/axiom/
  langfuse-prague.env         # production classroom signal (workspace default)
  langfuse-sandbox_dev1.env   # opt-in dev playground
```

Each file contains:

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-…"
export LANGFUSE_SECRET_KEY="sk-lf-…"
export LANGFUSE_HOST="http://rascal.austin.utexas.edu:30030"
export LANGFUSE_BASE_URL="http://rascal.austin.utexas.edu:30030"
```

The workspace-root `.envrc` sources `langfuse-prague.env` automatically when
direnv activates (so `axi` commands tag the production project by default).
For dev experimentation, override in the active shell:

```bash
source ~/.config/axiom/langfuse-sandbox_dev1.env   # later source wins
```

To add a new project (per-cohort isolation, etc.), create the project in the
LangFuse UI → generate API keys → drop them in a new
`~/.config/axiom/langfuse-<project>.env` and source it as needed.

See `langfuse.env.example` for the file template.

## First admin

Open the UI, sign up. The first account becomes the org admin. After that
the operator should set `langfuse.features.signUpDisabled: true` and
upgrade.

## Upgrade

```bash
helm repo update
helm upgrade langfuse langfuse/langfuse \
  --namespace langfuse \
  --version <new-chart-version> \
  --values values.yaml
```

## Known debt (resolved during deeper observability dive, post-Prague)

- **MinIO bundled** instead of SeaweedFS (violates the no-MinIO rule)
- **No ingress / TLS** — NodePort only; Ondrej from Prague needs Tailscale
  or external auth-proxy to reach this
- **Public sign-up open** — tighten after first admin
- **Not yet wrapped as a proper AEOS observability extension** with the
  standardized `deploy/helm/` skeleton
