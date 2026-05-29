🚀 AstraMind

An enterprise AI knowledge assistant that lets employees ask questions about company policies and internal documentation — with department-level access controls so Finance can't read HR docs, and Engineering can't access Finance data.

Built with FastAPI, OpenAI, and Retrieval-Augmented Generation (RAG).

✨ Features
Feature🔍RAG-powered answers grounded in your actual company documents🧠Context-aware follow-ups — remembers what was asked earlier in the session💬Persistent conversation memory across sessions🔐JWT Authentication🛡️Role-Based Access Control (RBAC) — department-level data isolation📄PDF and document knowledge retrieval⚡Semantic vector search via embeddings🌐FastAPI REST API☁️Cloud deployment support (Docker + Render)

🏗️ Architecture


<img width="511" height="499" alt="image" src="https://github.com/user-attachments/assets/dc522d7b-02c0-49c0-86d1-6381fbcdf6c9" />


🔒 Access Control
Users can only query documents from departments they are authorized to access.

<img width="518" height="200" alt="image" src="https://github.com/user-attachments/assets/60c74597-87b4-4f24-ba53-5e4440b2db8a" />


🛠️ Tech Stack

<img width="471" height="273" alt="image" src="https://github.com/user-attachments/assets/de6e2658-64c7-47ff-987a-9bc59153ae4e" />




⚙️ Prerequisites
Before running locally, make sure you have:

Python 3.9+
An OpenAI API key
Docker (optional, for containerized deployment)




🚀 Running Locally
1. Clone the repo
bashgit clone <repository-url>
cd AstraMind
2. Create a virtual environment
bashpython -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
3. Install dependencies
bashpip install -r requirements.txt
4. Set up environment variables
Create a .env file in the project root:
envOPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_jwt_secret_key_here
DATABASE_URL=sqlite:///./astramind.db
5. Start the server
bashuvicorn app.main:app --reload
Open the interactive API docs at http://127.0.0.1:8000/docs



📡 API Endpoints

<img width="512" height="297" alt="image" src="https://github.com/user-attachments/assets/bca9728d-2264-46c8-9944-cf96aa5ddfd0" />


👩‍💻 Author

Snehita Bharata

Designed and developed AstraMind as an enterprise AI knowledge assistant focused on secure retrieval, intelligent conversation management, and department-aware access control.
