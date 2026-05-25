# Merger Model

description: Build accretion/dilution analysis for M&A transactions. Models pro forma EPS impact, synergy sensitivities, and purchase price allocation. Use when evaluating a potential acquisition, preparing merger consequences analysis for a pitch, or advising on deal terms. Triggers on "merger model", "accretion dilution", "M&A model", "pro forma EPS", "merger consequences", or "deal impact analysis".



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
output_file = output_dir / f"{acquirer}_{target}_Merger_Model_{date}.xlsx"
```

### Completion Announcement (REQUIRED)

After writing the `.done` file, you MUST announce completion in this exact format:

```
✅ 任务完成，文件已生成：{filename}
```

Example:
```
✅ 任务完成，文件已生成：AAPL_MSFT_Merger_Model_2026-03-06.xlsx
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

## Workflow

### Step 1: Gather Inputs

**Acquirer:**
- Company name, current share price, shares outstanding
- LTM and NTM EPS (GAAP and adjusted)
- P/E multiple
- Pre-tax cost of debt, tax rate
- Cash on balance sheet, existing debt

**Target:**
- Company name, current share price, shares outstanding (if public)
- LTM and NTM EPS or net income
- Enterprise value or equity value

**Deal Terms:**
- Offer price per share (or premium to current)
- Consideration mix: % cash vs. % stock
- New debt raised to fund cash portion
- Expected synergies (revenue and cost) and phase-in timeline
- Transaction fees and financing costs
- Expected close date

### Step 2: Purchase Price Analysis

| Item | Value |
|------|-------|
| Offer price per share | |
| Premium to current | |
| Equity value | |
| Plus: net debt assumed | |
| Enterprise value | |
| EV / EBITDA implied | |
| P/E implied | |

### Step 3: Sources & Uses

| Sources | $ | Uses | $ |
|---------|---|------|---|
| New debt | | Equity purchase price | |
| Cash on hand | | Refinance target debt | |
| New equity issued | | Transaction fees | |
| | | Financing fees | |
| **Total** | | **Total** | |

### Step 4: Pro Forma EPS (Accretion / Dilution)

Calculate year-by-year (Year 1-3):

| | Standalone | Pro Forma | Accretion/(Dilution) |
|---|-----------|-----------|---------------------|
| Acquirer net income | | | |
| Target net income | | | |
| Synergies (after tax) | | | |
| Foregone interest on cash (after tax) | | | |
| New debt interest (after tax) | | | |
| Intangible amortization (after tax) | | | |
| Pro forma net income | | | |
| Pro forma shares | | | |
| **Pro forma EPS** | | | |
| **Accretion / (Dilution) %** | | | |

### Step 5: Sensitivity Analysis

**Accretion/Dilution vs. Synergies and Offer Premium:**

| | $0M syn | $25M syn | $50M syn | $75M syn | $100M syn |
|---|---------|----------|----------|----------|-----------|
| 15% premium | | | | | |
| 20% premium | | | | | |
| 25% premium | | | | | |
| 30% premium | | | | | |

**Accretion/Dilution vs. Cash/Stock Mix:**

| | 100% cash | 75/25 | 50/50 | 25/75 | 100% stock |
|---|-----------|-------|-------|-------|------------|
| Year 1 | | | | | |
| Year 2 | | | | | |

### Step 6: Breakeven Synergies

Calculate the minimum synergies needed for the deal to be EPS-neutral in Year 1.

### Step 7: Output

- Excel workbook with:
  - Assumptions tab
  - Sources & uses
  - Pro forma income statement
  - Accretion/dilution summary
  - Sensitivity tables
  - Breakeven analysis
- One-page merger consequences summary for pitch book

## Important Notes

- Always show both GAAP and adjusted (cash) EPS where relevant
- Stock deals: use acquirer's current price for exchange ratio, note dilution from new shares
- Include purchase price allocation — goodwill and intangible amortization matter for GAAP EPS

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
    "skill": "merger-model",
    "files": completed_files,
    "file_count": len(completed_files),
    "timestamp": datetime.utcnow().isoformat() + "Z"
}
done_file.write_text(json.dumps(done_data, indent=2))

print(f"✅ Merger model completed: {len(completed_files)} files generated")
print(f"📁 Output directory: {output_dir}")
print(f"📝 Files: {', '.join(completed_files)}")
```

### Rules

1. **Write .done LAST** — after all real files are fully written and renamed
2. **List all files** — the `files` array is the source of truth for frontend
3. **Never include .tmp files** — they should be renamed before writing .done
4. **JSON format** — must be valid JSON for frontend parsing
- Synergy phase-in is critical — Year 1 is often only 25-50% of run-rate synergies
- Don't forget foregone interest income on cash used and new interest expense on debt raised
- Tax rate on synergies and interest adjustments should match the acquirer's marginal rate
