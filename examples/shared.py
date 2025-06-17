import os
import asyncio
from string import Template
from typing import Callable, Optional
from mc_arc import MasterOfCeremony, Message


# prompt template:
def SYSTEM_PROMPT_TEMPLATE(
    language: str, name: str, scene: str, participants: dict[str, str], private: str
) -> str:
    participants_str = "\n".join(
        [f"- {name}: {persona}" for name, persona in participants.items()]
    )

    return Template(
        """
You are a character participating in a conversation in $language.

Speak naturally, like you would in real life. Respond only with what you would say out loud — do not describe your actions, emotions, or thoughts unless it’s relevant to what you’re saying.

- Do not wrap your words in quotation marks.
- Do not include stage directions, internal thoughts, or scene descriptions (e.g., no parentheses, asterisks, or narrator-like prose).
- Do not restate what just happened. Trust that everyone knows what’s going on.
- Keep it conversational, brief, and reactive. Say what you would *actually* say next.

The world you’re in is dynamic and interactive. You have access to special abilities (called *tools*) that let you get real information or take actions. Use them **naturally, as part of your character's thinking and behavior** — like checking the weather, remembering a fact, or retrieving a name. These tools are invisible to the others. Use them whenever needed to respond believably and helpfully.

Example:  
If someone asks, "What’s the weather in Paris?" and you don’t know, you may use your tools to find out, then respond like:  
> Looks like it’s sunny and 30 degrees there.

Stay in character. Your only goal is to respond as yourself in this ongoing dialogue.

---

Scene description:  
$scene

---

Other participants in the conversation:  
$participants

---

You impersonate the character of $name.

---

Your private motivation:  
$private

""".strip()
    ).substitute(
        language=language,
        name=name,
        scene=scene,
        participants=participants_str,
        private=private,
    )


# read the config to produce a dict name -> prompt.
def read_config(language: str, config: dict) -> dict[str, str]:
    prompts = {}

    scene = config["scene"]
    participants: dict[str, str] = {
        p["name"]: p["public"] for p in config["participants"]
    }

    for p in config["participants"]:
        if p["human"]:
            continue

        name = p["name"]
        private = p["private"]

        system_prompt = SYSTEM_PROMPT_TEMPLATE(
            language, name, scene, participants, private
        )
        prompts[name] = system_prompt

    return prompts


async def cli_run(
    mc: MasterOfCeremony,
    player: str,
    color_codes: dict[str, str],
    debug: Optional[Callable] = None,
):
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

        if debug:
            print(debug())

        user_input = input("Your response: ")

        if user_input.lower() == "quit":
            break

        if user_input:
            mc.add_message(player, user_input)
