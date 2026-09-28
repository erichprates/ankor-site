"""
Converte panorama equirretangular <-> 6 faces de cubo (ordem Pannellum: f r b l u d).

  python cubo.py split  pano.png  pasta_saida  [tamanho_face=1024] [fov=90]
  python cubo.py join   pasta_faces  saida.png [largura=4096]

As faces se chamam f.png r.png b.png l.png u.png d.png. "f" (frente) corresponde
ao centro horizontal do equirretangular.
"""
import sys, os
import numpy as np
from PIL import Image

FACES = {  # direção do centro e eixos (right, up) de cada face, em coordenadas (x=direita, y=cima, z=frente)
    'f': ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    'r': ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    'b': ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
    'l': ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    'u': ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
    'd': ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
}

def bilinear(img, u, v):
    h, w = img.shape[:2]
    u = np.mod(u, w); v = np.clip(v, 0, h - 1)
    x0 = np.floor(u).astype(int); y0 = np.floor(v).astype(int)
    x1 = (x0 + 1) % w; y1 = np.minimum(y0 + 1, h - 1)
    fx = (u - x0)[..., None]; fy = (v - y0)[..., None]
    a = img[y0, x0] * (1 - fx) + img[y0, x1] * fx
    b = img[y1, x0] * (1 - fx) + img[y1, x1] * fx
    return a * (1 - fy) + b * fy

def split(pano_path, out, size=1024, fov=90):
    img = np.asarray(Image.open(pano_path).convert('RGB')).astype(np.float32)
    H, W = img.shape[:2]
    os.makedirs(out, exist_ok=True)
    t = np.tan(np.radians(fov) / 2)
    g = (np.arange(size) + 0.5) / size * 2 - 1
    gx, gy = np.meshgrid(g * t, -g * t)
    for name, (c, r, up) in FACES.items():
        c, r, up = map(np.array, (c, r, up))
        d = c[None, None] + gx[..., None] * r[None, None] + gy[..., None] * up[None, None]
        d /= np.linalg.norm(d, axis=-1, keepdims=True)
        lon = np.arctan2(d[..., 0], d[..., 2])
        lat = np.arcsin(np.clip(d[..., 1], -1, 1))
        u = (lon / (2 * np.pi) + 0.5) * W - 0.5
        v = (0.5 - lat / np.pi) * H - 0.5
        face = bilinear(img, u, v)
        Image.fromarray(np.clip(face, 0, 255).astype(np.uint8)).save(os.path.join(out, name + '.png'))

def join(folder, out, width=4096):
    faces = {n: np.asarray(Image.open(os.path.join(folder, n + '.png')).convert('RGB')).astype(np.float32) for n in FACES}
    size = faces['f'].shape[0]
    Wd, Hd = width, width // 2
    lon = ((np.arange(Wd) + 0.5) / Wd - 0.5) * 2 * np.pi
    lat = (0.5 - (np.arange(Hd) + 0.5) / Hd) * np.pi
    lon, lat = np.meshgrid(lon, lat)
    d = np.stack([np.cos(lat) * np.sin(lon), np.sin(lat), np.cos(lat) * np.cos(lon)], -1)
    result = np.zeros((Hd, Wd, 3), np.float32)
    best = np.full((Hd, Wd), -np.inf)
    for name, (c, r, up) in FACES.items():
        c, r, up = map(np.array, (c, r, up))
        dot = d @ c
        mask = dot > best
        with np.errstate(divide='ignore', invalid='ignore'):
            x = (d @ r) / dot; y = (d @ up) / dot
        u = (x + 1) / 2 * size - 0.5
        v = (1 - (y + 1) / 2) * size - 0.5
        sel = mask & (dot > 0)
        if not sel.any():
            continue
        f = faces[name]
        uu = np.clip(u[sel], 0, size - 1); vv = np.clip(v[sel], 0, size - 1)
        x0 = np.floor(uu).astype(int); y0 = np.floor(vv).astype(int)
        x1 = np.minimum(x0 + 1, size - 1); y1 = np.minimum(y0 + 1, size - 1)
        fx = (uu - x0)[:, None]; fy = (vv - y0)[:, None]
        val = (f[y0, x0] * (1 - fx) + f[y0, x1] * fx) * (1 - fy) + (f[y1, x0] * (1 - fx) + f[y1, x1] * fx) * fy
        result[sel] = val
        best[sel] = dot[sel]
    Image.fromarray(np.clip(result, 0, 255).astype(np.uint8)).save(out)

def join_blend(folder, out, width=4096, fov=110, inner=90):
    """Remonta faces geradas com abertura > 90° fazendo transição suave na sobreposição.
    Peso 1 dentro de 'inner' graus e cai até 0 na borda da face (fov)."""
    faces = {n: np.asarray(Image.open(os.path.join(folder, n + '.png')).convert('RGB')).astype(np.float32) for n in FACES}
    size = faces['f'].shape[0]
    t = np.tan(np.radians(fov) / 2)
    ti = np.tan(np.radians(inner) / 2) / t          # limite interno em coords normalizadas
    Wd, Hd = width, width // 2
    lon = ((np.arange(Wd) + 0.5) / Wd - 0.5) * 2 * np.pi
    lat = (0.5 - (np.arange(Hd) + 0.5) / Hd) * np.pi
    lon, lat = np.meshgrid(lon, lat)
    d = np.stack([np.cos(lat) * np.sin(lon), np.sin(lat), np.cos(lat) * np.cos(lon)], -1)
    acc = np.zeros((Hd, Wd, 3), np.float32)
    wsum = np.zeros((Hd, Wd), np.float32)
    for name, (c, r, up) in FACES.items():
        c, r, up = map(np.array, (c, r, up))
        dot = d @ c
        with np.errstate(divide='ignore', invalid='ignore'):
            x = (d @ r) / dot / t; y = (d @ up) / dot / t
        m = np.maximum(np.abs(x), np.abs(y))
        sel = (dot > 0) & (m < 1)
        if not sel.any():
            continue
        s = np.clip((1 - m[sel]) / (1 - ti), 0, 1)
        w = s * s * (3 - 2 * s)  # smoothstep
        u = (x[sel] + 1) / 2 * size - 0.5
        v = (1 - (y[sel] + 1) / 2) * size - 0.5
        f = faces[name]
        uu = np.clip(u, 0, size - 1); vv = np.clip(v, 0, size - 1)
        x0 = np.floor(uu).astype(int); y0 = np.floor(vv).astype(int)
        x1 = np.minimum(x0 + 1, size - 1); y1 = np.minimum(y0 + 1, size - 1)
        fx = (uu - x0)[:, None]; fy = (vv - y0)[:, None]
        val = (f[y0, x0] * (1 - fx) + f[y0, x1] * fx) * (1 - fy) + (f[y1, x0] * (1 - fx) + f[y1, x1] * fx) * fy
        acc[sel] += val * w[:, None]
        wsum[sel] += w
    res = acc / np.maximum(wsum, 1e-6)[..., None]
    Image.fromarray(np.clip(res, 0, 255).astype(np.uint8)).save(out)

if __name__ == '__main__':
    if sys.argv[1] == 'joinblend':
        join_blend(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 4096,
                   float(sys.argv[5]) if len(sys.argv) > 5 else 110)
        sys.exit()
    cmd = sys.argv[1]
    if cmd == 'split':
        split(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 1024, float(sys.argv[5]) if len(sys.argv) > 5 else 90)
    else:
        join(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 4096)
