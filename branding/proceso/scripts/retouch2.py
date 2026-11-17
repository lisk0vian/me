"""LinkedIn portrait: studio slate backdrop (brand), lens glare/haze fix, square framing. Face/body/hair untouched.
Runs fully local: U2-Net human segmentation via onnxruntime."""
import os, sys
import numpy as np, cv2, onnxruntime as ort

SRC = r"D:\Downloads\Gemini_Generated_Image_l6osmxl6osmxl6os.jpg"
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "..", "models", "u2net_human_seg.onnx")
OUT = r"D:\projects\me\branding\linkedin"
os.makedirs(OUT, exist_ok=True)

img = cv2.imread(SRC, cv2.IMREAD_COLOR)[:, :, ::-1].astype(np.float32) / 255.0   # RGB 0..1
H, W = img.shape[:2]


# ------------------------------------------------------------------ 1. segmentation
def segment(rgb):
    x = cv2.resize(rgb, (320, 320), interpolation=cv2.INTER_AREA)
    x = x / max(x.max(), 1e-6)
    x = (x - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
    x = x.transpose(2, 0, 1)[None].astype(np.float32)
    s = ort.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
    p = s.run(None, {s.get_inputs()[0].name: x})[0][0, 0]
    p = (p - p.min()) / (p.max() - p.min() + 1e-6)
    return cv2.resize(p, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_LINEAR)


def guided(I, p, r, eps):
    mean = lambda a: cv2.boxFilter(a, -1, (2 * r + 1, 2 * r + 1))
    mI, mp = mean(I), mean(p)
    a = (mean(I * p) - mI * mp) / (mean(I * I) - mI * mI + eps)
    b = mp - a * mI
    return mean(a) * I + mean(b)


def blur_norm(val, w, sigma):
    """Normalized convolution: smooth estimate of val where weight w is high, extrapolated elsewhere."""
    num = cv2.GaussianBlur(val * w[..., None], (0, 0), sigma)
    den = cv2.GaussianBlur(w, (0, 0), sigma)[..., None]
    return num / np.maximum(den, 1e-4)


raw = segment(img)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
alpha = np.clip(guided(gray, raw, 14, 1e-3), 0, 1)

# local colour-model matting in the uncertain band (hair strands vs maroon backdrop)
sure_bg = (alpha < 0.04).astype(np.float32)
sure_fg = (alpha > 0.96).astype(np.float32)
Bold = blur_norm(img, sure_bg, 30)                     # backdrop colour, extrapolated under the person
Fest = blur_norm(img, sure_fg, 6)
band = cv2.dilate(((alpha > 0.04) & (alpha < 0.96)).astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
d = Fest - Bold
a_cm = np.clip(((img - Bold) * d).sum(-1) / np.maximum((d * d).sum(-1), 1e-4), 0, 1)
wcm = np.clip((d * d).sum(-1) / 0.04, 0, 1) * band
alpha = alpha * (1 - 0.5 * wcm) + a_cm * 0.5 * wcm
# skin / sweater edges: crisp alpha (soft edges there only add colour fringes); hair stays soft
lum0 = img.mean(-1)
hard = np.clip((alpha - 0.3) / 0.4, 0, 1)
is_hair = cv2.GaussianBlur((lum0 < 0.22).astype(np.float32), (0, 0), 2)
alpha = np.clip((alpha - 0.12) / 0.88, 0, 1) * is_hair + hard * (1 - is_hair)
alpha = np.clip(guided(gray, alpha, 2, 1e-4), 0, 1)

# ------------------------------------------------------------------ 2. lenses: green glare + haze
def lens_masks(rgb):
    g8 = (cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY) * 255).astype(np.uint8)
    masks = []
    for (x0, y0, x1, y1), seed in (((400, 900, 770, 1175), (600, 1110)), ((850, 860, 1215, 1120), (1040, 1060))):
        roi = g8[y0:y1, x0:x1]
        frame = (roi < 55).astype(np.uint8)
        frame = cv2.dilate(frame, np.ones((3, 3), np.uint8))
        free = (1 - frame).astype(np.uint8)
        ff = np.zeros((roi.shape[0] + 2, roi.shape[1] + 2), np.uint8)
        cv2.floodFill(free.copy(), ff, (seed[0] - x0, seed[1] - y0), 1, flags=4 | (1 << 8))
        lens = ff[1:-1, 1:-1]
        cnts, _ = cv2.findContours(lens, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        filled = np.zeros_like(lens)
        cv2.drawContours(filled, [max(cnts, key=cv2.contourArea)], -1, 1, -1)
        filled = cv2.erode(filled, np.ones((5, 5), np.uint8))
        m = np.zeros((H, W), np.float32)
        m[y0:y1, x0:x1] = filled
        masks.append(m)
    return masks


lmasks = lens_masks(img)
fixed = img.copy()
for m in lmasks:
    soft = cv2.GaussianBlur(m, (0, 0), 3)
    ys, xs = np.nonzero(m)
    # haze: match lens-interior cheek band to the cheek just outside the frame (mean/std per channel)
    yb = ys.max()
    inside = (m > 0) & (np.arange(H)[:, None] > yb - 22) & (np.arange(H)[:, None] < yb - 4)
    xs_in = np.nonzero(inside.any(0))[0]
    outside = np.zeros((H, W), bool)
    outside[yb + 18:yb + 34, xs_in.min() + 10:xs_in.max() - 10] = True
    a_k = np.clip(img[outside].std(0) / np.maximum(img[inside].std(0), 1e-4), 1.0, 1.15)
    b_k = img[outside].mean(0) - a_k * img[inside].mean(0)
    dehazed = np.clip(img * a_k + b_k, 0, 1)
    # green glare: pull chroma back to the lens's own skin chroma, keep luminance
    lum = img.mean(-1, keepdims=True)
    chroma = img - lum
    ref = np.median(chroma[m > 0], axis=0)
    ref = np.median(chroma[(m > 0) & (lum[..., 0] > 0.4)], axis=0)
    gr = img[..., 1] - img[..., 0]
    win = np.zeros((H, W), np.float32)
    win[945:1020, 470:560] = 1
    win = cv2.GaussianBlur(win, (0, 0), 5)
    greenish = np.clip((gr - (ref[1] - ref[0]) - 0.06) / 0.08, 0, 1) * np.clip((lum[..., 0] - 0.18) / 0.06, 0, 1) * m * win
    greenish = cv2.GaussianBlur(greenish, (0, 0), 4)[..., None]
    lum_fix = lum + greenish * 0.35 * np.maximum(cv2.GaussianBlur(lum[..., 0], (0, 0), 12)[..., None] - lum, 0)
    deglare = np.clip(lum_fix + chroma * (1 - greenish) + ref * greenish, 0, 1)
    dehazed = np.clip(dehazed + (deglare - img), 0, 1)
    fixed = fixed * (1 - soft[..., None]) + dehazed * soft[..., None]
img_fix = img                      # user asked: leave eyes and lenses untouched

# ------------------------------------------------------------------ 3. square canvas + studio backdrop
G = 300                                    # side extension: canvas 1100 x 1100 at native scale
CW = W + 2 * G
CH = CW
pad = lambda a: cv2.copyMakeBorder(a, 0, 0, G, G, cv2.BORDER_REFLECT)
I = pad(img_fix)[:CH]
A = pad(alpha)[:CH]
for col, side in ((0, slice(0, G)), (W - 1, slice(G + W, CW))):
    touch = int(np.argmax(alpha[:, col] > 0.5)) if (alpha[:, col] > 0.5).any() else CH
    A[:touch, side] = 0.0
    A[touch:, side] = 1.0
Bo = pad(Bold)[:CH]

yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
cx, cy = CW * 0.5, CH * 0.36
r = np.sqrt(((xx - cx) / (CW * 0.62)) ** 2 + ((yy - cy) / (CH * 0.70)) ** 2)
t = np.clip(r, 0, 1) ** 1.6
c_in, c_out = np.array([0x3d, 0x45, 0x54]) / 255, np.array([0x14, 0x18, 0x1f]) / 255
Bnew = c_in * (1 - t[..., None]) + c_out * t[..., None]
rng = np.random.default_rng(7)
Bnew = Bnew + rng.normal(0, 0.006, Bnew.shape)          # fine grain: no banding, photographic

out = I + (1 - A[..., None]) * (Bnew - Bo)               # = a*F + (1-a)*Bnew without dividing by alpha
# colour fringe: at the person's edge use the person's own local colour (hair/skin), not backdrop spill
Fp = pad(Fest)[:CH]
edge = ((A > 0.05) & (A < 0.995)).astype(np.float32)
edge = cv2.GaussianBlur(cv2.dilate(edge, np.ones((5, 5), np.uint8)), (0, 0), 1.5)
Ac = A[..., None]
use = (edge[..., None] * np.clip((A[..., None] - 0.25) / 0.15, 0, 1))      # only pixels that are mostly person
F = (out - (1 - Ac) * Bnew) / np.maximum(Ac, 0.25)                           # person colour inside the edge pixel
lF = F.mean(-1, keepdims=True)
w = np.clip(2 * (1 - Ac), 0, 1) * 0.8
F2 = lF + (F - lF) * (1 - w) + (Fp - Fp.mean(-1, keepdims=True)) * w
out = out * (1 - use) + (Ac * F2 + (1 - Ac) * Bnew) * use

# side extension: continue each shoulder line past the frame edge, sweater below it, backdrop above
def shoulder_line(cols):
    xs, ys = [], []
    for c in cols:
        hit = np.nonzero(alpha[:, c] > 0.5)[0]
        hit = hit[hit > H * 0.55]
        if len(hit):
            xs.append(c); ys.append(hit[0])
    return np.polyfit(xs, ys, 1)
for cols, side_cols in ((range(0, 70), range(0, G)), (range(W - 70, W), range(G + W, CW))):
    b, a0 = shoulder_line(list(cols))
    for cx_ in side_cols:
        xo = cx_ - G                                   # original-image x (negative or > W)
        yb = int(np.clip(a0 + b * xo, 0, CH))
        out[:yb, cx_] = Bnew[:yb, cx_]
        out[yb:, cx_] = I[yb:, cx_]
out = np.clip(out, 0, 1)

# gentle studio finish: soft S-curve, nothing local on the face
out = np.clip(0.5 + (out - 0.5) * 1.04, 0, 1)

res = (out * 255 + 0.5).astype(np.uint8)
cv2.imwrite(os.path.join(OUT, "foto.jpg"), res[:, :, ::-1], [cv2.IMWRITE_JPEG_QUALITY, 95])
cv2.imwrite(os.path.join(HERE, "alpha.png"), (alpha * 255).astype(np.uint8))
before_after = np.concatenate([
    (img[880:1180, 380:1220] * 255).astype(np.uint8), (img_fix[880:1180, 380:1220] * 255).astype(np.uint8)], 0)
cv2.imwrite(os.path.join(HERE, "lenses_ba.png"), cv2.resize(before_after[:, :, ::-1], None, fx=1, fy=1, interpolation=cv2.INTER_LANCZOS4))
print("ok", res.shape)
