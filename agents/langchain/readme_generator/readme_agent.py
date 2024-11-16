import os
import json
from github import Github
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from flask import Flask, request, render_template_string
from rich.console import Console
from rich.markdown import Markdown
import markdown2
from http.server import SimpleHTTPRequestHandler
import socketserver
import argparse


# GitHub API Integration
def fetch_repo_details(github_token, repo_name):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    details = {
        "name": repo.name,
        "description": repo.description or "No description provided.",
        "url": repo.html_url,
        "languages": repo.get_languages(),
        "open_issues": repo.open_issues_count,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
    }
    return details


def create_pull_request(github_token, repo_name, branch_name, file_path, commit_message):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    with open(file_path, "r") as file:
        content = file.read()

    # Create a branch
    ref = repo.get_git_ref("heads/main")
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=ref.object.sha)

    # Push changes
    repo.create_file(
        path="README.md",
        message=commit_message,
        content=content,
        branch=branch_name,
    )

    # Create PR
    pr = repo.create_pull(
        title="Add or Update README.md",
        body="This pull request updates the README file with detailed content.",
        head=branch_name,
        base="main",
    )
    return pr.html_url


# Automatic Dependency Parsing
def parse_python_dependencies(repo_path):
    req_path = f"{repo_path}/requirements.txt"
    if not os.path.exists(req_path):
        return "No `requirements.txt` found."
    with open(req_path, "r") as file:
        dependencies = file.readlines()
    return "\n".join(f"- {dep.strip()}" for dep in dependencies)


def parse_node_dependencies(repo_path):
    pkg_path = f"{repo_path}/package.json"
    if not os.path.exists(pkg_path):
        return "No `package.json` found."
    with open(pkg_path, "r") as file:
        data = json.load(file)
    dependencies = data.get("dependencies", {})
    return "\n".join(f"- {dep}: {version}" for dep, version in dependencies.items())


# Markdown Preview
def preview_markdown(file_path):
    console = Console()
    with open(file_path, "r") as file:
        md = Markdown(file.read())
    console.print(md)


def live_preview(file_path, port=8000):
    with open(file_path, "r") as file:
        html_content = markdown2.markdown(file.read())

    class MarkdownPreviewHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode())

    with socketserver.TCPServer(("", port), MarkdownPreviewHandler) as httpd:
        print(f"Preview available at http://localhost:{port}")
        httpd.serve_forever()


# Custom Sections
def add_custom_sections(base_content, custom_sections):
    for section_name, section_content in custom_sections.items():
        base_content += f"\n\n## {section_name}\n{section_content}"
    return base_content


# Interactive Web-Based Editor
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def editor():
    if request.method == "POST":
        content = request.form["markdown"]
        with open("README.md", "w") as file:
            file.write(content)
        return "README.md saved successfully!"
    with open("README.md", "r") as file:
        current_content = file.read()
    return render_template_string("""
        <!doctype html>
        <title>Edit README</title>
        <form method="post">
            <textarea name="markdown" style="width:100%;height:90%;">{{ content }}</textarea>
            <button type="submit">Save</button>
        </form>
    """, content=current_content)


# LangChain README Generation
def analyze_repo(repo_path):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    loader = DirectoryLoader(repo_path, glob="**/*")
    documents = loader.load_and_split(text_splitter)
    return documents


def generate_prompt(project_name, template_type="detailed"):
    if template_type == "minimal":
        return PromptTemplate.from_template("""
# {project_name}

## Description
{description}

## Usage
{usage}

## Installation
{installation}
""")
    return PromptTemplate.from_template("""
# {project_name} 🚀✨

## 📖 Description
{description}

## 📂 Project Structure
{structure}

## 🛠️ Installation
{installation}

## 🚀 Usage
{usage}

## 🤝 Contributing
{contributing}

---
Generated with ❤️ using the AI-powered README Generator.
""")


def create_readme(repo_path, project_name, template_type="detailed"):
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = generate_prompt(project_name, template_type)
    chain = LLMChain(llm=llm, prompt=prompt)

    inputs = {
        "project_name": project_name,
        "description": "Extracted or summarized description of the project.",
        "usage": "Auto-generated usage instructions.",
        "installation": "Installation steps derived from dependencies.",
        "structure": "Auto-detected directory structure.",
        "contributing": "Contribution guidelines (if available)."
    }

    readme_content = chain.run(inputs)
    return readme_content


# CLI Integration
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced README Generator")
    parser.add_argument("--repo", required=True, help="Path to repository.")
    parser.add_argument("--github-token", required=True, help="GitHub API token.")
    parser.add_argument("--repo-name", required=True, help="GitHub repository name.")
    parser.add_argument("--branch-name", default="readme-update", help="Branch name.")
    parser.add_argument("--template", default="detailed", help="Template type.")
    args = parser.parse_args()

    # Fetch repo details
    details = fetch_repo_details(args.github_token, args.repo_name)

    # Parse dependencies
    python_deps = parse_python_dependencies(args.repo)
    node_deps = parse_node_dependencies(args.repo)

    # Generate README
    readme_content = create_readme(args.repo, details["name"], args.template)
    readme_content += f"\n\n## Dependencies\n### Python\n{python_deps}\n### Node.js\n{node_deps}"

    # Save README
    with open(f"{args.repo}/README.md", "w") as file:
        file.write(readme_content)

    # Preview README
    preview_markdown(f"{args.repo}/README.md")

    # Optionally push to GitHub
    pr_url = create_pull_request(
        args.github_token, args.repo_name, args.branch_name, f"{args.repo}/README.md", "Update README"
    )
    print(f"Pull request created: {pr_url}")
