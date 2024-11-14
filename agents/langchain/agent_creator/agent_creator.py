from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.tools import Tool
from langchain.agents import create_openai_functions_agent
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableParallel
from langchain.memory import ConversationBufferMemory
import requests

# --- 1. SETUP LM-STUDIO API WRAPPER ---
class LMStudioWrapper:
    def __init__(self, endpoint_url: str, api_key: str = None):
        self.endpoint_url = endpoint_url
        self.api_key = api_key

    def call_model(self, prompt: str, temperature: float = 0.2):
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": 1000,
            "stop": None,
        }
        response = requests.post(self.endpoint_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["text"]

# Initialize LM-Studio API wrapper
lm_studio_model = LMStudioWrapper(endpoint_url="http://localhost:8000/api/v1/completions")

# --- 2. SETUP LANGCHAIN DOCUMENT DATABASE ---
def setup_langchain_docs_vectorstore(doc_path):
    loader = DirectoryLoader(doc_path, glob="**/*.txt")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local("langchain_docs_faiss")
    return vectorstore

# Uncomment the below line to preprocess documents and save the FAISS index
# vectorstore = setup_langchain_docs_vectorstore("/path/to/langchain/docs")

vectorstore = FAISS.load_local("langchain_docs_faiss", OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# --- 3. RAG AGENT ---
rag_template = """
Use the provided LangChain documentation context to answer the query. Be comprehensive and provide actionable insights.

Context:
{context}

Query:
{query}
"""

def run_rag_agent(query):
    context_docs = retriever.get_relevant_documents(query)
    context_text = "\n".join([doc.page_content for doc in context_docs])
    prompt = rag_template.format(context=context_text, query=query)
    response = lm_studio_model.call_model(prompt)
    return response

# --- 4. CODE-GENERATION AGENT ---
code_gen_template = """
Write Python code for a LangChain agent with the following specifications:
1. Tools: {tools}
2. Memory: {memory}
3. Behavior: {behavior}
4. Advanced Features: {features}

Provide complete and executable Python code.
"""

def run_code_gen_agent(tools, memory, behavior, features):
    prompt = code_gen_template.format(tools=tools, memory=memory, behavior=behavior, features=features)
    response = lm_studio_model.call_model(prompt)
    return response

# --- 5. CRITICAL REVIEW AGENT ---
review_template = """
Review the following Python code for correctness, completeness, and alignment with LangChain standards:
{code}

Provide a list of issues and suggestions.
"""

revision_template = """
Revise the following Python code based on the feedback:
Code:
{code}

Feedback:
{feedback}

Provide the revised code.
"""

def review_and_revise_code(code):
    review_prompt = review_template.format(code=code)
    feedback = lm_studio_model.call_model(review_prompt)
    if "issue" in feedback.lower():
        revision_prompt = revision_template.format(code=code, feedback=feedback)
        revised_code = lm_studio_model.call_model(revision_prompt)
        return revised_code
    return code

# --- 6. SUPERVISOR AGENT ---
rag_tool = Tool(name="RAG", func=run_rag_agent, description="Retrieve LangChain documentation.")
code_tool = Tool(name="CodeGen", func=run_code_gen_agent, description="Generate LangChain agents.")
review_tool = Tool(name="Review", func=review_and_revise_code, description="Review and revise Python code.")

tools = [rag_tool, code_tool, review_tool]

supervisor_prompt = ChatPromptTemplate.from_template(
    "Orchestrate tools dynamically to generate, review, and finalize a LangChain agent based on user requirements."
)

def supervisor_agent(input_query, tools, memory, behavior, features):
    rag_response = run_rag_agent(input_query)
    code_response = run_code_gen_agent(tools, memory, behavior, features)
    reviewed_code = review_and_revise_code(code_response)
    return reviewed_code

# --- 7. SHARED MEMORY ---
shared_memory = ConversationBufferMemory()

# --- 8. PARALLEL PROCESSING ---
parallel_agents = RunnableParallel(
    rag=lambda x: run_rag_agent(x["query"]),
    code_gen=lambda x: run_code_gen_agent(x["tools"], x["memory"], x["behavior"], x["features"]),
    review=lambda x: review_and_revise_code(x["code"])
)

# --- 9. END-TO-END WORKFLOW ---
def full_workflow(query, tools, memory, behavior, features):
    shared_memory.save_context({"input": query}, {"output": "Starting workflow..."})

    # Run RAG
    rag_response = run_rag_agent(query)
    shared_memory.save_context({"input": "RAG query"}, {"output": rag_response})

    # Generate code
    code_response = run_code_gen_agent(tools, memory, behavior, features)
    shared_memory.save_context({"input": "Generated code"}, {"output": code_response})

    # Review code
    reviewed_code = review_and_revise_code(code_response)
    shared_memory.save_context({"input": "Reviewed code"}, {"output": reviewed_code})

    return reviewed_code

# --- MAIN EXAMPLE ---
if __name__ == "__main__":
    query = "How do I build an agent that summarizes Wikipedia articles?"
    tools = "Wikipedia tool"
    memory = "ConversationBufferMemory for context retention"
    behavior = "Summarize and format information"
    features = "Error handling, logging, and modularity"

    final_code = full_workflow(query, tools, memory, behavior, features)
    print("Final Generated Agent Code:\n")
    print(final_code)
