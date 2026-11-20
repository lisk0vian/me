"""Genera los CV en PDF desde los .typ de esta carpeta. Uso: python cv/build.py

pdf/      versión pública sin teléfono (se sube al repo para el botón de descarga)
privado/  versión con teléfono, solo si existe telefono.txt (git la ignora)
"""
import pathlib

import typst

CV = pathlib.Path(__file__).resolve().parent
RAIZ = CV.parent  # la plantilla lee /branding/logo/symbol.svg
tel_txt = CV / "telefono.txt"
tel = tel_txt.read_text(encoding="utf-8").strip() if tel_txt.exists() else ""

salidas = {"pdf": ""} | ({"privado": tel} if tel else {})
for carpeta, numero in salidas.items():
    (CV / carpeta).mkdir(exist_ok=True)
    for src in sorted(CV.glob("*.typ")):
        if src.stem == "plantilla":
            continue
        pdf = CV / carpeta / f"CV-Jerremi-Chancan-{src.stem}.pdf"
        typst.compile(
            str(src),
            output=str(pdf),
            root=str(RAIZ),
            font_paths=[str(CV / "fuentes")],
            ignore_system_fonts=True,  # mismo resultado en cualquier PC
            sys_inputs={"tel": numero},
        )
        assert pdf.stat().st_size > 10_000, f"PDF vacío: {pdf}"
        print(pdf.relative_to(RAIZ))
