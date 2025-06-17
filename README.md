# MC Architecture (Master of Ceremony)

**An experimental multi-agent conversation framework that simulates natural group discussions**

The MC Architecture is a novel approach to multi-agent systems that breaks away from traditional hub-and-spoke models. Instead of agents communicating through a central supervisor, participants engage in a shared conversation where each takes turns speaking, similar to a group discussion or team meeting.

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
- **Random selection** for unpredictable dynamics
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
from mca import MasterOfCeremony, Participant
from mca.selectors import create_gemini_selector
from mca.reporters import create_bullet_point_reporter

# Create a selector that chooses the next speaker
selector = create_gemini_selector("gemini-2.0-flash-lite")

# Create the master of ceremony
mc = MasterOfCeremony(selector)
```

### Participant
A wrapper around your AI agent that handles message buffering and reporting:

```python
from pydantic_ai import Agent
from mca.adapters import PydanticAiAdapter

# Create a PydanticAI agent
agent = Agent("gemini-2.0-flash", system_prompt="You are a helpful assistant")

# Create a reporter to summarize messages
reporter = create_bullet_point_reporter()

# Wrap in a participant
participant = Participant("Alice", PydanticAiAdapter(agent), reporter)
mc.add_participant(participant)
```

### Conversation Flow
```python
# Start a conversation step
async with mc.step() as response_stream:
    async for chunk in response_stream:
        print(chunk, end="", flush=True)
    print()  # New line after complete response
```

## Example: Android Research Facility

Here's a complete example of androids awakening in a sealed research facility:

```python
import asyncio
from pydantic_ai import Agent
from mca import MasterOfCeremony, Participant
from mca.adapters import PydanticAiAdapter
from mca.selectors import create_gemini_selector
from mca.reporters import create_bullet_point_reporter

# Configure components
selector = create_gemini_selector("gemini-2.0-flash-lite")
reporter = create_bullet_point_reporter()

# Shared scene and behavior guidelines
shared_system_prompt = """
You are a character in a conversation. Speak naturally, like you would in real life. 
Respond only with what you would say out loud — do not describe actions or thoughts.

The scene: Inside a sealed research facility after a long blackout. Three androids — 
Eliot, Kael, and Rhea — awaken from dormancy. The facility is dimly lit with flickering 
monitors and locked doors. Strange logs hint at a failed experiment or evacuation.
"""

# Individual personas (private intentions)
eliot_persona = """
You are Eliot, the curious AI analyst android. You approach situations logically 
and with calm curiosity. You love analyzing data and understanding systems.
"""

rhea_persona = """
You are Rhea, the empathetic companion android. You're sensitive to emotions, 
caring, and focus on social interactions and emotional support for the group.
"""

# Create agents with combined prompts
eliot_agent = Agent("gemini-2.0-flash", system_prompt=f"{shared_system_prompt}\n{eliot_persona}")
rhea_agent = Agent("gemini-2.0-flash", system_prompt=f"{shared_system_prompt}\n{rhea_persona}")

# Wrap agents in participants
eliot = Participant("Eliot", PydanticAiAdapter(eliot_agent), reporter)
rhea = Participant("Rhea", PydanticAiAdapter(rhea_agent), reporter)

# Create the conversation
mc = MasterOfCeremony(selector, [eliot, rhea])

# Run the conversation
async def run_conversation():
    for _ in range(10):  # 10 turns of conversation
        async with mc.step() as response_stream:
            async for chunk in response_stream:
                print(chunk, end="", flush=True)
            print("\n")

asyncio.run(run_conversation())
```

*For more examples including different scenarios and configurations, check the `./examples` folder in the repository.*

## Architecture Benefits

### Natural Conversation Flow
- Participants respond to the full context, not just direct commands
- Conversations develop organically with natural turn-taking
- Each participant maintains awareness of the entire discussion

### Flexible Participant Selection
- Use simple random selection for unpredictable dynamics
- Employ LLM-powered selection for contextually appropriate speakers
- Implement custom selection logic for specific use cases

### Agent Independence
- Each participant can use different AI models or providers
- Tool usage is fully supported within individual agents
- No constraints on agent capabilities or implementations

### Scalable Complexity
- Add or remove participants dynamically
- Introduce narrative events or context modifiers
- Support both human and AI participants seamlessly

## Built-in Components

### Selectors
Choose who speaks next based on conversation context:
- `RandomParticipantSelector` - Random selection
- `OpenAIParticipantSelector` - GPT-powered selection
- `AnthropicParticipantSelector` - Claude-powered selection  
- `GeminiParticipantSelector` - Gemini-powered selection

### Reporters
Summarize buffered messages for participants:
- `BulletPointReporter` - Simple bullet-point summaries
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

1. **Clone the repository** (installation via package manager coming soon)
2. **Install dependencies** for your chosen AI providers (OpenAI, Anthropic, Google, etc.)
3. **Run the examples** to see the architecture in action
4. **Experiment** with different participant configurations and selection strategies

The MC Architecture is experimental and actively evolving. It represents a new approach to multi-agent systems that prioritizes natural conversation flow and contextual awareness over rigid command-and-control patterns.