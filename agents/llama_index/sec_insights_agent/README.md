# SECinsights Agent
Overview

SECinsights Agent is a FastAPI-based application designed for querying and retrieving information from a vectorized document store. It leverages LlamaIndex for indexing and querying, along with PostgreSQL as a vector store for efficient data management.

The application supports:

    REST API with query endpoints.
    CORS for cross-origin requests.
    Seamless document indexing using a PostgreSQL-based vector store.

Features

    FastAPI Framework: Provides an efficient, asynchronous API.
    Vector Store Indexing: Uses LlamaIndex and PGVectorStore for document storage and query operations.
    Dynamic Querying: Allows queries against indexed documents with results generated dynamically.
    CORS Support: Enables interaction with external frontends.

Prerequisites
Dependencies

    Python 3.9+
    PostgreSQL
    Installed Python libraries:
        fastapi
        starlette
        llama-index
        sqlalchemy
        uvicorn

Environment

Ensure that the following environment variables or configuration files are set up:

    DATABASE_URL: Connection string for the PostgreSQL database.

Installation

    Clone the repository:

git clone https://github.com/your-repo-name.git
cd your-repo-name

Install the dependencies:

    pip install -r requirements.txt

    Set up your PostgreSQL database and provide the connection string in the DATABASE_URL environment variable.

    Prepare your documents in the data/ directory.

Usage
Running the Application

Start the application with:

python main.py

Or use Uvicorn directly:

uvicorn main:app --host 0.0.0.0 --port 8000

Querying the API

Use the /query endpoint to search documents:

    URL: http://<host>:<port>/query

    Method: POST

    Payload:

{
  "query": "Your search query here"
}

Response:

    {
      "response": "Relevant information from documents"
    }

Project Structure

.
├── app/
│   ├── core/
│   │   └── config.py       # Configuration and settings
├── data/                   # Directory for documents
├── main.py                 # Main application script
└── requirements.txt        # Python dependencies

