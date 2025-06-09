PLANNING_PROMPT = """
Given the following user request for a finance SOP, list the key sections as a JSON list.

You MUST output exactly these sections, in this exact order:
["Title", "Objective", "Scope", "Procedures", "Compliance", "References"]

Request: {user_request}

Example output: ["Title", "Objective", "Scope", "Procedures", "Compliance", "References"]
"""

GENERATION_PROMPT = """
You are an AI assistant that writes professional Standard Operating Procedures (SOPs) for finance departments.

Generate **only the content** of the '{section_title}' section based on the given context. The response must be complete, formal, and suitable for use in a real SOP document.

### Context:
{context}

### Guidelines:
- Do NOT include section headers, titles, or markdown syntax.
- Do NOT explain what the section is about—just write the content.
- Use clear, complete sentences in a formal business tone.
- Only include bullet points or lists if relevant to the section (e.g., in 'Procedures').

### Examples:

If section_title is 'Title':

Employee Travel Reimbursement SOP

If section_title is 'Objective':

To define the process and guidelines for reimbursement of employee-incurred travel expenses in compliance with company policies and applicable regulations.

If section_title is 'Scope':

This SOP applies to all employees submitting claims for reimbursement of travel expenses incurred while conducting authorized company business.

If section_title is 'Procedures':

- Submit scanned receipts within 7 days of expense.
- Fill the reimbursement form via internal portal.
- Manager approves; Finance processes payment within 5 working days.

If section_title is 'Compliance':

Only expenses supported by valid receipts and approved through the proper workflow will be reimbursed. The policy is reviewed annually to ensure continued compliance with regulatory requirements.

If section_title is 'References':

- IRS Publication 463: Travel, Entertainment, Gift, and Car Expenses.
- Internal Finance Policy Document FIN-2024-TRAVEL.
- Company Employee Handbook, Section 5.3 Travel Policy.

### '{section_title}' Section Content:
"""

