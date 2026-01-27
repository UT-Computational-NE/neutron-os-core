# Infrastructure

Infrastructure-as-Code for Neutron OS deployment.

## Status

**⏸️ PAUSED** - Awaiting hosting decision for data lake.

## Standards

| ✅ Use | ❌ Avoid |
|--------|----------|
| Terraform | CloudFormation, ARM, Pulumi |
| Kubernetes | Docker Swarm, Nomad |
| Helm | Raw manifests only |
| K3D (local) | Docker-Compose, Minikube |
| S3-compatible | Provider-locked storage |

## Structure

```
infra/
├── terraform/
│   ├── modules/           # Reusable modules
│   │   ├── k8s-cluster/   # Cloud-agnostic K8s
│   │   ├── storage/       # S3-compatible storage
│   │   └── networking/    # VPC, DNS, etc.
│   └── environments/      # Environment-specific
│       ├── local/         # K3D (no-op TF)
│       ├── tacc/          # TACC Kubernetes
│       └── cloud/         # AWS/GCP/Azure
│
├── helm/
│   ├── charts/            # Helm charts
│   │   ├── neutron-lakehouse/
│   │   ├── neutron-fabric/
│   │   └── neutron-keycloak/
│   └── values/            # Environment values
│       ├── local.yaml
│       ├── tacc.yaml
│       └── prod.yaml
│
└── k3d/
    └── cluster-config.yaml
```

## Local Development (When Ready)

```bash
# Create local K3D cluster
k3d cluster create neutron --config k3d/cluster-config.yaml

# Install lakehouse stack
helm install lakehouse helm/charts/neutron-lakehouse -f helm/values/local.yaml

# Access Superset
kubectl port-forward svc/superset 8088:8088
open http://localhost:8088
```

## Pending Decisions

1. **Data Lake Hosting** - TACC? Cloud? Hybrid?
2. **Storage Backend** - SeaweedFS? MinIO? S3?
3. **Database** - TACC PostgreSQL? Cloud managed?
