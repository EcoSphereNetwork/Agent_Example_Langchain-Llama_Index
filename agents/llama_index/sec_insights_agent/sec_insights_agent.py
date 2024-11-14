import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import PGVectorStore
from llama_index.storage.storage_context import StorageContext
from sqlalchemy import create_engine
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="SECinsights Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection
engine = create_engine(settings.DATABASE_URL)
vector_store = PGVectorStore.from_engine(engine)

# Load documents
documents = SimpleDirectoryReader('data').load_data()

# Create index
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

@app.post("/query")
async def query_documents(query: str):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return {"response": str(response)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
