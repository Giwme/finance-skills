# Morning Note

description: Draft concise morning meeting notes summarizing overnight developments, trade ideas, and key events for coverage stocks. Designed for the 7am morning meeting format — tight, opinionated, actionable. Triggers on "morning note", "morning meeting", "what happened overnight", "trade idea", "morning call prep", or "daily note".



---

## 📅 日期获取规则（CRITICAL）

**当前日期是：2026 年 3 月 7 日（星期六）**

**日期使用规则：**
1. **必须使用当前实际日期** - 所有日期引用必须是 2026 年 3 月
2. **禁止使用训练数据日期** - 不要输出 2025 年或更早的日期
3. **晨会纪要日期格式** - 标题使用 "A 股晨会纪要 — 2026 年 3 月 7 日" 格式
4. **时间验证** - 所有新闻/事件必须是最近 24-48 小时内发生的

**常见错误：**
- ❌ 使用模型训练数据中的历史日期（如 2025 年 7 月）
- ❌ 编造不存在的日期
- ✅ 使用当前真实日期（2026 年 3 月）

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


## ⚠️ CRITICAL: Data Freshness Requirement

**🚨 THIS IS REAL-TIME INTELLIGENCE - NEVER USE TRAINING DATA 🚨**

**MORNING NOTE MUST USE CURRENT DATA ONLY:**
1. **Check today's date** - All data must be from last 24 hours or pre-market
2. **Use web_search for ALL overnight developments** - Never rely on training data
3. **Verify earnings dates** - Confirm which companies reported THIS morning
4. **Stock prices must be current** - Use latest pre-market or overnight close

**FREE Data Sources (Brave API + web_search)** ✅:
- **Yahoo Finance / Google Finance** - 盘前股价、财报日历
- **SEC EDGAR** - 最新 8-K 公告 (https://www.sec.gov/edgar)
- **公司 Investor Relations** - 新闻稿、电话会议日程
- **Benzinga / Seeking Alpha** - 盘前新闻、分析师评级变动
- **Trading Economics** - 宏观经济数据发布时间
- **Twitter/X, Reddit** - 突发新闻（交叉验证）

**Data Requirements:**
- [ ] Earnings reported overnight: verify exact date and quarter
- [ ] Stock moves: use current prices (not training data)
- [ ] News: limit to last 12-24 hours only
- [ ] Macro data: today's scheduled releases only

**COMMON MISTAKE**: Using historical earnings from training data instead of searching for what happened OVERNIGHT.

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
    "skill": "morning-note",
    "files": completed_files,
    "file_count": len(completed_files),
    "timestamp": datetime.utcnow().isoformat() + "Z"
}
done_file.write_text(json.dumps(done_data, indent=2))
```

**Violation of this rule causes file collisions between concurrent users.**

## Tooling Hard Constraints (CRITICAL)

1. **Python command**
   - Always use `python3`.
   - Never use `python` (may not exist in runtime).

2. **web_search language parameter**
   - For Chinese queries, always set `search_lang: "zh-hans"`.
   - Do not use `search_lang: "zh"` (invalid for Brave API).

3. **web_search execution policy (serial + throttle)**
   - Execute web searches **serially**, not in parallel.
   - Keep searches to the minimum needed (usually 3-5 queries total).
   - Add throttle between calls: wait ~1.2-1.8s between `web_search` requests.
   - If `429 RATE_LIMITED` appears, stop burst calls, wait longer, then retry with fewer queries.

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

### Step 1: Overnight Developments

Scan for relevant events across coverage universe:

**Earnings & Guidance**
- Any coverage companies reporting overnight or pre-market?
- Earnings surprises (beat/miss on revenue, EPS, key metrics)
- Guidance changes (raised, lowered, maintained)

**News & Events**
- M&A announcements or rumors
- Management changes
- Product launches or regulatory decisions
- Analyst upgrades/downgrades from competitors
- Macro data or policy changes affecting the sector

**Market Context**
- Overnight futures / pre-market moves
- Sector ETF performance
- Relevant commodity or currency moves
- Key economic data releases today

### Step 2: Morning Note Format

Keep it tight — a morning note should be readable in 2 minutes:

---

**[Date] Morning Note — [Analyst Name]**
**[Sector Coverage]**

**Top Call: [Headline — the one thing PMs need to hear]**
- 2-3 sentences on the key development and why it matters
- Stock impact: price target, rating reiteration/change

**Overnight/Pre-Market Developments**
- [Company A]: One-line summary of earnings/news + our take
- [Company B]: One-line summary + our take
- [Sector/Macro]: Relevant sector-wide development

**Key Events Today**
- [Time]: [Company] earnings call
- [Time]: Economic data release (expectations vs. our view)
- [Time]: Conference or investor day

**Trade Ideas** (if any)
- [Long/Short] [Company]: 1-2 sentence thesis + catalyst
- Risk: What would make this wrong

---

### Step 3: Quick Takes on Earnings

If a coverage company reported, provide a quick reaction:

| Metric | Consensus | Actual | Beat/Miss |
|--------|-----------|--------|-----------|
| Revenue | | | |
| EPS | | | |
| [Key metric] | | | |
| Guidance | | | |

**Our Take**: 2-3 sentences — is this good or bad for the stock? Does it change our thesis?

**Action**: Maintain / Upgrade / Downgrade rating? Adjust price target?

### Step 4: Output

**默认：直接输出 Markdown 内容**
除非用户明确要求"生成文件"、"保存为 Word"或"导出"，否则直接回复 Markdown 格式的 morning note。

**直接输出示例：**
```
**[Date] Morning Note — [Analyst Name]**
**[Sector Coverage]**

**Top Call: [Headline]**
...
```

**需要生成文件的情况：**
- 用户明确要求生成 Word 文档
- 需要作为附件发送邮件
- 内容超长需要下载

**输出格式选项：**
- Markdown text for email/Slack distribution ← 默认
- Word document if formal distribution is needed ← 仅当用户要求
- Keep to 1 page max — PMs and traders won't read more

## Important Notes

- Be opinionated — morning notes that just summarize news without a view are useless
- Lead with the most important thing — don't bury the headline
- "No news" is a valid morning note — say "nothing material overnight, maintaining positioning"
- Distinguish between actionable events (earnings, M&A) and noise (minor analyst notes, non-events)
- Time-stamp your takes — if you're writing at 6am, note that pre-market may change by open
- If you're wrong, own it in the next morning note — credibility matters more than being right every time
