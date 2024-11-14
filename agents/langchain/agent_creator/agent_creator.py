from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.tools import Tool
from langchain.agents import create_openai_functions_agent
from langchain_core.runnables import RunnableParallel
from langchain.memory import ConversationBufferMemory

# --- 1. SETUP LANGCHAIN DOCUMENT DATABASE ---
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

# --- 2. RAG AGENT ---
rag_template = """
Use the provided LangChain documentation context to answer the query. Be comprehensive and provide actionable insights.

Context:
{context}

Query:
{query}
"""

rag_prompt = ChatPromptTemplate.from_template(rag_template)
model = ChatOpenAI(temperature=0.2, model="gpt-4")
output_parser = StrOutputParser()

def run_rag_agent(query):
    context = retriever.get_relevant_documents(query)
    context_text = "\n".join([doc.page_content for doc in context])
    rag_chain = rag_prompt | model | output_parser
    response = rag_chain.invoke({"context": context_text, "query": query})
    return response

# --- 3. CODE-GENERATION AGENT ---
code_gen_template = """
Write Python code for a LangChain agent with the following specifications:
1. Tools: {tools}
2. Memory: {memory}
3. Behavior: {behavior}
4. Advanced Features: {features}

Provide complete and executable Python code.
"""

code_gen_prompt = PromptTemplate.from_template(code_gen_template)
code_gen_parser = JsonOutputParser()

def run_code_gen_agent(tools, memory, behavior, features):
    input_data = {
        "tools": tools,
        "memory": memory,
        "behavior": behavior,
        "features": features
    }
    chain = code_gen_prompt | model | code_gen_parser
    return chain.invoke(input_data)

# --- 4. CRITICAL REVIEW AGENT ---
review_template = """
Review the following Python code for correctness, completeness, and alignment with LangChain standards:
{code}

Provide a list of issues and suggestions.
"""

review_prompt = ChatPromptTemplate.from_template(review_template)

def review_and_revise_code(code):
    review_chain = review_prompt | model | output_parser
    feedback = review_chain.invoke({"code": code})

    # If issues are found, revise the code
    if "issue" in feedback.lower():
        revision_prompt = ChatPromptTemplate.from_template(
            "Revise the following code based on this feedback:\n\nCode:\n{code}\n\nFeedback:\n{feedback}"
        )
        revise_chain = revision_prompt | model | output_parser
        revised_code = revise_chain.invoke({"code": code, "feedback": feedback})
        return revised_code
    return code

# --- 5. SUPERVISOR AGENT ---
rag_tool = Tool(name="RAG", func=run_rag_agent, description="Retrieve LangChain documentation.")
code_tool = Tool(name="CodeGen", func=run_code_gen_agent, description="Generate agents.")
review_tool = Tool(name="Review", func=review_and_revise_code, description="Review and revise code.")

tools = [rag_tool, code_tool, review_tool]

supervisor_prompt = ChatPromptTemplate.from_template(
    "Orchestrate tools dynamically to generate, review, and finalize a LangChain agent based on user requirements."
)
supervisor_agent = create_openai_functions_agent(llm=model, tools=tools, prompt=supervisor_prompt)

# --- 6. SHARED MEMORY ---
shared_memory = ConversationBufferMemory()

# --- 7. PARALLEL PROCESSING ---
parallel_agents = RunnableParallel(
    rag=lambda x: run_rag_agent(x["query"]),
    code_gen=lambda x: run_code_gen_agent(x["tools"], x["memory"], x["behavior"], x["features"]),
    review=lambda x: review_and_revise_code(x["code"])
)

# --- 8. END-TO-END WORKFLOW ---
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
