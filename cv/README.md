# CV

Cuatro CV de una página, pensados para pasar el ATS (el filtro automático) y para que un reclutador entienda el perfil en 6 segundos. El diseño usa la marca de [`../branding/`](../branding/): Sora y JetBrains Mono, Pizarra, Hueso y Pervinca, la Escalera SOLID y el círculo como firma.

| PDF | Para ofertas de | Foto |
|---|---|---|
| [`CV-Jerremi-Chancan-fullstack-es.pdf`](pdf/CV-Jerremi-Chancan-fullstack-es.pdf) | Full Stack, Backend Node/NestJS (Perú) | sí |
| [`CV-Jerremi-Chancan-datos-es.pdf`](pdf/CV-Jerremi-Chancan-datos-es.pdf) | Ingeniero de Datos, ML, Analista de Datos (Perú) | sí |
| [`CV-Jerremi-Chancan-fullstack-en.pdf`](pdf/CV-Jerremi-Chancan-fullstack-en.pdf) | Full Stack / Backend, remoto internacional | no |
| [`CV-Jerremi-Chancan-datos-en.pdf`](pdf/CV-Jerremi-Chancan-datos-en.pdf) | Data Engineer / ML, remoto internacional | no |

En inglés no va foto: para empresas de EE. UU. y remotas es la norma, porque evita sesgos.

## Enlaces para el botón de descarga

Los nombres no cambian al regenerar, así que los enlaces no se rompen:

- Descarga: `https://raw.githubusercontent.com/lisk0vian/me/main/cv/pdf/CV-Jerremi-Chancan-fullstack-es.pdf`
- Vista en el navegador: `https://github.com/lisk0vian/me/blob/main/cv/pdf/CV-Jerremi-Chancan-fullstack-es.pdf`

Para otro CV, cambia `fullstack-es` por `datos-es`, `fullstack-en` o `datos-en`.

## Editar y generar

1. Edita el texto en el `.typ` que corresponda. El estilo compartido está en `plantilla.typ`. En los `.typ`:
   - una viñeta empieza con `- `;
   - `*texto*` es negrita;
   - escribe `\~`, `\@`, `\#` y `\$` para que salgan literales, porque Typst los interpreta.
2. Instala y genera:
   ```sh
   pip install -r cv/requirements.txt
   python cv/build.py
   ```
3. Mide antes de enviar: `python cv/score.py`. Si algo sale como `FALLA`, corrígelo y vuelve a generar. Para una oferta concreta: `python cv/score.py --oferta aviso.txt`.

## Teléfono (solo local)

El repo es público, así que los PDF de `pdf/` no llevan teléfono. Para enviar a reclutadores:

1. Crea `cv/telefono.txt` con tu número (por ejemplo `+51 9XX XXX XXX`).
2. Ejecuta `python cv/build.py`. Las versiones con teléfono quedan en `cv/privado/`.

Git ignora tanto `telefono.txt` como `privado/`.

## Qué mide `score.py`

Lee cada PDF con pypdf, igual que un ATS. Estos son los umbrales; si uno no se cumple, el script sale con error:

| Métrica | Umbral |
|---|---|
| Páginas | 1 |
| Glifos rotos o ligaduras (por ejemplo "ﬁ") | 0 |
| Secciones estándar detectadas | 7/7 |
| Email, LinkedIn y GitHub detectables | 3/3 |
| Orden de lectura | nombre → contacto → secciones |
| Palabras partidas por salto de línea ("CI/ CD") | 0 |
| Líneas con columnas mezcladas | 0 |
| Skills propias del rol presentes | 100 % |
| Viñetas con una cifra | ≥ 60 % |
| Viñetas que empiezan con verbo | ≥ 90 % |
| Palabras por viñeta | ≤ 25 |
| Palabras totales (1 página que respira) | 400–600 |
| Teléfono | ausente en `pdf/`, presente en `privado/` |

## ¿Te deja pasar el ATS? Match por oferta

`score.py` también compara cada CV con ofertas reales de Lima y de remoto LatAm. La lista está en `OFERTAS`, dentro de `score.py`. Para cada oferta muestra el % de sus keywords que el ATS encuentra en tu CV y un veredicto:

| Veredicto | Cuándo |
|---|---|
| pasa el ATS | match ≥ 75 % y los años pedidos no te dejan fuera |
| posible: adapta el CV | match del 50 al 74 %: ajusta el Perfil y las Habilidades a esa oferta |
| brecha de skills | match < 50 %: te faltan tecnologías que no puedes poner sin haberlas usado |
| filtro por años | la oferta pide más años de los que tienes (2 de prácticas) |

Para medir una oferta nueva, pega el texto del aviso en un `.txt` y corre:

```sh
python cv/score.py --oferta aviso.txt
```

Lo que falta es una brecha real: no lo agregues al CV sin experiencia que lo respalde.

## Antes de postular

- **Adapta a cada oferta:** cambia el Perfil y el orden de las Habilidades para que usen las mismas palabras que la oferta, sin inventar nada.
- **Mantén LinkedIn igual:** mismo título, mismas fechas y mismos logros que el CV.
- **Elige la versión correcta:**
  - Directo a un reclutador o a un formulario: la de `privado/`, con teléfono.
  - Botón del portafolio: la de `pdf/`.
