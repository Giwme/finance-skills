---
name: earnings-analysis
description: Create professional equity research earnings update reports (8-12 pages, 3,000-5,000 words) analyzing quarterly results for companies already under coverage. Fast-turnaround format focusing on beat/miss analysis, key metrics, updated estimates, and revised thesis. Includes 1-3 summary tables and 8-12 charts. Use when user requests "earnings update", "quarterly update", "earnings analysis", "Q1/Q2/Q3/Q4 results", or post-earnings report.
---

# Equity Research Earnings Update

Create professional **EARNINGS UPDATE REPORTS** analyzing quarterly results for companies already under coverage, following institutional standards (JPMorgan, Goldman Sachs, Morgan Stanley format).

**Key Characteristics:**
- **Length**: 8-12 pages
- **Word Count**: 3,000-5,000 words
- **Tables**: 1-3 summary tables (NOT comprehensive)
- **Figures**: 8-12 charts
- **Turnaround**: 1-2 days (within 24-48 hours of earnings)
- **Audience**: Clients already familiar with the company
- **Focus**: What's NEW - beat/miss, updated estimates, thesis impact
- **Font**: Times New Roman throughout (unless user specifies otherwise)

## When to Use

Use when the user requests:
- "Create an earnings update for [Company] Q3 2024"
- "Analyze [Company]'s quarterly results"
- "Post-earnings report for [Company]"
- "Q1/Q2/Q3/Q4 update for [Company]"

**Do NOT use if:**
- User requests "initiation report" → Use different skill
- User requests "flash note" or "quick take" → Different format
- Company is not already covered → Need initiation first

## Critical Requirements

### 1. Speed & Timeliness
- Publish within 24-48 hours of earnings release
- Focus on NEW information only
- Don't rehash company background extensively

### 2. Data Sources (FREE alternatives)

**MCP sources preferred:** FactSet, S&P Kensho, Daloopa (if available)

**FREE alternatives** ✅:
- **Brave API + web_search** - 已配置，搜索最新财报
- **SEC EDGAR** - 免费 10-Q, 10-K 文件 (https://www.sec.gov/cgi-bin/browse-edgar)
- **公司官网 Earnings/Investor Relations** - 财报发布、电话会议文稿
- **Yahoo Finance / Google Finance** - 股价、共识预期数据
- **Seeking Alpha / Investing.com** - 财报电话会议记录
- **TradingView** - 实时股价、图表

**CRITICAL**: 所有数据必须标注具体来源和日期，带可点击链接。

### 3. Beat/Miss Analysis
- Lead with whether company beat or missed estimates
- Quantify variances (e.g., "Revenue beat by $120M or 3%")
- Explain WHY results differed from expectations

### 4. Summary Format
- Keep tables to 1-3 (summary only, not comprehensive)
- No full P&L/Cash Flow/Balance Sheet (just key metrics)
- Assume reader has seen initiation report

### 5. Citations & Source Attribution ⭐⭐⭐ MANDATORY

**CRITICAL**: Properly cite all data with SPECIFIC sources and CLICKABLE HYPERLINKS.

Include specific citations WITH CLICKABLE LINKS in every figure and table. Required sources:
- ✅ Earnings release (with date and URL)
- ✅ 10-Q filing (with filing date and EDGAR link)
- ✅ Earnings call transcript (with date)
- ✅ Investor presentation/supplemental materials (if available)
- ✅ Consensus estimates source (Bloomberg/FactSet/etc. with date)
- ✅ Prior guidance (from previous quarter's materials)

Reference section must include all earnings materials with clickable hyperlinks. Every figure/table needs source, document name, and date.

### 6. Updated Estimates
- Update forward estimates based on results
- Show old vs. new estimates clearly
- Explain what changed and why

## High-Level Workflow

The earnings update process follows 5 phases:

### Phase 1: Data Collection (30-60 minutes)

**🚨🚨🚨 CRITICAL: TRAINING DATA IS OUTDATED 🚨🚨🚨**

**BEFORE STARTING - COMPLETE THESE 4 STEPS IN ORDER:**
1. **CHECK TODAY'S DATE** - Write down the current date
2. **SEARCH FOR LATEST** - Use web search: "[Company] latest earnings results"
3. **VERIFY THE DATE** - Confirm earnings release is within last 3 months
4. **CHECK TRANSCRIPT DATE** - Verify transcript date matches release date

See [references/workflow.md](references/workflow.md) for detailed search procedures and verification steps.

### Phase 2: Analysis (2-3 hours)
- Beat/miss analysis for each key metric
- Segment/geographic/product breakdown
- Margin and guidance analysis
- Update financial model and estimates

### Phase 3: Chart Generation (1-2 hours)
Create 8-12 charts focusing on quarterly trends and what's new:
- Quarterly revenue progression
- Quarterly EPS progression
- Quarterly margin trends
- Revenue by segment/geography
- Key operating metrics
- Beat/miss summary
- Estimate revisions
- Valuation charts

### Phase 4: Report Creation (2-3 hours)
Create 8-12 page DOCX report. See [references/report-structure.md](references/report-structure.md).

High-level structure:
- Page 1: Earnings summary with rating and price target
- Pages 2-3: Detailed results analysis
- Pages 4-5: Key metrics & guidance
- Pages 6-7: Updated investment thesis
- Pages 8-10: Valuation & estimates
- Pages 11-12: Appendix (optional)

### Phase 5: Quality Check & Delivery (30 minutes)
Verify content, formatting, accuracy, and timeliness. See [references/best-practices.md](references/best-practices.md).

## Output Specification

**Primary Deliverable**: DOCX report (8-12 pages)
**File Name**: `[Company]_Q[Quarter]_[Year]_Earnings_Update.docx`

**Contents:**
- Page 1: Summary with rating, price target, key takeaways
- Pages 2-3: Detailed results analysis
- Pages 4-5: Key metrics and guidance
- Pages 6-7: Updated thesis assessment
- Pages 8-10: Valuation and estimates
- Pages 11-12: Appendix (optional)
- 8-12 embedded charts
- 1-3 summary tables
- Complete sources section with clickable hyperlinks

**Optional Deliverable**: XLS model update (optional for earnings updates)

## Key Differences from Initiation Report

| Aspect | Earnings Update | Initiation Report |
|--------|----------------|-------------------|
| Length | 8-12 pages | 30-50 pages |
| Words | 3,000-5,000 | 10,000-15,000 |
| Tables | 1-3 summary | 12-20 comprehensive |
| Figures | 8-12 | 25-35 |
| Turnaround | 1-2 days | 3-6 weeks |
| Scope | Quarterly results | Complete company |
| Focus | What's NEW | Everything |
| Company Background | Brief mention | 6-10 pages |
| XLS Model | Optional | Required |

## Resources

- [references/workflow.md](references/workflow.md)
- [references/report-structure.md](references/report-structure.md)
- [references/best-practices.md](references/best-practices.md)

## Dependencies

**Required:**
- Python (matplotlib, pandas, seaborn) for chart generation
- DOCX skill or python-docx for report creation

**Optional:**
- XLS skill for model updates
