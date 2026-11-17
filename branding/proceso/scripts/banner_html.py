"""Generate linkedin/banner.html: an offline, editable LinkedIn banner (fonts embedded) that exports a 1584x396 PNG."""
import base64, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r"D:\projects\me\branding\linkedin\banner.html"
b64 = lambda p: base64.b64encode(open(os.path.join(HERE, "fonts", p), "rb").read()).decode()

HTML = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Banner de LinkedIn</title>
<style>
  :root { --bg:#12151a; --card:#181c22; --line:#2a303a; --fg:#e8e4dc; --muted:#9aa0a8; --acc:#949fd8; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--fg); font:15px/1.5 Sora, system-ui, sans-serif; }
  main { max-width:1200px; margin:0 auto; padding:32px 16px 48px; }
  h1 { font-size:24px; font-weight:600; margin:0 0 4px; }
  p.hint { color:var(--muted); margin:0 0 24px; }
  canvas { width:100%; height:auto; display:block; border-radius:10px; border:1px solid var(--line); }
  form { display:grid; gap:14px; margin-top:24px; background:var(--card); padding:20px; border-radius:14px; }
  label { display:grid; gap:6px; font-size:13px; color:var(--muted); }
  input[type=text] { font:inherit; color:var(--fg); background:var(--bg); border:1px solid var(--line); border-radius:8px; padding:10px 12px; }
  input[type=text]:focus { outline:2px solid var(--acc); outline-offset:1px; }
  .row { display:flex; flex-wrap:wrap; gap:12px; align-items:center; }
  .check { display:flex; gap:8px; align-items:center; color:var(--muted); font-size:13px; }
  button { font:inherit; font-weight:600; border:0; border-radius:8px; padding:10px 18px; cursor:pointer; }
  .primary { background:var(--acc); color:#12151a; }
  .ghost { background:transparent; color:var(--fg); border:1px solid var(--line); }
  small { color:var(--muted); }
</style>
</head>
<body>
<main>
  <h1>Banner de LinkedIn</h1>
  <p class="hint">Cambia los textos y descarga el PNG (1584 × 396 px, el tamaño de LinkedIn). Tus cambios se guardan en este navegador.</p>
  <canvas id="c" width="1584" height="396" role="img" aria-label="Vista previa del banner"></canvas>
  <form id="f" autocomplete="off">
    <label>Título <input type="text" id="title"></label>
    <label>Subtítulo <input type="text" id="subtitle"></label>
    <label>Enlace (va con el círculo pervinca) <input type="text" id="link"></label>
    <div class="row">
      <label class="check"><input type="checkbox" id="zone"> Mostrar zona aproximada de tu foto de perfil</label>
    </div>
    <div class="row">
      <button type="button" class="primary" id="dl">Descargar PNG</button>
      <button type="button" class="ghost" id="reset">Restablecer textos</button>
      <small>Si un texto es muy largo, se achica solo para no chocar con el símbolo.</small>
    </div>
  </form>
</main>
<script>
const DEFAULTS = {
  title: "Full-stack Developer",
  subtitle: "TypeScript · JavaScript · Software Architecture",
  link: "github.com/lisk0vian",
};
const C = { bg:"#12151a", grid:"#1d222a", fg:"#e8e4dc", muted:"#9aa0a8", acc:"#949fd8" };
const SORA = "__SORA__";
const MONO = "__MONO__";

const cv = document.getElementById("c"), ctx = cv.getContext("2d");
const W = 1584, H = 396, X = 470, MAXW = 1184 - 40 - X;
const ids = ["title", "subtitle", "link"];
const els = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));
const zone = document.getElementById("zone");

function load() {
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem("jeremi-banner") || "{}"); } catch (e) {}
  ids.forEach(id => els[id].value = saved[id] ?? DEFAULTS[id]);
}
function save() {
  try { localStorage.setItem("jeremi-banner", JSON.stringify(Object.fromEntries(ids.map(id => [id, els[id].value])))); } catch (e) {}
}

function fit(text, weight, size, family, maxw) {
  let s = size;
  do { ctx.font = `${weight} ${s}px ${family}`; } while (ctx.measureText(text).width > maxw && (s -= 1) > 10);
  return s;
}

function draw(showZone) {
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = C.grid;
  for (let x = 1080; x < W; x += 36) for (let y = 18; y < H; y += 36) ctx.fillRect(x, y, 3, 3);
  // symbol: Escalera SOLID (block 60, joint 12, footprint 204), L block = circle
  const k = 280 / 204, sx = W - 120 - 204 * k, sy = (H - 204 * k) / 2;
  [[0,0],[1,0],[1,1],[2,1],[2,2]].forEach(([c, lv], i) => {
    const px = sx + c * 72 * k, py = sy + (2 - lv) * 72 * k, s = 60 * k;
    if (i === 2) { const d = s * 1.04; ctx.fillStyle = C.acc; ctx.beginPath(); ctx.arc(px + s / 2, py + s / 2, d / 2, 0, Math.PI * 2); ctx.fill(); }
    else { ctx.fillStyle = C.fg; ctx.fillRect(px, py, s, s); }
  });
  ctx.textBaseline = "alphabetic";
  ctx.fillStyle = C.fg; fit(els.title.value, 600, 63, "Sora", MAXW); ctx.fillText(els.title.value, X, 168);
  ctx.fillStyle = C.muted; fit(els.subtitle.value, 400, 26, "Sora", MAXW); ctx.fillText(els.subtitle.value, X, 214);
  if (els.link.value.trim()) {
    ctx.fillStyle = C.acc; ctx.beginPath(); ctx.arc(X + 7, 255, 7, 0, Math.PI * 2); ctx.fill();
    fit(els.link.value, 600, 24, "'JetBrains Mono'", MAXW - 26); ctx.fillText(els.link.value, X + 26, 262);
  }
  if (showZone) {  // rough area LinkedIn's profile photo covers on desktop
    ctx.save(); ctx.globalAlpha = 0.35; ctx.fillStyle = "#e07a5f";
    ctx.beginPath(); ctx.arc(205, 400, 165, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    ctx.fillStyle = "#e07a5f"; ctx.font = "600 18px Sora"; ctx.fillText("foto de perfil (aprox.)", 120, 215);
  }
}

const render = () => { save(); draw(zone.checked); };
ids.forEach(id => els[id].addEventListener("input", render));
zone.addEventListener("change", render);
document.getElementById("reset").addEventListener("click", () => { ids.forEach(id => els[id].value = DEFAULTS[id]); render(); });
document.getElementById("dl").addEventListener("click", () => {
  draw(false);   // export never includes the guide overlay
  cv.toBlob(b => {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(b); a.download = "linkedin-banner.png"; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    draw(zone.checked);
  }, "image/png");
});

Promise.all([
  new FontFace("Sora", `url(data:font/ttf;base64,${SORA})`, { weight: "100 800" }).load(),
  new FontFace("JetBrains Mono", `url(data:font/ttf;base64,${MONO})`, { weight: "100 800" }).load(),
]).then(fs => { fs.forEach(f => document.fonts.add(f)); load(); render(); })
  .catch(() => { load(); render(); });
</script>
</body>
</html>
"""

html = HTML.replace("__SORA__", b64("sora.ttf")).replace("__MONO__", b64("jetbrains.ttf"))
open(OUT, "w", encoding="utf-8").write(html)
print("ok", len(html) // 1024, "KB")
