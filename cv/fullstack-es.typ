#import "plantilla.typ": *
#show: cv.with(
  lang: "es",
  rol: "Desarrollador Full Stack · Backend",
  disponibilidad: "Disponibilidad inmediata · Híbrido en Lima o remoto",
  lugar: "Lima, Perú",
  foto: true,
)

= Perfil
Desarrollador Full Stack con más de 2 años de prácticas profesionales construyendo software en producción con TypeScript, Node.js, NestJS, React, PHP/Laravel y Ruby. Lideré un equipo de 4 personas, reduje un listado crítico de 4–5 min a menos de 30 s y automatizo CI/CD con GitHub Actions y Docker.

= Habilidades técnicas
#habilidades(
  ("Backend", "Node.js, TypeScript, NestJS, Express, PHP, Laravel, Ruby, Go, FastAPI, API REST, Socket.IO"),
  ("Frontend", "React, TanStack Query/Router, Tailwind CSS, Astro, jQuery"),
  ("Datos y colas", "SQL (window functions, CTE), MySQL, PostgreSQL, Redis, BullMQ, TypeORM, SQLite"),
  ("DevOps y CI/CD", "Docker, GitHub Actions, Git, Lighthouse CI, GitHub Pages, AWS (Lambda, S3, IAM, VPC)"),
  ("Calidad", "Jest, Vitest, Testing Library, pytest, Zod, principios SOLID"),
)

= Experiencia
#entrada(
  "Practicante de Desarrollo Full Stack",
  derecha: "mar 2025 – sep 2026",
  sub: [J&P Periféricos SAC #sep() Lima, Perú · Híbrido],
  stack: "TypeScript · PHP · Laravel · MySQL · Docker",
)[
  - Lideré un equipo de 4 personas en proyectos paralelos: un ERP para abogados y un sistema de tickets.
  - Reduje el listado de facturas de 4–5 min a menos de 30 s (\~90 %) optimizando consultas MySQL y caché.
  - Desarrollé un Kanban con tablas de auditoría en el ERP, adoptado por 2 empresas cliente además de J&P.
]

#entrada(
  "Practicante de Desarrollo Full Stack",
  derecha: "jun 2024 – nov 2025",
  sub: [Codecta Perú #sep() Remoto · equipo distribuido en Chile],
  stack: "Ruby · JavaScript · jQuery · AJAX · Docker",
)[
  - Desarrollé reportes con exportación a Excel y flujos de pago para importaciones y órdenes de compra en un sistema contable de una firma de 100–200 personas.
  - Implementé sincronización de datos para autocompletado; deploys en Docker y PRs en inglés.
]

= Proyectos
#entrada(
  [ChatCRM #suave[· Autor principal de la API y la app]],
  derecha: "github.com/chat-crm-suite/chat-crm-api",
  url: "https://github.com/chat-crm-suite/chat-crm-api",
  stack: "NestJS · React · MySQL · Redis · BullMQ · Socket.IO · Zod · FastAPI",
)[
  - Construí una bandeja compartida de WhatsApp con 1.000+ commits, en producción interna desde 2025.
  - Diseñé 3 servicios multiempresa: webhooks firmados HMAC-SHA256, colas BullMQ con reintentos, cifrado AES-256-GCM, contratos Zod que generan OpenAPI y 130 suites de pruebas.
]

#entrada(
  [Tribu #suave[· Autor único]],
  derecha: "npmjs.com/package/tribu",
  url: "https://www.npmjs.com/package/tribu",
  stack: "TypeScript · Node.js · UBL 2.1 · XMLDSig · SOAP · Vitest",
)[
  - Publiqué en npm un SDK que emite 4 tipos de comprobante SUNAT, validados en su entorno beta.
]

#entrada(
  [Portafolio web #suave[· Diseño, desarrollo y medición]],
  derecha: "github.com/lisk0vian/portafolio-web",
  url: "https://github.com/lisk0vian/portafolio-web",
  stack: "Astro · TypeScript · Tailwind CSS · GitHub Actions · Lighthouse CI",
)[
  - Subí Lighthouse móvil de 71 a 98 (86 % menos peso) con render en build y Lighthouse CI en GitHub Actions.
]


= Formación
*Profesional Técnico en Ingeniería de Software con Inteligencia Artificial* #sep() SENATI #sep() 2023 – 2025 \
Coautor de 2 artículos Q1 en Frontiers (2026) sobre machine learning aplicado #sep() #link("https://orcid.org/0009-0005-6789-076X", text(font: mono, size: 7.1pt, fill: pervinca-osc, "orcid.org/0009-0005-6789-076X"))

= Certificaciones y cursos
*AWS Training and Certification* (2026): Lambda Foundations, IAM, VPC, S3 #sep() *IBM* (2026): Machine Learning for Data Science Projects, Data Fundamentals #sep() *midudev* (2026): Aprende SQL #sep() *Anthropic* (2026): AI Fluency

= Idiomas
*Español:* nativo #sep() *Inglés:* técnico (lectura y escritura; código y pull requests en inglés)
