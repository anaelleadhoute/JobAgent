Job Description Analyzer Agent
A personal tool that takes a job description (pasted text or a URL), extracts the real requirements, scores honest fit against my actual experience,
and logs the analysis to a database for later querying.
This is a portfolio project built to demonstrate a specific engineering principle:
most of the pipeline is deterministic code (SQL, parsing, structure), and AI is reserved only for the two steps that genuinely need it — extracting meaning from unstructured text, and judging fit. 
It directly addresses interview feedback (Wonderful.ai, June 2026) about over-using LLMs for steps that don't need them.
