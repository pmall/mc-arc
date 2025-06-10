from string import Template
from typing import Optional
from mca.interfaces import Message, ContextModifier


# participant
def participant_no_modifier(report: str):
    return Template(
        """
Report of the conversation since your last turn:
$report

Now it is your turn:
""".strip()
    ).substitute(report=report)


def participant_with_modifiers(report: str, modifiers: list[ContextModifier]):
    modifiers_str = "\n".join(str(m) for m in modifiers)

    return Template(
        """
Report of the conversation since your last turn:
$report

Narrative event since your last turn:
$modifiers

Now it is your turn:
""".strip()
    ).substitute(report=report, modifiers=modifiers_str)


def PARTICIPANT_PROMPT_TEMPLATE(
    report: Optional[str], modifiers: list[ContextModifier]
) -> str:
    if not report:
        return "This is the begining of the conversation."

    if not modifiers:
        participant_no_modifier(report)

    return participant_with_modifiers(report, modifiers)


# selector
def SELECTOR_PROMPT_TEMPLATE(participants: list[str], messages: list[Message]):
    participants_str = ", ".join(participants)
    messages_str = "\n".join([f"- {m}" for m in messages])

    return Template(
        """
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
    ).substitute(participants=participants_str, messages=messages_str)


# reporter
def REPORTER_PROMPT_TEMPLATE(participant: str, messages: list[Message]):
    messages_str = "\n".join([f"- {m}" for m in messages])

    return Template(
        """
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
    ).substitute(participant=participant, messages=messages_str)
