---
name: lbo-model
description: This skill should be used when completing LBO (Leveraged Buyout) model templates in Excel for private equity transactions, deal materials, or investment committee presentations. The skill fills in formulas, validates calculations, and ensures professional formatting standards that adapt to any template structure.
---



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


## TEMPLATE REQUIREMENT

**This skill uses templates for LBO models. Always check for an attached template file first.**

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
output_file = output_dir / f"{company}_LBO_Model_{date}.xlsx"
```

### Completion Announcement (REQUIRED)

After writing the `.done` file, you MUST announce completion in this exact format:

```
✅ 任务完成，文件已生成：{filename}
```

Example:
```
✅ 任务完成，文件已生成：AAPL_LBO_Model_2026-03-06.xlsx
```

This signals the frontend to display the download card immediately.

**Violation of this rule causes file collisions between concurrent users.**

Before starting any LBO model:
1. **If a template file is attached/provided**: Use that template's structure exactly
2. **If no template is attached**: Ask the user for a template or use standard template
3. **If using the standard template**: Copy examples/LBO_Model.xlsx as starting point

**IMPORTANT**: When a file like LBO_Model.xlsx is attached, you MUST use it as your template - do not build from scratch.

## Core Principles
* **Every calculation must be an Excel formula** - NEVER compute values in Python and hardcode results
* **Use the template structure** - Follow the organization in the template
* **Use proper cell references** - All formulas should reference appropriate cells
* **Maintain sign convention consistency** - Follow template's sign convention
* **Work section by section** - Complete one section fully before moving to next

## Formula Color Conventions
* **Blue (0000FF)**: Hardcoded inputs - typed numbers
* **Black (000000)**: Formulas with calculations
* **Purple (800080)**: Links to cells on same tab
* **Green (008000)**: Links to cells on different tabs

## Number Formatting Standards
* **Currency**: $#,##0;($#,##0);"-"
* **Percentages**: 0.0% (one decimal)
* **Multiples**: 0.0"x" (one decimal)
* **MOIC/Detailed Ratios**: 0.00"x" (two decimals)
* **All numeric cells**: Right-aligned

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

## Workflow

### Step 1: Template Analysis
- Map the structure - identify where each section lives
- Understand the timeline - which columns represent which periods
- Identify input vs formula cells
- Read existing labels carefully
- Check for existing formulas
- Note template-specific conventions

### Step 2: Filling Formulas
For each cell needing formula:
- Check if cell already has formula
- Check row/column label for expected calculation
- Check user's instructions
- Apply standard LBO modeling conventions if unspecified

### Step 3: Common Problem Areas
- **Balancing Sections**: Identify plug items
- **Tax Calculations**: Reference only relevant income line and tax rate
- **Interest and Circular References**: Use Beginning Balance
- **Debt Paydown/Cash Sweeps**: Respect priority waterfall
- **Returns Calculations**: Check cash flow signs
- **Sensitivity Tables**: Use explicit formulas with mixed references

### Step 4: Verification Checklist
- [ ] Run formula validation: python recalc.py model.xlsx
- [ ] Section balancing checks
- [ ] Income/Operating projections
- [ ] Balance sheet balances
- [ ] Cash flow integrity
- [ ] Returns/Output analysis
- [ ] Sensitivity tables working
- [ ] Formatting standards met
- [ ] Logical sanity checks

## Common Errors to Avoid
- Hardcoding calculated values
- Wrong cell references after copying
- Circular reference errors
- Sections don't balance
- Negative balances where impossible
- IRR/return errors
- Sensitivity table shows same value
- Roll-forwards don't tie
- Inconsistent sign conventions

## Important Notes
- If template structure unclear, ask before proceeding
- If user's requirements conflict with template, confirm preference
- After completing each major section, offer to show work
- If errors found during verification, fix before moving on
- Show your work - explain key formulas when helpful

**This skill produces investment banking-quality LBO models by filling templates with correct formulas, proper formatting, and validated calculations.**

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
    "skill": "lbo-model",
    "files": completed_files,
    "file_count": len(completed_files),
    "timestamp": datetime.utcnow().isoformat() + "Z"
}
done_file.write_text(json.dumps(done_data, indent=2))

print(f"✅ LBO model completed: {len(completed_files)} files generated")
print(f"📁 Output directory: {output_dir}")
print(f"📝 Files: {', '.join(completed_files)}")
```

### Rules

1. **Write .done LAST** — after all real files are fully written and renamed
2. **List all files** — the `files` array is the source of truth for frontend
3. **Never include .tmp files** — they should be renamed before writing .done
4. **JSON format** — must be valid JSON for frontend parsing
