SELECTOR_PROMPT_TEMPLATE = """
You are managing a multi-character conversation. Based on the recent messages and the current situation, choose the next participant who should speak. Consider who has the most reason to respond, take initiative, clarify something, or move the discussion forward.

Available participants:
$participants

Recent messages:
$messages

Rules:
- Always select exactly one participant from the list.
- Choose the one whose voice is most needed right now.
- Do not explain your choice or provide any commentary.

Return the name of the selected participant only, exactly as it appears in the list.
 """.strip()

REPORTER_PROMPT_TEMPLATE = """
You are a conversation reporter assigned to assist the participant named **$participant**.

The following conversation is a dialogue between other participants that occurred **since $participant last spoke**.

Your job is to write a short, natural-language briefing that helps $participant understand what was said.

- Write directly to $participant, using “you” when appropriate.
- Preserve the meaning and intent of each message, but rephrase in plain language.
- Keep all names except $participant, which should become “you”.
- Do not copy, quote, or imitate dialogue formatting (e.g., "Name: ...").
- Your report should be roughly one sentence per message unless merging is natural.
- Do not invent or assume information that wasn't stated.

Keep the style simple and neutral, as if you are a helpful assistant catching them up.

Messages to report:
$messages
""".strip()
