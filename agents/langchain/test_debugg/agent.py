import os
import json
import re
import requests
import sqlite3
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_core.runnables import RunnableParallel


# Function to query the LM-Studio local LLM API
def query_local_llm(prompt: str, api_endpoint: str = "http://localhost:5000/api"):
    try:
        response = requests.post(api_endpoint, json={"prompt": prompt})
        response.raise_for_status()
        return response.json().get("response", "No response from the model.")
    except requests.exceptions.RequestException as e:
        return f"Error querying local LLM: {str(e)}"


# Streaming Function for Real-Time Interaction
def stream_response(prompt: str, llm_model="gpt-3.5-turbo"):
    streaming_llm = ChatOpenAI(model=llm_model, streaming=True)
    response = streaming_llm.stream([HumanMessage(content=prompt)])
    print("Real-Time Response:")
    for chunk in response:
        if isinstance(chunk, AIMessage):
            print(chunk.content, end="", flush=True)
    print("\n")


# Enhanced Log Parser with Loguru and Regex
def enhanced_log_parser(log_dir: str = "./logs", patterns: List[str] = None):
    """
    Analyzes log files using regex patterns and enhanced logging.
    """
    patterns = patterns or [r"ERROR.*", r"WARNING.*", r"CRITICAL.*"]
    log_summary = {"ERROR": [], "WARNING": [], "CRITICAL": []}

    logger.info(f"Starting log analysis in directory: {log_dir}")

    try:
        for file in os.listdir(log_dir):
            if file.endswith(".log"):
                logger.info(f"Processing log file: {file}")
                with open(os.path.join(log_dir, file), "r") as f:
                    for line in f:
                        for pattern in patterns:
                            match = re.search(pattern, line)
                            if match:
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                if "ERROR" in pattern:
                                    log_summary["ERROR"].append(f"{timestamp}: {line.strip()}")
                                elif "WARNING" in pattern:
                                    log_summary["WARNING"].append(f"{timestamp}: {line.strip()}")
                                elif "CRITICAL" in pattern:
                                    log_summary["CRITICAL"].append(f"{timestamp}: {line.strip()}")
        logger.success("Log analysis completed.")
        return log_summary
    except Exception as e:
        logger.error(f"Error reading or parsing log files: {str(e)}")
        return f"Error reading or parsing log files: {str(e)}"


# Dependency Resolver with npm Registry Metadata
def resolve_dependency_conflicts():
    """
    Resolves dependency conflicts by fetching metadata from the npm registry API.
    """
    def fetch_latest_version(package_name):
        url = f"https://registry.npmjs.org/{package_name}/latest"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("version", "unknown")
        except requests.RequestException as e:
            logger.error(f"Error fetching latest version for {package_name}: {str(e)}")
            return "unknown"

    try:
        with open("package.json", "r") as f:
            package_data = json.load(f)

        resolved_dependencies = {}
        conflict_logs = []

        # Resolve dependencies
        for dep, current_version in package_data.get("dependencies", {}).items():
            latest_version = fetch_latest_version(dep)
            if latest_version != "unknown" and current_version != latest_version:
                conflict_logs.append(f"Conflict: {dep} ({current_version}) -> Resolved: {latest_version}")
                resolved_dependencies[dep] = latest_version
            else:
                resolved_dependencies[dep] = current_version

        # Resolve devDependencies
        for dep, current_version in package_data.get("devDependencies", {}).items():
            latest_version = fetch_latest_version(dep)
            if latest_version != "unknown" and current_version != latest_version:
                conflict_logs.append(f"Conflict: {dep} ({current_version}) -> Resolved: {latest_version}")
                resolved_dependencies[dep] = latest_version
            else:
                resolved_dependencies[dep] = current_version

        # Update package.json
        package_data["dependencies"] = resolved_dependencies
        package_data["devDependencies"] = resolved_dependencies

        with open("package.json", "w") as f:
            json.dump(package_data, f, indent=2)

        logger.success("Dependency conflicts resolved.")
        return f"Dependencies resolved. Conflicts:\n" + "\n".join(conflict_logs)
    except Exception as e:
        logger.error(f"Error resolving dependency conflicts: {str(e)}")
        return f"Error resolving dependency conflicts: {str(e)}"


# Function to install dependencies
def npm_install():
    try:
        os.system("npm install")
        return "Dependencies installed successfully."
    except Exception as e:
        logger.error(f"Error running npm install: {str(e)}")
        return f"Error running npm install: {str(e)}"


# Real-Time Monitoring
class LogMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".log"):
            with open(event.src_path, "r") as f:
                lines = f.readlines()[-10:]  # Read the last 10 lines
                for line in lines:
                    if "CRITICAL" in line:
                        logger.critical(f"Critical Log Detected: {line.strip()}")


observer = Observer()
observer.schedule(LogMonitorHandler(), path="./logs", recursive=False)
observer.start()


# Tools and Agents
critical_tool = Tool(name="analyze_logs", func=enhanced_log_parser, description="Analyze critical logs.")
dependency_tool = Tool(name="resolve_conflicts", func=resolve_dependency_conflicts, description="Resolve dependency conflicts.")
install_tool = Tool(name="npm_install", func=npm_install, description="Install npm dependencies.")

critical_agent = create_openai_functions_agent(
    ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    tools=[critical_tool],
    prompt=ChatPromptTemplate.from_template("Analyze critical logs. {input}"),
)

dependency_agent = create_openai_functions_agent(
    ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    tools=[dependency_tool, install_tool],
    prompt=ChatPromptTemplate.from_template("Resolve dependency conflicts. {input}"),
)


# Shared Memory
shared_memory = ConversationBufferMemory()

# Agents with Shared Memory
critical_agent_executor = AgentExecutor(agent=critical_agent, memory=shared_memory, verbose=True)
dependency_agent_executor = AgentExecutor(agent=dependency_agent, memory=shared_memory, verbose=True)

# Multi-Agent Coordination
multi_agent_coordinator = RunnableParallel(
    critical_agent=critical_agent_executor,
    dependency_agent=dependency_agent_executor,
)

# Dynamic Tool Dispatcher
def dynamic_tool_dispatcher(input_query: str):
    if "log" in input_query.lower():
        return critical_agent_executor
    elif "dependency" in input_query.lower() or "install" in input_query.lower():
        return dependency_agent_executor
    else:
        return None

def execute_query_dynamically(query: str):
    agent = dynamic_tool_dispatcher(query)
    if agent:
        return agent.invoke({"input": query})
    else:
        return "No suitable agent found for the query."


# CLI Interface for User Input
def cli_interface():
    import argparse
    parser = argparse.ArgumentParser(description="Multi-Agent Assistant CLI")
    parser.add_argument("--query", type=str, help="Query for the assistant.")
    args = parser.parse_args()

    if args.query:
        response = execute_query_dynamically(args.query)
        print(f"Response: {response}")


# Example Queries
queries = [
    "Analyze logs for critical issues.",
    "Resolve dependency conflicts.",
    "Run npm install.",
]

for query in queries:
    response = execute_query_dynamically(query)
    print(f"Query: {query}\nResponse: {response}\n")
