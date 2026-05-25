---
name: datapack-builder
description: Build professional financial services data packs from various sources including CIMs, offering memorandums, SEC filings, web search, or MCP servers. Extract, normalize, and standardize financial data into investment committee-ready Excel workbooks with consistent structure, proper formatting, and documented assumptions.
---

# Financial Data Pack Builder

Build professional, standardized financial data packs for private equity, investment banking, and asset management.

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
