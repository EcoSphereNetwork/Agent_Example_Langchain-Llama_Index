# Agent_Example_Langchain-Llama_Index

This repository contains examples of agents created using Llama_Index and Langchain. The first implemented agent is a simplified version of the SECinsights agent.

## SECinsights Agent

The SECinsights agent is a simplified version of the original SECinsights project. It uses LlamaIndex to create a searchable index of documents and provides a query endpoint.

### Setup

1. Install the required dependencies:
   ```
   pip install fastapi uvicorn llama-index sqlalchemy psycopg2-binary
   ```

2. Set up your PostgreSQL database and update the `DATABASE_URL` in the `settings` object.

3. Create a `data` directory in the same folder as the script and add your documents to it.

### Running the Agent

1. Start the FastAPI server:
   ```
   python sec_insights_agent.py
   ```

2. The server will start running on `http://localhost:8000`.

### Usage

To query the documents, send a POST request to the `/query` endpoint:

```
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query": "Your query here"}'
```

The response will contain the answer based on the information in the indexed documents.

### Note

This is a simplified version of the SECinsights agent. For more advanced features and configurations, please refer to the original SECinsights project.

## Original Task

The original task was to create individual agents based on examples from Llama_Index and Langchain cookbook. The implementation should follow these guidelines:

- Develop a separate agent for each example in the list.
- Save each agent's code in its own distinct file.
- After completing an agent's code, push it to the GitHub repository before starting on the next one.
- Utilize only the tools and frameworks specified in the examples.
- Implement all code in Python.
- Ensure that the implementation adheres to the following token limits:
  - Maximum Requests per minute (RPM): 50
  - Maximum Tokens per minute (TPM): 40,000

The code examples can be accessed at:
- Llama_Index: https://github.com/run-llama/llama_index.git
- Langchain cookbook: https://github.com/langchain-ai/langchain/tree/master/cookbook
## Definiere Tools

**Language**
- Python

**Frameworks**
- LlamaIndex
- Langchain
- Huggingface trasnformer

**Database**
- MongoDB
- SQL
- ChromaDB

**LLM Provider free local**
- LM-Studio
- Ollama
- Llama.ccp
- Llamafile

**LLM Provider paid online**
- OpenAI
- Antropic
- TogetherAI

## Define Agent Examples

### **[Llama_Index](https://github.com/run-llama/llama_index.git)**

- [SECinsights](https://github.com/run-llama/sec-insights.git)
- [multi-agent-concierge](https://github.com/run-llama/multi-agent-concierge.git)
- [app-creator](https://github.com/run-llama/app-creator.git)
- [multi-agents-workflow](https://github.com/run-llama/multi-agents-workflow.git)
- [llama-slides](https://github.com/run-llama/llama-slides.git)
- [chat-llamaindex](https://github.com/run-llama/chat-llamaindex.git)
- [newsletter-generator](https://github.com/run-llama/newsletter-generator.git)
- [llama_extract](https://github.com/run-llama/llama_extract.git)
- [python-agents-tutorial](https://github.com/run-llama/python-agents-tutorial.git)
- [file-organizer](https://github.com/run-llama/file-organizer.git)
- [ts-agents](https://github.com/run-llama/ts-agents.git)
- [mongodb-demo](https://github.com/run-llama/mongodb-demo.git)
- [automatic-doc-translate](https://github.com/run-llama/automatic-doc-translate.git)
- [pdf-viewer](https://github.com/run-llama/pdf-viewer.git)

### **[Langchain cookbook](https://github.com/langchain-ai/langchain/tree/master/cookbook)**

- cookbook/llm_bash.ipynb
- cookbook/custom_agent_with_plugin_retrieval.ipynb
- cookbook/analyze_document.ipynb
- cookbook/Multi_modal_RAG.ipynb
- cookbook/advanced_rag_eval.ipynb
- cookbook/human_input_llm.ipynb
- cookbook/learned_prompt_optimization.ipynb
- cookbook/mongodb-langchain-cache-memory.ipynb
- cookbook/multi_modal_QA.ipynb
- cookbook/multi_modal_RAG_chroma.ipynb
- cookbook/multi_modal_output_agent.ipynb
- cookbook/multiagent_authoritarian.ipynb
- cookbook/multiagent_bidding.ipynb
- cookbook/openai_functions_retrieval_qa.ipynb
- cookbook/plan_and_execute_agent.ipynb
- cookbook/program_aided_language_model.ipynb
- cookbook/qa_citations.ipynb
- cookbook/rag-locally-on-intel-cpu.ipynb
- cookbook/rag_with_quantized_embeddings.ipynb
- cookbook/retrieval_in_sql.ipynb
- cookbook/rewrite.ipynb
- cookbook/selecting_llms_based_on_context_length.ipynb
- cookbook/self-discover.ipynb
- cookbook/sharedmemory_for_tools.ipynb
- cookbook/smart_llm.ipynb
- cookbook/sql_db_qa.mdx
- cookbook/stepback-qa.ipynb
- cookbook/together_ai.ipynb
- cookbook/tool_call_messages.ipynb
- cookbook/tree_of_thought.ipynb
- cookbook/two_agent_debate_tools.ipynb
- cookbook/wikibase_agent.ipynb
- cookbook/anthropic_structured_outputs.ipynb



**Custom**


## Definiere Agent_Teams
