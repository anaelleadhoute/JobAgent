-- Job Description Analyzer Agent — schema
-- Two tables: profile (seeded once by hand, source of truth for score_fit)
-- and analyses (one row per JD analyzed, written automatically by the agent).

CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS analyses;
DROP TABLE IF EXISTS profile;

CREATE TABLE profile (
    id              SERIAL PRIMARY KEY,
    category        TEXT NOT NULL,   -- e.g. 'education', 'experience', 'project', 'skill'
    label           TEXT NOT NULL,   -- e.g. 'Mobileye', 'Python'
    detail          TEXT,            -- free-text description / dates / context
    embedding       vector(1536),    -- text-embedding-3-small; populated by embed_profile.py
    created_at      TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX ON profile USING ivfflat (embedding vector_cosine_ops) WITH (lists = 10);

CREATE TABLE analyses (
    id              SERIAL PRIMARY KEY,
    company         TEXT,
    role            TEXT,
    fit_score       INTEGER,
    missing_skills  TEXT,
    source_url      TEXT,            -- nullable; populated only if fetched via URL
    analyzed_at     TIMESTAMP NOT NULL DEFAULT now(),
    status          TEXT             -- nullable; manually updated later by the user
);