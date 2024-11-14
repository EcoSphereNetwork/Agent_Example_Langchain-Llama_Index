import os
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent.react_multimodal.step import MultimodalReActAgentWorker
from llama_index.core.agent import Task, AgentRunner
from llama_index.core.schema import ImageDocument
from llama_index.llms.openai import OpenAI
from llama_index.multi_modal_llms.openai import OpenAIMultiModal

# Set up LM Studio API endpoint
LM_STUDIO_API_BASE = "http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"] = "lm-studio"
os.environ["OPENAI_API_BASE"] = LM_STUDIO_API_BASE

# Download the image for analysis
!wget "https://images.openai.com/blob/a2e49de2-ba5b-4869-9c2d-db3b4b5dcc19/new-models-and-developer-products-announced-at-devday.jpg?width=2000" -O dev_day.png

# Fetch web content for RAG
url = "https://openai.com/blog/new-models-and-developer-products-announced-at-devday"
reader = SimpleWebPageReader(html_to_text=True)
documents = reader.load_data(urls=[url])

# Set up LLM using LM Studio
Settings.llm = OpenAI(temperature=0, model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF")

# Create vector index
vector_index = VectorStoreIndex.from_documents(documents)

# Create query tool
query_tool = QueryEngineTool(
    query_engine=vector_index.as_query_engine(),
    metadata=ToolMetadata(
        name="vector_tool",
        description="Useful to lookup new features announced by OpenAI"
    )
)

# Set up multi-modal LLM using LM Studio
# Note: LM Studio might not support multi-modal models, so we'll use a text-only model here
mm_llm = OpenAI(model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF", max_tokens=1000)

# Create ReAct agent
react_step_engine = MultimodalReActAgentWorker.from_tools(
    [query_tool],
    multi_modal_llm=mm_llm,
    verbose=True
)
agent = react_step_engine.as_agent()

# Define query and create task
query_str = (
    "The photo shows some new features released by OpenAI. "
    "Can you pinpoint the features in the photo and give more details using relevant tools?"
)
image_document = ImageDocument(image_path="dev_day.png")
task = agent.create_task(
    query_str,
    extra_state={"image_docs": [image_document]}
)

# Define execution functions
def execute_step(agent: AgentRunner, task: Task):
    step_output = agent.run_step(task.task_id)
    if step_output.is_last:
        response = agent.finalize_response(task.task_id)
        print(f"> Agent finished: {str(response)}")
        return response
    else:
        return None

def execute_steps(agent: AgentRunner, task: Task):
    response = execute_step(agent, task)
    while response is None:
        response = execute_step(agent, task)
    return response

# Run the agent
response = execute_steps(agent, task)

# Print the final response
print(str(response))
