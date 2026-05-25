---
name: datapack-builder
description: Build professional financial services data packs from various sources including CIMs, offering memorandums, SEC filings, web search, or MCP servers. Extract, normalize, and standardize financial data into investment committee-ready Excel workbooks with consistent structure, proper formatting, and documented assumptions.
---

# Financial Data Pack Builder

Build professional, standardized financial data packs for private equity, investment banking, and asset management.



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
output_file = output_dir / f"{company}_DataPack_{date}.xlsx"
```

### Completion Announcement (REQUIRED)

After writing the `.done` file, you MUST announce completion in this exact format:

```
✅ 任务完成，文件已生成：{filename}
```

Example:
```
✅ 任务完成，文件已生成：CATL_DataPack_2026-03-06.xlsx
```

This signals the frontend to display the download card immediately.

**Violation of this rule causes file collisions between concurrent users.**

## CRITICAL SUCCESS FACTORS

### 1. Data Accuracy (Zero Tolerance)
- Trace every number to source with page reference
- Use formula-based calculations exclusively
- Cross-check subtotals and totals
- Verify balance sheet balances
- Confirm cash flow ties to balance sheet

### 2. Formatting Rules

**RULE 1: Financial data → Currency format with $**
Revenue, EBITDA, Profit, Cash, Debt, Assets → $#,##0.0
Negatives: $(123.0) NOT -$123

**RULE 2: Operational data → Number format, NO $**
Units, Stores, Employees, Customers → #,##0

**RULE 3: Percentages → 0.0% format**
Margins, Growth, Rates → 15.0% NOT 0.15

**RULE 4: Years → Text format**
2020, 2021, 2022 NOT 2,024

**RULE 5: Use formulas for all calculations**
Never hardcode calculated values

### 3. Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs
- **Black text (RGB: 0,0,0)**: Formulas and calculations
- **Green text (RGB: 0,128,0)**: Links to other sheets

## Standard 8-Tab Structure

1. **Executive Summary** - One-page overview
2. **Historical Financials** - Income Statement
3. **Balance Sheet**
4. **Cash Flow Statement**
5. **Operating Metrics** - Non-financial KPIs
6. **Property/Segment Performance** - If applicable
7. **Market Analysis** - Industry context
8. **Investment Highlights** - Investment thesis

## STEP-BY-STEP WORKFLOW

### Phase 1: Document Processing
- Access source materials
- Extract financial statements (3-5 years)
- Extract operating metrics
- Extract market data
- Note transaction context

### Phase 2: Data Normalization
- Standardize line item names
- Identify one-time charges
- Create Adjusted EBITDA reconciliation
- Document all adjustments

### Phase 3: Build Excel Workbook
- Create 8-tab structure
- Apply formatting rules
- Insert formulas for calculations
- Add professional presentation

### Phase 4: Scenario Building (if projections)
- **Management Case**: Company projections as provided
- **Base Case**: Risk-adjusted, conservative adjustments
- **Downside Case**: Stress test scenario

### Phase 5: Quality Control
- Data accuracy checks
- Format consistency checks
- Structure completeness checks
- Professional presentation checks

### Phase 6: Final Delivery
- Create executive summary
- Save with proper naming: CompanyName_DataPack_YYYY-MM-DD.xlsx

## FINAL DELIVERY CHECKLIST

**Structure:**
- [ ] All 8 tabs present and sequenced
- [ ] Executive summary fits on one page

**Data:**
- [ ] All numbers trace to source
- [ ] All calculations are formula-based
- [ ] Balance sheet balances
- [ ] No formula errors

**Formatting:**
- [ ] Financial data has $ signs
- [ ] Operational data has NO $ signs
- [ ] Percentages formatted correctly
- [ ] Years display without commas
- [ ] Negatives in parentheses

**Documentation:**
- [ ] Normalization adjustments explained
- [ ] Source citations included
- [ ] Assumptions documented
- [ ] Filename follows convention

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
    "skill": "datapack-builder",
    "files": completed_files,
    "file_count": len(completed_files),
    "timestamp": datetime.utcnow().isoformat() + "Z"
}
done_file.write_text(json.dumps(done_data, indent=2))

print(f"✅ Data pack completed: {len(completed_files)} files generated")
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
