#!/usr/bin/env python3
"""
PDF to Text/Markdown Converter with Comment Extraction
Author: Ben
Date: January 22, 2026

Extracts text content and annotations/comments from PDFs into readable format.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install PyMuPDF")
    sys.exit(1)


def extract_pdf_content(pdf_path: Path, include_comments: bool = True) -> dict:
    """Extract text and comments from a PDF file."""
    doc = fitz.open(pdf_path)
    
    result = {
        'filename': pdf_path.name,
        'pages': [],
        'comments': [],
        'metadata': {}
    }
    
    # Extract metadata (metadata can be None)
    metadata = doc.metadata or {}
    result['metadata'] = {
        'title': metadata.get('title', ''),
        'author': metadata.get('author', ''),
        'subject': metadata.get('subject', ''),
        'pages': len(doc),
        'created': metadata.get('creationDate', ''),
        'modified': metadata.get('modDate', ''),
    }
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_number = page_num + 1  # 1-based for display
        # Extract text
        text: str = page.get_text("text")  # type: ignore[assignment]
        result['pages'].append({
            'number': page_number,
            'text': text.strip()
        })
        
        # Extract annotations/comments
        if include_comments:
            for annot in page.annots() or []:
                annot_type = annot.type[1]  # Type name
                content = annot.info.get('content', '')
                author = annot.info.get('title', '')  # Author is often in 'title'
                created = annot.info.get('creationDate', '')
                
                # Get highlighted/marked text if applicable
                marked_text = ''
                if annot_type in ['Highlight', 'Underline', 'StrikeOut', 'Squiggly']:
                    try:
                        # Get the quad points and extract underlying text
                        quads = annot.vertices
                        if quads:
                            rect = fitz.Rect(quads[0], quads[2])
                            extracted: str = page.get_text("text", clip=rect)  # type: ignore[assignment]
                            marked_text = extracted.strip()
                    except:
                        pass
                
                if content or marked_text:
                    result['comments'].append({
                        'page': page_number,
                        'type': annot_type,
                        'author': author,
                        'content': content,
                        'marked_text': marked_text,
                        'created': created
                    })
    
    doc.close()
    return result


def format_as_markdown(data: dict) -> str:
    """Format extracted data as markdown."""
    lines = []
    
    # Header
    lines.append(f"# {data['filename']}")
    lines.append("")
    lines.append(f"**Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Metadata
    if data['metadata'].get('title'):
        lines.append(f"**Title:** {data['metadata']['title']}")
    if data['metadata'].get('author'):
        lines.append(f"**Author:** {data['metadata']['author']}")
    lines.append(f"**Pages:** {data['metadata']['pages']}")
    lines.append("")
    
    # Comments summary (if any)
    if data['comments']:
        lines.append("---")
        lines.append("")
        lines.append("## 💬 Comments & Annotations")
        lines.append("")
        lines.append(f"*{len(data['comments'])} annotations found*")
        lines.append("")
        
        # Group by author
        by_author = {}
        for c in data['comments']:
            author = c['author'] or 'Unknown'
            if author not in by_author:
                by_author[author] = []
            by_author[author].append(c)
        
        for author, comments in by_author.items():
            lines.append(f"### {author}")
            lines.append("")
            for c in comments:
                lines.append(f"**Page {c['page']}** ({c['type']})")
                if c['marked_text']:
                    lines.append(f"> {c['marked_text']}")
                if c['content']:
                    lines.append(f"")
                    lines.append(f"*{c['content']}*")
                lines.append("")
    
    # Full text content
    lines.append("---")
    lines.append("")
    lines.append("## 📄 Document Content")
    lines.append("")
    
    for page in data['pages']:
        lines.append(f"### Page {page['number']}")
        lines.append("")
        if page['text']:
            lines.append(page['text'])
        else:
            lines.append("*(No extractable text on this page)*")
        lines.append("")
    
    return '\n'.join(lines)


def format_as_text(data: dict) -> str:
    """Format extracted data as plain text."""
    lines = []
    
    lines.append(f"FILE: {data['filename']}")
    lines.append(f"EXTRACTED: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"PAGES: {data['metadata']['pages']}")
    lines.append("=" * 70)
    lines.append("")
    
    # Comments first
    if data['comments']:
        lines.append("COMMENTS & ANNOTATIONS")
        lines.append("-" * 70)
        for c in data['comments']:
            author = c['author'] or 'Unknown'
            lines.append(f"[Page {c['page']}] {author} ({c['type']})")
            if c['marked_text']:
                lines.append(f"  Marked: \"{c['marked_text']}\"")
            if c['content']:
                lines.append(f"  Comment: {c['content']}")
            lines.append("")
        lines.append("=" * 70)
        lines.append("")
    
    # Full text
    lines.append("DOCUMENT CONTENT")
    lines.append("-" * 70)
    for page in data['pages']:
        lines.append(f"\n--- Page {page['number']} ---\n")
        lines.append(page['text'] if page['text'] else "(No text)")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract text and comments from PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_to_text.py document.pdf                    # Output to stdout
  python pdf_to_text.py document.pdf -o output.md      # Save as markdown
  python pdf_to_text.py document.pdf -o output.txt     # Save as text
  python pdf_to_text.py document.pdf --no-comments     # Skip annotations
        """
    )
    parser.add_argument('pdf', type=Path, help='PDF file to process')
    parser.add_argument('-o', '--output', type=Path, help='Output file (default: stdout)')
    parser.add_argument('--format', choices=['md', 'txt', 'auto'], default='auto',
                        help='Output format (default: auto from extension)')
    parser.add_argument('--no-comments', action='store_true', 
                        help='Skip extracting comments/annotations')
    
    args = parser.parse_args()
    
    if not args.pdf.exists():
        print(f"ERROR: File not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)
    
    # Extract content
    print(f"Processing: {args.pdf}", file=sys.stderr)
    data = extract_pdf_content(args.pdf, include_comments=not args.no_comments)
    print(f"  Pages: {data['metadata']['pages']}", file=sys.stderr)
    print(f"  Comments: {len(data['comments'])}", file=sys.stderr)
    
    # Determine format
    fmt = args.format
    if fmt == 'auto':
        if args.output:
            fmt = 'md' if args.output.suffix == '.md' else 'txt'
        else:
            fmt = 'md'
    
    # Format output
    if fmt == 'md':
        output = format_as_markdown(data)
    else:
        output = format_as_text(data)
    
    # Write output
    if args.output:
        args.output.write_text(output, encoding='utf-8')
        print(f"  Output: {args.output}", file=sys.stderr)
    else:
        print(output)
    
    print("Done!", file=sys.stderr)


if __name__ == "__main__":
    main()
