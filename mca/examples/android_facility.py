import asyncio
from dotenv import load_dotenv
from google import genai
from pydantic_ai import Agent
from mca.mc import MasterOfCeremony
from mca.participant import Participant
from mca.selectors.gemini import GeminiParticipantSelector
from mca.summarizers.gemini import GeminiSummarizer
from mca.adapters.pydantic_ai import PydanticAiAdapter

# Load environment variables from .env file
load_dotenv()

# Configure providers
client = genai.Client()
model = "gemini-2.0-flash"
lite_model = "gemini-2.0-flash-lite"

# Configure components
selector = GeminiParticipantSelector(lite_model, client)
summarizer = GeminiSummarizer(lite_model, client)

# Shared scene description and per-agent personas (placeholders)
shared_system_prompt = """
You are chatting with one or multiple other characters.
You produce what your character is saying. It means:
You must **never** express your inner thoughts out loud.
You must **never** give stage directions or environment description out loud.
You must **never** describe your actions, only dialogue.
Focus on chatting with the others.

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

eliot_pydantic_agent = Agent(model=model, system_prompt=eliot_system_prompt)
eliot_agent_adapter = PydanticAiAdapter(eliot_pydantic_agent)

rhea_pydantic_agent = Agent(model=model, system_prompt=rhea_system_prompt)
rhea_agent_adapter = PydanticAiAdapter(rhea_pydantic_agent)

# Create participants.
eliot = Participant("Eliot", eliot_agent_adapter, summarizer)
rhea = Participant("Rhea", rhea_agent_adapter, summarizer)

# Configure MC with output handler.
mc = MasterOfCeremony(participants=[eliot, rhea], selector=selector)


# Run conversation with external control and step-by-step execution
import os

reset = "\033[0m"
color_code = {"Eliot": "\033[96m", "Rhea": "\033[95m", "Kael": "\033[92m"}


def out_line(name: str, content: str):
    print(f"{color_code[name]}💬 {name}:{reset} {content}▊")


def clear(timeline: list[(str, str)]):
    os.system("clear" if os.name == "posix" else "cls")
    for name, content in timeline:
        out_line(name, content)


async def main():
    while True:
        async with mc.step() as stream:
            output = ""
            async for name, message in stream:
                for char in list(message[len(output) :]):
                    output += char

                    clear(mc.timeline)
                    out_line(name, output)

                    await asyncio.sleep(0.01)

        clear(mc.timeline)

        user_input = input("Your response: ")

        if user_input.lower() == "quit":
            break

        if user_input:
            mc.add_message("Kael", user_input)


if __name__ == "__main__":
    asyncio.run(main())
