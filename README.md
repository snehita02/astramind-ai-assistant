🚀 AstraMind

An enterprise AI knowledge assistant that lets employees ask questions about company policies and internal documentation — with department-level access controls so Finance can't read HR docs, and Engineering can't access Finance data.

Built with FastAPI, OpenAI, and Retrieval-Augmented Generation (RAG).

✨ Features

🔍 RAG-powered answers grounded in your actual company documents
🧠 Context-aware follow-ups — the assistant remembers what was asked earlier in the session
💬 Persistent conversation memory across sessions
🔐 JWT Authentication
🛡️ Role-Based Access Control (RBAC) — department-level data isolation
📄 PDF and document knowledge retrieval
⚡ Semantic vector search via embeddings
🌐 FastAPI REST API
☁️ Cloud deployment support (Docker + Render)


🏗️ Architecture
text                 ┌─────────────────┐
                     │     User UI     │
                     └────────┬────────┘
                              │
                              ▼
                  ┌─────────────────────┐
                  │   FastAPI Backend   │
                  └────────┬────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
 ┌────────────────┐ ┌───────────────┐ ┌──────────────┐
 │ Authentication │ │ Chat Memory   │ │ Authorization│
 │     (JWT)      │ │  (Sessions)   │ │   (RBAC)     │
 └────────┬───────┘ └───────┬───────┘ └──────┬───────┘
          │                 │                │
          └─────────────────┼────────────────┘
                            ▼
                  ┌──────────────────┐
                  │ Query Processing │
                  │ & Follow-Ups     │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │ Vector Search    │
                  │ (Embeddings)     │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │ Context Builder  │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │ OpenAI LLM       │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │ Grounded Answer  │
                  └──────────────────┘

🔒 Access Control
Users can only query documents from departments they are authorized to access:
UserAccessible DepartmentsHR UserHR + GeneralFinance UserFinance + GeneralEngineering UserEngineering + GeneralAdminAll departments

🛠️ Tech Stack
LayerTechnologyBackendPython, FastAPILLMOpenAI APISearchVector EmbeddingsDatabaseSQLite (dev) / PostgreSQL (prod)AuthJWTDeploymentDocker, Render

⚙️ Prerequisites
Before running locally, make sure you have:

Python 3.9+
An OpenAI API key
(Optional) Docker, for containerized deployment


🚀 Running Locally
1. Clone the repo
bashgit clone <repository-url>
cd AstraMind
2. Create a virtual environment
bashpython -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3. Install dependencies
bashpip install -r requirements.txt
4. Set up environment variables
Create a .env file in the project root:
envOPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_jwt_secret_key_here
DATABASE_URL=sqlite:///./astramind.db   # or your PostgreSQL URL
5. Start the server
bashuvicorn app.main:app --reload
Visit the interactive API docs at:
http://127.0.0.1:8000/docs

📡 API Endpoints
MethodEndpointDescriptionPOST/auth/loginAuthenticate and receive a JWT tokenPOST/api/v1/askAsk a question (RAG-powered)GET/api/v1/chat-history/{session_id}Retrieve conversation historyPOST/auth/admin/create-userCreate a new user (Admin only)
Example: Ask a question
bashcurl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the remote work policy?", "session_id": "abc123"}'
json{
  "answer": "Employees may work remotely up to 3 days per week, subject to manager approval...",
  "sources": ["hr_policy_2024.pdf"],
  "session_id": "abc123"
}

👩‍💻 Author
Snehita Bharata 
Designed and developed AstraMind as an enterprise AI knowledge assistant focused on secure retrieval, intelligent conversation management, and department-aware access control.
