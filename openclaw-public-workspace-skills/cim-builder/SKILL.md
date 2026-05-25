# CIM Builder

description: Structure and draft a Confidential Information Memorandum for sell-side M&A processes. Organizes company information into a professional, investor-ready document with consistent formatting and narrative flow. Use when preparing sell-side materials, drafting a CIM, or organizing company data for a sale process. Triggers on "CIM", "confidential information memorandum", "offering memorandum", "info memo", "draft CIM", or "sell-side materials".



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
    "skill": "cim-builder",
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
✅ 任务完成，文件已生成：Project_Alpha_CIM_2026-03-06.pptx
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

### Step 1: Gather Source Materials

Ask for available inputs:
- Management presentations
- Historical financials (3-5 years)
- Budget/forecast
- Company website and marketing materials
- Customer data (anonymized if needed)
- Org chart
- Prior presentations or board decks
- Quality of earnings report (if available)

### Step 2: CIM Structure

Standard CIM table of contents:

**I. Executive Summary** (2-3 pages)
- Company overview — what they do, why they win
- Investment highlights (5-7 key selling points)
- Financial summary — headline revenue, EBITDA, growth, margins
- Transaction overview — what's being sold, indicative timeline

**II. Company Overview** (3-5 pages)
- History and founding story
- Mission and value proposition
- Products and services description
- Business model and revenue streams
- Key differentiators and competitive advantages

**III. Industry Overview** (3-5 pages)
- Market size and growth dynamics (TAM/SAM/SOM)
- Key industry trends and tailwinds
- Competitive landscape
- Regulatory environment
- Barriers to entry

**IV. Growth Opportunities** (2-3 pages)
- Organic growth levers (new products, markets, pricing)
- M&A / add-on opportunities
- Operational improvements
- Technology investments
- White space analysis

**V. Customers & Sales** (3-5 pages)
- Customer overview (number, segments, geography)
- Top customer analysis (anonymized if pre-LOI)
- Customer concentration and retention metrics
- Sales process and go-to-market strategy
- Pipeline and backlog

**VI. Operations** (2-3 pages)
- Organizational structure
- Key personnel
- Facilities and geographic footprint
- Technology and systems
- Supply chain / vendor relationships

**VII. Financial Overview** (5-8 pages)
- Historical income statement (3-5 years)
- Revenue analysis — by segment, geography, customer type
- EBITDA bridge and margin analysis
- Balance sheet overview
- Cash flow summary
- Capital expenditure history
- Working capital analysis
- Management forecast / budget (if included)

**VIII. Appendix**
- Detailed financial statements
- Customer list (anonymized)
- Product catalog
- Management bios

### Step 3: Drafting Guidelines

- **Tone**: Professional, factual, compelling but not hyperbolic
- **Narrative**: Tell a story — why this business is attractive, defensible, and positioned for growth
- **Data-driven**: Support every claim with data. "Strong growth" → "Revenue grew at a 15% CAGR from 2021-2024"
- **Visuals**: Charts and graphs for financial trends, market size, competitive positioning
- **Length**: 40-60 pages total — enough detail to inform first-round bids, not so long buyers won't read it
- **Confidentiality**: Include a disclaimer page. Anonymize sensitive customer data unless seller approves

### Step 4: Output

- Word document (.docx) with professional formatting
- Separate Excel appendix with detailed financials
- Charts and exhibits embedded in the document

## Important Notes

- The CIM is a sales document — lead with strengths, but don't hide material issues (buyers will find them in diligence)
- Investment highlights should address the 3 things every buyer cares about: growth potential, margin profile, and defensibility
- Financial normalization / pro forma adjustments should be clearly labeled and explained
- Work with legal on the confidentiality disclaimer and any regulatory disclosures
- Get management to review for factual accuracy before distribution
- The CIM sets expectations on valuation — make sure the narrative supports the asking price
