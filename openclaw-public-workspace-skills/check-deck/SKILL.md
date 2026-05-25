---
name: check-deck
description: |
  Investment banking presentation quality checker. Reviews pitch decks and client-ready
  presentations for: (1) Number consistency across slides, (2) Data-narrative alignment,
  (3) Language polish for IB standards, (4) Formatting QC. Use when asked to review,
  check, or QC any IB presentation, pitch deck, or client materials before delivery.
---

# IB Deck Checker

Perform comprehensive QC on investment banking presentations across four dimensions.



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
output_file = output_dir / f"QC_Report_{date}.md"
```

### Completion Announcement (REQUIRED)

After writing the `.done` file, you MUST announce completion in this exact format:

```
✅ 任务完成，文件已生成：{filename}
```

Example:
```
✅ 任务完成，文件已生成：QC_Report_2026-03-06.md
```

This signals the frontend to display the download card immediately.

**Violation of this rule causes file collisions between concurrent users.**

## Prerequisites

Extract presentation content before checking:
```bash
python -m markitdown presentation.pptx > content.md
```

For visual inspection, convert to images using the `pptx` skill workflow.

## Check Workflow

### 1. Number Consistency

Extract numbers with slide references:
```bash
python scripts/extract_numbers.py content.md --check
```

Verify:
- Key metrics match across all slides (revenue, EBITDA, multiples)
- Calculations are correct (totals, percentages, growth rates)
- Units consistent (same scale used: millions vs billions, % vs bps)
- Unit formatting consistent (e.g., $M vs $MM, $B vs $Bn)
- Time periods aligned (FY vs LTM vs quarterly)

### 2. Data-Narrative Alignment

Map claims to supporting data:
- Trend statements → chart directions
- Market position claims → revenue/share data
- Factual assertions → verify accuracy

Check plausibility (e.g., "#1 player in $100B market" with $200M revenue = 0.2% share).

### 3. Language Polish

Scan for:
- Casual phrasing ("pretty good", "a lot of")
- Vague quantifiers without specifics
- Contractions, exclamation points
- Inconsistent terminology

### 4. Formatting QC

Audit each slide for:
- **Charts**: Source citations, axis labels, legends
- **Typography**: Consistent fonts, size hierarchy
- **Numbers**: Consistent formatting (1,000 vs 1K)
- **Dates**: Consistent format throughout
- **Footnotes**: Proper sourcing and disclaimers

## Output

Present findings using report template.

Categorize by severity:
- **Critical**: Number mismatches, factual errors
- **Important**: Language, narrative alignment
- **Minor**: Formatting inconsistencies

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
    "skill": "check-deck",
    "files": completed_files,
    "file_count": len(completed_files),
    "timestamp": datetime.utcnow().isoformat() + "Z"
}
done_file.write_text(json.dumps(done_data, indent=2))

print(f"✅ Deck check completed: {len(completed_files)} files generated")
print(f"📁 Output directory: {output_dir}")
print(f"📝 Files: {', '.join(completed_files)}")
```

### Rules

1. **Write .done LAST** — after all real files are fully written and renamed
2. **List all files** — the `files` array is the source of truth for frontend
3. **Never include .tmp files** — they should be renamed before writing .done
4. **JSON format** — must be valid JSON for frontend parsing

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
