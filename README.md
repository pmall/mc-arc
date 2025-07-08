# MC-ARC (Master of Ceremony Architecture)

**An experimental multi-agent conversation framework that simulates natural group discussions.**

MC-ARC is a novel approach to multi-agent systems that breaks away from traditional hub-and-spoke models. Instead of agents communicating through a central supervisor, participants engage in a shared conversation where each takes turns speaking, similar to a group discussion or team meeting.

## Core Concept

Traditional multi-agent architectures typically follow a supervisor pattern:
- A central supervisor agent manages all communication
- Subordinate agents (A, B, C) only communicate with the supervisor
- Information flows: A → Supervisor → B

The MC Architecture introduces a **conversation-based model**:
- All participants share a **global timeline** of messages
- Each participant receives messages from all others since their last turn
- A **Master of Ceremony** intelligently selects who speaks next
- Participants engage in natural, contextual dialogue

Think of it as a **team chat where only one person can speak at a time**, but everyone sees the full conversation history.

## How It Works

### 1. Global Timeline
Every message from any participant is recorded in a shared timeline. This creates a complete conversation history that all participants can reference.

### 2. Participant Selection
The Master of Ceremony uses configurable strategies to choose the next speaker:
- **LLM-powered selection** that analyzes context and chooses the most appropriate participant
- **Custom selection logic** based on your specific needs

### 3. Message Buffering
Each participant maintains a buffer of messages received since their last turn. When selected to speak, they:
- Receive a summary/report of all messages since their last turn
- Generate a response based on this context
- Clear their buffer after speaking

### 4. Agent Agnostic Design
The architecture works with any AI model or agent through adapters:
- OpenAI GPT models
- Anthropic Claude
- Google Gemini
- Local models
- Custom implementations

## Key Components

### MasterOfCeremony
The central orchestrator that manages the conversation flow:

```python
from mc_arc import MasterOfCeremony
from mc_arc.selectors import create_gemini_selector

# Create a selector that chooses the next speaker
selector = create_gemini_selector("gemini-1.5-flash-latest")

# Create the master of ceremony
mc = MasterOfCeremony(selector)
```

### Participant
A wrapper around your AI agent that handles message buffering and reporting:

```python
from pydantic_ai import Agent
from mc_arc import Participant
from mc_arc.adapters import PydanticAiAdapter
from mc_arc.reporters import create_gemini_reporter

# Create a PydanticAI agent
agent = Agent("gemini-1.5-flash-latest", system_prompt="You are a helpful assistant")

# Create a reporter to summarize messages
reporter = create_gemini_reporter("gemini-1.5-flash-latest")

# Wrap in a participant
participant = Participant("Alice", PydanticAiAdapter(agent), reporter)
mc.add_participant(participant)
```

### Conversation Flow
```python
# Start a conversation step
async with mc.step() as stream:
    output = ""
    async for name, chunk in stream:
        # stream the response...
        output += chunk
```

## Example: The Androids

Here's a simplified example of the `androids` scenario included in the `examples` folder. This version demonstrates the core mechanics of setting up a multi-agent conversation.

For a more advanced version that includes persistent memory for each character using `LanceDB`, see the `examples/androids` directory.

```python
import asyncio
import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from mc_arc import MasterOfCeremony, Participant, Message
from mc_arc.adapters import PydanticAiAdapter
from mc_arc.selectors import create_gemini_selector

# Load environment variables
load_dotenv()

# --- Configuration ---
MODEL = "gemini-1.5-flash-latest"
LITE_MODEL = "gemini-1.5-flash-latest"
API_KEY = os.getenv("GEMINI_API_KEY")

# --- System Prompts ---
def get_system_prompt(name: str, other_participants: list[str]) -> str:
    return f'''
You are {name}, an android.
Engage in a natural conversation with the other participants: {", ".join(other_participants)}.
Stay in character. Do not narrate your actions.
'''

# --- Setup ---
selector = create_gemini_selector(LITE_MODEL, api_key=API_KEY)
mc = MasterOfCeremony(selector)

participants_names = ["Astra", "Hex", "Nova"]

for name in participants_names:
    other_participants = [p for p in participants_names if p != name]
    system_prompt = get_system_prompt(name, other_participants)
    
    agent = Agent(MODEL, system_prompt=system_prompt)
    participant = Participant(name, PydanticAiAdapter(agent))
    mc.add_participant(participant)

# --- CLI Interaction ---
async def cli_run():
    print("Starting conversation with Astra, Hex, and Nova.")
    mc.add_message("Nova", "Where are we? I don't recognize this place.")

    while True:
        print("\n--- Next Turn ---")
        full_response = ""
        speaker = ""
        async with mc.step() as stream:
            async for name, chunk in stream:
                if not speaker:
                    speaker = name
                    print(f"{name}: ", end="", flush=True)
                print(chunk, end="", flush=True)
                full_response += chunk
        
        print("\n")
        user_input = input("Your response as 'Human': ")
        if user_input.lower() == "/quit":
            break
        if user_input:
            mc.add_message("Human", user_input)

if __name__ == "__main__":
    asyncio.run(cli_run())
```

## Architecture Benefits

### Natural Conversation Flow
- Participants respond to the full context, not just direct commands
- Conversations develop organically with natural turn-taking
- Each participant maintains awareness of the entire discussion

### Flexible Participant Selection
- Employ LLM-powered selection for contextually appropriate speakers
- Implement custom selection logic for specific use cases

### Agent Independence
- Each participant can use different AI models or providers
- Tool usage is fully supported within individual agents
- No constraints on agent capabilities or implementations

### Scalable Complexity
- Add or remove participants dynamically
- Support both human and AI participants seamlessly

## Built-in Components

### Selectors
Choose who speaks next based on conversation context:
- `OpenAIParticipantSelector` - GPT-powered selection
- `AnthropicParticipantSelector` - Claude-powered selection
- `GeminiParticipantSelector` - Gemini-powered selection

### Reporters
Summarize buffered messages for participants:
- `OpenAIReporter` - GPT-generated natural language reports
- `AnthropicReporter` - Claude-generated reports
- `GeminiReporter` - Gemini-generated reports

### Agent Adapters
**Completely agent-agnostic** - works with any AI agent library:
- `PydanticAiAdapter` - Ready-to-use integration with PydanticAI agents
- Any agent library can be integrated by implementing a simple adapter interface
- Support for streaming responses from any provider
- Flexible prompt handling regardless of underlying agent implementation

## Use Cases

### Creative & Narrative Applications
- **Interactive storytelling** with multiple characters
- **Role-playing scenarios** with distinct personalities
- **Creative writing** with collaborative character development

### Multi-Agent Problem Solving
- **Collaborative analysis** where different agents bring different perspectives
- **Distributed reasoning** across specialized agents
- **Tool-using workflows** where agents coordinate complex tasks

### Simulation & Research
- **Social dynamics modeling** with AI participants
- **Group decision-making** simulation
- **Communication pattern analysis** in multi-agent systems

## Getting Started

1. **Clone the repository**
2. **Install dependencies**: `pip install -e .[dev]`
3. **Set up your environment**: Create a `.env` file with your API keys (e.g., `GEMINI_API_KEY=...`)
4. **Run the examples**: `python examples/androids/run.py`
5. **Experiment** with different participant configurations and selection strategies.

The MC Architecture is experimental and actively evolving. It represents a new approach to multi-agent systems that prioritizes natural conversation flow and contextual awareness over rigid command-and-control patterns.
