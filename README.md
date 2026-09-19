# RecruitFlow AI

RecruitFlow AI is a recruitment intelligence platform with a Next.js frontend, independent FastAPI services, PostgreSQL persistence, resume storage, interview scheduling, Groq screening, and a recruiter assistant.

## Current Real Workflow

- Candidate CRUD and PDF resume storage in PostgreSQL BYTEA.
- Resume text extraction with `pypdf`.
- Validated Groq resume extraction updates the Candidate service with name, email, phone, education, skills, and experience.
- Job CRUD and application APIs.
- Interview scheduling backed by the Interview service.
- AI screening backed by the Screening service and configurable Groq model.
- Recruiter assistant backed by live candidate, job, and application APIs.
- Candidate screening status list and filters.

SQLite, mock databases, fake AI answers, and temporary database overrides are not supported.

## Configuration

Copy `.env.example` to `.env` and set your real values:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE
GROQ_API_KEY=your_key
GROQ_MODEL=openai/gpt-oss-20b
```

Never commit `.env`. Rotate any credential exposed in chat or logs.

## Start The Frontend

```powershell
npm install
npm run dev
```

Open `http://localhost:3000`.

## Start Services

Install backend dependencies once:

```powershell
python -m pip install -r services/requirements.txt
```

Start each service from its service directory using the shared root `.env`:

```powershell
cd services/candidate-service; $env:PYTHONPATH='.'; python -m uvicorn app.main:app --port 8001
cd services/job-service; $env:PYTHONPATH='.'; python -m uvicorn app.main:app --port 8002
cd services/resume-service; $env:PYTHONPATH='.'; python -m uvicorn app.main:app --port 8003
cd services/screening-service; $env:PYTHONPATH='.'; python -m uvicorn app.main:app --port 8004
cd services/interview-service; $env:PYTHONPATH='.'; python -m uvicorn app.main:app --port 8005
cd services/assistant-service; $env:PYTHONPATH='.'; python -m uvicorn app.main:app --port 8006
cd services/api-gateway; $env:PYTHONPATH='.'; python -m uvicorn app.main:app --port 8000
```

## Validation

```powershell
npx tsc --noEmit
npm run build
python -m compileall -q services
```

## Production Status

Phase 1 core workflows are implemented. Authentication, Alembic migrations, pgvector RAG, persisted agent runs/tool calls/audit logs, MCP integrations, and automated backend tests are still remaining production work. They are intentionally not faked or represented as complete.
# ai-recruitment-intelligence-hub-3a

This is a [Next.js](https://nextjs.org) project bootstrapped with [v0](https://v0.app).

## Built with v0

This repository is linked to a [v0](https://v0.app) project. You can continue developing by visiting the link below -- start new chats to make changes, and v0 will push commits directly to this repo. Every merge to `main` will automatically deploy.

[Continue working on v0 →](https://v0.app/chat/projects/prj_WOtw2yiYBy73OJogDnN1CXk2dmWS)

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## Learn More

To learn more, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
- [v0 Documentation](https://v0.app/docs) - learn about v0 and how to use it.
