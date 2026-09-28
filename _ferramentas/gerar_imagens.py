"""
Otimiza as fotos originais (pasta _originais/) em WebP e gera assets/js/data.js.

Uso (na pasta do site):  python3 _ferramentas/gerar_imagens.py
Requer Pillow:           python3 -m pip install pillow

- Cada foto do catálogo M vira  assets/img/<pasta>/<slug>.webp  (até 1600px, qualidade 90)
  e  <slug>-sm.webp  (até 1000px, qualidade 86), usada em miniaturas.
- Para trocar uma foto: substitua o arquivo em _originais/ (mesmo nome) e rode de novo.
- Para adicionar: inclua uma linha em M (arquivo, slug, categoria, legenda, unidade).
  Categorias: empreendimento, lazer, localizacao, plantas, coberturas, vista, serra.
  Unidade '303'/'304' faz a foto aparecer só na landing page da cobertura.
"""
import json, os, shutil
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

ROOT = os.environ.get('ANKOR_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_originais')
OUT = os.path.join(ROOT, 'assets/img')
WA = 'WhatsApp-Image-2026-02-09-at-'

# (arquivo original, slug, categoria, legenda, unidade)
M = [
  # Empreendimento
  ('DJI_0007.jpg', 'fachada-aerea', 'empreendimento', 'Fachada do Ankor Exclusive Residence', ''),
  (WA+'11.47.47-2.jpeg', 'fachada-piscina', 'empreendimento', 'Fachada e área de lazer', ''),
  ('fachada-frontal.png', 'arquitetura-varandas', 'empreendimento', 'Fachada do Ankor', ''),
  (WA+'11.47.47.jpeg', 'varandas-madeira', 'empreendimento', 'Varandas com acabamento em madeira', ''),
  ('DSC00094.jpg', 'detalhe-fachada', 'empreendimento', 'Detalhe da fachada', ''),
  ('DSC00122.jpg', 'acesso-social', 'empreendimento', 'Acesso social', ''),
  ('DSC00198.jpg', 'identidade', 'empreendimento', 'Identidade Ankor no paisagismo', ''),
  ('DSC00151.jpg', 'paisagismo-entrada', 'empreendimento', 'Paisagismo de entrada', ''),
  (WA+'11.47.45.jpeg', 'acesso-jardim', 'empreendimento', 'Acesso integrado ao jardim', ''),
  ('DSC00040.jpg', 'hall-pedra', 'empreendimento', 'Hall social com parede em pedra', ''),
  ('DSC00042.jpg', 'hall-estar', 'empreendimento', 'Estar do hall social', ''),
  ('DSC00046.jpg', 'hall-jardim', 'empreendimento', 'Hall social integrado ao jardim', ''),
  ('DSC00111.jpg', 'lounge-social', 'empreendimento', 'Lounge social', ''),
  ('DSC00048.jpg', 'cobogos', 'empreendimento', 'Cobogós e iluminação', ''),
  ('DSC00050.jpg', 'hall-elevadores', 'empreendimento', 'Hall dos elevadores', ''),
  ('DSC00156.jpg', 'circulacao-social', 'empreendimento', 'Circulação social', ''),
  ('DSC00196.jpg', 'hall-cobogo', 'empreendimento', 'Hall com parede de cobogós', ''),
  ('DSC00197.jpg', 'cobogo-curvo', 'empreendimento', 'Parede curva de cobogós', ''),
  ('DSC00191.jpg', 'luminarias', 'empreendimento', 'Luminárias do hall', ''),
  (WA+'11.47.46-1.jpeg', 'circulacao-cobogo', 'empreendimento', 'Circulação com cobogós', ''),
  (WA+'11.47.44-2.jpeg', 'terraco-social', 'empreendimento', 'Terraço social', ''),
  (WA+'11.47.45-1.jpeg', 'apoio-pranchas', 'empreendimento', 'Espaço de apoio para pranchas', ''),
  # Lazer
  (WA+'11.47.48-2.jpeg', 'piscinas-mar', 'lazer', 'Piscinas com vista para o mar', ''),
  (WA+'11.47.46.jpeg', 'piscina-deck', 'lazer', 'Piscina e deck', ''),
  ('DJI_0020.jpg', 'piscina-pergolado-aereo', 'lazer', 'Piscina e pergolado vistos do alto', ''),
  ('DSC00084.jpg', 'piscina-serra', 'lazer', 'Piscina com vista para a serra', ''),
  ('DSC00087.jpg', 'pergolado', 'lazer', 'Pergolado e jardim tropical', ''),
  ('DSC00089.jpg', 'piscina-deck-madeira', 'lazer', 'Piscina com deck de madeira', ''),
  ('DSC00092.jpg', 'piscina', 'lazer', 'Piscina', ''),
  ('DSC00093.jpg', 'piscina-jardim', 'lazer', 'Piscina e paisagismo', ''),
  ('DSC00103.jpg', 'piscina-borda', 'lazer', 'Piscina com guarda-corpo de vidro', ''),
  ('DSC00090.jpg', 'piscina-detalhe', 'lazer', 'Detalhe da piscina', ''),
  ('DSC00115.jpg', 'solario', 'lazer', 'Deck com espreguiçadeiras', ''),
  ('DSC00057.jpg', 'gourmet', 'lazer', 'Espaço gourmet', ''),
  ('DSC00058.jpg', 'gourmet-mesa', 'lazer', 'Mesa do espaço gourmet', ''),
  ('DSC00071.jpg', 'gourmet-cozinha', 'lazer', 'Cozinha do espaço gourmet', ''),
  ('DSC00055.jpg', 'gourmet-balcao', 'lazer', 'Balcão do espaço gourmet', ''),
  ('DSC00054.jpg', 'gourmet-integrado', 'lazer', 'Espaço gourmet integrado', ''),
  ('DSC00075.jpg', 'gourmet-jantar', 'lazer', 'Jantar do espaço gourmet', ''),
  ('DSC00076.jpg', 'gourmet-bancada', 'lazer', 'Bancada do espaço gourmet', ''),
  ('DSC00072.jpg', 'gourmet-ilha', 'lazer', 'Ilha em pedra natural', ''),
  ('DSC00063.jpg', 'gourmet-grill', 'lazer', 'Grill do espaço gourmet', ''),
  ('DSC00052.jpg', 'adega', 'lazer', 'Adega e aparador', ''),
  ('DSC00080.jpg', 'lounge-rebaixado', 'lazer', 'Lounge rebaixado entre jardins', ''),
  ('DSC00081.jpg', 'lounge-piscina', 'lazer', 'Lounge com vista para a piscina', ''),
  (WA+'11.47.48-3.jpeg', 'lounge-mar', 'lazer', 'Lounge e piscina', ''),
  (WA+'11.47.44.jpeg', 'lounge-jardim', 'lazer', 'Lounge no jardim', ''),
  ('DSC00077.jpg', 'pergolado-mesas', 'lazer', 'Pergolado com mesas', ''),
  ('DSC00098.jpg', 'jardim-piscina', 'lazer', 'Jardim e piscina', ''),
  ('DSC00100.jpg', 'lounge-almofadas', 'lazer', 'Lounge externo', ''),
  ('DSC00104.jpg', 'terraco-lounge', 'lazer', 'Terraço com lounge', ''),
  ('DSC00108.jpg', 'lounge-degraus', 'lazer', 'Estar externo', ''),
  ('DSC00107.jpg', 'pergolado-madeira', 'lazer', 'Pergolado em madeira', ''),
  ('DSC00109.jpg', 'terraco-coberto', 'lazer', 'Terraço coberto', ''),
  ('DSC00110.jpg', 'acesso-piscina', 'lazer', 'Acesso à piscina e ao lounge', ''),
  ('DSC00199.jpg', 'lounge-coberto', 'lazer', 'Lounge coberto', ''),
  (WA+'11.47.43-1.jpeg', 'terraco-mesas', 'lazer', 'Terraço com mesas', ''),
  (WA+'11.47.43.jpeg', 'jardim-deck', 'lazer', 'Jardim e deck', ''),
  ('DSC00163.jpg', 'spa', 'lazer', 'Spa', ''),
  ('DSC00164.jpg', 'spa-piscina', 'lazer', 'Spa com piscina', ''),
  ('DSC00166.jpg', 'spa-descanso', 'lazer', 'Área de descanso do spa', ''),
  ('DSC00159.jpg', 'spa-espreguicadeira', 'lazer', 'Espreguiçadeiras do spa', ''),
  ('DSC00160.jpg', 'spa-deck', 'lazer', 'Deck do spa', ''),
  ('DSC00161.jpg', 'spa-deck-2', 'lazer', 'Spa', ''),
  ('DSC00167.jpg', 'spa-agua', 'lazer', 'Piscina do spa', ''),
  ('DSC00169.jpg', 'spa-borda', 'lazer', 'Spa', ''),
  ('DSC00170.jpg', 'spa-detalhe', 'lazer', 'Detalhe do spa', ''),
  ('DSC00172.jpg', 'sauna', 'lazer', 'Sauna', ''),
  ('DSC00178.jpg', 'fitness', 'lazer', 'Fitness', ''),
  ('DSC00181.jpg', 'fitness-estacao', 'lazer', 'Estação de treino', ''),
  (WA+'11.47.48-1.jpeg', 'fitness-vista', 'lazer', 'Fitness com vista para o jardim', ''),
  ('DSC00177.jpg', 'fitness-2', 'lazer', 'Fitness', ''),
  ('DSC00176.jpg', 'fitness-equipamentos', 'lazer', 'Equipamentos de musculação', ''),
  (WA+'11.47.47-1.jpeg', 'fitness-3', 'lazer', 'Fitness', ''),
  ('DSC00179.jpg', 'fitness-esteira', 'lazer', 'Esteira', ''),
  ('DSC00183.jpg', 'fitness-4', 'lazer', 'Fitness', ''),
  ('DSC00186.jpg', 'fitness-banco', 'lazer', 'Fitness', ''),
  ('DSC00187.jpg', 'fitness-kettlebell', 'lazer', 'Fitness', ''),
  (WA+'11.47.46-2.jpeg', 'kids', 'lazer', 'Espaço kids', ''),
  ('DSC00133.jpg', 'kids-estar', 'lazer', 'Espaço kids', ''),
  ('DSC00130.jpg', 'kids-casinha', 'lazer', 'Espaço kids', ''),
  ('DSC00131.jpg', 'kids-bolinhas', 'lazer', 'Espaço kids', ''),
  ('DSC00132.jpg', 'kids-detalhe', 'lazer', 'Espaço kids', ''),
  ('DSC00135.jpg', 'jogos', 'lazer', 'Salão de jogos', ''),
  ('DSC00140.jpg', 'jogos-bilhar', 'lazer', 'Mesa de bilhar', ''),
  ('DSC00139.jpg', 'jogos-xadrez', 'lazer', 'Salão de jogos', ''),
  ('DSC00136.jpg', 'jogos-mesa', 'lazer', 'Mesa de jogos', ''),
  ('DSC00138.jpg', 'jogos-tabuleiro', 'lazer', 'Xadrez', ''),
  ('DSC00145.jpg', 'jogos-detalhe', 'lazer', 'Salão de jogos', ''),
  # Localização
  ('DJI_0028.jpg', 'aerea-itagua', 'localizacao', 'O Ankor e a baía do Itaguá', ''),
  ('DJI_0012.jpg', 'aerea-orla', 'localizacao', 'Orla do Itaguá', ''),
  ('DJI_0010.jpg', 'aerea-avenida', 'localizacao', 'Avenida da orla e a Marina', ''),
  ('DJI_0008.jpg', 'aerea-bairro', 'localizacao', 'Bairro do Itaguá', ''),
  ('DJI_0034.jpg', 'aerea-baia', 'localizacao', 'Baía de Ubatuba', ''),
  ('DJI_0017.jpg', 'aerea-implantacao', 'localizacao', 'Vista superior do empreendimento', ''),
  ('DSC00119.jpg', 'acesso-orla', 'localizacao', 'Acesso em direção à orla', ''),
  # Plantas
  ('planta303.png', 'planta-303', 'plantas', 'Planta humanizada — Cobertura 303', '303'),
  ('planta304.png', 'planta-304', 'plantas', 'Planta humanizada — Cobertura 304', '304'),
  # Cobertura 303 (fotos reais, unidade sem decoração)
  (WA+'11.46.07-3.jpeg', '303-living-solarium', 'coberturas', 'Living com acesso ao solarium', '303'),
  (WA+'11.46.07-2.jpeg', '303-living-cozinha', 'coberturas', 'Living integrado à cozinha', '303'),
  (WA+'11.46.08-1.jpeg', '303-living', 'coberturas', 'Living amplo', '303'),
  (WA+'11.46.08.jpeg', '303-living-2', 'coberturas', 'Living e cozinha', '303'),
  (WA+'11.46.08-2.jpeg', '303-cozinha', 'coberturas', 'Cozinha', '303'),
  (WA+'11.46.08-3.jpeg', '303-cozinha-2', 'coberturas', 'Cozinha integrada', '303'),
  (WA+'11.46.06-1.jpeg', '303-suite', 'coberturas', 'Suíte', '303'),
  (WA+'11.46.06.jpeg', '303-suite-2', 'coberturas', 'Suíte', '303'),
  (WA+'11.46.05.jpeg', '303-circulacao', 'coberturas', 'Circulação íntima', '303'),
  (WA+'11.46.05-2.jpeg', '303-corredor', 'coberturas', 'Corredor das suítes', '303'),
  (WA+'11.46.06-3.jpeg', '303-banho', 'coberturas', 'Banheiro da suíte', '303'),
  (WA+'11.46.07-1.jpeg', '303-lavabo', 'coberturas', 'Lavabo', '303'),
  (WA+'11.46.09.jpeg', '303-solarium', 'coberturas', 'Solarium com bancada gourmet', '303'),
  (WA+'11.46.09-3.jpeg', '303-solarium-2', 'coberturas', 'Solarium', '303'),
  (WA+'11.46.09-2.jpeg', '303-bancada', 'coberturas', 'Bancada da área gourmet', '303'),
  # Vista 303
  (WA+'11.46.10-2.jpeg', '303-vista-solarium', 'vista', 'Vista a partir do solarium da Cobertura 303', '303'),
  (WA+'11.46.10-3.jpeg', '303-vista-mar', 'vista', 'Vista lateral para o mar — Cobertura 303', '303'),
  (WA+'11.46.09-1.jpeg', '303-vista-janela', 'vista', 'Vista a partir do living — Cobertura 303', '303'),
  (WA+'11.46.07.jpeg', '303-vista-marina', 'vista', 'Vista para a Marina — Cobertura 303', '303'),
  (WA+'11.46.10-1.jpeg', '303-vista-verde', 'serra', 'Vista para a serra a partir do solarium — Cobertura 303', '303'),
  (WA+'11.46.10.jpeg', '303-vista-lateral', 'serra', 'Vista para a serra a partir do solarium — Cobertura 303', '303'),
  # Cobertura 304
  (WA+'11.47.05-3.jpeg', '304-living-solarium', 'coberturas', 'Living com acesso ao solarium', '304'),
  (WA+'11.47.07.jpeg', '304-living-cozinha', 'coberturas', 'Living integrado à cozinha', '304'),
  (WA+'11.47.06.jpeg', '304-living', 'coberturas', 'Living amplo', '304'),
  (WA+'11.47.06-1.jpeg', '304-living-2', 'coberturas', 'Living', '304'),
  (WA+'11.47.07-1.jpeg', '304-living-3', 'coberturas', 'Living com iluminação natural', '304'),
  (WA+'11.47.06-3.jpeg', '304-cozinha', 'coberturas', 'Cozinha integrada', '304'),
  (WA+'11.47.06-4.jpeg', '304-cozinha-2', 'coberturas', 'Cozinha', '304'),
  (WA+'11.47.03-1.jpeg', '304-suite-varanda', 'coberturas', 'Suíte com varanda', '304'),
  (WA+'11.47.04.jpeg', '304-suite', 'coberturas', 'Suíte', '304'),
  (WA+'11.47.03.jpeg', '304-suite-2', 'coberturas', 'Suíte', '304'),
  (WA+'11.47.03-2.jpeg', '304-suite-3', 'coberturas', 'Suíte', '304'),
  (WA+'11.47.05-1.jpeg', '304-suite-4', 'coberturas', 'Suíte', '304'),
  (WA+'11.47.05-2.jpeg', '304-suite-5', 'coberturas', 'Suíte', '304'),
  (WA+'11.47.07-2.jpeg', '304-circulacao', 'coberturas', 'Circulação', '304'),
  (WA+'11.47.06-2.jpeg', '304-banho', 'coberturas', 'Banheiro da suíte', '304'),
  (WA+'11.47.07-3.jpeg', '304-lavabo', 'coberturas', 'Lavabo', '304'),
  (WA+'11.47.08-3.jpeg', '304-solarium', 'coberturas', 'Solarium com bancada gourmet', '304'),
  (WA+'11.47.08.jpeg', '304-solarium-2', 'coberturas', 'Solarium', '304'),
  (WA+'11.47.08-1.jpeg', '304-solarium-3', 'coberturas', 'Solarium', '304'),
  # Vista 304
  (WA+'11.47.08-2.jpeg', '304-vista-solarium', 'vista', 'Vista a partir do solarium da Cobertura 304', '304'),
  (WA+'11.47.09.jpeg', '304-vista-mar', 'vista', 'Vista lateral para o mar — Cobertura 304', '304'),
  (WA+'11.47.04-2.jpeg', '304-vista-varanda', 'vista', 'Vista a partir da varanda — Cobertura 304', '304'),
  (WA+'11.47.04-1.jpeg', '304-vista-varanda-2', 'vista', 'Vista a partir da varanda — Cobertura 304', '304'),
  (WA+'11.47.05.jpeg', '304-vista-varanda-3', 'vista', 'Vista a partir da suíte — Cobertura 304', '304'),
]

data = []
os.makedirs(OUT, exist_ok=True)
for fn, slug, cat, cap, unit in M:
    im = Image.open(os.path.join(SRC, fn))
    is_plan = fn.startswith('planta')
    if is_plan:
        im = im.convert('RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg.convert('RGB')
    else:
        im = im.convert('RGB')
    folder = 'vista' if cat == 'serra' else cat  # fotos da serra ficam na pasta vista/
    d = os.path.join(OUT, folder)
    os.makedirs(d, exist_ok=True)
    full = im.copy()
    full.thumbnail((1600, 1600), Image.LANCZOS)
    full.save(os.path.join(d, slug + '.webp'), 'WEBP', quality=95 if is_plan else 90, method=6)
    sm = im.copy()
    sm.thumbnail((1000, 1000), Image.LANCZOS)
    sm.save(os.path.join(d, slug + '-sm.webp'), 'WEBP', quality=86, method=6)
    data.append({'id': slug, 'src': f'{folder}/{slug}.webp', 'sm': f'{folder}/{slug}-sm.webp',
                 'w': full.width, 'h': full.height, 'cat': cat, 'cap': cap, 'unit': unit})

# Marca
os.makedirs(os.path.join(ROOT, 'assets/brand'), exist_ok=True)
shutil.copy(os.path.join(SRC, 'ankorlogo.png'), os.path.join(ROOT, 'assets/brand/ankor-logo.png'))
shutil.copy(os.path.join(SRC, 'convenio.svg'), os.path.join(ROOT, 'assets/brand/convenio.svg'))

# Fotos do topo da home (pasta _originais/header/). Fotos com mais de 1200px ganham
# duas versões (-1200 e -2400) para o navegador escolher conforme a tela.
HERO = os.path.join(ROOT, 'assets/img/hero')
os.makedirs(HERO, exist_ok=True)
for i, fn in enumerate(['foto1.png', 'foto3.png', 'foto2.png', 'foto4.jpg', 'foto5.png'], 1):
    im = Image.open(os.path.join(SRC, 'header', fn)).convert('RGB')
    if im.width <= 1200:
        im.save(os.path.join(HERO, f'hero-{i}.webp'), 'WEBP', quality=82, method=6)
        continue
    for w, q in ((2400, 84), (1200, 82)):
        c = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if im.width > w else im
        c.save(os.path.join(HERO, f'hero-{i}-{w}.webp'), 'WEBP', quality=q, method=6)

# Topo das landing pages e foto aérea da localização (tamanho original, qualidade 88)
for fn, out in (('hero-cobertura-303.png', 'hero/lp-303.webp'), ('hero-cobertura-304.png', 'hero/lp-304.webp'),
                ('localizacao-aerea.png', 'localizacao/aerea-baia-ankor.webp')):
    Image.open(os.path.join(SRC, fn)).convert('RGB').save(os.path.join(OUT, out), 'WEBP', quality=88, method=6)

with open(os.path.join(ROOT, 'assets/js/data.js'), 'w') as f:
    f.write('/* Catálogo de imagens (gerado a partir das fotos originais do site). */\n')
    f.write('window.ANKOR_IMAGES = ' + json.dumps(data, ensure_ascii=False, indent=0) + ';\n')
print(len(data), 'imagens')
