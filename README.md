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
#mermaid-rmt3{font-family:inherit;font-size:16px;fill:#E5E5E5;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-rmt3 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-rmt3 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-rmt3 .error-icon{fill:#CC785C;}#mermaid-rmt3 .error-text{fill:#3387a3;stroke:#3387a3;}#mermaid-rmt3 .edge-thickness-normal{stroke-width:1px;}#mermaid-rmt3 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-rmt3 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-rmt3 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-rmt3 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-rmt3 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-rmt3 .marker{fill:#A1A1A1;stroke:#A1A1A1;}#mermaid-rmt3 .marker.cross{stroke:#A1A1A1;}#mermaid-rmt3 svg{font-family:inherit;font-size:16px;}#mermaid-rmt3 p{margin:0;}#mermaid-rmt3 .label{font-family:inherit;color:#E5E5E5;}#mermaid-rmt3 .cluster-label text{fill:#3387a3;}#mermaid-rmt3 .cluster-label span{color:#3387a3;}#mermaid-rmt3 .cluster-label span p{background-color:transparent;}#mermaid-rmt3 .label text,#mermaid-rmt3 span{fill:#E5E5E5;color:#E5E5E5;}#mermaid-rmt3 .node rect,#mermaid-rmt3 .node circle,#mermaid-rmt3 .node ellipse,#mermaid-rmt3 .node polygon,#mermaid-rmt3 .node path{fill:transparent;stroke:#A1A1A1;stroke-width:1px;}#mermaid-rmt3 .rough-node .label text,#mermaid-rmt3 .node .label text,#mermaid-rmt3 .image-shape .label,#mermaid-rmt3 .icon-shape .label{text-anchor:middle;}#mermaid-rmt3 .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-rmt3 .rough-node .label,#mermaid-rmt3 .node .label,#mermaid-rmt3 .image-shape .label,#mermaid-rmt3 .icon-shape .label{text-align:center;}#mermaid-rmt3 .node.clickable{cursor:pointer;}#mermaid-rmt3 .root .anchor path{fill:#A1A1A1!important;stroke-width:0;stroke:#A1A1A1;}#mermaid-rmt3 .arrowheadPath{fill:#0b0b0b;}#mermaid-rmt3 .edgePath .path{stroke:#A1A1A1;stroke-width:1px;}#mermaid-rmt3 .flowchart-link{stroke:#A1A1A1;fill:none;}#mermaid-rmt3 .edgeLabel{background-color:transparent;text-align:center;}#mermaid-rmt3 .edgeLabel p{background-color:transparent;}#mermaid-rmt3 .edgeLabel rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-rmt3 .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#mermaid-rmt3 .cluster rect{fill:#CC785C;stroke:hsl(15, 12.3364485981%, 48.0392156863%);stroke-width:1px;}#mermaid-rmt3 .cluster text{fill:#3387a3;}#mermaid-rmt3 .cluster span{color:#3387a3;}#mermaid-rmt3 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:inherit;font-size:12px;background:#CC785C;border:1px solid hsl(15, 12.3364485981%, 48.0392156863%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-rmt3 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#E5E5E5;}#mermaid-rmt3 rect.text{fill:none;stroke-width:0;}#mermaid-rmt3 .icon-shape,#mermaid-rmt3 .image-shape{background-color:transparent;text-align:center;}#mermaid-rmt3 .icon-shape p,#mermaid-rmt3 .image-shape p{background-color:transparent;padding:2px;}#mermaid-rmt3 .icon-shape .label rect,#mermaid-rmt3 .image-shape .label rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-rmt3 .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-rmt3 .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-rmt3 .node .neo-node{stroke:#A1A1A1;}#mermaid-rmt3 [data-look="neo"].node rect,#mermaid-rmt3 [data-look="neo"].cluster rect,#mermaid-rmt3 [data-look="neo"].node polygon{stroke:url(#mermaid-rmt3-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-rmt3 [data-look="neo"].node path{stroke:url(#mermaid-rmt3-gradient);stroke-width:1px;}#mermaid-rmt3 [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-rmt3 [data-look="neo"].node .neo-line path{stroke:#A1A1A1;filter:none;}#mermaid-rmt3 [data-look="neo"].node circle{stroke:url(#mermaid-rmt3-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-rmt3 [data-look="neo"].node circle .state-start{fill:#000000;}#mermaid-rmt3 [data-look="neo"].icon-shape .icon{fill:url(#mermaid-rmt3-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-rmt3 [data-look="neo"].icon-shape .icon-neo path{stroke:url(#mermaid-rmt3-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-rmt3 :root{--mermaid-font-family:inherit;}👤 User UIFastAPI Backend🔐 AuthenticationJWT🧠 Chat MemorySessions🛡️ AuthorizationRBACQuery Processing& Follow-UpsVector SearchEmbeddingsContext BuilderOpenAI LLM✅ Grounded Answer

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
Snehita Bharata — LinkedIn · GitHub
Designed and developed AstraMind as an enterprise AI knowledge assistant focused on secure retrieval, intelligent conversation management, and department-aware access control.
