SUMMARIZER_PROMPT_TEMPLATE = """
Summarize the recent conversation in natural language.
Focus on what changed, what was said, and what the character should know — but do not include direct quotes, names, or any dialogue formatting.
Avoid listing who said what.
Just explain what’s going on in plain terms.

---
            
$conversation
""".strip()

SELECTOR_PROMPT_TEMPLATE = """
You are managing a multi-character conversation. Based on the recent messages and the current situation, choose the next participant who should speak. Consider who has the most reason to respond, take initiative, clarify something, or move the discussion forward.

Available participants:
$participants

Recent messages:
$conversation

Rules:
- Always select exactly one participant from the list.
- Choose the one whose voice is most needed right now.
- Do not explain your choice or provide any commentary.

Return the name of the selected participant only, exactly as it appears in the list.
 """.strip()
