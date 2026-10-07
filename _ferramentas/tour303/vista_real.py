"""
Monta a paisagem 360° (equirretangular 2:1) a partir da panorâmica REAL tirada do terraço
(`_originais/vista30X/vista_30X_real.webp`, panorâmica de celular = projeção cilíndrica).

  python vista_real.py 303            # grava _originais/vista303/paisagem_360_real.png
  python vista_real.py 303_deck       # idem, com a vista mais aberta (mar) à esquerda: paisagem_360_real_deck.png
  python vista_real.py 303 --mascara  # grava também a máscara do que é foto real (branco)

A foto real ocupa só a faixa que ela cobre (HFOV graus na horizontal); o resto é completado:
céu acima = continuação suave do topo da foto; laterais/atrás = foto espelhada (fica atrás do
prédio); abaixo = cor da base da foto, desfocada (fica atrás do piso/mureta).

Convenção: centro do panorama (yaw 0) = +x da planta (saindo do living para o terraço).
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.abspath(os.path.join(HERE, '..', '..', '_originais'))
W, H = 6144, 3072

# por cobertura: HFOV da panorâmica, yaw do centro dela e altura do horizonte (fração da altura)
VISTAS = {
    # vista_303_real_ampla.webp = a vista tratada do terraço com mais área para baixo (até ~37° abaixo do horizonte).
    # Versões anteriores, guardadas na mesma pasta: vista_303_real.webp (até ~23°) e vista_303_real_ext.png (até ~31°).
    '303': dict(arquivo='vista303/vista_303_real_ampla.webp', saida='vista303/paisagem_360_real.png',
                hfov=190.0, yaw=-52.0, horizonte=0.631),
    # vista mais aberta (pega o mar à esquerda), usada no deck: entra à esquerda da emenda e a '303' fica à direita
    # (vista_303_deck.jpg é a mesma vista com mais área para baixo; a anterior, vista_303_aberta.png, ia só até ~21° abaixo do horizonte)
    '303_deck': dict(arquivo='vista303/vista_303_deck.jpg', saida='vista303/paisagem_360_real_deck.png',
                     hfov=187.0, yaw=-97.4, horizonte=0.59, base='303', emenda=-43.0),
}

def reflect(i, n):
    """índice espelhado nas bordas (… 2 1 0 | 0 1 2 … n-1 | n-1 n-2 …)"""
    i = np.mod(i, 2 * n)
    return np.where(i >= n, 2 * n - 1 - i, i)

def montar(cob, mascara=False, salvar=True):
    cfg = VISTAS[cob]
    src = Image.open(os.path.join(ORIG, cfg['arquivo'])).convert('RGB')
    src = src.crop((6, 0, src.width - 6, src.height))            # as bordas laterais podem trazer um filete da edição
    w, h = src.size
    a = np.asarray(src).astype(np.float32)
    f = w / np.radians(cfg['hfov'])            # px por radiano (cilíndrica)
    yh = cfg['horizonte'] * h

    lon = ((np.arange(W) + 0.5) / W - 0.5) * 360.0
    lat = (0.5 - (np.arange(H) + 0.5) / H) * 180.0
    dl = (lon - cfg['yaw'] + 180.0) % 360.0 - 180.0
    py = yh - np.tan(np.radians(np.clip(lat, -89.0, 89.0))) * f       # (H,)
    lat_top = np.degrees(np.arctan(yh / f))

    def hblur(row, graus):
        """desfoque horizontal circular de uma linha (n,3)"""
        k = max(1, int(len(row) * graus / 360.0))
        pad = np.concatenate([row[-k:], row, row[:k]])
        ker = np.hanning(2 * k + 1); ker /= ker.sum()
        return np.stack([np.convolve(pad[:, c], ker, mode='valid') for c in range(3)], -1)

    def amostra(dl):
        px = w / 2 + np.radians(dl) * f                                # (W,)
        xi = reflect(np.floor(px).astype(np.int64), w)
        PY = np.repeat(py[:, None], W, 1)
        yi = np.clip(np.where(PY > h - 1, np.full_like(PY, h - 1.0), PY), 0, h - 1)
        out = a[yi.astype(np.int64), xi[None, :]]
        # abaixo da foto: a última linha se dissolve na cor da base, bem desfocada e mais escura (sem espelhar)
        # abaixo da foto: a cor da última linha continua para baixo, cada vez mais desfocada na horizontal (sem faixa
        # escura, sem espelho e sem riscos verticais). É só um acabamento: câmeras a menos de ~1,5 m do guarda-corpo
        # enxergam esse trecho pelo vidro, por isso os pontos do tour ficam afastados da borda.
        ult = a[-6:].mean(0)[xi]
        niveis = [(0.0, ult), (3.0, hblur(ult, 1.0)), (8.0, hblur(ult, 4.0)), (18.0, hblur(ult, 12.0)), (45.0, hblur(ult, 28.0) * 0.88)]
        lat_bot = -np.degrees(np.arctan((h - yh) / f))
        prof = np.clip(lat_bot - lat, 0, 45.0)                          # graus abaixo do fim da foto
        fill = np.zeros((H, W, 3), np.float32)
        for (d0, c0), (d1, c1) in zip(niveis[:-1], niveis[1:]):
            m = (prof >= d0) & (prof <= d1)
            k = ((prof[m] - d0) / (d1 - d0))[:, None, None]
            fill[m] = c0[None] * (1 - k) + c1[None] * k
        out = np.where((PY > h - 1)[..., None], fill, out)
        # acima da foto: céu limpo (sem as nuvens cortadas na borda), cada vez mais uniforme até o zênite
        top_b = hblur(np.percentile(a[:int(0.12 * h)], 20, axis=0)[xi], 30.0)
        zen = top_b.mean(0) * np.array([0.86, 0.92, 1.0])              # zênite um pouco mais fundo
        s = np.clip((lat - lat_top) / (90.0 - lat_top), 0, 1)[:, None, None]
        ceu = top_b[None] * (1 - s ** 0.8) + zen * s ** 0.8
        d = np.clip(1 - PY / (0.10 * h), 0, 1)[..., None] ** 1.5         # nuvens se desfazem perto do topo da foto
        out = out * (1 - d) + ceu * d
        return out, px

    out, PXr = amostra(dl)
    # emenda dos dois espelhos (lado oposto à foto): transição suave de 30°
    alt, _ = amostra(np.where(dl < 0, dl + 360.0, dl - 360.0))
    g = np.clip((np.abs(dl) - 165.0) / 30.0, 0, 0.5)[None, :, None]
    out = out * (1 - g) + alt * g

    if cfg.get('base'):
        # junta com a paisagem base: esta foto à esquerda da emenda, a base à direita (transição de 10°)
        base = montar(cfg['base'], salvar=False)
        d = (lon - cfg['emenda'] + 180.0) % 360.0 - 180.0             # >0 = à direita da emenda
        larg = np.interp(lat, [1.0, 12.0], [6.0, 70.0])[:, None]      # emenda estreita no chão (sem fantasma), bem larga no céu
        g = np.clip(d[None, :] / larg + 0.5, 0, 1)
        op = (lon - (cfg['emenda'] + 168.0) + 180.0) % 360.0 - 180.0   # segunda emenda, do lado oposto (atrás do prédio)
        g = np.where(np.abs(op)[None, :] < 90, np.clip(0.5 - op / 30.0, 0, 1)[None, :], g)[..., None]
        out = out * (1 - g) + base * g
    if not salvar:
        return out
    saida = os.path.join(ORIG, cfg['saida'])
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(saida)
    if mascara:
        real = ((PXr >= 0) & (PXr <= w - 1))[None, :] & ((py >= 0) & (py <= h - 1))[:, None]
        Image.fromarray((real * 255).astype(np.uint8)).save(saida.replace('.png', '_mascara.png'))
    print('ok', saida, 'foto cobre lat %.1f..%.1f' % (-np.degrees(np.arctan((h - yh) / f)), lat_top))

if __name__ == '__main__':
    montar(sys.argv[1], '--mascara' in sys.argv)
