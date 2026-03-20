import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env
from dotenv import load_dotenv
load_dotenv()

# We define the lifespan dict to hold our SBERT model
@asynccontextmanager
async def lifespan(app: FastAPI):
    from core.embedder import Embedder
    
    # Load model on startup
    logger.info("Initializing Embedder...")
    model_name = os.getenv("SBERT_MODEL", "all-MiniLM-L6-v2")
    embedder = Embedder(model_name)
    embedder.load()
    app.state.embedder = embedder
    logger.info("Embedder loaded successfully.")
    
    yield
    # Unload on shutdown
    logger.info("Shutting down...")
    app.state.embedder = None

app = FastAPI(lifespan=lifespan, title="RoleReady AI Backend")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root/Health Check
@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": app.state.embedder is not None}

# Include routers eventually here...
from api.routes import router as api_router
app.include_router(api_router)
