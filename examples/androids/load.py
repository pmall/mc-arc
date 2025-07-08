import os
import json
import lancedb
from google import genai
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

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


# get a lancedb database.
db = lancedb.connect(cwd / "loredb")

# open the lore.json file.
with open(cwd / "lore.json") as f:
    config = json.load(f)

# embed the world lore.
world_entries = []

for fact in config["world"]:
    world_entries.append({"fact": fact, "vector": embed(fact)})

# for each character, add its lore to the world lore and store it into a lancedb collection.
for name, lore in config["characters"].items():
    entries = list(world_entries)

    for fact in lore:
        entries.append({"fact": fact, "vector": embed(fact)})

    db.create_table(name, data=entries, mode="overwrite")
