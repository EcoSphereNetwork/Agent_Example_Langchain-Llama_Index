# Multi-Modal ReAct Agent

This script implements a multi-modal Retrieval-Augmented Generation (RAG) agent using the LlamaIndex framework and LM Studio API. The agent can analyze images and use a RAG pipeline to provide detailed information.
Features

    Multi-modal input processing (text and images)
    RAG pipeline for information retrieval
    Integration with LM Studio API for language model inference
    Web content fetching for up-to-date information

Prerequisites

    Python 3.7+
    LlamaIndex library
    LM Studio running locally with API endpoint exposed

Installation

    Clone this repository:

    text
    git clone https://github.com/yourusername/multi-modal-react-agent.git
    cd multi-modal-react-agent

Install the required packages:

text
pip install llama-index

    Ensure LM Studio is running and exposing an API endpoint (default: http://localhost:1234/v1).

Usage

    Update the LM_STUDIO_API_BASE variable if your LM Studio API endpoint differs from the default.
    Run the script:

    text
    python multi-modal_react_agent.py

    The script will:
        Download a sample image
        Fetch web content for the RAG system
        Set up the language model and vector index
        Create a ReAct agent
        Execute the agent to analyze the image and provide information

Customization

    Modify the query_str variable to change the input query.
    Adjust the url variable to fetch different web content for the RAG system.
    Change the LM Studio model by modifying the model parameter in the OpenAI constructor calls.

Limitations

    The current implementation uses a text-only model for multi-modal tasks, which may limit performance in image analysis.
    LM Studio may not support all features of OpenAI's GPT-4 Vision model.
