# Demo: Model Corral in 5 Minutes

## Setup (before demo)
- Clean terminal, large font
- `cd /tmp/demo-workspace && rm -rf *`
- Verify: `neut model --help` shows clean Tier 0 output

## Demo Script

### Act 1: "What materials do we have?" (1 min)

```bash
neut facility list
# -> Shows NETL-TRIGA, MSRE, PWR-generic

neut model materials --category fuel
# -> Shows UZrH-20, UO2-3.1, UO2-4.95, MSRE-salt

neut model materials --card UZrH-20
# -> Beautiful MCNP material card with isotopes, comments, provenance
```

**Talking point:** "Every material is verified, sourced, and generates correct MCNP/MPACT cards."

### Act 2: "Create a new model" (2 min)

```bash
neut model init demo-triga --reactor-type TRIGA --facility NETL --materials
# -> Creates directory with model.yaml + materials pre-populated

cat demo-triga/model.yaml
# -> Show the auto-generated manifest

neut model validate demo-triga
# -> Should pass

neut model lint demo-triga
# -> Shows any warnings (TODO description, etc.)
```

**Talking point:** "One command to scaffold. Materials from your facility pack. Validation catches problems early."

### Act 3: "Submit and find" (1 min)

```bash
neut model add demo-triga -m "demo steady-state model"
# -> Added: demo-triga v0.1.0

neut model list
# -> Shows demo-triga in the registry

neut model show demo-triga
# -> Full details with version history
```

**Talking point:** "Every model is versioned, searchable, and has full provenance."

### Act 4: "Generate input" (1 min)

```bash
neut model generate demo-triga --format mcnp
# -> Deterministic MCNP material cards

neut model generate demo-triga --format mpact
# -> Same model, MPACT format
```

**Talking point:** "Same model.yaml, any output format. Deterministic -- run it twice, get identical output."

### Closer

"This is Model Corral. Version your models. Verify your materials. Generate your input. All from the command line, all with `--json` for automation."
