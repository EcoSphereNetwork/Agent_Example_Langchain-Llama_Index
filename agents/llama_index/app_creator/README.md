# App Creator Agent

This is a Python implementation of an autonomous agent that creates applications based on natural language specifications. The agent uses LlamaIndex and OpenAI's GPT models to generate, review, and improve code.

## Features

- Automated code generation from specifications
- Multi-step review and improvement process
- Code quality checks
- Automatic file packaging
- Maximum of 3 review cycles to prevent infinite loops

## Components

- `agent.py`: Core agent implementation with architect, coder, and reviewer roles
- `packager.py`: Handles code organization and file creation
- `main.py`: Example usage of the agent

## Usage

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

2. Install dependencies:
```bash
pip install llama-index openai
```

3. Run the example:
```bash
python main.py
```

## How it Works

1. **Architect**: Creates initial code based on specification
2. **Reviewer**: Reviews code quality and specification compliance
3. **Coder**: Improves code based on reviews
4. **Packager**: Organizes final code into appropriate files

The agent will continue the review-improve cycle until either:
- The reviewer is satisfied with the code
- The maximum number of reviews (3) is reached

## Output

Generated files are saved in the `output` directory, along with a manifest.json file listing all created files.
