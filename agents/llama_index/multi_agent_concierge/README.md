# Concierge Agent
Overview

The Concierge Agent is a conversational workflow application built to handle multiple tasks through specialized agents. It utilizes OpenAI's language model and LlamaIndex for efficient interaction and memory management.
Features

    Multi-Agent System: Includes agents for stock lookups, authentication, account balance inquiries, and money transfers.
    Dynamic Workflow: Processes user inputs with adaptive responses based on available agents.
    Chat History Management: Maintains conversation context using ChatMemoryBuffer.
    Flexible Tool Integration: Easily extendable with custom tools.

Prerequisites

    Python 3.9+
    Installed Python libraries:
        llama-index
        openai

Installation

    Clone the repository:

git clone https://github.com/your-repo-name.git
cd your-repo-name

Install dependencies:

pip install -r requirements.txt

Configure OpenAI API key as an environment variable:

    export OPENAI_API_KEY="your-api-key"

Usage
Running the Application

Start the application with:

python main.py

Interacting with the Agent

    Input a message, e.g., Hello!.
    The agent will respond and guide you based on available agent configurations.
    Type exit, quit, or bye to end the session.

Agent Configurations

The application includes the following agents:

    Stock Lookup Agent: Fetches stock prices and symbols.
    Authentication Agent: Manages user authentication.
    Account Balance Agent: Checks user account balances.
    Transfer Money Agent: Facilitates money transfers.

Each agent is equipped with specific tools and a system prompt tailored to its purpose.
Extending the Application

    Add a New Tool:
        Create a function returning a list of tools.
        Implement logic as per requirements.

    Add a New Agent:
        Define a new AgentConfig with a name, description, system prompt, and tools.
        Add it to get_agent_configs().

