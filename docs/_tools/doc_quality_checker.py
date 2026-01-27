#!/usr/bin/env python3
"""
Documentation Quality Checker and Fixer

Comprehensive tool for auditing and fixing Markdown documentation issues:
- Mermaid diagram color/contrast problems
- Missing heading markers (e.g., " 1. Title" → "## 1. Title")
- linkStyle consistency in flowcharts

Can be run repeatedly as part of CI/CD or regular documentation maintenance.
Works with any Markdown documentation directory.
"""

import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import argparse
from dataclasses import dataclass
from enum import Enum

class IssueType(Enum):
    """Types of documentation issues we can detect and fix."""
    MISSING_COLOR = "missing_color"
    LIGHT_ON_LIGHT = "light_on_light"
    DARK_ON_DARK = "dark_on_dark"
    MISSING_LINKSTYLE = "missing_linkstyle"
    WRONG_ARROW_COLOR = "wrong_arrow_color"
    LONG_SUBGRAPH_TITLE = "long_subgraph_title"
    WRONG_STROKE_WIDTH = "wrong_stroke_width"
    MISSING_HEADING_MARKER = "missing_heading_marker"

@dataclass
class Issue:
    """Represents a documentation quality issue."""
    file_path: Path
    issue_type: IssueType
    line_number: int
    description: str
    current_text: str
    suggested_fix: str
    
class MermaidColors:
    """Color definitions and contrast rules for Mermaid diagrams."""
    
    # Light backgrounds that need dark text (#000000)
    LIGHT_BACKGROUNDS = {
        '#e1f5fe', '#e3f2fd', '#e8f5e9', '#fce4ec', '#f3e5f5',
        '#fff3e0', '#e0f2f1', '#f5f5f5', '#c8e6c9', '#ffecb3',
        '#fff9c4', '#f1f8e9', '#ede7f6', '#fffde7', '#ffebee',
        '#ffcdd2', '#f8bbd0', '#e1bee7', '#d1c4e9', '#c5cae9',
        '#bbdefb', '#b3e5fc', '#b2ebf2', '#b2dfdb', '#c8e6c9',
        '#dcedc8', '#fff', '#ffffff', '#fafafa'
    }
    
    # Dark backgrounds that need light text (#ffffff or #fff)
    DARK_BACKGROUNDS = {
        '#1976d2', '#388e3c', '#f57c00', '#7b1fa2', '#c2185b',
        '#0d47a1', '#1b5e20', '#e65100', '#4a148c', '#880e4f',
        '#263238', '#1565c0', '#00897b', '#424242', '#bf360c',
        '#455a64', '#2e7d32', '#c62828', '#d32f2f', '#b71c1c',
        '#37474f', '#5d4037', '#3e2723', '#212121'
    }
    
    # Standard arrow color and width
    ARROW_COLOR = '#777777'
    ARROW_WIDTH = '3px'
    
    @classmethod
    def needs_dark_text(cls, bg_color: str) -> bool:
        """Check if a background color needs dark text."""
        return bg_color.lower() in cls.LIGHT_BACKGROUNDS
    
    @classmethod
    def needs_light_text(cls, bg_color: str) -> bool:
        """Check if a background color needs light text."""
        return bg_color.lower() in cls.DARK_BACKGROUNDS

class DocQualityChecker:
    """Main class for checking and fixing documentation quality issues."""
    
    def __init__(self, docs_dir: Path, fix_mode: bool = False, verbose: bool = False):
        self.docs_dir = docs_dir
        self.fix_mode = fix_mode
        self.verbose = verbose
        self.issues: List[Issue] = []
        
    def scan_all(self) -> List[Issue]:
        """Scan all markdown files for issues."""
        self.issues = []
        
        for md_file in sorted(self.docs_dir.glob('**/*.md')):
            # Skip generated files and backups
            if any(part in str(md_file) for part in ['_tools/generated', '.backup', '_old']):
                continue
                
            if self.verbose:
                print(f"Scanning: {md_file.relative_to(self.docs_dir)}")
                
            self.scan_file(md_file)
        
        return self.issues
    
    def scan_file(self, file_path: Path) -> None:
        """Scan a single file for issues."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for missing heading markers
        self.check_headings(file_path, content)
        
        # Find all mermaid blocks
        mermaid_pattern = r'```mermaid\n(.*?)\n```'
        
        for match in re.finditer(mermaid_pattern, content, re.DOTALL):
            diagram = match.group(1)
            start_pos = match.start(1)
            
            # Calculate line number for better reporting
            line_number = content[:start_pos].count('\n') + 1
            
            self.check_diagram(file_path, diagram, line_number)
    
    def check_diagram(self, file_path: Path, diagram: str, start_line: int) -> None:
        """Check a single mermaid diagram for issues."""
        lines = diagram.split('\n')
        
        # Check for missing linkStyle
        if 'linkStyle' not in diagram and any('-->' in line or '---' in line for line in lines):
            self.add_issue(
                file_path, IssueType.MISSING_LINKSTYLE, start_line + len(lines),
                "Diagram has connections but no linkStyle definition",
                "",
                f"linkStyle default stroke:{MermaidColors.ARROW_COLOR},stroke-width:{MermaidColors.ARROW_WIDTH}"
            )
        
        # Check each line
        for i, line in enumerate(lines):
            line_num = start_line + i
            
            # Check style statements
            if 'style ' in line:
                self.check_style_line(file_path, line, line_num)
            
            # Check linkStyle statements
            if 'linkStyle' in line:
                self.check_linkstyle_line(file_path, line, line_num)
            
            # Check subgraph titles
            if 'subgraph ' in line:
                self.check_subgraph_title(file_path, line, line_num)
    
    def check_style_line(self, file_path: Path, line: str, line_num: int) -> None:
        """Check a style line for color issues."""
        # Parse style statement
        style_match = re.search(r'style\s+(\w+)\s+fill:(#\w+)', line)
        if not style_match:
            return
        
        node_name = style_match.group(1)
        fill_color = style_match.group(2).lower()
        
        # Check if color property exists
        has_color = 'color:' in line
        
        if not has_color:
            # Missing color property
            if MermaidColors.needs_dark_text(fill_color):
                self.add_issue(
                    file_path, IssueType.MISSING_COLOR, line_num,
                    f"Node '{node_name}' with light background {fill_color} missing text color",
                    line.strip(),
                    self.add_color_to_style(line, '#000000')
                )
            elif MermaidColors.needs_light_text(fill_color):
                self.add_issue(
                    file_path, IssueType.MISSING_COLOR, line_num,
                    f"Node '{node_name}' with dark background {fill_color} missing text color",
                    line.strip(),
                    self.add_color_to_style(line, '#ffffff')
                )
        else:
            # Has color, check if it's correct
            color_match = re.search(r'color:(#\w+)', line)
            if color_match:
                text_color = color_match.group(1).lower()
                
                # Check for contrast issues
                if MermaidColors.needs_dark_text(fill_color) and text_color not in ['#000000', '#000']:
                    self.add_issue(
                        file_path, IssueType.LIGHT_ON_LIGHT, line_num,
                        f"Light text {text_color} on light background {fill_color}",
                        line.strip(),
                        re.sub(r'color:#\w+', 'color:#000000', line.strip())
                    )
                elif MermaidColors.needs_light_text(fill_color) and text_color not in ['#ffffff', '#fff']:
                    self.add_issue(
                        file_path, IssueType.DARK_ON_DARK, line_num,
                        f"Dark text {text_color} on dark background {fill_color}",
                        line.strip(),
                        re.sub(r'color:#\w+', 'color:#ffffff', line.strip())
                    )
    
    def check_linkstyle_line(self, file_path: Path, line: str, line_num: int) -> None:
        """Check linkStyle for correct arrow properties."""
        # Check stroke color
        if 'stroke:' in line:
            stroke_match = re.search(r'stroke:(#\w+)', line)
            if stroke_match:
                stroke_color = stroke_match.group(1).lower()
                if stroke_color != MermaidColors.ARROW_COLOR.lower():
                    self.add_issue(
                        file_path, IssueType.WRONG_ARROW_COLOR, line_num,
                        f"Arrow color {stroke_color} should be {MermaidColors.ARROW_COLOR}",
                        line.strip(),
                        re.sub(r'stroke:#\w+', f'stroke:{MermaidColors.ARROW_COLOR}', line.strip())
                    )
        
        # Check stroke width
        if 'stroke-width:' in line:
            width_match = re.search(r'stroke-width:(\d+px)', line)
            if width_match:
                width = width_match.group(1)
                if width != MermaidColors.ARROW_WIDTH:
                    self.add_issue(
                        file_path, IssueType.WRONG_STROKE_WIDTH, line_num,
                        f"Arrow width {width} should be {MermaidColors.ARROW_WIDTH}",
                        line.strip(),
                        re.sub(r'stroke-width:\d+px', f'stroke-width:{MermaidColors.ARROW_WIDTH}', line.strip())
                    )
    
    def check_subgraph_title(self, file_path: Path, line: str, line_num: int) -> None:
        """Check subgraph titles for excessive length."""
        # Extract title between quotes
        title_match = re.search(r'subgraph\s+\w+\["([^"]+)"\]', line)
        if title_match:
            title = title_match.group(1)
            # Remove HTML breaks for length calculation
            clean_title = title.replace('<br/>', ' ').replace('<br>', ' ')
            
            if len(clean_title) > 35:
                self.add_issue(
                    file_path, IssueType.LONG_SUBGRAPH_TITLE, line_num,
                    f"Subgraph title too long ({len(clean_title)} chars): '{clean_title[:50]}...'",
                    line.strip(),
                    f"Consider shortening to under 35 characters"
                )
    
    def check_headings(self, file_path: Path, content: str) -> None:
        """Check for lines that look like headings but are missing # markers."""
        lines = content.split('\n')
        
        # Track if we're inside a code block
        in_code_block = False
        
        for i, line in enumerate(lines):
            line_num = i + 1
            
            # Track code blocks to skip them
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                continue
            
            # Skip if already a proper heading
            if line.startswith('#'):
                continue
            
            # Skip empty lines
            if not line.strip():
                continue
            
            # Pattern: " 1. Executive Summary" → "## 1. Executive Summary"
            m = re.match(r'^ (\d+)\. (.+)$', line)
            if m:
                self.add_issue(
                    file_path, IssueType.MISSING_HEADING_MARKER, line_num,
                    f"H2 section missing '#' marker: '{m.group(1)}. {m.group(2)}'",
                    line,
                    f'## {m.group(1)}. {m.group(2)}'
                )
                continue
            
            # Pattern: " 1.1 Digital Twin" → "### 1.1 Digital Twin"
            m = re.match(r'^ (\d+\.\d+) (.+)$', line)
            if m:
                self.add_issue(
                    file_path, IssueType.MISSING_HEADING_MARKER, line_num,
                    f"H3 subsection missing '#' marker: '{m.group(1)} {m.group(2)}'",
                    line,
                    f'### {m.group(1)} {m.group(2)}'
                )
                continue
            
            # Pattern: " 3.2.1 Bronze Layer" → "#### 3.2.1 Bronze Layer"
            m = re.match(r'^ (\d+\.\d+\.\d+) (.+)$', line)
            if m:
                self.add_issue(
                    file_path, IssueType.MISSING_HEADING_MARKER, line_num,
                    f"H4 subsubsection missing '#' marker: '{m.group(1)} {m.group(2)}'",
                    line,
                    f'#### {m.group(1)} {m.group(2)}'
                )
                continue
    
    def add_color_to_style(self, line: str, color: str) -> str:
        """Add color property to a style line."""
        # If there's a stroke property, add color before it
        if ',stroke:' in line:
            return re.sub(r'(,stroke:)', f',color:{color}\\1', line.strip())
        # Otherwise add at the end
        else:
            return line.strip().rstrip() + f',color:{color}'
    
    def add_issue(self, file_path: Path, issue_type: IssueType, line_num: int,
                  description: str, current: str, fix: str) -> None:
        """Add an issue to the list."""
        self.issues.append(Issue(
            file_path=file_path,
            issue_type=issue_type,
            line_number=line_num,
            description=description,
            current_text=current,
            suggested_fix=fix
        ))
    
    def fix_issues(self) -> int:
        """Apply fixes to all found issues."""
        if not self.fix_mode:
            print("Fix mode not enabled. Use --fix to apply changes.")
            return 0
        
        # Group issues by file
        issues_by_file: Dict[Path, List[Issue]] = {}
        for issue in self.issues:
            if issue.file_path not in issues_by_file:
                issues_by_file[issue.file_path] = []
            issues_by_file[issue.file_path].append(issue)
        
        total_fixed = 0
        for file_path, file_issues in issues_by_file.items():
            # Sort by line number (reverse) to fix from bottom to top
            file_issues.sort(key=lambda i: i.line_number, reverse=True)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            file_fixed = 0
            for issue in file_issues:
                if issue.issue_type in [IssueType.MISSING_COLOR, IssueType.LIGHT_ON_LIGHT, 
                                       IssueType.DARK_ON_DARK, IssueType.WRONG_ARROW_COLOR,
                                       IssueType.WRONG_STROKE_WIDTH]:
                    # Apply line-level fixes
                    line_idx = issue.line_number - 1
                    if 0 <= line_idx < len(lines):
                        old_line = lines[line_idx].strip()
                        if old_line == issue.current_text:
                            # Calculate indentation
                            indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())
                            lines[line_idx] = ' ' * indent + issue.suggested_fix + '\n'
                            file_fixed += 1
                elif issue.issue_type == IssueType.MISSING_HEADING_MARKER:
                    # Replace the line with the corrected heading
                    line_idx = issue.line_number - 1
                    if 0 <= line_idx < len(lines):
                        # Compare the full line (with leading space)
                        if lines[line_idx].rstrip('\n') == issue.current_text:
                            lines[line_idx] = issue.suggested_fix + '\n'
                            file_fixed += 1
                elif issue.issue_type == IssueType.MISSING_LINKSTYLE:
                    # Add linkStyle at the end of the diagram
                    # Find the end of the mermaid block before this line
                    for i in range(issue.line_number - 1, -1, -1):
                        if '```' in lines[i] and i > 0:
                            # Insert before the closing ```
                            lines.insert(i, f"    {issue.suggested_fix}\n")
                            file_fixed += 1
                            break
            
            # Write back the fixed content
            if file_fixed > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"✓ Fixed {file_fixed} issues in {file_path.relative_to(self.docs_dir)}")
                total_fixed += file_fixed
        
        return total_fixed
    
    def report(self) -> None:
        """Generate a report of found issues."""
        if not self.issues:
            print("✅ No issues found! Documentation quality check passed.")
            return
        
        # Group by issue type
        by_type: Dict[IssueType, List[Issue]] = {}
        for issue in self.issues:
            if issue.issue_type not in by_type:
                by_type[issue.issue_type] = []
            by_type[issue.issue_type].append(issue)
        
        print(f"\n{'='*70}")
        print(f"DOCUMENTATION QUALITY REPORT")
        print(f"{'='*70}")
        print(f"Total issues found: {len(self.issues)}")
        print()
        
        for issue_type, issues in by_type.items():
            print(f"\n{issue_type.value.replace('_', ' ').title()}: {len(issues)} issues")
            print("-" * 50)
            
            # Group by file
            by_file: Dict[Path, List[Issue]] = {}
            for issue in issues:
                if issue.file_path not in by_file:
                    by_file[issue.file_path] = []
                by_file[issue.file_path].append(issue)
            
            for file_path, file_issues in by_file.items():
                rel_path = file_path.relative_to(self.docs_dir)
                print(f"\n  📄 {rel_path}")
                for issue in file_issues[:3]:  # Show max 3 issues per file
                    print(f"    Line {issue.line_number}: {issue.description}")
                    if self.verbose:
                        print(f"      Current: {issue.current_text[:60]}...")
                        print(f"      Fix: {issue.suggested_fix[:60]}...")
                if len(file_issues) > 3:
                    print(f"    ... and {len(file_issues) - 3} more")
        
        print(f"\n{'='*70}")
        auto_fixable = [i for i in self.issues if i.issue_type != IssueType.LONG_SUBGRAPH_TITLE]
        print(f"Run with --fix to automatically fix {len(auto_fixable)} issues")
        print(f"Manual fixes needed: {len([i for i in self.issues if i.issue_type == IssueType.LONG_SUBGRAPH_TITLE])}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Documentation Quality Checker - Audit and fix Markdown/Mermaid issues"
    )
    # Default to parent directory (assumes tool is in _tools/ subdirectory)
    default_dir = Path(__file__).parent.parent
    parser.add_argument(
        '--docs-dir',
        type=Path,
        default=default_dir,
        help='Documentation directory to scan (default: parent of script directory)'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Apply fixes automatically (where possible)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--type',
        choices=[t.value for t in IssueType],
        help='Check only specific issue type'
    )
    
    args = parser.parse_args()
    
    if not args.docs_dir.exists():
        print(f"Error: Documentation directory not found: {args.docs_dir}")
        sys.exit(1)
    
    checker = DocQualityChecker(args.docs_dir, args.fix, args.verbose)
    
    print(f"Scanning documentation in: {args.docs_dir}")
    issues = checker.scan_all()
    
    if args.type:
        # Filter to specific issue type
        issues = [i for i in issues if i.issue_type.value == args.type]
        checker.issues = issues
    
    if args.fix and issues:
        fixed = checker.fix_issues()
        print(f"\n✅ Fixed {fixed} issues")
    else:
        checker.report()
    
    # Exit with error code if issues found (useful for CI/CD)
    sys.exit(1 if issues and not args.fix else 0)

if __name__ == '__main__':
    main()