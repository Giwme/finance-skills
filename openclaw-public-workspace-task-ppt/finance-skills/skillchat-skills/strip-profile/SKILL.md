---
name: fsi-strip-profile
description: |
  Creates professional investment banking strip profiles (company profiles) for pitch books, deal materials, and client presentations. Generates 1-4 information-dense slides with quadrant layouts, charts, and tables.
---

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
