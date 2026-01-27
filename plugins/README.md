# Plugins

Reactor-specific plugins that extend Neutron OS core functionality.

## Status

**Stub** - Will be implemented in later phases.

## Concept

Neutron OS core is reactor-agnostic. Reactor-specific logic lives in plugins:

| Plugin | Reactor | Functionality |
|--------|---------|---------------|
| `plugin-triga` | UT NETL TRIGA | TRIGA-specific data transforms, audit rules, UI components |
| `plugin-msr` | Molten Salt Reactor | MSR-specific physics, thermal-hydraulics |
| `plugin-mit-loop` | MIT Irradiation Loop | Loop-specific experiment analysis |

## Structure (Planned)

```
plugins/
├── plugin-triga/
│   ├── pyproject.toml
│   ├── plugin_triga/
│   │   ├── models/        # TRIGA-specific data models
│   │   ├── transforms/    # dbt models for TRIGA data
│   │   ├── rules/         # Audit rules
│   │   └── ui/            # React components
│   └── tests/
│
├── plugin-msr/
│   └── ...
│
└── plugin-mit-loop/
    └── ...
```

## Plugin Interface

Plugins implement standard interfaces defined in `packages/python/neutron_core`:

```python
class ReactorPlugin(Protocol):
    name: str
    reactor_type: str
    
    def register_transforms(self) -> list[DbtModel]: ...
    def register_audit_rules(self) -> list[AuditRule]: ...
    def register_schemas(self) -> list[IcebergSchema]: ...
```
