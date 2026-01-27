# Packages

Shared libraries for Neutron OS, organized by language.

## Structure

```
packages/
├── schemas/           # Language-agnostic (Protobuf/Avro)
│   ├── domain/        # Domain models (Person, Experiment, etc.)
│   └── api/           # API contracts
│
├── python/            # Python packages
│   ├── neutron_core/  # Domain models (Pydantic)
│   ├── neutron_data/  # Iceberg/DuckDB utilities
│   ├── neutron_auth/  # Keycloak client
│   └── neutron_audit/ # Audit trail client
│
├── typescript/        # TypeScript packages
│   ├── neutron-sdk/   # API client
│   └── neutron-ui/    # Shared React components
│
├── c/                 # C libraries (future)
│   └── neutron_realtime/
│
└── mojo/              # Mojo packages (future)
    └── neutron_compute/
```

## Language-Agnostic Schemas

Domain models are defined in Protobuf/Avro in `schemas/` and code-generated for each target language. This ensures consistency across Python, TypeScript, Go (chaincode), etc.

## Python Packages

Install in development mode:
```bash
cd packages/python/neutron_core
pip install -e .
```

Or with Bazel:
```bash
bazel build //packages/python/neutron_core:neutron_core
```

## TypeScript Packages

```bash
cd packages/typescript/neutron-sdk
pnpm install
pnpm build
```
