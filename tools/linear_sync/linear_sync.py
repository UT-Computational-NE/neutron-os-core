#!/usr/bin/env python3
"""
Linear Sync Tool for TRIGA Digital Twin Roadmap

This script manages bi-directional sync between:
- Strategy documentation (Markdown files)
- Linear project management (via GraphQL API)

Usage:
    python linear_sync.py --list-teams          # Find your team ID
    python linear_sync.py --export-all          # Initial export to Linear
    python linear_sync.py --export-new          # Export only new initiatives
    python linear_sync.py --import              # Import status from Linear
    python linear_sync.py --csv                 # Export to CSV for manual import
    python linear_sync.py --detect-changes      # Scan codebase for new features
"""

import os
import re
import json
import csv
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    exit(1)

# Configuration
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
SYNC_STATE_FILE = SCRIPT_DIR / "sync_state.json"
INITIATIVES_FILE = SCRIPT_DIR / "initiatives.json"

LINEAR_API_URL = "https://api.linear.app/graphql"


def load_config() -> dict:
    """Load configuration from config.json."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def load_sync_state() -> dict:
    """Load current sync state."""
    if SYNC_STATE_FILE.exists():
        with open(SYNC_STATE_FILE) as f:
            return json.load(f)
    return {"initiatives": {}, "last_sync": None}


def save_sync_state(state: dict):
    """Save sync state to file."""
    state["last_sync"] = datetime.now().isoformat()
    with open(SYNC_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_api_key() -> Optional[str]:
    """Get Linear API key from environment."""
    key = os.environ.get("LINEAR_API_KEY")
    if not key:
        print("ERROR: LINEAR_API_KEY environment variable not set")
        print("Get your API key from: https://linear.app/settings/account/security")
        return None
    return key


def graphql_request(query: str, variables: dict = None, api_key: str = None) -> dict:
    """Make a GraphQL request to Linear API."""
    if not api_key:
        api_key = get_api_key()
    if not api_key:
        return {"errors": [{"message": "No API key"}]}
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    response = requests.post(LINEAR_API_URL, json=payload, headers=headers)
    return response.json()


def list_teams(api_key: str = None):
    """List all teams in the workspace."""
    query = """
    query Teams {
        teams {
            nodes {
                id
                name
                key
            }
        }
    }
    """
    result = graphql_request(query, api_key=api_key)
    
    if "errors" in result:
        print(f"Error: {result['errors']}")
        return
    
    print("\nAvailable Teams:")
    print("-" * 50)
    for team in result.get("data", {}).get("teams", {}).get("nodes", []):
        print(f"  {team['name']} ({team['key']})")
        print(f"    ID: {team['id']}")
    print()
    print("Copy the ID and add it to config.json as 'linear_team_id'")


def extract_initiatives_from_docs() -> list:
    """Parse strategy docs to extract all initiatives."""
    config = load_config()
    # Support both new okrs_file path and legacy strategy_docs_path
    if "okrs_file" in config:
        okrs_file = SCRIPT_DIR / config["okrs_file"]
    else:
        docs_path = SCRIPT_DIR / config.get("strategy_docs_path", "../")
        okrs_file = docs_path / "04_okrs_goals.md"
    
    if not okrs_file.exists():
        print(f"ERROR: OKRs file not found: {okrs_file}")
        return []
    
    with open(okrs_file) as f:
        content = f.read()
    
    initiatives = []
    current_quarter = None
    current_track = None
    
    # Parse the quarterly roadmap section
    lines = content.split("\n")
    in_roadmap = False
    in_objective = False
    current_objective = None
    
    for i, line in enumerate(lines):
        # Detect quarterly roadmap section
        if "## Quarterly Roadmap Summary" in line:
            in_roadmap = True
            continue
        
        if in_roadmap:
            # Quarter headers like "### Q1 2026: Foundation"
            quarter_match = re.match(r"### (Q[1-4] 202[67]):", line)
            if quarter_match:
                current_quarter = quarter_match.group(1).replace(" ", "-")
                continue
            
            # Items in quarterly roadmap (bulleted)
            if line.strip().startswith("- ") and current_quarter:
                item_text = line.strip()[2:].strip()
                # Bold items are isotope-related
                is_isotope = "**" in item_text
                item_text = item_text.replace("**", "")
                
                initiative_id = hashlib.md5(f"{current_quarter}:{item_text}".encode()).hexdigest()[:8]
                
                initiatives.append({
                    "id": initiative_id,
                    "title": item_text,
                    "quarter": current_quarter,
                    "track": "Isotope" if is_isotope else "Pipeline",
                    "source": "quarterly_roadmap",
                    "priority": 2 if is_isotope else 3,
                })
        
        # Detect objectives sections (for more detailed initiatives)
        objective_match = re.match(r"## Objective (\d+): (.+)", line)
        if objective_match:
            in_roadmap = False  # Exit roadmap section
            in_objective = True
            objective_num = objective_match.group(1)
            objective_name = objective_match.group(2)
            
            # Map objectives to tracks
            track_mapping = {
                "1": "Pipeline",     # Trusted Automated Operations
                "2": "Pipeline",     # Near-Real-Time Insights
                "3": "Accuracy",     # Validated Simulation Accuracy
                "4": "Adoption",     # Active User Community
                "5": "Compliance",   # Compliance Automation
                "6": "Isotope",      # Medical Isotope Production
                "7": "Commercial",   # Commercialization Foundation
            }
            current_track = track_mapping.get(objective_num, "Pipeline")
            current_objective = objective_name
            continue
        
        # Supporting initiatives (checkbox items)
        if in_objective and line.strip().startswith("- [ ]"):
            item_text = line.strip()[6:].strip()
            initiative_id = hashlib.md5(f"{current_track}:{item_text}".encode()).hexdigest()[:8]
            
            # Determine quarter based on objective
            # (This is simplified - in practice you'd parse the timeline column)
            quarter = "Q1-2026"  # Default
            
            initiatives.append({
                "id": initiative_id,
                "title": item_text,
                "quarter": quarter,
                "track": current_track,
                "source": f"objective_{current_objective}",
                "priority": 3,
                "objective": current_objective,
            })
        
        # Completed checkbox items
        if in_objective and line.strip().startswith("- [x]"):
            item_text = line.strip()[6:].strip()
            initiative_id = hashlib.md5(f"{current_track}:{item_text}".encode()).hexdigest()[:8]
            
            initiatives.append({
                "id": initiative_id,
                "title": item_text,
                "quarter": "Q1-2026",
                "track": current_track,
                "source": f"objective_{current_objective}",
                "priority": 3,
                "objective": current_objective,
                "completed": True,
            })
    
    # Save extracted initiatives
    with open(INITIATIVES_FILE, "w") as f:
        json.dump({"initiatives": initiatives, "extracted_at": datetime.now().isoformat()}, f, indent=2)
    
    print(f"Extracted {len(initiatives)} initiatives from strategy docs")
    return initiatives


def create_linear_project(api_key: str, team_id: str, name: str) -> Optional[str]:
    """Create a Linear project and return its ID."""
    query = """
    mutation CreateProject($input: ProjectCreateInput!) {
        projectCreate(input: $input) {
            success
            project {
                id
                name
            }
        }
    }
    """
    
    variables = {
        "input": {
            "name": name,
            "teamIds": [team_id],
            "description": "Roadmap initiatives from TRIGA Digital Twin strategy documentation",
        }
    }
    
    result = graphql_request(query, variables, api_key)
    
    if result.get("data", {}).get("projectCreate", {}).get("success"):
        project = result["data"]["projectCreate"]["project"]
        print(f"Created project: {project['name']} (ID: {project['id']})")
        return project["id"]
    else:
        print(f"Failed to create project: {result}")
        return None


def create_linear_label(api_key: str, team_id: str, name: str, color: str) -> Optional[str]:
    """Create a Linear label and return its ID."""
    query = """
    mutation CreateLabel($input: IssueLabelCreateInput!) {
        issueLabelCreate(input: $input) {
            success
            issueLabel {
                id
                name
            }
        }
    }
    """
    
    variables = {
        "input": {
            "name": name,
            "color": color,
            "teamId": team_id,
        }
    }
    
    result = graphql_request(query, variables, api_key)
    
    if result.get("data", {}).get("issueLabelCreate", {}).get("success"):
        label = result["data"]["issueLabelCreate"]["issueLabel"]
        return label["id"]
    return None


def get_or_create_labels(api_key: str, team_id: str, config: dict) -> dict:
    """Get existing labels or create them, return mapping of name -> ID."""
    # First, fetch existing labels
    query = """
    query TeamLabels($teamId: String!) {
        team(id: $teamId) {
            labels {
                nodes {
                    id
                    name
                }
            }
        }
    }
    """
    
    result = graphql_request(query, {"teamId": team_id}, api_key)
    existing_labels = {}
    
    for label in result.get("data", {}).get("team", {}).get("labels", {}).get("nodes", []):
        existing_labels[label["name"]] = label["id"]
    
    label_mapping = {}
    
    # Create quarter labels
    for quarter, props in config.get("labels", {}).get("quarters", {}).items():
        if quarter in existing_labels:
            label_mapping[quarter] = existing_labels[quarter]
        else:
            label_id = create_linear_label(api_key, team_id, quarter, props["color"])
            if label_id:
                label_mapping[quarter] = label_id
    
    # Create track labels
    for track, props in config.get("labels", {}).get("tracks", {}).items():
        if track in existing_labels:
            label_mapping[track] = existing_labels[track]
        else:
            label_id = create_linear_label(api_key, team_id, track, props["color"])
            if label_id:
                label_mapping[track] = label_id
    
    return label_mapping


def create_linear_issue(api_key: str, team_id: str, initiative: dict, 
                       project_id: str = None, label_ids: list = None) -> Optional[str]:
    """Create a Linear issue for an initiative."""
    query = """
    mutation CreateIssue($input: IssueCreateInput!) {
        issueCreate(input: $input) {
            success
            issue {
                id
                identifier
                title
                url
            }
        }
    }
    """
    
    description = f"""## Initiative from Strategy Docs

**Source:** `{initiative.get('source', 'unknown')}`
**Quarter:** {initiative.get('quarter', 'TBD')}
**Track:** {initiative.get('track', 'General')}

---

{initiative.get('description', '')}

---

_Auto-imported from TRIGA Digital Twin strategy documentation_
_See: [docs/strategy/04_okrs_goals.md](https://github.com/YOUR_ORG/TRIGA_Digital_Twin/blob/main/docs/strategy/04_okrs_goals.md)_
"""
    
    variables = {
        "input": {
            "title": initiative["title"],
            "description": description,
            "teamId": team_id,
            "priority": initiative.get("priority", 3),
        }
    }
    
    if project_id:
        variables["input"]["projectId"] = project_id
    
    if label_ids:
        variables["input"]["labelIds"] = label_ids
    
    result = graphql_request(query, variables, api_key)
    
    if result.get("data", {}).get("issueCreate", {}).get("success"):
        issue = result["data"]["issueCreate"]["issue"]
        print(f"  ✓ Created: {issue['identifier']} - {issue['title'][:50]}...")
        return issue["id"]
    else:
        print(f"  ✗ Failed: {initiative['title'][:50]}... - {result.get('errors', 'Unknown error')}")
        return None


def export_all_to_linear():
    """Export all initiatives to Linear."""
    api_key = get_api_key()
    if not api_key:
        return
    
    config = load_config()
    team_id = config.get("linear_team_id")
    
    if not team_id or team_id == "YOUR_TEAM_ID_HERE":
        print("ERROR: Please configure linear_team_id in config.json")
        print("Run: python linear_sync.py --list-teams")
        return
    
    # Extract initiatives from docs
    initiatives = extract_initiatives_from_docs()
    if not initiatives:
        print("No initiatives found in strategy docs")
        return
    
    # Create project
    project_name = config.get("project_name", "TRIGA Digital Twin Roadmap")
    project_id = create_linear_project(api_key, team_id, project_name)
    
    # Get or create labels
    print("\nSetting up labels...")
    label_mapping = get_or_create_labels(api_key, team_id, config)
    
    # Create issues
    print(f"\nCreating {len(initiatives)} issues in Linear...")
    sync_state = load_sync_state()
    
    for initiative in initiatives:
        # Skip if already synced
        if initiative["id"] in sync_state["initiatives"]:
            print(f"  → Skipping (exists): {initiative['title'][:50]}...")
            continue
        
        # Determine labels
        label_ids = []
        if initiative.get("quarter") in label_mapping:
            label_ids.append(label_mapping[initiative["quarter"]])
        if initiative.get("track") in label_mapping:
            label_ids.append(label_mapping[initiative["track"]])
        
        # Create issue
        issue_id = create_linear_issue(
            api_key, team_id, initiative, 
            project_id=project_id, 
            label_ids=label_ids
        )
        
        if issue_id:
            sync_state["initiatives"][initiative["id"]] = {
                "linear_id": issue_id,
                "title": initiative["title"],
                "synced_at": datetime.now().isoformat(),
            }
    
    save_sync_state(sync_state)
    print(f"\nDone! Sync state saved to {SYNC_STATE_FILE}")


def export_to_csv():
    """Export initiatives to CSV for manual import."""
    initiatives = extract_initiatives_from_docs()
    if not initiatives:
        print("No initiatives found")
        return
    
    csv_file = SCRIPT_DIR / "initiatives_export.csv"
    
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Description", "Priority", "Labels"])
        
        for init in initiatives:
            labels = f"{init.get('quarter', '')}, {init.get('track', '')}"
            description = f"Source: {init.get('source', 'strategy_docs')}"
            if init.get('objective'):
                description += f"\nObjective: {init['objective']}"
            
            writer.writerow([
                init["title"],
                description,
                init.get("priority", 3),
                labels
            ])
    
    print(f"Exported {len(initiatives)} initiatives to: {csv_file}")
    print("\nTo import into Linear:")
    print("1. Go to Linear Settings > Workspace > Import")
    print("2. Choose 'CSV' import")
    print("3. Upload the CSV file")


def import_from_linear():
    """Import issue statuses from Linear to update docs."""
    api_key = get_api_key()
    if not api_key:
        return
    
    sync_state = load_sync_state()
    if not sync_state["initiatives"]:
        print("No synced initiatives found. Run --export-all first.")
        return
    
    print(f"Checking status of {len(sync_state['initiatives'])} issues...")
    
    # Get all issue IDs
    issue_ids = [v["linear_id"] for v in sync_state["initiatives"].values()]
    
    # Fetch issue statuses (batch query)
    query = """
    query IssueStatuses($ids: [String!]!) {
        issues(filter: { id: { in: $ids } }) {
            nodes {
                id
                title
                state {
                    name
                    type
                }
                completedAt
            }
        }
    }
    """
    
    result = graphql_request(query, {"ids": issue_ids}, api_key)
    
    if "errors" in result:
        print(f"Error fetching issues: {result['errors']}")
        return
    
    completed = []
    in_progress = []
    
    for issue in result.get("data", {}).get("issues", {}).get("nodes", []):
        state_type = issue.get("state", {}).get("type", "")
        
        if state_type == "completed" or issue.get("completedAt"):
            completed.append(issue["title"])
        elif state_type == "started":
            in_progress.append(issue["title"])
    
    print(f"\n✓ Completed: {len(completed)}")
    for title in completed[:5]:
        print(f"  - {title[:60]}...")
    if len(completed) > 5:
        print(f"  ... and {len(completed) - 5} more")
    
    print(f"\n→ In Progress: {len(in_progress)}")
    for title in in_progress[:5]:
        print(f"  - {title[:60]}...")
    
    save_sync_state(sync_state)
    print(f"\nSync state updated: {SYNC_STATE_FILE}")


def detect_codebase_changes():
    """Scan codebase for new features that might need documentation."""
    repo_root = SCRIPT_DIR.parent.parent.parent
    
    print("Scanning codebase for recent changes...")
    print(f"Repository: {repo_root}")
    
    # Areas to scan
    scan_paths = [
        repo_root / "triga_dt_website" / "routes",
        repo_root / "triga_modsim_tools",
        repo_root / "netl_pxi",
    ]
    
    recent_files = []
    
    for scan_path in scan_paths:
        if scan_path.exists():
            for py_file in scan_path.rglob("*.py"):
                # Check if file was modified recently (last 30 days)
                mtime = datetime.fromtimestamp(py_file.stat().st_mtime)
                if (datetime.now() - mtime).days < 30:
                    recent_files.append((py_file, mtime))
    
    if recent_files:
        print(f"\nRecently modified files ({len(recent_files)}):")
        for f, mtime in sorted(recent_files, key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {f.relative_to(repo_root)} - {mtime.strftime('%Y-%m-%d')}")
        
        print("\n💡 Consider updating strategy docs if these represent new features:")
        print("   - docs/strategy/01_mission_objectives.md")
        print("   - docs/strategy/04_okrs_goals.md")
    else:
        print("No recent changes detected")


def main():
    parser = argparse.ArgumentParser(
        description="Sync TRIGA Digital Twin roadmap with Linear"
    )
    parser.add_argument("--list-teams", action="store_true", 
                       help="List available Linear teams")
    parser.add_argument("--export-all", action="store_true",
                       help="Export all initiatives to Linear")
    parser.add_argument("--export-new", action="store_true",
                       help="Export only new initiatives")
    parser.add_argument("--import", dest="do_import", action="store_true",
                       help="Import status from Linear")
    parser.add_argument("--csv", action="store_true",
                       help="Export to CSV for manual import")
    parser.add_argument("--detect-changes", action="store_true",
                       help="Scan codebase for new features")
    parser.add_argument("--extract", action="store_true",
                       help="Extract initiatives from docs (no API)")
    
    args = parser.parse_args()
    
    if args.list_teams:
        list_teams()
    elif args.export_all:
        export_all_to_linear()
    elif args.export_new:
        # Same as export_all but respects existing sync state
        export_all_to_linear()
    elif args.do_import:
        import_from_linear()
    elif args.csv:
        export_to_csv()
    elif args.detect_changes:
        detect_codebase_changes()
    elif args.extract:
        extract_initiatives_from_docs()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
