"""
Recoloca a vista real numa imagem refinada por IA (a IA redesenha a imagem inteira, inclusive a paisagem).

  python restaurar_vista.py 303 living  refinada.png        # grava tour-303/img/living.webp (4096x2048)
  python restaurar_vista.py 304 deck    refinada.png --ver  # grava também render/higgsfield/resultados/304-deck_final.jpg

Usa o render cru do Blender (render/v5 ou render/304) e a máscara <ambiente>_360_mask.png (alfa 0 = paisagem,
gerada com `cena_living.py --mascara`). Onde a máscara diz "paisagem", volta o pixel do render cru (que tem a foto real,
já com o tom do vidro); no resto fica a imagem refinada. A refinada é esticada para 2:1 antes.
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', '..'))
W, H = 4096, 2048

def main(apto, amb, refinada, ver=False):
    pasta = os.path.join(HERE, 'render', 'v5' if apto == '303' else '304')
    cru = Image.open(os.path.join(pasta, amb + '_360.png')).convert('RGB').resize((W, H), Image.LANCZOS)
    ia = Image.open(refinada).convert('RGB').resize((W, H), Image.LANCZOS)
    mpath = os.path.join(pasta, amb + '_360_mask.png')
    # Padrão (decisão de 07/10/2026): NÃO recolocar a vista. A IA reproduz bem a paisagem do render e a colagem pela
    # máscara deixava bordas e montantes duplicados nas janelas. Use --vista só se a IA trocar a paisagem.
    if '--vista' in sys.argv and os.path.exists(mpath):
        a = Image.open(mpath).split()[-1].resize((W, H), Image.LANCZOS)
        a = a.filter(ImageFilter.MedianFilter(5))                      # tira o granulado da máscara
        m = 1.0 - np.asarray(a).astype(np.float32) / 255.0             # 1 = paisagem
        m = np.clip((m - 0.25) / 0.5, 0, 1)                            # só onde a paisagem domina (vidro limpo ou céu aberto)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.0))).astype(np.float32) / 255.0
        out = np.asarray(ia).astype(np.float32) * (1 - m[..., None]) + np.asarray(cru).astype(np.float32) * m[..., None]
        img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    else:
        img = ia
    destino = os.path.join(SITE, 'tour-' + apto, 'img', amb + '.webp')
    img.save(destino, quality=90)
    if ver:
        d = os.path.join(HERE, 'render', 'higgsfield', 'resultados'); os.makedirs(d, exist_ok=True)
        img.resize((2000, 1000), Image.LANCZOS).save(os.path.join(d, '%s-%s_final.jpg' % (apto, amb)), quality=88)
    print('ok', destino)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], '--ver' in sys.argv)
