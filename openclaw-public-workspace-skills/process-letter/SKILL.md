# Process Letter

description: Draft process letters and bid instructions for sell-side M&A processes. Covers initial indication of interest (IOI) instructions, final bid procedures, and management meeting logistics. Triggers on "process letter", "bid instructions", "IOI letter", "bid procedures", "final round letter", or "management meeting invite".



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
    "skill": "process-letter",
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
✅ 任务完成，文件已生成：Project_Alpha_Process_Letter_2026-03-06.docx
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

### Step 1: Determine Letter Type

- **Initial process letter**: Sent with teaser/CIM to outline process and IOI requirements
- **IOI instructions**: Specific requirements for first-round indications
- **Second round / final bid letter**: Instructions for submitting binding offers
- **Management meeting invitation**: Logistics for in-person management presentations

### Step 2: Initial Process Letter / IOI Instructions

**Header:**
- Date, deal code name
- "Confidential"
- Addressed to prospective buyer

**Sections:**

1. **Introduction**: Brief overview of opportunity and seller's objectives
2. **Process Overview**: Timeline, key dates, expected number of rounds
3. **IOI Requirements**:
   - Proposed valuation range (enterprise value)
   - Consideration form (cash, stock, earnout, rollover)
   - Financing sources and certainty
   - Key due diligence requirements
   - Indicative timeline to close
   - Conditions or contingencies
   - Brief description of buyer and strategic rationale
4. **Submission Details**: Where to send, deadline, format
5. **Confidentiality Reminder**: Reference to NDA, data room access
6. **Contact Information**: Banker contacts for questions

### Step 3: Final Bid / Second Round Letter

Additional requirements:

1. **Markup of purchase agreement**: Provide draft SPA/APA and request markup
2. **Detailed financing commitments**: Committed financing letters required
3. **Remaining diligence items**: Specify confirmatory diligence expected
4. **Exclusivity terms**: Duration and conditions
5. **Regulatory analysis**: Antitrust filing requirements
6. **Key personnel terms**: Employment agreements, compensation, rollover
7. **Binding vs. non-binding**: Clarify what is binding at this stage
8. **Evaluation criteria**: How bids will be evaluated

### Step 4: Management Meeting Invitation

1. **Logistics**: Date, time, location, duration
2. **Attendees**: Who from company will present, who from buyer should attend
3. **Agenda**: Typical management presentation agenda
4. **Ground rules**: No recording, confidentiality, questions format
5. **Materials**: What will be distributed
6. **Follow-up**: Process for submitting additional questions

### Step 5: Output

- Word document (.docx) with professional letter formatting
- Firm letterhead placeholder
- Track changes version for client review

## Important Notes

- Process letters set the tone for the entire deal — be clear, professional, organized
- Deadlines should be firm but reasonable — 2-3 weeks for IOIs, 3-4 weeks for final bids
- Always include evaluation criteria — buyers want to know how they'll be judged
- Coordinate with legal on any representations or commitments
- Client should review and approve before sending
- Keep a log of who received each letter and when
