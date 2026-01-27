#!/usr/bin/env python3
"""
Generate All Documentation - Comprehensive batch generator for Neutron OS
Author: Ben
Date: January 22, 2026
"""

import os
import sys
from pathlib import Path
import subprocess
import argparse
from datetime import datetime

# Add the tools directory to path
TOOLS_DIR = Path(__file__).parent
DOCS_DIR = TOOLS_DIR.parent
PROJECT_ROOT = DOCS_DIR.parent

def run_command(cmd, cwd=None):
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def ensure_output_dirs():
    """Create output directory structure."""
    output_dir = TOOLS_DIR / "generated"
    dirs = [
        output_dir,
        output_dir / "specs",
        output_dir / "prd", 
        output_dir / "adr",
        output_dir / "scenarios",
        output_dir / "scenarios" / "superset",
        output_dir / "design-prompts"
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    return output_dir

def find_markdown_files():
    """Find all markdown files to process."""
    files = {
        'specs': [],
        'prd': [],
        'adr': [],
        'scenarios': [],
        'design-prompts': []
    }
    
    # Specs directory
    specs_dir = DOCS_DIR / "specs"
    if specs_dir.exists():
        files['specs'] = list(specs_dir.glob("*.md"))
    
    # PRD directory  
    prd_dir = DOCS_DIR / "prd"
    if prd_dir.exists():
        files['prd'] = list(prd_dir.glob("*.md"))
    
    # ADR directory
    adr_dir = DOCS_DIR / "adr" 
    if adr_dir.exists():
        files['adr'] = list(adr_dir.glob("*.md"))
    
    # Scenarios directory
    scenarios_dir = DOCS_DIR / "scenarios"
    if scenarios_dir.exists():
        for scenario_file in scenarios_dir.rglob("*.md"):
            if "_archive" not in str(scenario_file):
                files['scenarios'].append(scenario_file)
    
    # Design prompts directory
    prompts_dir = DOCS_DIR / "specs" / "design-prompts"
    if prompts_dir.exists():
        files['design-prompts'] = list(prompts_dir.glob("*.md"))
    
    return files

def convert_file(md_path, output_dir, category):
    """Convert a single markdown file to docx."""
    # Determine output path
    rel_path = md_path.relative_to(DOCS_DIR)
    
    if category == 'scenarios':
        # Maintain scenario subdirectory structure
        output_path = output_dir / rel_path.with_suffix('.docx')
    else:
        # Standard category/filename structure
        output_path = output_dir / category / md_path.with_suffix('.docx').name
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Run conversion
    cmd = f'python3 "{TOOLS_DIR}/md_to_docx.py" "{md_path}" "{output_path}"'
    
    # Change to the directory containing the markdown file for proper relative path resolution
    cwd = md_path.parent
    
    print(f"  Converting: {md_path.name} -> {output_path.name}")
    success, output = run_command(cmd, cwd=cwd)
    
    if not success:
        print(f"    ERROR: {output}")
        return False
    
    return True

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Generate all Neutron OS documentation")
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--category', '-c', help='Only process specific category (specs, prd, adr, scenarios)')
    args = parser.parse_args()
    
    print("=" * 70)
    print("NEUTRON OS DOCUMENTATION GENERATOR")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Author: Ben")
    print()
    
    # Setup
    output_dir = ensure_output_dirs()
    print(f"Output directory: {output_dir}")
    print()
    
    # Find files
    files = find_markdown_files()
    
    # Filter by category if specified
    if args.category:
        files = {k: v for k, v in files.items() if k == args.category}
    
    # Statistics
    total_files = sum(len(f) for f in files.values())
    print(f"Found {total_files} markdown files to process")
    for category, file_list in files.items():
        if file_list:
            print(f"  {category}: {len(file_list)} files")
    print()
    
    # Process each category
    success_count = 0
    error_count = 0
    
    for category, file_list in files.items():
        if not file_list:
            continue
            
        print(f"\nProcessing {category.upper()}:")
        print("-" * 40)
        
        for md_file in sorted(file_list):
            if convert_file(md_file, output_dir, category):
                success_count += 1
            else:
                error_count += 1
    
    # Generate special combined documents
    print("\n" + "=" * 40)
    print("GENERATING SPECIAL DOCUMENTS")
    print("=" * 40)
    
    # Master tech spec (already in specs, just ensure it's in the right place)
    master_spec = DOCS_DIR / "specs" / "neutron-os-master-tech-spec.md"
    if master_spec.exists():
        print("\nMaster Technical Specification:")
        if convert_file(master_spec, output_dir, 'specs'):
            success_count += 1
        else:
            error_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"Success: {success_count} files")
    if error_count > 0:
        print(f"Errors: {error_count} files")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # List key generated files
    print("Key Generated Files:")
    key_files = [
        output_dir / "specs" / "neutron-os-master-tech-spec.docx",
        output_dir / "specs" / "neutron-os-executive-summary.docx",
        output_dir / "prd" / "neutron-os-master-prd.docx",
    ]
    
    for key_file in key_files:
        if key_file.exists():
            size = key_file.stat().st_size / (1024 * 1024)  # MB
            print(f"  ✓ {key_file.name} ({size:.1f} MB)")
    
    print("\nAll generated files are in: {}".format(output_dir))
    
    return 0 if error_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())