# Linear Integration for TRIGA Digital Twin

This folder contains tools for managing project initiatives in Linear and keeping them synchronized with strategy documentation and codebase changes.

## Overview

The sync system has three components:

1. **Export to Linear** - Push roadmap initiatives from strategy docs → Linear issues
2. **Import from Linear** - Pull Linear issue status → update strategy docs  
3. **Codebase Changelog** - Detect new features in code → suggest doc updates

## Quick Start

### 1. Get a Linear API Key

1. Go to [Linear Settings > Account > Security & Access](https://linear.app/settings/account/security)
2. Create a new Personal API Key
3. Copy the key and save it as `LINEAR_API_KEY` environment variable

```bash
export LINEAR_API_KEY="lin_api_xxxxx"
```

### 2. Configure Your Workspace

Edit `config.json` with your Linear workspace details:

```json
{
  "linear_team_id": "YOUR_TEAM_ID",
  "project_name": "TRIGA Digital Twin",
  "default_assignee": null
}
```

To find your team ID, run:
```bash
python linear_sync.py --list-teams
```

### 3. Initial Export to Linear

Push all roadmap initiatives to Linear:

```bash
python linear_sync.py --export-all
```

This creates:
- A Linear Project for "TRIGA Digital Twin Roadmap 2026-2027"
- Issues for each initiative, labeled by quarter and track
- Links back to strategy documentation

### 4. Ongoing Sync

**Pull updates from Linear:**
```bash
python linear_sync.py --import
```

This updates:
- `sync_state.json` with current Linear issue statuses
- Strategy docs with completion checkmarks

**Push new initiatives:**
```bash
python linear_sync.py --export-new
```

## File Structure

```
linear_integration/
├── README.md              # This file
├── config.json            # Linear workspace configuration
├── linear_sync.py         # Main sync script
├── initiatives.json       # Extracted initiatives from roadmap
├── sync_state.json        # Current sync state (auto-generated)
└── templates/
    └── issue_template.md  # Template for Linear issue descriptions
```

## How It Works

### Initiative Extraction

The `linear_sync.py` script parses strategy documents to extract:
- Quarterly goals from `04_okrs_goals.md`
- Supporting initiatives (checkbox items)
- Key deliverables
- Target dates

Each initiative becomes a Linear issue with:
- **Title**: Initiative description
- **Labels**: Quarter (Q1-2026), Track (Pipeline, Isotope, etc.)
- **Project**: TRIGA Digital Twin Roadmap
- **Description**: Links to strategy docs, acceptance criteria

### Bi-directional Sync

```
┌─────────────────┐     export      ┌─────────────────┐
│  Strategy Docs  │ ──────────────► │     Linear      │
│  (Markdown)     │                 │    (Issues)     │
│                 │ ◄────────────── │                 │
└─────────────────┘     import      └─────────────────┘
        │                                   │
        │                                   │
        └──────────┬──────────────┬────────┘
                   │              │
                   ▼              ▼
           ┌─────────────────────────────┐
           │        sync_state.json      │
           │  (ID mappings, timestamps)  │
           └─────────────────────────────┘
```

### Conflict Resolution

When both Linear and docs have changed:
1. Linear status wins (it's the "work in progress" system)
2. Doc changes to scope/description create a warning
3. Manual review required for conflicts

## GitLab CI/CD Integration

Add to `.gitlab-ci.yml` in the repository root:

```yaml
stages:
  - sync

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

# Weekly sync with Linear
linear-sync:
  stage: sync
  image: python:3.11-slim
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"  # Scheduled runs
    - if: $CI_PIPELINE_SOURCE == "push"
      changes:
        - docs/strategy/**/*
  cache:
    paths:
      - .cache/pip
  before_script:
    - pip install requests
  script:
    - cd docs/strategy/linear_integration
    - python linear_sync.py --import --export-new
  after_script:
    - |
      git config user.name "GitLab CI"
      git config user.email "ci@gitlab.com"
      git add docs/strategy/
      git diff --staged --quiet || git commit -m "chore: sync Linear state [skip ci]"
      git push https://oauth2:${GITLAB_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git HEAD:${CI_COMMIT_REF_NAME}
  variables:
    LINEAR_API_KEY: $LINEAR_API_KEY  # Set in GitLab CI/CD Variables
```

### Setting Up GitLab CI

1. **Add CI/CD Variables** (Settings > CI/CD > Variables):
   - `LINEAR_API_KEY`: Your Linear API key (masked)
   - `GITLAB_TOKEN`: Project access token with `write_repository` scope (for auto-commits)

2. **Create a Pipeline Schedule** (CI/CD > Schedules):
   - Description: "Weekly Linear Sync"
   - Interval: `0 9 * * 1` (Mondays at 9 AM)
   - Target branch: `main`

3. **Optional: Doc Change Detection**
   
   Add to your `.gitlab-ci.yml`:
   
   ```yaml
   # Detect codebase changes that need docs
   doc-changelog:
     stage: sync
     image: python:3.11-slim
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
         changes:
           - triga_dt_website/**/*
           - triga_modsim_tools/**/*
           - netl_pxi/**/*
     script:
       - cd docs/strategy/linear_integration
       - python linear_sync.py --detect-changes
     allow_failure: true
   ```

## Codebase Feature Detection

To track when new features are built (for updating docs):

```bash
python linear_sync.py --detect-changes
```

This scans recent commits for:
- New route handlers in `triga_dt_website/`
- New simulation scripts
- New data processing pipelines

And suggests documentation updates.

## Labels Used

| Label | Color | Purpose |
|-------|-------|---------|
| `Q1-2026` | Blue | Quarter targeting |
| `Q2-2026` | Green | Quarter targeting |
| `Pipeline` | Gray | Track: reliability |
| `Accuracy` | Purple | Track: simulation |
| `Adoption` | Orange | Track: users |
| `Compliance` | Red | Track: NRC |
| `Isotope` | Teal | Track: medical isotopes |
| `Commercial` | Gold | Track: commercialization |
| `from-docs` | Light | Imported from strategy docs |

## Troubleshooting

### "Team not found"
Run `python linear_sync.py --list-teams` and update `config.json` with correct team ID.

### "Issue already exists"  
The script uses idempotency keys based on initiative text. Edit `sync_state.json` to force recreation.

### "Rate limited"
Linear allows 1500 requests/hour. The script batches operations but large initial exports may hit limits. Wait and retry.

## Manual Workflow (No API)

If you prefer not to use the API:

1. Run `python linear_sync.py --csv` to export initiatives to CSV
2. Import CSV manually via Linear's UI (Settings > Import)
3. Manually update strategy docs when issues complete

## Questions?

- Linear API docs: https://linear.app/developers
- GraphQL schema: https://studio.apollographql.com/public/Linear-API
