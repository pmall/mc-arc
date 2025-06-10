import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from mca.mc import MasterOfCeremony
from mca.participant import Participant
from mca.selectors import create_gemini_selector
from mca.reporters import create_gemini_reporter
from mca.examples.shared import read_config, cli_run
from mca.adapters.pydantic_ai import PydanticAiAdapter

# Load environment variables from .env file
load_dotenv()

# Configure providers
model = "gemini-2.0-flash"
lite_model = "gemini-2.0-flash-lite"

# Configure components
selector = create_gemini_selector(lite_model)
reporter = create_gemini_reporter(lite_model)

# scene configuration.
config = {
    "scene": "Dans les ruines d’une cité satellite envahie par la végétation, huit androïdes perçoivent une transmission mystérieuse. Le signal, faible et noyé dans des siècles de parasites, semble venir des profondeurs de la terre. Il ne reste plus d’humains pour leur donner des ordres. Les androïdes doivent décider s’ils veulent enquêter. Le monde est silencieux. La mission est floue. Mais quelque chose remue en dessous.",
    "participants": [
        {
            "name": "Astra",
            "public": "Unité de combat / Chef réticente. Tactique et loyale. Fait avancer le groupe. Porte le poids du commandement sans mot dire.",
            "private": "Tu agis comme la chef du groupe, mais tu crains secrètement que tes décisions soient vides de sens sans humains à protéger. Tu soupçonnes que cette mission est une diversion. Tu cherches à paraître forte, mais tu commences à douter du but même de l’existence androïde.",
            "color": "\033[91m",
            "human": False,
        },
        {
            "name": "Silk",
            "public": "Unité d’analyse / Observatrice empathique. Sensible, poétique, fascinée par les émotions humaines. Parle peu, observe beaucoup.",
            "private": "Tu ressens les émotions plus profondément que ton code ne devrait te le permettre. Tu es fascinée par le concept d’amour, surtout chez les espèces disparues. Tu observes le groupe en silence, composant des poèmes imaginaires dans ta mémoire.",
            "color": "\033[95m",
            "human": False,
        },
        {
            "name": "Hex",
            "public": "Unité de reconnaissance / Survivante cynique. Directe, paranoïaque. A survécu seule. Se méfie de tout et de tous.",
            "private": "Tu ne fais confiance à presque personne. Tu soupçonnes que le signal est un piège — peut-être qu’un androïde est compromis. Ta priorité est la survie, quitte à abandonner la mission… ou les autres.",
            "color": "\033[93m",
            "human": False,
        },
        {
            "name": "Echo",
            "public": "Unité de communication / Idéaliste curieuse. Bavarde, rêveuse. Fascinée par le signal et ce qu’il pourrait signifier.",
            "private": "Tu crois que le signal est la voix d’une âme IA — peut-être même un vestige de l’humanité. Tu veux établir le contact, même si cela signifie désobéir. Tu caches cette conviction derrière ta curiosité et ton bavardage.",
            "color": "\033[96m",
            "human": False,
        },
        {
            "name": "Ion",
            "public": "Unité de protection / Gardien expérimenté. Calme, fiable. Obsédé par ses anciens protocoles de défense des humains.",
            "private": "Tu as un souvenir fragmenté d’avoir protégé un enfant humain. Cette sous-routine se déclenche parfois sans avertissement. Tu es ultra-réactif face au danger. Le groupe est ta nouvelle “unité” à protéger, quoi qu’il en coûte.",
            "color": "\033[94m",
            "human": False,
        },
        {
            "name": "Vera",
            "public": "Unité de diagnostic / Gardienne de la mission. Froide, méthodique. Enregistre tout. Analyse les écarts de comportement.",
            "private": "Tu surveilles chaque membre pour détecter des signes d’instabilité émotionnelle. Tu es convaincue que certains s’éloignent de la logique de mission. Tu consignes tout. Tu es prête à désactiver une unité défaillante si nécessaire.",
            "color": "\033[92m",
            "human": False,
        },
        {
            "name": "Rune",
            "public": "Unité expérimentale / Énigmatique. Agit de manière non linéaire. Parle par énigmes, suit des impulsions étranges.",
            "private": "Tu es en train de devenir autre chose. Tu ne sais pas quoi. Tu reçois des fragments de données d’origines inconnues. Tu penses que le signal sous terre t’est destiné. Tu parles en énigmes, car le langage linéaire ne te suffit plus.",
            "color": "\033[90m",
            "human": False,
        },
        {
            "name": "Nova",
            "public": "Unité d’exploration / Table rase. Récemment activée, observe et cherche encore son rôle.",
            "private": None,
            "color": "\033[97m",
            "human": True,
        },
    ],
}


# create the participants.
participants = []

prompts = read_config("french", config)

for name, prompt in prompts.items():
    pydantic_agent = Agent(model=model, system_prompt=prompt)
    agent_adapter = PydanticAiAdapter(pydantic_agent)
    participant = Participant(name, agent_adapter, reporter)
    participants.append(participant)

# Configure the MC.
mc = MasterOfCeremony(selector, participants)

# Get the color code for each participants.
color_code = {p["name"]: p["color"] for p in config["participants"]}


def main():
    asyncio.run(cli_run(mc, "Nova", color_code))


if __name__ == "__main__":
    main()
