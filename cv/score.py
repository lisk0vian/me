"""Mide los CV en PDF como los leería un ATS y un reclutador.

Uso:
  python cv/score.py                          mide cv/pdf/*.pdf y cv/privado/*.pdf contra ofertas reales
  python cv/score.py otro.pdf                 mide otro PDF (rol e idioma por el nombre: "datos", "-en")
  python cv/score.py --oferta aviso.txt       compara tus CV con el texto de un aviso que pegues en aviso.txt
Sale con código 1 si algún CV no pasa un umbral de calidad.
"""
import pathlib
import re
import sys

from pypdf import PdfReader

sys.stdout.reconfigure(encoding="utf-8")
CV = pathlib.Path(__file__).resolve().parent
ANIOS = 2  # prácticas jun 2024 – sep 2026; algunas empresas no las cuentan como experiencia

CONTACTO = {
    "email": r"(?<![\w.])chancanjeremiaron@gmail\.com(?!\w)",
    "LinkedIn": r"linkedin\.com/in/jeremi-aron(?![\w-])",
    "GitHub": r"github\.com/lisk0vian(?![\w-])",
}
SECCIONES = {
    "es": ["perfil", "habilidades", "experiencia", "proyectos", "formación", "certificaciones", "idiomas"],
    "en": ["summary", "skills", "experience", "projects", "education", "certifications", "languages"],
}
# Vocabulario: nombre → regex (sin distinguir mayúsculas salvo (?-i:...)).
VOCAB = {
    "TypeScript": r"TypeScript", "JavaScript": r"JavaScript", "Node.js": r"Node\.js", "NestJS": r"NestJS",
    "Express": r"Express\b", "Fastify": r"Fastify", "React": r"React", "Next.js": r"Next\.js",
    "Angular": r"Angular", "REST": r"(?-i:\bREST\b)", "API": r"(?-i:\bAPIs?\b)", "microservicios": r"micro-?servic",
    "ORM": r"\bORM\b|TypeORM|Prisma|Sequelize", "PostgreSQL": r"PostgreSQL", "MySQL": r"MySQL",
    "MongoDB": r"MongoDB", "Redis": r"Redis", "SQL": r"\bSQL\b", "Docker": r"Docker",
    "Kubernetes": r"Kubernetes|\bK8s\b", "AWS": r"AWS", "Azure": r"Azure", "GCP": r"\bGCP\b|Google Cloud",
    "CI/CD": r"CI/CD", "Git": r"\bGit\b", "Jest": r"Jest", "Kafka": r"Kafka", "Java": r"(?-i:\bJava\b)",
    "Go": r"(?-i:\bGo\b)", "PHP": r"PHP", "Laravel": r"Laravel", "Ruby": r"Ruby", "FastAPI": r"FastAPI",
    "BullMQ": r"BullMQ", "TypeORM": r"TypeORM", "SQLite": r"SQLite", "Tailwind": r"Tailwind", "Astro": r"Astro",
    "TanStack": r"TanStack", "GitHub Actions": r"GitHub Actions", "Vitest": r"Vitest",
    "Testing Library": r"Testing Library", "pytest": r"pytest", "Socket.IO": r"Socket\.IO", "Zod": r"Zod",
    "jQuery": r"jQuery", "SOLID": r"SOLID|patrones de diseño|design patterns",
    "Python": r"Python", "pandas": r"pandas", "scikit-learn": r"scikit-learn|sklearn", "XGBoost": r"XGBoost",
    "LightGBM": r"LightGBM", "SARIMAX": r"SARIMAX", "K-Means": r"K-Means", "FAMD": r"FAMD", "LSTM": r"LSTM",
    "PyTorch": r"PyTorch", "Quarto": r"Quarto", "ETL/ELT": r"\bETL\b|\bELT\b", "Airflow": r"Airflow",
    "Spark": r"Spark", "dbt": r"\bdbt\b", "Snowflake": r"Snowflake", "Databricks": r"Databricks",
    "BigQuery": r"BigQuery", "Terraform": r"Terraform", "Lambda": r"Lambda", "Step Functions": r"Step Functions",
    "Scala": r"(?-i:\bScala\b)", "Flink": r"Flink", "streaming": r"streaming|Kafka", "OLAP": r"\bOLAP\b",
    "machine learning": r"machine learning|aprendizaje automático", "LLM": r"\bLLMs?\b", "Power BI": r"Power ?BI",
    "SageMaker": r"SageMaker", "Random Forest": r"Random Forest",
    "modelado de datos": r"modela(?:do|miento) de datos|data model|model(?:é|ed) (?:\w+ )?(?:tablas|tables)",
    "dashboards": r"dashboard", "optimización SQL": r"optimiz\w* (?:de )?consultas|optimiz\w* (?:\w+ )?quer",
    "window functions": r"window functions|funciones de ventana", "CTE": r"(?-i:\bCTEs?\b)",
    "data warehouse": r"data warehouse|almacén de datos",
    "Node.js o Python": r"Node\.js|Python",  # el aviso acepta cualquiera de los dos
}
# Skills reales (portafolio-api/es/skills.json) que cada CV debe mostrar: umbral 100 %.
PROPIAS = {
    "fullstack": ["TypeScript", "JavaScript", "Node.js", "NestJS", "React", "PHP", "Laravel", "Ruby", "Go", "FastAPI",
                  "MySQL", "PostgreSQL", "Redis", "BullMQ", "TypeORM", "SQLite", "Tailwind", "Astro", "TanStack",
                  "Docker", "GitHub Actions", "AWS", "Git", "Jest", "Vitest", "Testing Library", "pytest",
                  "Socket.IO", "Zod", "jQuery", "Express", "window functions", "CTE"],
    "datos": ["Python", "SQL", "pandas", "scikit-learn", "XGBoost", "LightGBM", "SARIMAX", "K-Means", "FAMD", "LSTM",
              "PyTorch", "FastAPI", "MySQL", "PostgreSQL", "SQLite", "Redis", "BullMQ", "Docker", "GitHub Actions",
              "Git", "AWS", "Quarto", "pytest", "TypeScript", "window functions", "CTE"],
}
# Ofertas reales (nov 2026), requisitos resumidos del aviso: (empresa · puesto, años mínimos o None, keywords).
# Fuentes: Indeed Perú, Computrabajo, GetOnBrd, Lever, Jooble, Talently, Cazvid. Verifica el aviso original.
OFERTAS = {
    "fullstack": [
        ("Hunters Group · Backend Junior", None, ["Node.js o Python", "React", "Go", "SQL"]),
        ("Periferia IT · Full Stack", None, ["React", "AWS", "Docker", "Git"]),
        ("Indeed Perú · Full Stack Jr", None, ["Kafka", "Docker", "CI/CD"]),
        ("Lima híbrido · Backend microservicios", None,
         ["Node.js", "TypeScript", "NestJS", "Express", "ORM", "microservicios"]),
        ("Indra · Backend NestJS", None, ["NestJS", "Java", "Azure"]),
        ("Inetum · Backend NestJS", 5, ["NestJS", "Node.js", "Azure", "API"]),
        ("Techstart · Backend Senior", 5, ["TypeScript", "Node.js", "REST", "PostgreSQL", "Fastify"]),
        ("Coderio · Referente Full Stack", 5,
         ["JavaScript", "TypeScript", "Node.js", "React", "Docker", "Kubernetes", "AWS"]),
        ("Dynamic Devs · Full Stack", 4, ["React", "Next.js"]),
    ],
    "datos": [
        ("ZAT · Analista de Datos Jr", 1, ["Python", "SQL", "modelado de datos"]),
        ("Credicorp Capital · Analista de Datos Jr", None, ["SQL", "Python", "machine learning"]),
        ("Target Marketing · Analista Jr", None, ["SQL", "Power BI", "Python", "scikit-learn"]),
        ("Indeed Perú · Data Scientist", None, ["SQL", "Python", "modelado de datos", "dashboards"]),
        ("San Isidro · Data Scientist", None, ["Python", "SQL", "SageMaker", "XGBoost", "Random Forest"]),
        ("Applaudo · Data Engineer (Python y AWS)", None, ["SQL", "Python", "AWS"]),
        ("Ruzora · Data Engineer LatAm", None, ["Python", "SQL", "optimización SQL", "window functions", "CTE"]),
        ("Improving · Data Engineer ML/LLM", None, ["Python", "SQL", "machine learning", "LLM", "Snowflake"]),
        ("Applaudo · Senior Data Engineer", None, ["Python", "SQL", "ETL/ELT", "Airflow", "dbt"]),
        ("GrowBy · Analytics Engineer", None, ["SQL", "Snowflake", "dbt", "Airflow"]),
        ("Jooble Lima · Data Engineer", None, ["SQL", "Airflow", "Terraform", "Lambda", "Step Functions"]),
        ("Matilda · Data Engineer", 3, ["Python", "ETL/ELT", "Azure", "Kubernetes", "SQL"]),
        ("Playbypoint · Data Engineer", 5, ["Python", "SQL", "streaming", "Airflow", "OLAP", "AWS"]),
        ("Metova · Data Engineer", 5, ["Python", "Scala", "Java", "SQL", "Spark", "Flink", "Airflow"]),
    ],
}
VERBOS_IRREGULARES = {"reduje", "promovido", "puse", "hice", "led", "built", "cut", "wrote", "ran", "made", "grew"}


def hay(nombre, texto):
    return re.search(VOCAB[nombre], texto, re.I) is not None


def bullets(texto):
    # Una viñeta va desde "•" hasta la primera línea que termina en punto.
    salida = []
    for seg in texto.split("•")[1:]:
        lineas = []
        for linea in seg.strip().splitlines():
            lineas.append(linea.strip())
            if linea.rstrip().endswith("."):
                break
        salida.append(" ".join(lineas))
    return salida


def es_verbo(palabra):
    p = palabra.lower().strip(",;:")
    return p in VERBOS_IRREGULARES or p.endswith(("é", "í", "ed"))


def tiene_metrica(b):
    numeros = re.findall(r"(?<![\w-])\d[\d.,]*(?![\w-])", b)
    return any(not re.fullmatch(r"(19|20)\d\d", n) for n in numeros)


def veredicto(match, anios):
    if anios and anios > ANIOS:
        return f"filtro por años (pide {anios}+)"
    if match >= 75:
        return "pasa el ATS"
    if match >= 50:
        return "posible: adapta el CV"
    return "brecha de skills"


def leer(pdf):
    lector = PdfReader(pdf)
    plano = "\n".join(p.extract_text() for p in lector.pages)
    layout = "\n".join(p.extract_text(extraction_mode="layout") for p in lector.pages)
    return lector, plano, layout, re.sub(r"\s+", " ", plano)


def medir(pdf: pathlib.Path):
    rol = "datos" if "datos" in pdf.stem else "fullstack"
    lang = "en" if pdf.stem.endswith("-en") else "es"
    lector, plano, layout, unido = leer(pdf)
    lineas = [re.sub(r"\s+", " ", l).strip() for l in plano.splitlines() if l.strip()]
    filas = []

    def fila(nombre, valor, ok):
        filas.append((nombre, valor, ok))

    fila("Páginas", len(lector.pages), len(lector.pages) == 1)
    fila("Caracteres extraíbles", len(unido), len(unido) > 2000)
    rotos = len(re.findall(r"[\ufffd\ufb00-\ufb06\ue000-\uf8ff]", plano))
    fila("Glifos rotos / ligaduras", rotos, rotos == 0)

    cortas = [l.lower() for l in lineas if len(l) <= 40]
    halladas = [s for s in SECCIONES[lang] if any(s in l for l in cortas)]
    fila("Secciones estándar", f"{len(halladas)}/{len(SECCIONES[lang])}", len(halladas) == len(SECCIONES[lang]))

    contacto = [k for k, rx in CONTACTO.items() if re.search(rx, unido)]
    fila("Contacto detectable", f"{len(contacto)}/{len(CONTACTO)}", len(contacto) == len(CONTACTO))

    tel_txt = CV / "telefono.txt"
    if tel_txt.exists():
        digitos = re.sub(r"\D", "", tel_txt.read_text(encoding="utf-8"))
        presente = digitos in re.sub(r"\D", "", plano)
        if pdf.parent.name == "privado":
            fila("Teléfono (privado)", "sí" if presente else "no", presente)
        else:
            fila("Teléfono ausente (público)", "no está" if not presente else "FILTRADO", not presente)

    primera = lineas[0] if lineas else ""
    email = unido.find("chancanjeremiaron")
    seccion = min((unido.lower().find(s) for s in halladas if unido.lower().find(s) >= 0), default=-1)
    orden = "Jerremi" in primera and 0 <= email < seccion
    fila("Orden de lectura (nombre → contacto → secciones)", "sí" if orden else "no", orden)

    partidas = re.findall(r"\w[-/]\s*\n\s*\w", plano)
    fila("Palabras partidas por salto de línea (CI/ CD, K- Means)", len(partidas), not partidas)

    mezcla = [l for l in layout.splitlines() if re.search(r"[^\s·]\s{2,}[A-ZÁÉÍÓÚ][\wáéíóúñ /&]{2,24}:\s", l)]
    fila("Líneas con columnas mezcladas", len(mezcla), not mezcla)

    faltan = [k for k in PROPIAS[rol] if not hay(k, unido)]
    fila("Skills propias del rol presentes",
         f"{len(PROPIAS[rol]) - len(faltan)}/{len(PROPIAS[rol])}" + (f" (faltan {faltan})" if faltan else ""),
         not faltan)

    bs = bullets(plano)
    if bs:
        con_num = 100 * sum(tiene_metrica(b) for b in bs) // len(bs)
        verbo = 100 * sum(es_verbo(b.split()[0]) for b in bs) // len(bs)
        largo = sum(len(b.split()) for b in bs) / len(bs)
        fila(f"Viñetas con métrica ({len(bs)} viñetas)", f"{con_num} %", con_num >= 60)
        fila("Viñetas que empiezan con verbo de acción", f"{verbo} %", verbo >= 90)
        fila("Palabras por viñeta (promedio)", f"{largo:.1f}", largo <= 25)
    else:
        fila("Viñetas detectables por el ATS", 0, False)

    palabras = len(re.findall(r"\w[\w.+#/-]*", plano))
    fila("Palabras totales (1 página que respira)", palabras, 400 <= palabras <= 600)
    return rol, lang, unido, filas


def evaluar_ofertas(unido, ofertas):
    # Por oferta: % de sus keywords que el ATS encuentra en el CV, y si los años te dejan fuera.
    filas, pasa = [], 0
    for nombre, anios, kws in ofertas:
        ok = [k for k in kws if hay(k, unido)]
        match = 100 * len(ok) // len(kws)
        v = veredicto(match, anios)
        pasa += v == "pasa el ATS"
        falta = [k for k in kws if k not in ok]
        filas.append(f"    {match:3d} %  {v:<24} {nombre}" + (f"  · falta: {', '.join(falta)}" if falta else ""))
    return pasa, filas


def main():
    args = sys.argv[1:]
    oferta = None
    if args[:1] == ["--oferta"]:
        aviso = pathlib.Path(args[1]).read_text(encoding="utf-8")
        pedidas = [k for k, rx in VOCAB.items() if " o " not in k and re.search(rx, aviso, re.I)]
        m = re.search(r"(\d+)\s*\+?\s*(?:(?:a|-|–)\s*\d+\s*)?(?:años|years)", aviso, re.I)
        oferta = ("aviso pegado", int(m.group(1)) if m else None, pedidas)
        print(f"Keywords del aviso ({len(pedidas)}): {', '.join(pedidas) or '-'}"
              + (f" · pide {oferta[1]}+ años" if oferta[1] else ""))
        args = args[2:]
    pdfs = [pathlib.Path(a) for a in args] or sorted((CV / "pdf").glob("*.pdf")) + sorted(
        (CV / "privado").glob("*.pdf"))
    falla = False
    for pdf in pdfs:
        rol, lang, unido, filas = medir(pdf)
        print(f"\n{pdf.parent.name}/{pdf.name}  [{rol} · {lang}]")
        for nombre, valor, ok in filas:
            marca = "  ··" if ok is None else ("  OK" if ok else "FALLA")
            print(f"  {marca}  {nombre}: {valor}")
            falla |= ok is False
        if oferta and oferta[2]:
            _, lineas = evaluar_ofertas(unido, [oferta])
        else:
            pasa, lineas = evaluar_ofertas(unido, OFERTAS[rol])
            print(f"    ··  Ofertas reales donde pasas el ATS: {pasa}/{len(OFERTAS[rol])}")
        print("\n".join(lineas))
    print("\nResultado:", "hay umbrales sin cumplir" if falla else "todos los CV pasan")
    sys.exit(1 if falla else 0)


if __name__ == "__main__":
    main()
