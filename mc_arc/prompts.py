from mc_arc.interfaces import Message


# participant
def PARTICIPANT_PROMPT_TEMPLATE(report: str):
    return f"""
Report of the conversation since your last turn:
{report}

Now it is your turn:
""".strip()


# selector
def SELECTOR_PROMPT_TEMPLATE(participants: list[str], messages: list[Message]):
    participants_str = ", ".join(participants)
    messages_str = "\n".join([f"- {m}" for m in messages])

    return f"""
You are managing a multi-character conversation. Based on the recent messages and the current situation, choose the next participant who should speak. Consider who has the most reason to respond, take initiative, clarify something, or move the discussion forward.

Available participants:
{participants_str}

Recent messages:
${messages_str}

Rules:
- Always select exactly one participant from the list.
- Choose the one whose voice is most needed right now.
- Do not explain your choice or provide any commentary.

Return the name of the selected participant only, exactly as it appears in the list.
 """.strip()


# reporter
def REPORTER_PROMPT_TEMPLATE(name: str, messages: list[Message]):
    messages_str = "\n".join([f"- {m}" for m in messages])

    return f"""
You are a conversation reporter assigned to assist the participant named **{name}**.

The following conversation is a dialogue between other participants that occurred **since {name} last spoke**.

Your job is to write a short, natural-language briefing that helps {name} understand what was said.

- Write directly to {name}, using “you” when appropriate.
- Preserve the meaning and intent of each message, but rephrase in plain language.
- Keep all names except {name}, which should become “you”.
- Do not copy, quote, or imitate dialogue formatting (e.g., "Name: ...").
- Your report should be roughly one sentence per message unless merging is natural.
- Do not invent or assume information that wasn't stated.
- Do not add intro or final note, output the report only.

Keep the style simple and neutral, as if you are a helpful assistant catching them up.

Messages to report:
{messages_str}
""".strip()
