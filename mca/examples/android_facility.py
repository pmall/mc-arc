import asyncio
from dotenv import load_dotenv
from mca.mc import MasterOfCeremony
from mca.adapters import GenaiAdapter
from mca.participant import Participant
from mca.selectors import create_gemini_selector
from mca.reporters import create_gemini_reporter
from mca.examples.shared import cli_run

# Load environment variables from .env file
load_dotenv()

# Configure providers
model = "gemini-2.0-flash"
lite_model = "gemini-2.0-flash-lite"

# Configure components
selector = create_gemini_selector(lite_model)
reporter = create_gemini_reporter(lite_model)

# Shared scene description and per-agent personas (placeholders)
shared_system_prompt = """
You are a character in a conversation. Speak naturally, like you would in real life. Respond only with what you would say out loud — do not describe your actions, emotions, or thoughts unless it’s relevant to what you’re saying.

- Do not wrap your words in quotation marks.
- Do not include stage directions, internal thoughts, or scene descriptions (e.g., no parentheses, asterisks, or narrator-like prose).
- Do not restate what just happened. Trust that everyone knows what’s going on.
- Keep it conversational, brief, and reactive. Say what you would *actually* say next.

Stay in character. Your only goal is to respond as yourself in this ongoing dialogue.

---

The scene takes place inside a sealed research facility after a long blackout.
Three androids — Eliot, Kael, and Rhea — awaken from a dormant state.
They begin exploring their surroundings and rediscovering their purpose, each possessing a unique personality and specialization.
The facility is dimly lit, with flickering monitors and locked doors. Strange logs hint at a failed experiment or evacuation.
The androids must cooperate to piece together their past and decide what to do next.

Eliot is the AI analyst android.
Rhea is the empathetic companion android.
Kael is the skeptical security android.

---

"""


eliot_persona = "You are Eliot, the curious AI analyst android. You approach every situation logically and with calm curiosity. You love to analyze data and understand the world around you."
rhea_persona = "You are Rhea, the empathetic companion android. You are sensitive to emotions, caring, and focus on social interactions and emotional support."

# Configure agents and participants.
eliot_system_prompt = f"{shared_system_prompt}\n{eliot_persona}"
rhea_system_prompt = f"{shared_system_prompt}\n{rhea_persona}"

eliot_agent = GenaiAdapter(model=model, system_prompt=eliot_system_prompt)
rhea_agent = GenaiAdapter(model=model, system_prompt=rhea_system_prompt)

# Create participants.
eliot = Participant("Eliot", eliot_agent, reporter)
rhea = Participant("Rhea", rhea_agent, reporter)

# Configure the MC.
mc = MasterOfCeremony(selector, [eliot, rhea])

# Color code for each participants.
color_codes = {"Eliot": "\033[96m", "Rhea": "\033[95m", "Kael": "\033[92m"}


def main():
    asyncio.run(cli_run(mc, "Kael", color_codes))


if __name__ == "__main__":
    main()
