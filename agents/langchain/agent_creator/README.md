# AgentCreator

Multi-Agent LangChain System

This project implements a sophisticated multi-agent system designed to generate LangChain agents dynamically. The system uses Retrieval-Augmented Generation (RAG) to fetch LangChain documentation, generates flexible agent code based on user-defined parameters, performs critical code reviews, and orchestrates these functionalities seamlessly.
Features

    Dynamic Retrieval (RAG): Retrieves relevant LangChain documentation stored in a FAISS vector database for context-aware generation.
    Flexible Code Generation: Generates Python agents dynamically using customizable prompts based on user requirements.
    Critical Feedback Loop: Automatically reviews and revises generated code to ensure quality and adherence to LangChain standards.
    Supervisor Agent: Coordinates tasks dynamically, invoking RAG, code generation, and review tools as required.
    Shared Memory: Maintains context across tasks for better continuity.
    Parallel Processing: Supports concurrent execution of tasks for improved performance.
    End-to-End Workflow: Combines all features to create, review, and finalize LangChain agents based on user specifications.

Requirements

    Python 3.8+
    Required Python Libraries:
        langchain
        faiss-cpu
        openai
        tiktoken

Install all dependencies:

pip install langchain faiss-cpu openai tiktoken

Project Structure

    Main Script: multi_agent_system.py - Contains the complete implementation of the multi-agent system.
    LangChain Documentation: Preprocessed and stored locally in FAISS vector database for efficient retrieval.

