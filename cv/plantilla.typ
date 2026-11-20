// Plantilla compartida por los 4 CV. Colores, fuentes y reglas de marca: /branding/README.md
// Reglas ATS: todo texto es texto real en una columna; lo decorativo (banda, símbolo,
// foto, círculos) no lleva texto; separadores y viñetas son caracteres; sin ligaduras ni guiones de corte.

#let pizarra = rgb("#12151A")
#let superficie = rgb("#1D222A")
#let hueso = rgb("#E8E4DC")
#let niebla = rgb("#9AA0A8")
#let pervinca = rgb("#949FD8")
#let pervinca-osc = rgb("#55609C")
#let sans = "Sora"
#let mono = "JetBrains Mono"
#let margen = 13mm

// El teléfono llega desde build.py (telefono.txt); vacío en la versión pública.
#let tel = sys.inputs.at("tel", default: "")

#let sep(color: pervinca) = text(fill: color, " · ")
#let punto(r: 1.9pt) = box(baseline: -0.5pt, circle(radius: r, fill: pervinca))

#let cv(
  rol: "",
  disponibilidad: "",
  lugar: "",
  extra: (), // enlaces adicionales para el contacto: ((texto, url), ...)
  foto: false,
  lang: "es",
  doc,
) = {
  let nombre = "Jerremi Aron Chancan Labajos"
  set document(title: nombre + " — CV " + rol, author: nombre)
  set page(paper: "a4", margin: (top: 0mm, bottom: 9mm, x: margen))
  set text(font: sans, size: 9pt, fill: superficie, lang: lang, ligatures: false, hyphenate: false)
  set par(leading: 0.7em, spacing: 0.9em, justify: false)
  set list(marker: text(fill: pervinca, "•"), indent: 1pt, body-indent: 5pt, spacing: 0.75em)
  set grid(column-gutter: 6pt)
  // Sin cortes de línea dentro de "CI/CD", "K-Means", "AES-256-GCM"...: el ATS leería "CI/ CD".
  show regex("[\w.+#]+(?:[-/][\w.+#]+)+"): box

  show heading.where(level: 1): it => block(above: 15pt, below: 8pt, sticky: true, {
    text(weight: 600, size: 10.2pt, fill: pizarra, it.body)
    h(2.2pt)
    punto()
    block(above: 4.5pt, below: 0pt, line(length: 100%, stroke: 0.5pt + niebla))
  })

  // Banda superior en Pizarra: símbolo + nombre (como el lockup) y foto en círculo con aro pervinca.
  let contacto1 = (
    (lugar, none),
    ..if tel != "" { ((tel, "tel:" + tel.replace(" ", "")),) },
    ("chancanjeremiaron@gmail.com", "mailto:chancanjeremiaron@gmail.com"),
    ("linkedin.com/in/jeremi-aron", "https://www.linkedin.com/in/jeremi-aron"),
  )
  let contacto2 = (
    ("github.com/lisk0vian", "https://github.com/lisk0vian"),
    ("lisk0vian.github.io/portafolio-web", "https://lisk0vian.github.io/portafolio-web/"),
    ..extra,
  )
  let fila(items) = items.map(((t, u)) => box(if u == none { t } else { link(u, t) })).join(sep())
  let textos = {
    text(weight: 600, size: 20pt, fill: hueso, nombre)
    v(4pt, weak: true)
    text(size: 10.5pt, fill: pervinca, rol)
    v(5pt, weak: true)
    [#punto(r: 2.1pt) #text(size: 8.2pt, fill: hueso, disponibilidad)]
    v(5.5pt, weak: true)
    text(font: mono, weight: 600, size: 7.1pt, fill: hueso)[#fila(contacto1) \ #fila(contacto2)]
  }
  let simbolo = image("/branding/logo/symbol.svg", height: 15mm)
  let retrato = box(clip: true, radius: 50%, stroke: 1.6pt + pervinca, image("foto.jpg", width: 25mm, height: 25mm))
  pad(x: -margen, block(width: 100%, fill: pizarra, inset: (x: margen, top: 7mm, bottom: 5.5mm),
    grid(
      columns: if foto { (auto, 1fr, auto) } else { (auto, 1fr) },
      column-gutter: 4mm,
      align: horizon,
      simbolo, textos, ..if foto { (retrato,) },
    )))
  v(2pt)
  doc
}

// Una entrada de experiencia, proyecto o publicación.
// titulo | derecha (fechas o URL) / subtitulo / viñetas / stack en mono.
#let entrada(titulo, derecha: none, url: none, sub: none, stack: none, cuerpo) = block(above: 11pt, below: 0pt, {
  grid(
    columns: (1fr, auto),
    align: (left + bottom, right + bottom),
    text(weight: 600, size: 9.3pt, fill: pizarra, titulo),
    if url != none {
      link(url, text(font: mono, size: 7.1pt, fill: pervinca-osc, derecha))
    } else if derecha != none {
      text(font: mono, size: 7.1pt, fill: pervinca-osc, derecha)
    },
  )
  if sub != none { block(above: 4.5pt, below: 0pt, text(size: 8.4pt, fill: pervinca-osc, sub)) }
  block(above: 6.5pt, below: 0pt, cuerpo)
  if stack != none { block(above: 5.5pt, below: 0pt, text(font: mono, size: 6.9pt, fill: pervinca-osc, stack)) }
})

// Habilidades: "Categoría: a, b, c" por línea, una sola columna lógica.
#let habilidades(..filas) = grid(
  columns: (auto, 1fr),
  column-gutter: 7pt,
  row-gutter: 6.5pt,
  ..filas.pos().map(((k, v)) => (text(weight: 600, fill: pizarra, k + ":"), v)).flatten(),
)

// Texto secundario en línea (títulos de proyecto, notas).
#let suave(t) = text(weight: 400, fill: pervinca-osc, t)
