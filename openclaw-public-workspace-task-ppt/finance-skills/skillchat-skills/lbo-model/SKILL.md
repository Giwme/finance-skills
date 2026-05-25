---
name: lbo-model
description: This skill should be used when completing LBO (Leveraged Buyout) model templates in Excel for private equity transactions, deal materials, or investment committee presentations. The skill fills in formulas, validates calculations, and ensures professional formatting standards that adapt to any template structure.
---

## TEMPLATE REQUIREMENT

**This skill uses templates for LBO models. Always check for an attached template file first.**

Before starting any LBO model:
1. **If a template file is attached/provided**: Use that template's structure exactly
2. **If no template is attached**: Ask the user for a template or use standard template
3. **If using the standard template**: Copy examples/LBO_Model.xlsx as starting point

**IMPORTANT**: When a file like LBO_Model.xlsx is attached, you MUST use it as your template - do not build from scratch.

## Core Principles
* **Every calculation must be an Excel formula** - NEVER compute values in Python and hardcode results
* **Use the template structure** - Follow the organization in the template
* **Use proper cell references** - All formulas should reference appropriate cells
* **Maintain sign convention consistency** - Follow template's sign convention
* **Work section by section** - Complete one section fully before moving to next

## Formula Color Conventions
* **Blue (0000FF)**: Hardcoded inputs - typed numbers
* **Black (000000)**: Formulas with calculations
* **Purple (800080)**: Links to cells on same tab
* **Green (008000)**: Links to cells on different tabs

## Number Formatting Standards
* **Currency**: $#,##0;($#,##0);"-"
* **Percentages**: 0.0% (one decimal)
* **Multiples**: 0.0"x" (one decimal)
* **MOIC/Detailed Ratios**: 0.00"x" (two decimals)
* **All numeric cells**: Right-aligned

## Workflow

### Step 1: Template Analysis
- Map the structure - identify where each section lives
- Understand the timeline - which columns represent which periods
- Identify input vs formula cells
- Read existing labels carefully
- Check for existing formulas
- Note template-specific conventions

### Step 2: Filling Formulas
For each cell needing formula:
- Check if cell already has formula
- Check row/column label for expected calculation
- Check user's instructions
- Apply standard LBO modeling conventions if unspecified

### Step 3: Common Problem Areas
- **Balancing Sections**: Identify plug items
- **Tax Calculations**: Reference only relevant income line and tax rate
- **Interest and Circular References**: Use Beginning Balance
- **Debt Paydown/Cash Sweeps**: Respect priority waterfall
- **Returns Calculations**: Check cash flow signs
- **Sensitivity Tables**: Use explicit formulas with mixed references

### Step 4: Verification Checklist
- [ ] Run formula validation: python recalc.py model.xlsx
- [ ] Section balancing checks
- [ ] Income/Operating projections
- [ ] Balance sheet balances
- [ ] Cash flow integrity
- [ ] Returns/Output analysis
- [ ] Sensitivity tables working
- [ ] Formatting standards met
- [ ] Logical sanity checks

## Common Errors to Avoid
- Hardcoding calculated values
- Wrong cell references after copying
- Circular reference errors
- Sections don't balance
- Negative balances where impossible
- IRR/return errors
- Sensitivity table shows same value
- Roll-forwards don't tie
- Inconsistent sign conventions

## Important Notes
- If template structure unclear, ask before proceeding
- If user's requirements conflict with template, confirm preference
- After completing each major section, offer to show work
- If errors found during verification, fix before moving on
- Show your work - explain key formulas when helpful

**This skill produces investment banking-quality LBO models by filling templates with correct formulas, proper formatting, and validated calculations.**
