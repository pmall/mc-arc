import os
import lancedb
import asyncio
from google import genai
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from mc_arc import MasterOfCeremony, Participant, Message
from mc_arc.adapters import PydanticAiAdapter
from mc_arc.selectors import create_gemini_selector
from prompts import SYSTEM_PROMPT_TEMPLATE

load_dotenv()

# Configure providers
model = "gemini-2.0-flash"
lite_model = "gemini-2.0-flash-lite"

# Configure components
selector = create_gemini_selector(lite_model)

# get the current directory.
cwd = Path(__file__).parent.resolve()

# get a gemini client.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_EMBED_MODEL_NAME = os.getenv("GEMINI_EMBED_MODEL_NAME", "text-embedding-004")

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY env var must be defined")

client = genai.Client(api_key=GEMINI_API_KEY)


# embed the given contents using gemini.
def embed(contents: str):
    response = client.models.embed_content(
        model=GEMINI_EMBED_MODEL_NAME,
        contents=contents,
    )

    if not response.embeddings:
        raise Exception("Unable to embed contents")

    return response.embeddings[0].values


# create a tool to query the lore database.
db = lancedb.connect(cwd / "loredb")


def read_memory_of(key: str, query: str) -> str:
    print(f"Querying memory or {key} for: {query}")

    embedding = embed(query)

    tbl = db.open_table(key)

    results = tbl.search(embedding).limit(5).to_list()

    return "\n".join([f"- {r['fact']}" for r in results])


# build the agents and the mc.
mc = MasterOfCeremony(selector)

names = ["Astra", "Silk", "Hex", "Echo", "Ion", "Vera", "Rune", "Nova"]

for name in names:
    key = name.lower()
    system_prompt = SYSTEM_PROMPT_TEMPLATE(name, names)
    agent = Agent(model, system_prompt=system_prompt)

    def register_tool(key: str):
        @agent.tool_plain
        def read_memory(query: str) -> str:
            """
            Query your internal memory and return the matching pieces of knowledge

            Args:
                query (str): The query to run against your internal memory.

            Returns:
                str: A bulltet point list of the matching pieces of knowledge.
            """
            return read_memory_of(key, query)

    register_tool(key)  # fix closure capturing problem.

    mc.add_participant(Participant(name, PydanticAiAdapter(agent)))

# run a session.
colors = {
    "Astra": "\033[91m",
    "Silk": "\033[95m",
    "Hex": "\033[93m",
    "Echo": "\033[96m",
    "Ion": "\033[94m",
    "Vera": "\033[92m",
    "Rune": "\033[90m",
    "Nova": "\033[97m",
}


async def cli_run():
    reset = "\033[0m"

    def out_line(name: str, content: str):
        print(f"{colors[name]}💬 {name}:{reset} {content.strip()}")

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

        user_input = input("/quit to quit: ")

        if user_input.lower() == "/quit":
            break


if __name__ == "__main__":
    asyncio.run(cli_run())
