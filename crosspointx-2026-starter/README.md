# CrossPointX 2026 — Starter Project

A small React + FastAPI starter for an AI hackathon prototype. It includes:
- React + Vite frontend
- FastAPI backend
- Optional Dify Chat API integration
- Optional OpenAI-compatible API integration (for an AIHubMix-compatible endpoint)
- Health check and a basic chat interface

> This is a reusable foundation, not a finished hackathon solution. Add your chosen track's actual features after your team confirms its problem statement.

## 1. Requirements

- Python 3.10+
- Node.js 20+
- Git
- API credentials only if using Dify or an OpenAI-compatible model endpoint

## 2. Configure environment

From the project root:

```bash
cp backend/.env.example backend/.env
```

On Windows PowerShell:

```powershell
Copy-Item backend/.env.example backend/.env
```

Edit `backend/.env`. Choose one provider:

### Option A — Dify

```env
AI_PROVIDER=dify
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_API_KEY=your_dify_app_api_key
```

### Option B — AIHubMix / OpenAI-compatible endpoint

Use the exact base URL and model name supplied by the hackathon organisers:

```env
AI_PROVIDER=openai_compatible
AIHUBMIX_BASE_URL=your_organiser_provided_base_url
AIHUBMIX_API_KEY=your_team_api_key
AIHUBMIX_MODEL=your_organiser_provided_model_name
```

Do not commit `.env` or share API keys in GitHub, screenshots, frontend code, or chat messages.

## 3. Run the backend

Open a terminal in the project root:

```bash
cd backend
python -m venv .venv
```

Activate the environment:

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install and run:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend:
- API: http://localhost:8000
- Health: http://localhost:8000/health
- Interactive API docs: http://localhost:8000/docs

## 4. Run the frontend

Open a second terminal from the project root:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite (normally http://localhost:5173).

## 5. Git workflow for a five-person team

Create a branch for each task, for example:

```bash
git switch -c feature/frontend
git add .
git commit -m "Build initial frontend"
git push -u origin feature/frontend
```
