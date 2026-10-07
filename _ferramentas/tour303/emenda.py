"""
Conserta a emenda lateral (onde as pontas esquerda/direita do 360° se encontram) de uma imagem refinada por IA.

  python emenda.py girar   resultados/303-suite2.png  emenda/303-suite2_rolado.jpg
      gira a imagem meia volta: a emenda vai para o centro. Mandar esse arquivo para a IA pedindo para consertar
      só a costura vertical central, sem mudar o resto.
  python emenda.py aplicar resultados/303-suite2.png  emenda/303-suite2_reparo.png  resultados/303-suite2.png
      pega do reparo só a faixa central (±LARG da largura, com transição suave) e devolve a imagem na posição original.
      O resto continua sendo a imagem original, então nada mais muda.
"""
import sys
import numpy as np
from PIL import Image, ImageChops

LARG = 0.16      # meia-largura da faixa aproveitada do reparo (fração da largura)
SUAVE = 0.06     # largura da transição em cada lado

def girar(src, dst):
    im = Image.open(src).convert('RGB')
    ImageChops.offset(im, im.width // 2, 0).save(dst, quality=95)

def aplicar(orig, reparo, dst):
    a = Image.open(orig).convert('RGB'); w, h = a.size
    ar = np.asarray(ImageChops.offset(a, w // 2, 0)).astype(np.float32)
    b = np.asarray(Image.open(reparo).convert('RGB').resize((w, h), Image.LANCZOS)).astype(np.float32)
    x = np.abs((np.arange(w) + 0.5) / w - 0.5)
    m = np.clip((LARG - x) / SUAVE, 0, 1)[None, :, None]
    out = Image.fromarray(np.clip(ar * (1 - m) + b * m, 0, 255).astype(np.uint8))
    ImageChops.offset(out, -(w // 2), 0).save(dst)

if __name__ == '__main__':
    (girar if sys.argv[1] == 'girar' else aplicar)(*sys.argv[2:])
