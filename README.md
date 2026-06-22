# Job Description Analyzer Agent

A personal tool that takes a job description (pasted text or a URL), extracts the real requirements, scores honest fit against my actual experience, and logs the analysis to a database for later querying.

This is a portfolio project built to demonstrate a specific engineering principle: most of the pipeline is deterministic code (SQL, parsing, structure), and AI is reserved only for the two steps that genuinely need it — extracting meaning from unstructured text, and judging fit. It directly addresses interview feedback (Wonderful.ai, June 2026) about over-using LLMs for steps that don't need them.


curl -X POST https://jd-analyzer-396478058418.us-central1.run.app/analyze \
  -H "Content-Type: application/json" \
  -d '{"jd_text": "We are looking for a Senior ML Engineer at Anthropic. Must have Python, PyTorch, 5+ years ML experience. Nice to have: Kubernetes, RLHF."}'

  
## Stack

- Python, FastAPI
- PostgreSQL (real database — load-bearing for the interview story, not SQLite)
- Raw OpenAI tool-calling agent loop (no LangChain/LangGraph abstractions — the loop is visible and explainable, same pattern as HW3)
- Docker + GCP Cloud Run for deployment
- Environment variables for all secrets

## Database schema

### `profile`
Seeded once by hand with my real, verified skills and experience. Source of truth for `score_fit`. Contains only accurate information — no fabricated or unverified skills.

| column | type | notes |
|---|---|---|
| id | serial | primary key |
| category | text | `education` / `experience` / `project` / `skill` |
| label | text | short name, e.g. "Mobileye", "Python" |
| detail | text | free-text description / dates |
| created_at | timestamp | default now() |

### `analyses`
One row per JD analyzed. Written automatically by the agent. **Not** a record of an actual job application — just a record that an analysis happened.

| column | type | notes |
|---|---|---|
| id | serial | primary key |
| company | text | |
| role | text | |
| fit_score | integer | |
| missing_skills | text | |
| source_url | text | nullable — only populated if fetched via URL |
| analyzed_at | timestamp | default now() |
| status | text | nullable — manually updated later: `applied` / `interviewing` / `rejected` / null |

## Agent tools

1. **`fetch_job_posting(url)`** — optional first step, fetches a job posting page and extracts raw text. No LLM call.
2. **`extract_requirements(jd_text)`** — LLM call. Pulls structured data out of messy JD text: company, role, must-have skills, nice-to-have skills, seniority level.
3. **`score_fit(requirements, profile)`** — LLM call. Compares extracted requirements against the real profile. Must produce an honest score and explicitly list real gaps — no flattery, no softening.
4. **`log_analysis(...)`** — pure SQL INSERT into `analyses`. No LLM call. Runs automatically after every analysis.
5. **`query_analyses(sql_or_filter)`** — pure SQL SELECT against logged history. No LLM needed.

## Flow

1. Paste JD text (or a URL) into the `/analyze` FastAPI endpoint.
2. Agent loop starts: system prompt + input + tool list sent to the LLM.
3. If a URL was given, `fetch_job_posting` runs first.
4. `extract_requirements` runs, pulling out company/role/skills.
5. `score_fit` runs, comparing extracted skills against the profile table.
6. `log_analysis` runs automatically, writing a row to `analyses`.
7. LLM generates a final plain-language answer: score + real gaps, no flattery.
8. Answer returned; row now exists for later querying via `query_analyses`.

## Non-goals (intentionally cut)

- No RAG layer — no unstructured document corpus that justifies it
- No trained ML model / churn-prediction component
- No active job-board scraping
- No company research / web search enrichment (possible phase 2)

## Local setup

### Prerequisites
- Python 3.10+
- PostgreSQL running locally (see `db/schema.sql` and `db/seed.sql`)
- An OpenAI API key

### Database setup

```bash
# create a dedicated user and database
psql -U postgres -h localhost
```
```sql
CREATE USER jdanalyzer WITH PASSWORD 'your_dev_password';
CREATE DATABASE jdanalyzer_db OWNER jdanalyzer;
\q
```

```bash
# create tables
psql -U jdanalyzer -d jdanalyzer_db -h localhost -f db/schema.sql

# seed with real profile data
psql -U jdanalyzer -d jdanalyzer_db -h localhost -f db/seed.sql
```

### Environment variables

Create a `.env` file (never commit this):

```
OPENAI_API_KEY=sk-...
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jdanalyzer_db
DB_USER=jdanalyzer
DB_PASSWORD=your_dev_password
```

### Run the app

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then POST job description text or a URL to `/analyze`.

## Build progress

- [x] PostgreSQL schema created (`profile`, `analyses`)
- [x] `profile` seeded with real verified facts
- [ ] Five tools implemented
- [ ] Raw OpenAI tool-calling agent loop
- [ ] FastAPI `/analyze` endpoint
- [ ] `fetch_job_posting` URL enhancement
- [ ] Dockerized
- [ ] Deployed to GCP Cloud Run (Cloud SQL + env vars)

## Deployment

Deployed via Docker to GCP Cloud Run, with PostgreSQL provided by Cloud SQL in production. All secrets (API keys, DB credentials) are injected as environment variables — never hardcoded.
