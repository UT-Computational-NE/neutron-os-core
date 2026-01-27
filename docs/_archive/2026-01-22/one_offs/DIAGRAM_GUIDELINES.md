# Diagram Design Guidelines

## Purpose
This document establishes standards for creating diagrams that are suitable for professional documentation and collaboration.

## Space Optimization Rules

### Letter-Size Document Context
When creating diagrams intended for inclusion in Word documents (letter-size: 8.5" × 11"):
- **Standard margins**: 1 inch on all sides
- **Available width**: 6.5 inches
- **Available height**: 9 inches

### Diagram Sizing Requirements

1. **Maximum Vertical Height**: 80% of available vertical space
   - Target: ~7.2 inches (80% of 9 inches)
   - Maximum: Do not exceed this without justification
   - This ensures diagrams fit on a single page with minimal additional text

2. **Width Optimization**: Full available width
   - Target: 6.5 inches (use all available space)
   - Mermaid rendering at `scale=2` creates high-quality output

3. **Text Legibility**:
   - Node/box text must be readable at any zoom level
   - Font sizes in diagrams should scale with scale parameter
   - Avoid cramming too many nodes/elements

### Implementation Approach

When rendering a diagram for Word documents:
```
Diagram Height = 80% of (11 - 2 - margins_for_content) = ~7.2 inches
Diagram Width = 6.5 inches
Mermaid scale = 2 (for quality)
```

### Validation

The md_to_docx converter will:
1. **Render** diagrams with Mermaid scale=2
2. **Check** if rendered height exceeds 7.2 inches
3. **Warn** if oversized but do not force resize (root problem is in diagram design)
4. **Document** which diagrams exceed guidelines in conversion log

## Diagram Types & Considerations

- **Flowcharts**: Break into multiple diagrams if > 20 nodes
- **Architecture**: Use subgraphs to organize layers (keep to 3-5 layers)
- **Timelines/Gantt**: Limit to key phases only
- **Component maps**: Group related items in subgraphs

## Checklist for New Diagrams

- [ ] Diagram fits within 6.5" × 7.2" bounds when rendered at scale=2
- [ ] All text is legible at final size
- [ ] No more than 15-20 main elements visible at once
- [ ] Complex systems are broken into multiple diagrams
- [ ] Subgraph organization is clear and logical
- [ ] Color usage is intentional and aids comprehension

## Tools & Resources

- **Primary**: Mermaid (flowchart, architecture, timeline)
- **Rendering**: mermaid.ink API with `scale=2` parameter
- **Validation**: Run md_to_docx converter to check diagram sizes
- **Output**: 6.5" × variable height (target max 7.2")
