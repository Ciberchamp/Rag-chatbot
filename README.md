# RAG HR Chatbot
A Retrieval-Augmented Generation (RAG) chatbot for answering HR policy documentation queries using FAISS, BM25 re-ranking, and caching.

**Features as per rquirement**
- Document Processing: PDF text extraction, cleaning, and chunking
- Vector Search: FAISS index with embeddings
- Re-ranking: BM25 scoring on top of FAISS results
- Caching: Query cache to avoid repeated LLM calls
- Lightweight: Uses TF-IDF instead of heavy sentence transformers
- Dockerized: Complete containerization for easy deployment

**Architecture** 

Frontend (Streamlit) → Backend (FastAPI) → FAISS Index → Groq LLM

**Installation**

To Clone repository use commands:
git clone <your-repo-url>
cd rag-chatbot

For data folder HR policy PDF is already included

**Set environment variables**
create .env file in root folder and add
"GROQ_API_KEY=your_groq_api_key" (add your own groq api key value here) 

**to Run with Docker**
docker-compose up --build

**Usage**
Access frontend: http://localhost:8501

Example queries:
tell me about leave policy?
attendance policy?
working hours?

**Performance Optimization though self experiment**
This implementation uses TF-IDF instead of Sentence Transformers to:
Reduce build time from 40+ minutes to 3 minutes
Eliminate GPU dependencies
Simplify deployment
Reduce image size by 1.5GB to 2GB+
Avoid complex model downloads (like pytorch or Nvidia models for gpu)

**Security Notes**
API keys stored in .env (excluded via .gitignore)
No sensitive data committed to the repository
Docker containers run in isolation
Groq API calls secured via HTTPS
No persistent data storage

**Technical Stack**
Backend: FastAPI, FAISS, Scikit-learn (TF-IDF)
Frontend: Streamlit
LLM: Groq API (Llama instant) currently valid in groq
Embeddings: TF-IDF vectors (lightweight)
Cache: JSON-based query caching

**Docker Images**
Pre-built images available on Docker Hub: https://hub.docker.com/repositories/ciberchamp
Backend:
docker pull ciberchamp/rag-chatbot-backend:latest
Frontend:
docker pull ciberchamp/rag-chatbot-frontend:latest

Run manually:
**Start backend**
docker run -p 8000:8000 ciberchamp/rag-chatbot-backend:latest
**Start frontend**
docker run -p 8501:8501 ciberchamp/rag-chatbot-frontend:latest
Or run both together:
docker-compose up

**Known Issues**
View source in ui might give incomplete response due to model capacity
Docker compatibility warnings may appear on some Windows setups
