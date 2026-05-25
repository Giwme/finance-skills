---
name: pitch-deck
description: "Populates investment banking pitch deck templates with data from source files. Use when: user provides a PowerPoint template to fill in, user has source data (Excel/CSV) to populate into slides, user mentions populating or filling a pitch deck template, or user needs to transfer data into existing slide layouts. Not for creating presentations from scratch."
---

# Populating Investment Banking Pitch Deck Templates



---

## 输出规则（CRITICAL）

### 直接输出 vs 生成文件

**默认行为：直接输出文本内容**
- Markdown、纯文本内容 → 直接回复，**不生成 .md 文件**
- 除非用户明确要求"生成文件"、"保存为"、"导出"

**需要生成文件的情况：**
- 生成 Excel (.xlsx)、PPT (.pptx)、Word (.docx)、PDF (.pdf) 等二进制文件
- 用户明确要求："生成 md 文件"、"保存报告"、"导出到文件"
- 内容超过 4000 字符，需要作为附件下载

### .done 文件规则

**.done 文件的 `files` 字段只包含二进制文件：**

```python
# 只将二进制文件计入 completed_files（文本内容直接输出）
completed_files = [
    f.name for f in output_dir.iterdir() 
    if f.is_file() 
    and not f.name.startswith(".") 
    and not f.name.endswith(".tmp")
    and f.suffix.lower() in [".xlsx", ".pptx", ".docx", ".pdf"]  # 只包含二进制文件
]
```

---


## Run ID Isolation (CRITICAL - MUST FOLLOW)

**All file outputs MUST be isolated per request using run_id.**

### Run Context

User messages may contain a marker:

```
[[OPENCLAW_RUN_ID: <run_id>]]
```

**If present, you MUST:**

1. **Extract the run_id** from the marker
2. **When executing any script or generating files, always pass it as:**
   ```
   --run-id <run_id>
   ```
3. **All generated artifacts MUST be written under:**
   ```
   /home/ubuntu/.openclaw-public/workspace/<run_id>/
   ```

**NEVER write artifacts directly into the workspace root.**

### Implementation Pattern

```python
import re
import argparse
from pathlib import Path

# Extract run_id from conversation context
context = """{{user_input}}"""
match = re.search(r'\[\[OPENCLAW_RUN_ID:\s*([a-zA-Z0-9_-]+)\]\]', context)
run_id = match.group(1) if match else 'default'

# Create isolated output directory
workspace = Path("/home/ubuntu/.openclaw-public/workspace")
output_dir = workspace / run_id
output_dir.mkdir(parents=True, exist_ok=True)

# Write all files to this directory
output_file = output_dir / f"Pitch_Deck_{date}.pptx"
```

### Completion Announcement (REQUIRED)

After writing the `.done` file, you MUST announce completion in this exact format:

```
✅ 任务完成，文件已生成：{filename}
```

Example:
```
✅ 任务完成，文件已生成：Pitch_Deck_2026-03-06.pptx
```

This signals the frontend to display the download card immediately.

**Violation of this rule causes file collisions between concurrent users.**

## OpenAI/Codex Tooling Guardrails (Shared)

Apply these rules when using runtime tools (especially with openai-codex/gpt-5.3-codex):

1. Python runtime
- Always use `python3`.
- Never use `python`.

2. web_search language
- For Chinese queries, use `search_lang: "zh-hans"`.
- Do not use `search_lang: "zh"`.
- If language is not critical, omit `search_lang`.

3. web_search execution strategy
- Run searches serially (avoid parallel bursts).
- Use minimum queries needed (typically 3-5).
- Add throttle between calls (~1.2-1.8s).

4. Error auto-recovery
- On 422 with invalid `search_lang`, retry once with `zh-hans`.
- On 429 RATE_LIMITED, back off (wait longer), reduce query count, then retry.

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

---

## Completion Marker (REQUIRED)

**After ALL files are generated, you MUST write a `.done` marker file.**

This signals the frontend that processing is complete and files are ready.

### Implementation

```python
import json
from pathlib import Path
from datetime import datetime

# After all files are generated and atomically renamed
output_dir = Path(f"/home/ubuntu/.openclaw-public/workspace/{run_id}")

# Collect list of completed files (excluding .tmp and hidden files)
completed_files = [
    f.name for f in output_dir.iterdir()
    if f.is_file() 
    and not f.name.startswith('.') 
    and not f.name.endswith('.tmp')
]

# Write completion marker
done_file = output_dir / ".done"
done_data = {
    "status": "completed",
    "run_id": run_id,
    "skill": "pitch-deck",
    "files": completed_files,
    "file_count": len(completed_files),
    "timestamp": datetime.utcnow().isoformat() + "Z"
}
done_file.write_text(json.dumps(done_data, indent=2))

print(f"✅ Pitch deck completed: {len(completed_files)} files generated")
print(f"📁 Output directory: {output_dir}")
print(f"📝 Files: {', '.join(completed_files)}")
```

### Rules

1. **Write .done LAST** — after all real files are fully written and renamed
2. **List all files** — the `files` array is the source of truth for frontend
3. **Never include .tmp files** — they should be renamed before writing .done
4. **JSON format** — must be valid JSON for frontend parsing
