# Investment Committee Memo

description: Draft a structured investment committee memo for PE deal approval. Synthesizes due diligence findings, financial analysis, and deal terms into a professional IC-ready document. Use when preparing for investment committee, writing up a deal, or creating a formal recommendation. Triggers on "write IC memo", "investment committee memo", "deal write-up", "prepare IC materials", or "recommendation memo".



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
    "skill": "ic-memo",
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
✅ 任务完成，文件已生成：Project_Alpha_IC_Memo_2026-03-06.docx
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

Collect from the user (or from prior analysis in the session):

- Company overview and business description
- Industry/market context
- Historical financials (3-5 years)
- Management assessment
- Deal terms (price, structure, financing)
- Due diligence findings (commercial, financial, legal, operational)
- Value creation plan / 100-day plan
- Returns analysis (base, upside, downside)

### Step 2: Draft Memo Structure

Standard IC memo format:

**I. Executive Summary** (1 page)
- Company description, deal rationale, key terms
- Recommendation and headline returns
- Top 3 risks and mitigants

**II. Company Overview** (1-2 pages)
- Business description, products/services
- Customer base and go-to-market
- Competitive positioning
- Management team

**III. Industry & Market** (1 page)
- Market size and growth
- Competitive landscape
- Secular trends / tailwinds
- Regulatory environment

**IV. Financial Analysis** (2-3 pages)
- Historical performance (revenue, EBITDA, margins, cash flow)
- Quality of earnings adjustments
- Working capital analysis
- Capex requirements

**V. Investment Thesis** (1 page)
- Why this is an attractive investment (3-5 pillars)
- Value creation levers (organic growth, margin expansion, M&A, multiple expansion)
- 100-day priorities

**VI. Deal Terms & Structure** (1 page)
- Enterprise value and implied multiples
- Sources & uses
- Capital structure / leverage
- Key legal terms

**VII. Returns Analysis** (1 page)
- Base, upside, and downside scenarios
- IRR and MOIC across scenarios
- Key assumptions driving returns
- Sensitivity analysis

**VIII. Risk Factors** (1 page)
- Key risks ranked by severity and likelihood
- Mitigants for each risk
- Deal-breaker risks (if any)

**IX. Recommendation**
- Clear recommendation: Proceed / Pass / Conditional proceed
- Key conditions or next steps

### Step 3: Output Format

- Default: Word document (.docx) with professional formatting
- Alternative: Markdown for quick review
- Include tables for financials and returns, not just prose

## Important Notes

- IC memos should be factual and balanced — present both bull and bear cases honestly
- Don't minimize risks. IC members will find them anyway; credibility matters
- Use the firm's standard memo template if the user provides one
- Financial tables should tie — check that EBITDA bridges, S&U balances, and returns math is consistent
- Ask for missing inputs rather than making assumptions on deal terms or returns
