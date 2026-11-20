#import "plantilla.typ": *
#show: cv.with(
  lang: "en",
  rol: "Full Stack / Backend Developer",
  disponibilidad: "Available immediately · Hybrid in Lima or remote (UTC-5)",
  lugar: "Lima, Peru",
)

= Summary
Full Stack Developer with 2+ years of internship experience shipping production software with TypeScript, Node.js, NestJS, React, PHP/Laravel and Ruby. Led a team of 4, cut a critical invoice list from 4–5 min to under 30 s, and automate CI/CD with GitHub Actions and Docker.

= Technical skills
#habilidades(
  ("Backend", "Node.js, TypeScript, NestJS, Express, PHP, Laravel, Ruby, Go, FastAPI, REST APIs, Socket.IO"),
  ("Frontend", "React, TanStack Query/Router, Tailwind CSS, Astro, jQuery"),
  ("Data & queues", "SQL (window functions, CTEs), MySQL, PostgreSQL, Redis, BullMQ, TypeORM, SQLite"),
  ("DevOps & CI/CD", "Docker, GitHub Actions, Git, Lighthouse CI, GitHub Pages, AWS (Lambda, S3, IAM, VPC)"),
  ("Quality", "Jest, Vitest, Testing Library, pytest, Zod, SOLID principles"),
)

= Experience
#entrada(
  "Full Stack Developer Intern",
  derecha: "Mar 2025 – Sep 2026",
  sub: [J&P Periféricos SAC #sep() Lima, Peru · Hybrid],
  stack: "TypeScript · PHP · Laravel · MySQL · Docker",
)[
  - Led a team of 4 across parallel projects: an ERP for law firms and an inventory ticketing system.
  - Cut invoice list load time from 4–5 min to under 30 s (\~90%) by optimizing MySQL queries and caching.
  - Built a Kanban board with audit tables in the ERP, adopted by 2 client companies besides J&P.
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

= Projects
#entrada(
  [ChatCRM #suave[· Lead author of the API and web app]],
  derecha: "github.com/chat-crm-suite/chat-crm-api",
  url: "https://github.com/chat-crm-suite/chat-crm-api",
  stack: "NestJS · React · MySQL · Redis · BullMQ · Socket.IO · Zod · FastAPI",
)[
  - Built a shared WhatsApp inbox with 1,000+ commits, in production as internal software since 2025.
  - Designed 3 multi-tenant services: HMAC-SHA256 signed webhooks, BullMQ queues with retries, AES-256-GCM encryption, Zod contracts that generate OpenAPI, and 130 test suites.
]

#entrada(
  [Tribu #suave[· Sole author]],
  derecha: "npmjs.com/package/tribu",
  url: "https://www.npmjs.com/package/tribu",
  stack: "TypeScript · Node.js · UBL 2.1 · XMLDSig · SOAP · Vitest",
)[
  - Published an npm SDK that issues 4 SUNAT (Peru tax authority) e-invoice types, validated in its beta.
]

#entrada(
  [Portfolio website #suave[· Design, development and measurement]],
  derecha: "github.com/lisk0vian/portafolio-web",
  url: "https://github.com/lisk0vian/portafolio-web",
  stack: "Astro · TypeScript · Tailwind CSS · GitHub Actions · Lighthouse CI",
)[
  - Raised mobile Lighthouse from 71 to 98 (86% lighter) with build-time rendering and Lighthouse CI.
]

= Education
*Professional Technician in Software Engineering with Artificial Intelligence* #sep() SENATI #sep() 2023 – 2025 \
Co-author of 2 Q1 papers in Frontiers journals (2026) on applied machine learning #sep() #link("https://orcid.org/0009-0005-6789-076X", text(font: mono, size: 7.1pt, fill: pervinca-osc, "orcid.org/0009-0005-6789-076X"))

= Certifications and courses
*AWS Training and Certification* (2026): Lambda Foundations, IAM, VPC, S3 #sep() *IBM* (2026): Machine Learning for Data Science Projects, Data Fundamentals #sep() *midudev* (2026): SQL #sep() *Anthropic* (2026): AI Fluency

= Languages
*Spanish:* native #sep() *English:* technical (reading and writing; code and pull requests in English)
