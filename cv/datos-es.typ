#import "plantilla.typ": *
#show: cv.with(
  lang: "es",
  rol: "Ingeniero de Datos · Machine Learning",
  disponibilidad: "Disponibilidad inmediata · Híbrido en Lima o remoto",
  lugar: "Lima, Perú",
  extra: (("orcid.org/0009-0005-6789-076X", "https://orcid.org/0009-0005-6789-076X"),),
  foto: true,
)

= Perfil
Ingeniero de datos y machine learning con más de 2 años de prácticas en software de producción (SQL, TypeScript, Docker). Coautor de 2 artículos Q1 en Frontiers (2026) con ML tradicional en Python (XGBoost, LightGBM, K-Means, SARIMAX), pipelines reproducibles y CI/CD en GitHub Actions.

= Habilidades técnicas
#habilidades(
  ("Lenguajes", "Python, SQL (window functions, CTE), TypeScript, JavaScript"),
  ("Datos", "pandas, ETL en Python, modelado de datos, MySQL, PostgreSQL, SQLite, Redis, BullMQ"),
  ("Machine learning", "scikit-learn, XGBoost, LightGBM, SARIMAX, K-Means, FAMD, LSTM (PyTorch)"),
  ("MLOps y DevOps", "Docker, GitHub Actions (CI/CD), Git, FastAPI, Quarto, AWS (Lambda, S3, IAM, VPC)"),
  ("Calidad", "pytest, contratos de datos con Zod, resultados reproducibles"),
)

= Experiencia
#entrada(
  "Practicante de Desarrollo Full Stack",
  derecha: "mar 2025 – sep 2026",
  sub: [J&P Periféricos SAC #sep() Lima, Perú · Híbrido],
  stack: "SQL · MySQL · PHP · Laravel · TypeScript · Docker",
)[
  - Reduje el listado de facturas de 4–5 min a menos de 30 s (\~90 %) optimizando consultas SQL y caché.
  - Modelé tablas de auditoría para un Kanban del ERP, adoptado por 2 empresas cliente además de J&P.
  - Lideré un equipo de 4 personas en proyectos paralelos: un ERP para abogados y un sistema de tickets.
]

#entrada(
  "Practicante de Desarrollo Full Stack",
  derecha: "jun 2024 – nov 2025",
  sub: [Codecta Perú #sep() Remoto · equipo distribuido en Chile],
  stack: "Ruby · JavaScript · jQuery · AJAX · Docker",
)[
  - Desarrollé reportes en Excel y flujos de pago en el sistema contable de una firma de 100–200 personas.
  - Implementé sincronización de datos para autocompletado; deploys en Docker y PRs en inglés.
]

= Investigación y proyectos
#entrada(
  "Pronóstico del precio mayorista de la papa Canchán",
  derecha: "doi.org/10.3389/fsufs.2026.1883363",
  url: "https://doi.org/10.3389/fsufs.2026.1883363",
  sub: [Coautor #sep() Frontiers in Sustainable Food Systems (Q1) #sep() 2026],
  stack: "Python · pandas · XGBoost · LSTM · SARIMAX",
)[
  - Comparé SARIMAX, RNN, LSTM e híbridos (MIDAGRI 2020–2025): LSTM-XGBoost fue el más robusto.
]

#entrada(
  "Perfiles epidemiológicos de la enfermedad de Carrión",
  derecha: "doi.org/10.3389/frai.2026.1883357",
  url: "https://doi.org/10.3389/frai.2026.1883357",
  sub: [Coautor #sep() Frontiers in Artificial Intelligence (Q1) #sep() 2026],
  stack: "Python · scikit-learn · FAMD · K-Means",
)[
  - Analicé 43.000+ registros (2000–2024) con FAMD + K-Means: 2 perfiles epidemiológicos estables.
]

#entrada(
  "Modelos Boosting para predecir el desempeño académico",
  derecha: "LACCEI 2026",
  sub: [Coautor #sep() Conferencia LACCEI],
)[
  - Comparé modelos Boosting para predecir el desempeño de estudiantes en cursos blended.
]

#entrada(
  [ChatCRM #suave[· Autor principal de la API]],
  derecha: "github.com/chat-crm-suite/chat-crm-api",
  url: "https://github.com/chat-crm-suite/chat-crm-api",
  stack: "Python · FastAPI · pysentimiento · NestJS · BullMQ · Redis · Docker",
)[
  - Construí la ingesta de mensajes con webhooks HMAC-SHA256 y colas BullMQ con reintentos (1.000+ commits).
  - Integré un servicio FastAPI que clasifica el sentimiento en 3 clases para el dashboard de KPIs.
]

= Formación
*Profesional Técnico en Ingeniería de Software con Inteligencia Artificial* #sep() SENATI #sep() 2023 – 2025

= Certificaciones y cursos
*IBM* (2026): Machine Learning for Data Science Projects, Data Fundamentals #sep() *midudev* (2026): Aprende SQL #sep() *AWS Training and Certification* (2026): Lambda Foundations, IAM, VPC, S3 #sep() *Anthropic* (2026): AI Fluency

= Idiomas
*Español:* nativo #sep() *Inglés:* técnico (lectura y escritura; código, pull requests y artículos en inglés)
