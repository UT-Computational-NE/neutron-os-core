# Model Corral Examples

Example model directories for use with `neut model` commands.

## triga-steady-state

A reference steady-state MCNP model for the NETL TRIGA Mark II reactor. Includes a complete `model.yaml` manifest with seven materials (fuel, moderator, reflector, structural, control, and air). Use this as a starting point or to test `neut model validate` and `neut model generate`.

```bash
neut model validate docs/guides/examples/triga-steady-state
neut model generate docs/guides/examples/triga-steady-state --format mcnp
```
