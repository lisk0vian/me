# Scripts

Python 3. Las rutas de salida están escritas en cada script (`OUT = ...`) y apuntan a `D:\projects\me\branding`.

| Script | Qué hace |
|---|---|
| `kit.py` | Genera todo `logo/`: símbolo, versiones, lockups, avatar, favicon, guía y el banner SVG. La geometría está definida con `CELLS`, `S` y `GAP`. |
| `typo.py` | Convierte texto en trazos (paths) a partir de fuentes TTF, con fontTools y uharfbuzz. |
| `lib.py` | Utilidades de SVG. |
| `typestudy.py` | Genera el estudio de las cuatro tipografías (`proceso/tipografia.png`). |
| `banner_html.py` | Genera `linkedin/banner.html`, el banner editable con las fuentes en base64. |
| `retouch2.py` | Retoque local de la foto de LinkedIn: cambia el fondo por el degradado pizarra y lleva la imagen a formato cuadrado. No toca la cara, el pelo ni los ojos. |

**No incluido** (porque pesa mucho o tiene otra licencia):
- **Fuentes:** van en `fonts/` junto a los scripts. Son `sora.ttf` y `jetbrains.ttf` de [google/fonts](https://github.com/google/fonts) (OFL).
- **Modelo:** `models/u2net_human_seg.onnx`, de las [releases de rembg](https://github.com/danielgatis/rembg/releases).
- **Dependencias:** `pip install fonttools uharfbuzz shapely numpy opencv-python onnxruntime`.
