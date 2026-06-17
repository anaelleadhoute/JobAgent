-- Job Description Analyzer Agent — seed data for profile table
-- Only verified, real facts. Do not add unverified skills.

INSERT INTO profile (category, label, detail) VALUES
('education', 'BSc Electrical Engineering', 'Tel Aviv University'),
('education', 'MSc Computer Science (ML track)', 'Reichman University, ongoing'),

('experience', 'Mobileye', 'Design Verification Engineer, Jan 2023 - Sep 2025. Radar/lidar subsystems, Python tooling, large-scale simulation data analysis, root cause debugging.'),
('experience', 'Intel', 'Logic Design Engineer, May 2022 - Dec 2022. RTL/Verilog, Python automation.'),

('project', 'LangGraph self-correcting CSV agent', 'HW2 - agent that generates and self-corrects Python programs operating on CSV data.'),
('project', 'Raw OpenAI tool-calling agent (6 tools)', 'HW3 - tools for SQL, image extraction, calculator, web search, file writer.'),
('project', 'Gene expression / differential analysis', 'WRS test, FDR correction, Kendall tau on AMI vs. healthy cohorts.'),

('skill', 'Python', NULL),
('skill', 'MATLAB', NULL),
('skill', 'C', NULL),
('skill', 'OpenAI API', NULL),
('skill', 'LangGraph', NULL),
('skill', 'Prompt engineering', NULL),
('skill', 'Tool-calling / agent design', NULL),
('skill', 'pandas', NULL),
('skill', 'NumPy', NULL),
('skill', 'scikit-learn', NULL),
('skill', 'SQL', NULL),
('skill', 'Git', NULL),
('skill', 'JIRA', NULL),
('skill', 'RAG pipelines', 'From coursework, not production deployment experience.');