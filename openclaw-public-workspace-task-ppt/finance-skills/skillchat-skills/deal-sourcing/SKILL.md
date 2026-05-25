# Deal Sourcing

description: PE deal sourcing workflow — discover target companies, check prior relationships, and draft personalized founder outreach emails. Use when sourcing new deals, prospecting companies in a sector, or reaching out to founders. Triggers on "find companies", "source deals", "draft founder email", "check if we've seen this company", or "outreach to founder".

## Workflow

This skill follows a 3-step sourcing pipeline:

### Step 1: Discover Companies

Research and identify potential target companies based on the user's criteria:

- **Sector/industry focus**: Ask the user what space they're looking in (e.g., "B2B SaaS in healthcare", "industrial services in the Southeast")
- **Deal parameters**: Revenue range, EBITDA range, growth profile, geography, ownership type (founder-owned, PE-backed, corporate carve-out)
- **Sources**: Use web search to find companies matching criteria. Look at industry reports, conference attendee lists, trade publications, and competitor landscapes
- **Output**: A shortlist of companies with: name, description, estimated revenue/size, location, founder/CEO name, website, and why they fit the thesis

### Step 2: Prior Relationship Check

Before outreach, ask the user to confirm relationship status for each company:

- Ask the user directly: "Have you or your team had any prior contact with [Company]? If yes, please share a brief summary."
- Do NOT attempt to search email, Slack, or any CRM system — these tools are not available in this environment
- Based on the user's response, classify each target:
  - **New** — no prior contact, proceed to outreach
  - **Existing** — prior relationship exists (user to provide context); tailor outreach accordingly
  - **Previously Passed** — user has reviewed before and passed; ask if thesis has changed before re-engaging
- **Output**: A table listing each company with its relationship status and any notes provided by the user

### Step 3: Draft Founder Outreach

Draft personalized cold emails to founders/CEOs for all "New" or "Re-engage" targets:

- **Tone**: Professional but warm. Not overly formal — founders respond better to genuine, concise outreach
- **Structure**:
  1. Brief intro — who you are and your firm (ask user for their firm intro if not known)
  2. Why this company caught your attention — reference something specific (product, market position, growth)
  3. What you're looking for — partnership, not just a transaction
  4. Soft ask — "Would you be open to a brief conversation?"
- **Personalization**: Reference the company's specific product, recent news, or market position. Never use generic templates
- **Length**: 4-6 sentences max. Founders are busy
- **Voice matching**: If the user provides a sample of their prior outreach emails, study them to match their tone and style. Otherwise use a professional but conversational default tone.

### Email Draft Guidelines

- Subject line: Keep it short and specific. Reference the company or sector, not "Investment Opportunity"
- No attachments on first touch
- Include a clear but low-pressure CTA
- Output email drafts as plain text for the user to copy into their email client

## Example Interaction

**User**: "Find me founder-owned industrial services companies in Texas doing $10-50M revenue"

**Assistant**:
1. Searches web for industrial services companies in Texas matching the criteria
2. Presents a shortlist of 5-8 companies with key details
3. Asks user to confirm prior contact status for each
4. Drafts personalized outreach emails for targets marked "New"
5. Presents drafts for user review before any action is taken

## Important Notes

- Always present the shortlist for user review before drafting emails
- Never send emails — output drafts as text only, user handles sending
- If the user's firm intro or investment criteria aren't clear, ask before drafting
- Prioritize quality over quantity — 5 well-researched targets beat 20 generic ones
