"""
Monta um panorama equirretangular (2:1) da paisagem vista do terraço da 303 a partir de
fotos comuns, cada uma colocada na direção em que foi tirada.

  python vista_pano.py montar  saida.png  mascara.png
  python vista_pano.py fundir  ia.png  saida_final.png     # recoloca as fotos reais sobre a versão completada pela IA

Convenção do panorama: centro (yaw 0) = +x da planta (saindo do living para o terraço,
serra e cidade à frente); yaw -90 = esquerda (lado do parque/morro verde).
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, '..', '..', '_originais', 'vista303'))
W, H = 4096, 2048
HFOV = 100.0  # celular grande-angular

# (arquivo, yaw, pitch, polígono do que é paisagem em coords normalizadas da foto)
FOTOS = [
    ('saida_varanda.png', 0.0, -9.5, [[(0.0, 0.2), (0.245, 0.2), (0.245, 0.415), (0.0, 0.415)],
                                      [(0.30, 0.2), (0.61, 0.2), (0.61, 0.415), (0.30, 0.415)]]),
    ('esquerda.png', -87.0, 5.2, [[(0.1, 0.0), (1.0, 0.0), (1.0, 1.0), (0.72, 1.0), (0.44, 0.63), (0.1, 0.63)]]),
    ('centro.png', -52.0, 2.6, [[(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.52, 1.0), (0.0, 0.6)]]),
]

def mask_for(size, polys, feather):
    m = Image.new('L', size, 0); d = ImageDraw.Draw(m)
    for poly in polys:
        d.polygon([(x * size[0], y * size[1]) for x, y in poly], fill=255)
    return m.filter(ImageFilter.GaussianBlur(feather)) if feather else m

def project(feather=6):
    lon = ((np.arange(W) + 0.5) / W - 0.5) * 2 * np.pi
    lat = (0.5 - (np.arange(H) + 0.5) / H) * np.pi
    lon, lat = np.meshgrid(lon, lat)
    d = np.stack([np.cos(lat) * np.sin(lon), np.sin(lat), np.cos(lat) * np.cos(lon)], -1)  # x direita, y cima, z frente
    acc = np.zeros((H, W, 3), np.float32); wsum = np.zeros((H, W), np.float32)
    for fn, yaw, pitch, polys in FOTOS:
        img = Image.open(os.path.join(SRC, fn)).convert('RGB')
        w, h = img.size
        a = np.asarray(img).astype(np.float32)
        m = np.asarray(mask_for((w, h), polys, feather)).astype(np.float32) / 255
        y_, p_ = np.radians(yaw), np.radians(pitch)
        # base da câmera
        f = np.array([np.cos(p_) * np.sin(y_), np.sin(p_), np.cos(p_) * np.cos(y_)])
        r = np.array([np.cos(y_), 0, -np.sin(y_)])
        u = np.cross(f, r)   # para cima
        zc = d @ f
        t = np.tan(np.radians(HFOV) / 2)
        with np.errstate(divide='ignore', invalid='ignore'):
            xs = (d @ r) / zc / t
            ys = (d @ u) / zc / t * (w / h)
        px = (xs + 1) / 2 * w; py = (1 - ys) / 2 * h
        ok = (zc > 0) & (px >= 0) & (px < w - 1) & (py >= 0) & (py < h - 1)
        xi = px[ok].astype(int); yi = py[ok].astype(int)
        wt = m[yi, xi]
        acc[ok] += a[yi, xi] * wt[:, None]
        wsum[ok] += wt
    return acc, wsum

def montar(out, out_mask):
    acc, wsum = project()
    cover = np.clip(wsum, 0, 1)
    img = np.where(wsum[..., None] > 0, acc / np.maximum(wsum, 1e-6)[..., None], 0)
    grey = np.full_like(img, 128)
    comp = img * cover[..., None] + grey * (1 - cover[..., None])
    Image.fromarray(comp.astype(np.uint8)).save(out)
    Image.fromarray((cover * 255).astype(np.uint8)).save(out_mask)

def fundir(ia_path, out):
    acc, wsum = project(feather=14)
    real = acc / np.maximum(wsum, 1e-6)[..., None]
    cover = np.clip(wsum, 0, 1)[..., None]
    ia = np.asarray(Image.open(ia_path).convert('RGB').resize((W, H), Image.LANCZOS)).astype(np.float32)
    res = real * cover + ia * (1 - cover)
    Image.fromarray(np.clip(res, 0, 255).astype(np.uint8)).save(out)

if __name__ == '__main__':
    if sys.argv[1] == 'montar':
        montar(sys.argv[2], sys.argv[3])
    else:
        fundir(sys.argv[2], sys.argv[3])
