# Meeting Intake Tool

Agentic pipeline for extracting requirements from meeting recordings and syncing to GitLab.

## Overview

This tool:
1. Fetches meeting recordings from Microsoft Teams/OneDrive
2. Transcribes audio using Whisper
3. Extracts requirements using Claude (Anthropic)
4. Matches to existing GitLab issues (prefers APPEND over CREATE)
5. Queues for human review and approval
6. Applies approved changes to GitLab

## Architecture

```
Teams Recording → Transcribe → Extract → Match → Human Review → GitLab
```

Uses LangGraph for stateful workflow with human-in-the-loop checkpoints.

## Access Control

- Meeting context stored in PostgreSQL with pgvector
- Row-Level Security ensures users can only query meetings they attended
- External attendees not supported in initial version

## Setup

```bash
# Prerequisites
# - PostgreSQL 16+ with pgvector extension
# - Anthropic API key
# - Microsoft Graph API credentials (for Teams)
# - GitLab API token

# Install dependencies
cd tools/meeting-intake
pip install -e .

# Configure
cp .env.example .env
# Edit .env with your credentials
```

## Usage

```bash
# Process new meetings
meeting-intake fetch --since "2026-01-01"

# Review pending requirements
meeting-intake review

# Apply approved changes to GitLab
meeting-intake apply

# Search meeting context (respects access control)
meeting-intake search "data lake requirements"
```

## Configuration

Environment variables:
- `ANTHROPIC_API_KEY` - Anthropic API key for Claude
- `DATABASE_URL` - PostgreSQL connection string
- `GITLAB_URL` - GitLab instance URL
- `GITLAB_TOKEN` - GitLab API token
- `GITLAB_PROJECT_ID` - Target project for issues
- `MS_GRAPH_CLIENT_ID` - Microsoft Graph client ID
- `MS_GRAPH_CLIENT_SECRET` - Microsoft Graph client secret
- `MS_GRAPH_TENANT_ID` - Azure AD tenant ID

## Development

```bash
# Run tests
pytest

# Type checking
mypy meeting_intake

# Lint
ruff check meeting_intake
```
