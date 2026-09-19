# Production Readiness

## Implemented Real Workflows

- PostgreSQL-only service configuration. Services fail fast instead of creating temporary SQLite databases.
- Candidate CRUD, jobs, applications, PDF resume storage, interview scheduling, screening, and recruiter assistant.
- Resume PDF text extraction.
- Structured Groq resume extraction validated with Pydantic, followed by a real Candidate service update.
- Configurable `GROQ_MODEL` loaded from the root `.env`.
- Screening records with candidate IDs and recruiter-visible status filters.

## Remaining Before Production

1. Add authentication and role-based authorization at the gateway and service boundaries.
2. Replace startup `Base.metadata.create_all` with Alembic migrations. Never run destructive migrations against existing data.
3. Add PostgreSQL constraints, indexes, uniqueness rules, and transaction/outbox handling where cross-service consistency matters.
4. Add the required `users`, `candidate_skills`, `job_skills`, `documents`, `document_chunks`, `evaluations`, `agent_runs`, `agent_tool_calls`, and `audit_logs` data model.
5. Add pgvector and a configurable embedding provider for knowledge-base RAG.
6. Add persisted agent orchestration and real tool-call tracing before adding MCP integrations.
7. Add backend pytest coverage for CRUD, uploads, AI parsing, screening, interview scheduling, failure paths, and authorization.
8. Add rate limits, file size limits, security headers, structured logging, and secret redaction.

These items are intentionally listed as incomplete. The application does not claim to have RAG, MCP, multi-agent orchestration, or production authentication until those workflows are implemented and tested for real.

## Required Local Setup

- Create the PostgreSQL database referenced by `DATABASE_URL`.
- Install `services/requirements.txt`.
- Put a valid `GROQ_API_KEY` and account-accessible `GROQ_MODEL` in the root `.env`.
- Start each service without setting a `DATABASE_URL` override. The service must read the shared root `.env`.
- Start the frontend with `npm run dev`.
