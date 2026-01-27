#!/usr/bin/env python3
"""Diagnose why Mermaid diagrams are failing to render."""

from pathlib import Path
from md_to_docx import parse_markdown_to_blocks, render_mermaid_to_image
import requests
import base64

def test_mermaid_syntax(code: str, use_sanitization: bool = False) -> tuple[bool, str]:
    """Test if mermaid code is valid by trying to render it."""
    try:
        if use_sanitization:
            # Use the same rendering function as md_to_docx.py
            image_data = render_mermaid_to_image(code, use_cache=False)
            if image_data:
                return True, "OK (with sanitization)"
            else:
                return False, "Failed after sanitization"
        else:
            # Direct test without sanitization
            encoded = base64.urlsafe_b64encode(code.encode()).decode()
            
            # Try to render as PNG
            png_url = f"https://mermaid.ink/img/{encoded}?type=png&scale=2"
            response = requests.get(png_url, timeout=10)
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image/'):
                return True, "OK (direct)"
            else:
                return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)[:100]

def main():
    spec_file = Path('../specs/neutron-os-master-tech-spec.md')
    with open(spec_file, 'r') as f:
        content = f.read()
    
    blocks = parse_markdown_to_blocks(content)
    mermaid_blocks = [b for b in blocks if b['type'] == 'mermaid']
    
    print(f"Found {len(mermaid_blocks)} Mermaid diagrams\n")
    print("=" * 70)
    print("Testing WITHOUT sanitization first...\n")
    
    success_direct = 0
    success_sanitized = 0
    failed_diagrams = []
    
    for i, block in enumerate(mermaid_blocks, 1):
        code = block['content'].strip()
        
        # Get first line for identification
        lines = code.split('\n')
        first_line = lines[0][:60] if lines else ""
        
        # Test without sanitization
        is_valid_direct, msg_direct = test_mermaid_syntax(code, use_sanitization=False)
        
        # Test with sanitization
        is_valid_sanitized, msg_sanitized = test_mermaid_syntax(code, use_sanitization=True)
        
        if is_valid_direct:
            success_direct += 1
            status = "✓ DIRECT"
        elif is_valid_sanitized:
            success_sanitized += 1
            status = "✓ SANITIZED"
        else:
            status = "✗ FAILED"
            failed_diagrams.append((i, first_line, msg_direct, code))
        
        print(f"Diagram {i:2d}: {status} - {first_line}")
        if not is_valid_direct and not is_valid_sanitized:
            print(f"            Error: {msg_direct} / {msg_sanitized}")
    
    print("\n" + "=" * 70)
    print(f"Direct render: {success_direct}/{len(mermaid_blocks)} succeeded")
    print(f"With sanitization: {success_direct + success_sanitized}/{len(mermaid_blocks)} succeeded")
    
    if failed_diagrams:
        print(f"\nFailed diagrams ({len(failed_diagrams)}):\n")
        for num, first_line, error, code in failed_diagrams[:3]:  # Show first 3
            print(f"Diagram {num}:")
            print(f"  Error: {error}")
            print(f"  Code preview:")
            for line in code.split('\n')[:5]:  # Show first 5 lines
                print(f"    {line}")
            print()

if __name__ == "__main__":
    main()