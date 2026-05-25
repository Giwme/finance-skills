---
name: fsi-strip-profile
description: |
  Creates professional investment banking strip profiles (company profiles) for pitch books, deal materials, and client presentations. Generates 1-4 information-dense slides with quadrant layouts, charts, and tables.
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

### Completion Marker (REQUIRED)

After ALL files are generated:

```python
import json
from pathlib import Path
from datetime import datetime

output_dir = Path(f"/home/ubuntu/.openclaw-public/workspace/{run_id}")
completed_files = [
    f.name for f in output_dir.iterdir() 
    if f.is_file() 
    and not f.name.startswith(".") 
    and not f.name.endswith(".tmp")
    and f.suffix.lower() in [".xlsx", ".pptx", ".docx", ".pdf"]  # 只包含二进制文件，文本内容直接输出
]

done_file = output_dir / ".done"
done_data = {
    "status": "completed",
    "run_id": run_id,
    "skill": "strip-profile",
    "files": completed_files,
    "file_count": len(completed_files),
    "timestamp": datetime.utcnow().isoformat() + "Z"
}
done_file.write_text(json.dumps(done_data, indent=2))
```

### Completion Announcement (REQUIRED)

After writing the `.done` file, you MUST announce completion in this exact format:

```
✅ 任务完成，文件已生成：{filename}
```

Example:
```
✅ 任务完成，文件已生成：CATL_Strip_Profile_2026-03-06.pptx
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

### 0. Data Freshness Check (CRITICAL)

**🚨 TRAINING DATA IS OUTDATED - DO NOT USE FOR FINANCIALS 🚨**

Before researching any company:
1. **Check today's date** and write it down
2. **All financial data must be from web_search**, not training data
3. **Target data freshness**: Use 最新季度优先，其次 FY2025 annual reports, or latest quarterly results
4. **Never use training data cutoff (early 2024)** for revenue, EBITDA, or market cap

### 1. Clarify Requirements
- **Ask the user**: Single-slide or multi-slide (3-4 slides)?
- **Ask the user**: Any specific focus areas or topics to emphasize?
- **Only after user confirms**, proceed to research

### 2. Research & Planning (Use Web Search ONLY)

**⚠️ ALL metrics below must come from web_search, NOT training data:**

**Required Metrics (Latest Available):**
- **Financials**: Revenue, EBITDA, margins (%), EPS, FCF for ±3 years
  - Search query: "[Company] 最新季度优先，其次 FY2025 annual results revenue EBITDA"
  - Verify data date in search results (must be 2024 or 2025)
- **Valuation**: Market Cap, EV, EV/Revenue, EV/EBITDA, P/E multiples
  - Search query: "[Company] market cap valuation [today's date]"
- **Growth**: YoY growth rates (%)
- **Ownership**: Top 5 shareholders with % ownership
- **Segments**: Product mix and/or geographic mix (% breakdown)

**Data Verification Checklist:**
- [ ] All financial numbers include source URL
- [ ] Data date is explicitly stated (e.g., "最新季度" or "FY2025")
- [ ] Market cap is current (within last trading day)
- [ ] No use of training data cutoff knowledge (pre-2024)

### 3. First Page Layout (4-Quadrant)

| Quadrant | Content |
|----------|---------|
| **1 (Top-Left)** | **Company Overview**: HQ, founded, employees, CEO, market cap, ticker |
| **2 (Top-Right)** | **Business & Positioning**: revenue drivers, products, market share, competitive position |
| **3 (Bottom-Left)** | **Key Financials**: Revenue, EBITDA, margins, EPS + Valuation table |
| **4 (Bottom-Right)** | **Stock/Developments**: 1Y stock chart + top shareholders OR recent developments |

### 4. Formatting Standards

**Font Sizes:**
- Slide title: 18-24pt
- Quadrant headers: 14pt
- Body/bullet text: 11pt
- Table text: 10pt
- Source/footer: 8pt

**Visual Elements:**
- Accent bars next to section headers (brand color)
- Horizontal divider between top and bottom quadrants
- Company logo in top-right
- Subtle gridlines in tables

**Information Density:**
- 6-8 bullets per quadrant minimum
- Include specific numbers and percentages
- Add YoY changes: "Revenue: $125M (+28% YoY)"

### 5. Output

- PowerPoint file (.pptx) with 1-4 slides
- 4:3 aspect ratio (standard IB pitch book format)
- Professional formatting with company brand colors

## Important Notes

- Must pass "30-second comprehension test" for busy executives
- Research actual brand colors via web search before creating
- One slide at a time, get user approval before proceeding
- Convert to images for visual validation
