# AgentX

AgentX is a LangChain-powered agent that delegates tasks well. AgentX accomplishes this by communicating in parallel with Auto-GPT, babyagi, HuggingFace, and other AI agents to complete complex tasks.

## Proposed Architecture

1.  A user interacts with AgentX, requesting assistance with a task.
2.  AgentX processes the request and retrieves the necessary tools to help with the task.
3.  AgentX selects the relevant tools from the available options: Auto-GPT, babyagi, HuggingFace, and other AI agents.
4.  Each selected tool is then used to complete the task:
    -   Auto-GPT completes the task using its capabilities.
    -   babyagi completes the task using its capabilities.
    -   HuggingFace completes the task using its capabilities.
    -   Other AI agent completes the task using its capabilities.
5.  The results from each tool are combined into a coherent and comprehensive output.
6.  AgentX receives the combined results and processes them to provide the best response.
7.  Finally, AgentX presents the response to the user.

```mermaid
graph TB
A[User] --> B[AgentX]
B --> C[Find Relevant Agent]
C --> D{Delegate Task to Agent}
D --> E1[Auto-GPT]
D --> E2[BabyAGI]
D --> E3[HuggingFace]
D --> E4[Other AI Agent]
E1 --> F1[Complete Task with Auto-GPT]
E2 --> F2[Complete Task with BabyAGI]
E3 --> F3[Complete Task with HuggingFace]
E4 --> F4[Complete Task with Other AI Agent]
F1 --> G[Evaluate Task Completion]
F2 --> G
F3 --> G
F4 --> G
G --> H[AgentX]
H --> I[User]
```

Note, this AgentX flowchart was generated using Mermaid.

## Limitations of AgentX

Auto-GPT and babyagi do not (yet) have APIs to interact with. Also they do not (yet) have JSON manifest files (`.well-known/ai-plugin.json` and `.well-known/openai.yaml`), as described by [OpenAI](https://platform.openai.com/docs/plugins/production/plugins-in-production). This means, AgentX is (currently) limited to interacting with Auto-GPT and babyagi directly from the source via `$ git clone`. *More details coming soon.*

## Progress

- [x] babyagi via LangChain (see [baby_agi.pi](baby_agi.py) and [baby_agi_with_tools.py](baby_agi_with_tools.py))
- [ ] Auto-GPT from source (see [issue](https://github.com/slavakurilyak/agentx/issues/1))
- [ ] babyagi from source (see [issue](https://github.com/slavakurilyak/agentx/issues/2))
- [ ] Teenage-AGI from source (see [issue](https://github.com/slavakurilyak/agentx/issues/3))

## Installation

1. Clone this repository
2. Create a Python 3.8 virtual environment: `python3.8 -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate`
4. Copy `.env.example` to create `.env`.
5. Set your OpenAI API key in `.env`.
6. Install the required modules by running `pip install -r requirements.txt`.

## Usage

To use AgentX, run the following command with the virtual environment activated:

For babyagi without tools:

```bash
python baby_agi.py
```

For babyagi with tools:

```bash
python baby_agi_with_tools.py
```

## Requirements

The following modules are required and can be installed using the command `pip install -r requirements.txt`:

```txt
langchain
openai
pydantic
faiss-cpu
tiktoken
```

## .env.example

```
OPENAI_API_KEY=
```