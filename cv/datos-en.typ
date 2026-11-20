#import "plantilla.typ": *
#show: cv.with(
  lang: "en",
  rol: "Data Engineer · Machine Learning",
  disponibilidad: "Available immediately · Hybrid in Lima or remote (UTC-5)",
  lugar: "Lima, Peru",
  extra: (("orcid.org/0009-0005-6789-076X", "https://orcid.org/0009-0005-6789-076X"),),
)

= Summary
Data and machine learning engineer with 2+ years of internship experience on production software (SQL, TypeScript, Docker). Co-author of 2 Q1 papers in Frontiers journals (2026) using classical ML in Python (XGBoost, LightGBM, K-Means, SARIMAX), reproducible pipelines and CI/CD on GitHub Actions.

= Technical skills
#habilidades(
  ("Languages", "Python, SQL (window functions, CTEs), TypeScript, JavaScript"),
  ("Data", "pandas, ETL in Python, data modeling, MySQL, PostgreSQL, SQLite, Redis, BullMQ"),
  ("Machine learning", "scikit-learn, XGBoost, LightGBM, SARIMAX, K-Means, FAMD, LSTM (PyTorch)"),
  ("MLOps & DevOps", "Docker, GitHub Actions (CI/CD), Git, FastAPI, Quarto, AWS (Lambda, S3, IAM, VPC)"),
  ("Quality", "pytest, data contracts with Zod, reproducible results"),
)

= Experience
#entrada(
  "Full Stack Developer Intern",
  derecha: "Mar 2025 – Sep 2026",
  sub: [J&P Periféricos SAC #sep() Lima, Peru · Hybrid],
  stack: "SQL · MySQL · PHP · Laravel · TypeScript · Docker",
)[
  - Cut invoice list load time from 4–5 min to under 30 s (\~90%) by optimizing SQL queries and caching.
  - Modeled audit tables for a Kanban board in the ERP, adopted by 2 client companies besides J&P.
  - Led a team of 4 across parallel projects: an ERP for law firms and an inventory ticketing system.
]

#entrada(
  "Full Stack Developer Intern",
  derecha: "Jun 2024 – Nov 2025",
  sub: [Codecta Perú #sep() Remote · distributed team in Chile],
  stack: "Ruby · JavaScript · jQuery · AJAX · Docker",
)[
  - Developed Excel reports and payment flows for an accounting system used by a 100–200 person firm.
  - Implemented data syncing for autocomplete; Docker deploys and pull requests in English.
]

= Research and projects
#entrada(
  "Forecasting wholesale prices of Canchán potatoes",
  derecha: "doi.org/10.3389/fsufs.2026.1883363",
  url: "https://doi.org/10.3389/fsufs.2026.1883363",
  sub: [Co-author #sep() Frontiers in Sustainable Food Systems (Q1) #sep() 2026],
  stack: "Python · pandas · XGBoost · LSTM · SARIMAX",
)[
  - Compared SARIMAX, RNN, LSTM and hybrids (MIDAGRI 2020–2025): LSTM-XGBoost was the most robust.
]

#entrada(
  "Epidemiological profiles of Carrion's disease",
  derecha: "doi.org/10.3389/frai.2026.1883357",
  url: "https://doi.org/10.3389/frai.2026.1883357",
  sub: [Co-author #sep() Frontiers in Artificial Intelligence (Q1) #sep() 2026],
  stack: "Python · scikit-learn · FAMD · K-Means",
)[
  - Analyzed 43,000+ records (2000–2024) with FAMD + K-Means: 2 stable epidemiological profiles.
]

#entrada(
  "Boosting models to predict academic performance",
  derecha: "LACCEI 2026",
  sub: [Co-author #sep() LACCEI conference],
)[
  - Compared Boosting models to predict student performance in blended-learning courses.
]

#entrada(
  [ChatCRM #suave[· Lead author of the API]],
  derecha: "github.com/chat-crm-suite/chat-crm-api",
  url: "https://github.com/chat-crm-suite/chat-crm-api",
  stack: "Python · FastAPI · pysentimiento · NestJS · BullMQ · Redis · Docker",
)[
  - Built message ingestion with HMAC-SHA256 webhooks and BullMQ queues with retries (1,000+ commits).
  - Integrated a FastAPI service that classifies sentiment into 3 classes for the KPI dashboard.
]

= Education
*Professional Technician in Software Engineering with Artificial Intelligence* #sep() SENATI #sep() 2023 – 2025

= Certifications and courses
*IBM* (2026): Machine Learning for Data Science Projects, Data Fundamentals #sep() *midudev* (2026): SQL #sep() *AWS Training and Certification* (2026): Lambda Foundations, IAM, VPC, S3 #sep() *Anthropic* (2026): AI Fluency

= Languages
*Spanish:* native #sep() *English:* technical (reading and writing; code, pull requests and papers in English)
