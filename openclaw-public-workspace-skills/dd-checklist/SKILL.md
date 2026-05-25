# Due Diligence Checklist

description: Generate and track comprehensive due diligence checklists tailored to the target company's sector, deal type, and complexity. Covers all major workstreams with request lists, status tracking, and red flag escalation. Use when kicking off diligence, organizing a data room review, or tracking outstanding items. Triggers on "dd checklist", "due diligence tracker", "diligence request list", "what do we still need", or "data room review".



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
    "skill": "dd-checklist",
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
✅ 任务完成，文件已生成：DD_Checklist_2026-03-06.xlsx
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

### Step 1: Scope the Diligence

Ask the user for:
- **Target company**: Name, sector, business model
- **Deal type**: Platform acquisition, add-on, growth equity, recap, carve-out
- **Deal size / complexity**: Determines depth of diligence
- **Key concerns**: Any known issues to prioritize (customer concentration, regulatory, environmental, etc.)
- **Timeline**: When is LOI / close targeted?

### Step 2: Generate Workstream Checklists

Generate a checklist across all major workstreams, tailored to the sector:

**Financial Due Diligence**
- Quality of earnings (QoE) — revenue and EBITDA adjustments
- Working capital analysis — normalized vs. actual
- Debt and debt-like items
- Capital expenditure (maintenance vs. growth)
- Tax structure and exposure
- Audit history and accounting policies
- Pro forma adjustments (run-rate, synergies)

**Commercial Due Diligence**
- Market size and growth (TAM/SAM/SOM)
- Competitive positioning and market share
- Customer analysis — concentration, retention, NPS
- Pricing power and contract structure
- Sales pipeline and backlog
- Go-to-market effectiveness

**Legal Due Diligence**
- Corporate structure and org chart
- Material contracts (customer, supplier, partnership)
- Litigation history and pending claims
- IP portfolio and protection
- Regulatory compliance
- Employment agreements and non-competes

**Operational Due Diligence**
- Management team assessment
- Organizational structure and key person risk
- IT systems and infrastructure
- Supply chain and vendor dependencies
- Facilities and real estate
- Insurance coverage

**HR / People Due Diligence**
- Org chart and headcount trends
- Compensation benchmarking
- Benefits and pension obligations
- Key employee retention risk
- Culture assessment
- Union/labor agreements

**IT / Technology Due Diligence** (for tech-enabled businesses)
- Technology stack and architecture
- Technical debt assessment
- Cybersecurity posture
- Data privacy compliance (GDPR, CCPA, SOC2)
- Product roadmap and R&D spend
- Scalability assessment

**Environmental / ESG** (where applicable)
- Environmental liabilities
- Regulatory compliance history
- ESG risks and opportunities

### Step 3: Status Tracking

For each item, track:

| Item | Workstream | Priority | Status | Owner | Notes |
|------|-----------|----------|--------|-------|-------|
| QoE report | Financial | P0 | Pending | | |
| Customer interviews | Commercial | P0 | In Progress | | 3 of 10 complete |

Status options: Not Started → Requested → Received → In Review → Complete → Red Flag

### Step 4: Red Flag Summary

Maintain a running list of red flags discovered during diligence:
- What was found
- Which workstream
- Severity (deal-breaker / significant / manageable)
- Mitigant or path to resolution
- Impact on valuation or deal terms

### Step 5: Output

- Excel workbook with tabs per workstream (default)
- Summary dashboard: % complete by workstream, outstanding items, red flags
- Weekly status update format for deal team

## Sector-Specific Additions

Automatically add relevant items based on sector:
- **Software/SaaS**: ARR quality, cohort analysis, hosting costs, SOC2
- **Healthcare**: Regulatory approvals, reimbursement risk, payor mix
- **Industrial**: Equipment condition, environmental remediation, safety record
- **Financial services**: Regulatory capital, compliance history, credit quality
- **Consumer**: Brand health, channel mix, seasonality, inventory management

## Important Notes

- Prioritize P0 items that are gating to LOI or close
- Flag items where the seller is slow to respond — may indicate issues
- Cross-reference data room contents against the checklist to identify gaps
- Update the checklist as diligence progresses — it's a living document
