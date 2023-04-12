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

![](agentx-proposed-architecture.png)

AgentX flowchart generated using Mermaid.js

## Limitations of AgentX

Auto-GPT and babyagi do not (yet) have APIs to interact with. Also they do not (yet) have JSON manifest files (`.well-known/ai-plugin.json` and `.well-known/openai.yaml`), as described by [OpenAI](https://platform.openai.com/docs/plugins/production/plugins-in-production). This means, AgentX is (currently) limited to interacting with Auto-GPT and babyagi directly from the source via `$ git clone`. *More details coming soon.*

## Progress

- [x] babyagi via LangChain (see [baby_agi.pi](baby_agi.py) and [baby_agi_with_tools.py](agentx/baby_agi_with_tools.py))
- [ ] Auto-GPT from source (see [issue](https://github.com/slavakurilyak/agentx/issues/1))
- [ ] babyagi from source (see [issue](https://github.com/slavakurilyak/agentx/issues/2))
- [ ] Teenage-AGI from source (see [issue](https://github.com/slavakurilyak/agentx/issues/3))

## Installation

1. Clone this repository
2. Make sure to use python3.8 in your environment. You may install [pyenv](https://github.com/pyenv/pyenv) to manage multiple different python installations.
3. Install [poetry](https://python-poetry.org/docs/) via `curl -sSL https://install.python-poetry.org | python3 -`
4. Set up the project via `poetry install`

## Usage


To use AgentX, first activate the virtual environment via:
```bash
source $(poetry env info --path)/bin/activate
```
For babyagi without tools: 
```bash
python agentx/baby_agi.py
```

For babyagi with tools:

```bash
python agentx/baby_agi_with_tools.py
```

If you do not want to enable the virtual environment you can execute commands
directly via poetry, which will proxy the command into the correct virtual environment.

```bash
poetry run python agentx/baby_agi.py
poetry run python agentx/baby_agi_with_tools.py
```

## Requirements

We use poetry as a package manager. Have a look [here](pyproject.toml) for further details about existing requirements.
To add a dependency run `poetry add {{package_name}}`


## .env.example

```
OPENAI_API_KEY=
```