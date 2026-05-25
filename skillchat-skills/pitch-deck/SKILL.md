---
name: pitch-deck
description: "Populates investment banking pitch deck templates with data from source files. Use when: user provides a PowerPoint template to fill in, user has source data (Excel/CSV) to populate into slides, user mentions populating or filling a pitch deck template, or user needs to transfer data into existing slide layouts. Not for creating presentations from scratch."
---

# Populating Investment Banking Pitch Deck Templates

## Workflow Decision Tree

```
┌─ Populating empty template with source data?
│  └─→ Follow "Template Population Workflow" below
│
├─ Editing existing populated slides?
│  └─→ Extract current content, modify, revalidate
│
└─ Fixing formatting issues on existing slides?
   └─→ See "Common Failures" table, apply targeted fixes
```

## Template Population Workflow

### Phase 1: Data Extraction
1. **Create backup** of original template
2. Identify all source materials (Excel, CSV, PDF, Word, web)
3. Extract relevant data points
4. Validate all numbers against original sources
5. Standardize units and currency

### Phase 2: Content Mapping
1. **Open and visually review the template**
2. Analyze template structure
3. Map source data to corresponding template sections
4. Identify placeholder guidance boxes
5. Note any data gaps

### Phase 3: Template Population
1. **Remove or reformat placeholder boxes**
2. Populate each section with mapped content
3. **Then apply formatting** to match template style
4. Create tables as actual table objects
5. Insert company logo if provided

### Phase 4: Validate → Fix → Repeat
```bash
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 150 presentation.pdf slide
```

**Validation checklist:**
- [ ] Text readable against background?
- [ ] Tables are actual objects
- [ ] Charts/tables fill designated areas?
- [ ] Bullet formatting consistent?
- [ ] Font sizes match across same-level boxes?
- [ ] No content beyond slide boundaries?
- [ ] Cross-slide consistency for same metrics

### Phase 5: Final Verification
- All figures match original sources
- No [bracket] placeholders remaining
- All source citations in footnotes
- Text has sufficient contrast
- Recommend user validate in Microsoft PowerPoint

## Critical Anti-Patterns (NEVER DO)

1. **Populating data INTO placeholder boxes** - Delete colored instruction boxes
2. **Text-based "tables"** - Use actual table objects, not pipe/tab separators
3. **Inheriting placeholder contrast** - Use dark text on light backgrounds

## Common Failures

| Failure | Solution |
|---------|----------|
| Unstructured text dumps | Break into bullets |
| Pipe/tab-separated tables | Create actual table objects |
| Poor text/background contrast | Audit every text element |
| Tiny pasted charts | Resize to fill area |
| Inconsistent bullets | Define style once, apply to all |
| Content overflow | Set explicit box widths |

## Final Quality Checklist

- [ ] All figures match source documents
- [ ] No [bracket] placeholders remaining
- [ ] All source citations included
- [ ] Text readable against backgrounds
- [ ] Tables are actual objects
- [ ] Charts fill designated areas
- [ ] Bullet formatting consistent
- [ ] Font sizes match at same hierarchy
- [ ] No content extends beyond boundaries
- [ ] Logo present and positioned
