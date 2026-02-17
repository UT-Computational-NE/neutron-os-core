# DocFlow: Document Lifecycle Management System

**Version:** 0.1.0-alpha  
**Status:** Specification (In Development)  
**Last Updated:** February 10, 2026  
**Owner:** Ben Booth (UT Nuclear Engineering)

---

## Executive Summary

DocFlow is a comprehensive document lifecycle management system that treats markdown (.md) files as **source code** and published Word documents (.docx) as **deployment artifacts**. It automates the publication, review, feedback incorporation, and embedding pipeline for technical documentation while maintaining a clean Git workflow.

### Key Capabilities

- **Single-source truth:** .md files are the source; .docx files are generated outputs
- **Multi-stage publication:** Local → Draft Review → Published → Archived
- **Formal review cycles:** Review periods with required/optional reviewers, deadline tracking
- **Intelligent feedback:** Comment extraction from drafts and published versions
- **Cross-document linking:** Automatic URL rewriting for internal doc links
- **Meeting intelligence:** Automatically extract decisions/actions from meeting transcripts
- **Vector embedding:** Feed documents into RAG pipelines
- **CI/CD native:** Git-based workflow, branch-aware publication
- **Extensible:** Provider pattern for multiple storage targets (OneDrive, Google Drive, etc.)
- **Human-in-the-loop:** RACI-based autonomy levels with approval gates
- **Cost-conscious:** Uses Haiku (cheapest LLM) for most operations

---

## Problem Statement

### Current Pain Points

1. **Manual link management** — After publishing to OneDrive, internal markdown links break. Must manually recreate all hyperlinks.

2. **Branch confusion** — Multiple Git branches with divergent docs → unclear which version is "published" → multiple conflicting OneDrive URLs.

3. **Comment orphaning** — Feedback on draft documents during review isn't tracked when document is promoted to published version.

4. **Scattered review cycle** — No formal process for review periods, deadline enforcement, or tracking reviewer responses.

5. **Lost institutional memory** — Meeting decisions captured nowhere; context for why requirements exist is lost.

6. **Manual republication** — Every doc update requires manual generation, upload, and link fixing.

7. **Embedding lag** — Documents published to OneDrive but not indexed for RAG until manually triggered.

8. **Inconsistent access control** — Sharing decisions (who can see what) are made ad-hoc, inconsistently.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DocFlow System Architecture                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SOURCES                  GENERATION              PUBLISHING            │
│  ───────                  ──────────              ──────────            │
│                                                                         │
│  docs/                    md_to_docx              Storage Providers     │
│  ├─ prd/                  ──────────              ─────────────         │
│  ├─ specs/                • Comments             • OneDrive             │
│  ├─ adr/                  • Links                • Google Drive         │
│  └─ ...                   • Mermaid              • Local (test)         │
│       │                   • Watermark                  │                │
│       │                                                │                │
│       ▼                        ▼                       ▼                │
│  .md files          .docx files (generated)  Canonical URLs            │
│  (Git source)                                                           │
│                          │                          ▲                   │
│  ┌─────────────────────────────────────────────────────────┐            │
│  │            FEEDBACK & REVIEW LOOP                       │            │
│  ├─────────────────────────────────────────────────────────┤            │
│  │                                                         │            │
│  │  1. Fetch comments (draft + published)                 │            │
│  │  2. Extract insights (LLM categorization)              │            │
│  │  3. Update source .md (incorporate feedback)           │            │
│  │  4. Regenerate & republish                             │            │
│  └─────────────────────────────────────────────────────────┘            │
│                                  │                                      │
│  ┌──────────────────────────────────────────────────────┐               │
│  │       ADDITIONAL PIPELINES                           │               │
│  ├──────────────────────────────────────────────────────┤               │
│  │                                                      │               │
│  │  • Meeting Intelligence: Meetings → Decisions       │               │
│  │  • RAG Embedding: Docs → Vector Store               │               │
│  │  • Link Rewriting: Internal refs → Published URLs   │               │
│  │  • Version Archiving: Old versions → Archive        │               │
│  └──────────────────────────────────────────────────────┘               │
│                                                                         │
│  ┌──────────────────────────────────────────────────────┐               │
│  │       CONTROL LAYER                                 │               │
│  ├──────────────────────────────────────────────────────┤               │
│  │                                                      │               │
│  │  Git Integration:   Branch policies, sync checks    │               │
│  │  Autonomy Framework: RACI-based approval gates      │               │
│  │  LangGraph Workflow: Stateful agent orchestration   │               │
│  │  Scheduling:        Polling, reminders, deadlines   │               │
│  └──────────────────────────────────────────────────────┘               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## System Design

### 1. Document Lifecycle State Machine

```
┌────────────┐
│   LOCAL    │  .md file in Git (any branch)
└────┬───────┘
     │ publish --draft (if not main)
     ▼
┌────────────────────┐
│  DRAFT REVIEW      │  In /Drafts/ with review period
│  (+ Review Period) │  • Required reviewers
└────┬───────────────┘  • Deadline (default 7 days)
     │                  • Comments tracked in draft_comments
     │
     ├─ [extend review] ──► EXTENDED ──┐
     │                                 │
     │ [review deadline passes]        │
     │ all reviewers responded         │
     └─────────────────────────────────┤
                                       │
     ┌──────────────────────────────────┘
     │
     │ [promote to published]
     ▼
┌────────────────────┐
│   PUBLISHED        │  Canonical /Documents/Published/ URL
│   (PRODUCTION)     │  • Version numbered (v1.0, v2.0, etc.)
└────┬───────────────┘  • Feedback loop active
     │                  • Comments tracked in published_comments
     │
     ├─ [new changes] ──► Feedback incorporated ──┐
     │                    into .md                │
     │                                            │
     │ [superseded by new version]               │
     └────────────────────────────────────────────┤
                                                 │
     ┌──────────────────────────────────────────┘
     │
     ▼
┌────────────┐
│  ARCHIVED  │  /Archive/ (read-only, historical reference)
└────────────┘
```

### 2. Publication Targets

| Target | When | URL Pattern | Comments | Use Case |
|--------|------|------------|----------|----------|
| **Local** | Always | `./generated/*.docx` | None | Development preview |
| **Draft** | Before publish | `/Drafts/{doc_id}-{date}-DRAFT.docx` | Tracked in `draft_comments` | Formal review cycles |
| **Published** | After approval | `/Documents/Published/{doc_id}.docx` | Tracked in `published_comments` | Production use |
| **Archive** | When superseded | `/Archive/{doc_id}-v{N}.docx` | Read-only | Historical reference |

### 3. Review Period Workflow

```python
class ReviewPeriod:
    review_id: str
    started_at: datetime
    ends_at: datetime
    extended_to: Optional[datetime]
    
    required_reviewers: list[str]  # Must respond
    optional_reviewers: list[str]  # Nice-to-have
    
    responses: dict[str, ReviewerResponse]
    status: ReviewStatus  # open, extended, closed, promoted
    outcome: str  # approved, approved_with_changes, needs_revision
```

**Process:**
1. Author publishes draft with 7-day review period, specifies required reviewers
2. Reminders sent at T-3 days, T-1 day, T-0
3. Reviewers comment on OneDrive doc
4. Agent fetches comments, tracks reviewer responses
5. Deadline passes → if all required responded, prompt for promotion
6. Author reviews comments, incorporates feedback into .md
7. Draft promoted to published version
8. Previous version archived

### 4. Link Registry

```python
class LinkRegistry:
    entries: dict[doc_id, LinkEntry]
    # Example:
    # "experiment-manager-prd" → {
    #     source_file: "docs/prd/experiment-manager-prd.md",
    #     published_url: "https://.../experiment-manager-prd.docx",
    #     draft_url: (optional, if currently in review)
    # }

def rewrite_links_in_docx(docx_path, registry):
    """Convert all [text](file.md) → [text](https://...file.docx)"""
    # Parse docx hyperlinks, resolve via registry, rewrite
```

Persisted to `.doc-registry.json` in repo root.

### 5. Git Integration

**Branch policies:**
```yaml
publish_branches:
  - main          # Canonical location
  - release/*     # Version tags
```

**Feature branches:**
- No OneDrive publish
- No feedback loop
- Local .docx generation only
- Can use `--draft` to upload to drafts folder for review

**On merge to main:**
- CI/CD automatically publishes to canonical URL
- Comments are tracked
- Feedback loop activated

### 6. Autonomy Framework (RACI-Based)

```python
class AutonomyLevel(IntEnum):
    MANUAL = 0          # Human does work
    SUGGEST = 1         # AI proposes, human approves
    CONFIRM = 2         # AI acts after timeout (unless vetoed)
    NOTIFY = 3          # AI acts, human notified after
    AUTONOMOUS = 4      # AI acts silently
```

Per-action defaults:
```yaml
actions:
  poll_for_comments:       autonomous   # Safe, read-only
  fetch_comments:          autonomous   # Safe, read-only
  analyze_feedback:        notify       # LLM categorization, low risk
  update_source_file:      suggest      # CRITICAL - show diff first
  republish_approved_doc:  confirm      # Auto after 10min unless vetoed
  republish_new_doc:       suggest      # First publish = full review
  promote_draft:           suggest      # Important decision
```

---

## Core Components

### Component 1: Provider Pattern

**StorageProvider** (abstract base)
```python
class StorageProvider(ABC):
    def upload(file_path, destination_path) → UploadResult
    def download(file_id) → BinaryIO
    def get_comments(file_id) → list[CommentData]
    def create_share_link(file_id, scope, permission) → str
    def move(file_id, new_path) → bool
```

**Implementations:**
- `OneDriveProvider` — MS Graph API (primary)
- `GoogleDriveProvider` — Google Drive API (secondary)
- `LocalProvider` — Filesystem (testing)

**NotificationProvider** (abstract base)
```python
class NotificationProvider(ABC):
    def send_email(to, subject, body)
    def send_teams_message(channel, message)
```

**EmbeddingProvider** (abstract base)
```python
class EmbeddingProvider(ABC):
    def embed_texts(texts) → list[vector]
    def store(texts, embeddings, metadata)
    def search(query, k=10) → list[(text, score, metadata)]
```

**LLMProvider** (abstract base)
```python
class LLMProvider(ABC):
    def complete(prompt, **kwargs) → str
    def complete_structured(prompt, schema) → dict
```

### Component 2: State Management

**DocumentState** (TypedDict)
```python
doc_id: str
source_path: str

# Publication records (per-version)
published: CanonicalPublication  # Current version
active_draft: DraftPublication   # If in review
draft_history: list[DraftPublication]

# Git tracking
current_branch: str
current_commit: str

# Approval state
approval_status: "draft" | "in_review" | "approved"
auto_republish: bool

# Feedback
pending_comments: list[dict]  # Unincorporated

# Collaborators
stakeholders: list[str]
```

**WorkflowState** (TypedDict)
```python
documents: dict[str, DocumentState]
git_context: GitContext
last_poll: datetime
pending_actions: dict[str, ProposedAction]
```

### Component 3: Git Integration

**GitContext**
```python
current_branch: str
commit_sha: str
is_dirty: bool
ahead_count: int
behind_count: int
```

**Sync Detection**
```python
class SyncStatus(Enum):
    IN_SYNC = "in_sync"
    LOCAL_AHEAD = "local_ahead"    # Local changes not published
    REMOTE_AHEAD = "remote_ahead"  # OneDrive feedback not incorporated
    DIVERGED = "diverged"
```

### Component 4: Review Management

**ReviewManager**
- Fetch comments from draft/published versions
- Track reviewer responses
- Send deadline reminders
- Handle deadline passing
- Support deadline extension
- Promote drafts to published
- Archive previous versions

### Component 5: Comment Extraction

**DOCX Comment Parser**
- Extract from `word/comments.xml` (part of docx ZIP)
- Parse author, timestamp, text, range/context
- Support nested replies
- Track resolution status

### Component 6: LangGraph Workflow

**Nodes:**
1. `poll_onedrive` — Check for new/modified documents
2. `poll_meetings` — Check for new meeting transcripts
3. `fetch_comments` — Download and extract comments
4. `analyze_feedback` — LLM categorizes comments (actionable, info, approval)
5. `extract_meetings` — LLM extracts decisions/actions from transcripts
6. `update_source` — Incorporate feedback into .md (gated)
7. `check_readiness` — Verify no TODOs, TBDs remain
8. `republish` — Generate and publish .docx (gated)
9. `notify_reviewers` — Send publication notification
10. `embed` — Update RAG vector store

**Scheduling:**
- Poll interval: 15 minutes (configurable)
- Timeout on gates: 10 minutes per action
- Persistent state via SQLite

---

## Configuration Schema

```yaml
# .doc-workflow.yaml (repo root)

git:
  publish_branches: [main, release/*]
  draft_branches: [feature/*, dev]
  require_clean: true
  require_pushed: true

storage:
  provider: onedrive  # or google, local
  onedrive:
    client_id: ${MS_GRAPH_CLIENT_ID}
    client_secret: ${MS_GRAPH_CLIENT_SECRET}
    tenant_id: ${MS_GRAPH_TENANT_ID}
    draft_folder: /Documents/Drafts/
    published_folder: /Documents/Published/
    archive_folder: /Documents/Published/Archive/

notifications:
  provider: smtp  # or sendgrid, teams
  smtp:
    host: smtp.utexas.edu
    from_address: docflow@utexas.edu

review:
  default_days: 7
  reminders:
    - days_before: 3
    - days_before: 1

embedding:
  enabled: true
  provider: chromadb  # or pinecone, pgvector
  collection: neutron_os_docs

llm:
  provider: anthropic
  model: claude-3-5-haiku-20241022

autonomy:
  default_level: suggest
  actions:
    poll_for_comments: autonomous
    fetch_comments: autonomous
    analyze_feedback: notify
    update_source_file: suggest
    republish_approved_doc: confirm
    republish_new_doc: suggest
```

---

## CLI Commands

```bash
# Publishing
docflow publish docs/prd/foo.md              # Local generation
docflow publish --draft docs/prd/foo.md      # Draft with review
docflow publish --all --changed-only          # Batch publish

# Review management
docflow review list                          # Active reviews
docflow review extend foo --days 3           # Extend deadline
docflow review close foo --outcome approved  # Close review
docflow review incorporate foo               # Apply feedback to .md
docflow review promote foo                   # Draft → Published

# Monitoring
docflow status                               # Overall status
docflow meetings scan                        # Check for new transcripts
docflow check-links                          # Verify all cross-doc links

# Daemon/scheduling
docflow daemon --interval 15m                # Long-running monitor
docflow daemon --schedule "*/15 * * * *"     # Cron expression
```

---

## CI/CD Integration

```yaml
# .gitlab-ci.yml

stages:
  - validate
  - preview
  - publish

validate-docs:
  script:
    - docflow lint
    - docflow check-sync
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

generate-preview:
  script:
    - docflow generate --changed-only --output artifacts/
  artifacts:
    paths: [artifacts/*.docx]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

publish-docs:
  script:
    - docflow publish --changed-only --bump-version
  environment: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  needs: []
```

---

## Implementation Roadmap

### Phase 1: MVP (Weeks 1-2)
- [ ] Core state & config schema
- [ ] Provider base classes + factory
- [ ] OneDrive provider (minimal)
- [ ] Local provider (testing)
- [ ] Link registry & rewriting
- [ ] CLI basics (publish, status)
- **Milestone:** Can publish .md to OneDrive with working links

### Phase 2: Review & Feedback (Weeks 3-4)
- [ ] Draft publication with watermark
- [ ] Review period management
- [ ] DOCX comment extraction
- [ ] ReviewManager (deadline tracking, responses)
- [ ] Feedback incorporation (LLM-assisted)
- [ ] Promotion workflow (draft → published)
- **Milestone:** Complete review cycle working

### Phase 3: Autonomy & Workflows (Weeks 5-6)
- [ ] AutonomyLevel framework
- [ ] ActionGate (human-in-the-loop)
- [ ] Basic LangGraph nodes
- [ ] Polling/scheduling daemon
- [ ] Git integration (branch policies, sync detection)
- **Milestone:** Agents make proposals, humans approve/reject

### Phase 4: Intelligence (Weeks 7-8)
- [ ] Meeting intelligence (transcript → extraction)
- [ ] Meeting → document matching
- [ ] RAG embedding pipeline (ChromaDB)
- [ ] Embedding triggers on commit/publish
- **Milestone:** Document insights flow to RAG

### Phase 5: Polish & Extension (Weeks 9-10)
- [ ] CLI documentation
- [ ] Google Drive provider
- [ ] Unit & integration tests
- [ ] Error handling & recovery
- [ ] Packaging & dependencies
- **Milestone:** Ready for OSS release

---

## TODOs & Known Gaps

### Critical Path
- [ ] Link rewriting must work before beta (users can't handle broken links)
- [ ] Review workflow must be bulletproof (approval gates are critical)
- [ ] Git integration must be foolproof (branch confusion is the problem we're solving)

### Nice-to-Have (Phase 2+)
- [ ] PDF export (some users want PDF)
- [ ] Web dashboard (CLI is powerful but unfriendly)
- [ ] VS Code extension (native editor integration)
- [ ] Slack integration (notifications)
- [ ] Offline mode (queue actions when no network)
- [ ] Conflict resolution (simultaneous edits)
- [ ] Multiple accounts (personal + org OneDrive)
- [ ] OAuth token refresh (long-running daemons)

### Open Questions
1. **Self-hosted Mermaid rendering** — Currently uses mermaid.ink. Need fallback?
2. **Rate limiting** — MS Graph has throttling. How to handle gracefully?
3. **Batch operations** — Publishing 50+ docs efficiently?
4. **Backup strategy** — Archive folder only? Version control in git?
5. **Access control mapping** — Document approval status → SharePoint permissions?

---

## Security Considerations

- **Secrets management:** Use OS keyring, not YAML
- **Token refresh:** OAuth flows for long-lived daemons
- **Data classification:** Support restricted document sharing
- **Audit logging:** All actions logged with attribution
- **Encryption:** Secrets at rest (TBD implementation)

---

## Success Metrics

- [ ] All team .md files publish to OneDrive automatically (no manual upload)
- [ ] Cross-document links work without manual fixing
- [ ] Review feedback incorporated in < 1 day (vs current multi-day)
- [ ] Meeting decisions captured automatically
- [ ] RAG queries return relevant doc excerpts
- [ ] User reports < 2 minutes per publish cycle (vs current 15-20)

---

## Contributors

- Ben Booth (UT Nuclear Engineering) — Lead architect
- TBD

---

## References

- [Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) — Philosophy
- [Kent Beck - TDD](https://www.oreilly.com/library/view/test-driven-development/0321146530/) — Testing principles
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [MS Graph API](https://learn.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0)
- [LangGraph](https://langchain-ai.github.io/langgraph/)

---

*This specification is a living document and will be updated as the system evolves.*
