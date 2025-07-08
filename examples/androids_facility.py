import os
import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from mc_arc import MasterOfCeremony, Participant, Message
from mc_arc.adapters import PydanticAiAdapter
from mc_arc.selectors import create_gemini_selector

# Load environment variables from .env file
load_dotenv()

# Configure providers
model = "gemini-2.0-flash"
lite_model = "gemini-2.0-flash-lite"

# Configure components
selector = create_gemini_selector(lite_model)

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

eliot_agent = Agent(model=model, system_prompt=eliot_system_prompt)
rhea_agent = Agent(model=model, system_prompt=rhea_system_prompt)

# Create participants.
eliot = Participant("Eliot", PydanticAiAdapter(eliot_agent))
rhea = Participant("Rhea", PydanticAiAdapter(rhea_agent))

# Configure the MC.
mc = MasterOfCeremony(selector, [eliot, rhea])

# Color code for each participants.
color_codes = {"Eliot": "\033[96m", "Rhea": "\033[95m", "Kael": "\033[92m"}


async def cli_run(mc: MasterOfCeremony, player: str):
    reset = "\033[0m"

    def out_line(name: str, content: str):
        print(f"{color_codes[name]}💬 {name}:{reset} {content.strip()}")

    def clear(timeline: list[Message]):
        os.system("clear" if os.name == "posix" else "cls")
        for message in timeline:
            out_line(message.name, message.content)

    while True:
        async with mc.step() as stream:
            output = ""
            async for name, chunk in stream:
                for char in list(chunk):
                    output += char
                    clear(mc.timeline)
                    out_line(name, output.strip())

                    await asyncio.sleep(0.01)

        clear(mc.timeline)

        user_input = input("Your response (/quit to quit): ")

        if user_input.lower() == "/quit":
            break

        if user_input:
            mc.add_message(player, user_input)


if __name__ == "__main__":
    asyncio.run(cli_run(mc, "Kael"))
