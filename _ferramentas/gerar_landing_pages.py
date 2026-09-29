"""
Gera cobertura-303/index.html e cobertura-304/index.html a partir de um único modelo,
e as páginas de obrigado (obrigado/ e obrigado-contato/).

Uso (na pasta do site):  python3 _ferramentas/gerar_landing_pages.py

- Textos, preços e fotos de cada unidade: dicionário UNITS.
- Estrutura da página: função page().
- As seções "Vídeo institucional" e "Localização" são copiadas da home (index.html)
  a cada execução, então edite essas seções na home e rode este script.
- NÃO edite cobertura-30x/index.html à mão: serão sobrescritos na próxima geração.
"""
import os
ROOT = os.environ.get('ANKOR_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Google Analytics 4 e Google Ads, as mesmas tags do WordPress antigo do /ankor
# (ficam fora do GTM). A conversão do Ads é disparada só em /obrigado/.
GTAG = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-858ZVEWJJ1"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-858ZVEWJJ1');gtag('config','AW-10869641873');</script>"""
CONVERSAO_ADS = "<script>gtag('event','conversion',{'send_to':'AW-10869641873/pZuNCIeHxeAYEJGlhr8o'});</script>"
V = '20260929d'  # versão do CSS/JS (troque ao mudar style.css ou um JS; na home também)

UNITS = {
  '303': dict(area='240', price='R$ 3.980.000,00', price_short='R$ 3.980.000',
    title='Uma cobertura única, pensada para quem valoriza <em>espaço, conforto e sofisticação</em>.',
    title_plain='Uma cobertura única, pensada para quem valoriza espaço, conforto e sofisticação.',
    sub='Ambientes amplos, varanda gourmet e solarium com vista para o mar, em uma localização privilegiada no Itaguá.',
    hero='hero/lp-303.webp', hero_wh=(1344, 904), hero_pos='78% 100%', hero_zoom=1.2,
    intro='coberturas/303-living-solarium.webp', view='vista/303-vista-mar.webp',
    plan='plantas/planta-303.webp', other='304', other_img='vista/304-vista-solarium-sm.webp',
    other_area='254', other_price='R$ 4.280.000,00', pos='y303'),
  '304': dict(area='254', price='R$ 4.280.000,00', price_short='R$ 4.280.000',
    title='A amplitude de uma cobertura pensada para viver Ubatuba com <em>conforto e sofisticação</em>.',
    title_plain='A amplitude de uma cobertura pensada para viver Ubatuba com conforto e sofisticação.',
    sub='Ambientes integrados, varanda gourmet e solarium com vista para o mar, em uma localização privilegiada no Itaguá.',
    hero='hero/lp-304.webp', hero_wh=(1344, 1058), hero_pos='30% 100%', hero_zoom=1.4,
    intro='coberturas/304-living-cozinha.webp', intro_alt='Living amplo integrado à cozinha da Cobertura {u}', view='vista/304-vista-mar.webp',
    plan='plantas/planta-304.webp', other='303', other_img='vista/303-vista-solarium-sm.webp',
    other_area='240', other_price='R$ 3.980.000,00', pos='y304'),
}

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
I = {
 'area': '<path d="M4 4h16v16H4zM4 9h5M9 4v5M15 20v-5h5"/>',
 'bed': '<path d="M3 18v-6a2 2 0 012-2h14a2 2 0 012 2v6M3 15h18M6 10V7a1 1 0 011-1h4a1 1 0 011 1v3M12 10V7a1 1 0 011-1h4a1 1 0 011 1v3"/>',
 'sofa': '<path d="M4 11V8a2 2 0 012-2h12a2 2 0 012 2v3M2 13a2 2 0 014 0v2h12v-2a2 2 0 014 0v5H2zM5 18v2M19 18v2"/>',
 'grill': '<path d="M5 10h14l-1.5 5h-11zM9 15l-2 5M15 15l2 5M9 6c0-1 1-1 1-2M13 6c0-1 1-1 1-2"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 'car': '<path d="M5 16V11l2-5h10l2 5v5M5 16h14M5 16v2M19 16v2M7.5 13h.01M16.5 13h.01"/>',
 'anchor': '<circle cx="12" cy="5" r="2"/><path d="M12 7v14M8 11h8M5 15a7 7 0 0014 0"/>',
 'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
 'zoom': '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M11 8v6M8 11h6"/>',
}
def icon(k): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">{I[k]}</svg>'

def implant(u):
    hi, lo = ('#c9823b', 'none') if u == '303' else ('none', '#c9823b')
    # 303: metade superior da parte posterior | 304: metade inferior
    arrow_y = (34, 14) if u == '303' else (306, 326)
    return f'''<svg viewBox="0 0 520 340" role="img" aria-labelledby="impl-t">
  <title id="impl-t">Esquema de implantação: a Cobertura {u} fica na parte posterior do edifício, com vista lateral para o mar</title>
  <defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#ffe5d4"/></marker></defs>
  <path d="M40 40H470L490 300H40Z" fill="rgba(255,229,212,.04)" stroke="rgba(255,229,212,.4)" stroke-width="1.5"/>
  <rect x="48" y="48" width="196" height="244" rx="6" fill="rgba(255,229,212,.06)"/>
  <text x="146" y="166" fill="rgba(255,229,212,.55)" font-family="Manrope, sans-serif" font-size="12" text-anchor="middle" letter-spacing="2">UNIDADES</text>
  <text x="146" y="183" fill="rgba(255,229,212,.55)" font-family="Manrope, sans-serif" font-size="12" text-anchor="middle" letter-spacing="2">FRONTAIS</text>
  <rect x="200" y="150" width="56" height="40" rx="4" fill="rgba(255,229,212,.12)"/>
  <text x="228" y="174" fill="rgba(255,229,212,.55)" font-family="Manrope, sans-serif" font-size="9" text-anchor="middle">CIRC.</text>
  <path d="M262 48H466L474 164H262Z" fill="{hi if hi!='none' else 'rgba(255,229,212,.03)'}" stroke="{'#c9823b' if u=='303' else 'rgba(255,229,212,.35)'}" stroke-width="1.5"/>
  <path d="M262 176H475L483 292H262Z" fill="{lo if lo!='none' else 'rgba(255,229,212,.03)'}" stroke="{'#c9823b' if u=='304' else 'rgba(255,229,212,.35)'}" stroke-width="1.5"/>
  <text x="366" y="112" fill="{'#1f201c' if u=='303' else 'rgba(255,229,212,.55)'}" font-family="Cormorant Garamond, serif" font-size="30" font-weight="600" text-anchor="middle">303</text>
  <text x="370" y="241" fill="{'#1f201c' if u=='304' else 'rgba(255,229,212,.55)'}" font-family="Cormorant Garamond, serif" font-size="30" font-weight="600" text-anchor="middle">304</text>
  <text x="18" y="170" fill="#ffe5d4" font-family="Manrope, sans-serif" font-size="11" letter-spacing="3" text-anchor="middle" transform="rotate(-90 18 170)">FRENTE</text>
  <text x="506" y="170" fill="rgba(255,229,212,.6)" font-family="Manrope, sans-serif" font-size="11" letter-spacing="3" text-anchor="middle" transform="rotate(90 506 170)">FUNDOS</text>
  <line x1="330" y1="{arrow_y[0]}" x2="270" y2="{arrow_y[1]}" stroke="#ffe5d4" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#ah)"/>
  <line x1="400" y1="{arrow_y[0]}" x2="340" y2="{arrow_y[1]}" stroke="#ffe5d4" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#ah)"/>
  <text x="258" y="{arrow_y[1] + (4 if u=='303' else 10)}" fill="#ffe5d4" font-family="Manrope, sans-serif" font-size="11" letter-spacing="1" text-anchor="end">VISTA LATERAL PARA O MAR</text>
</svg>'''

def home_location():
    import re as _re
    h = open(f'{ROOT}/index.html').read()
    sec = _re.search(r'<section class="section section--sand" id="localizacao">.*?</section>', h, _re.S).group(0)
    return '<!-- LOCALIZAÇÃO (mesma da home) -->\n' + sec.replace('src="assets/', 'src="../assets/')

def home_video():
    import re as _re
    h = open(f'{ROOT}/index.html').read()
    sec = _re.search(r'<!-- =+ VÍDEO INSTITUCIONAL =+ -->\n<section.*?</section>', h, _re.S).group(0)
    return sec.replace('src="assets/', 'src="../assets/')

def page(u, d):
    o = d['other']
    LOCATION = home_location()
    VIDEO = home_video()
    return f'''<!doctype html>
<html lang="pt-BR" data-base="../">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Cobertura {u} · {d['area']} m² · Ankor Exclusive Residence</title>
<meta name="description" content="Cobertura {u} no Ankor Exclusive Residence, Itaguá, Ubatuba: {d['area']} m² privativos, 3 suítes, varanda gourmet, solarium com infraestrutura para jacuzzi, 2 vagas e armário náutico. {d['price']}.">
<meta name="theme-color" content="#2e2f2a">
<link rel="icon" href="../assets/brand/favicon.png">
<meta property="og:title" content="Cobertura {u} · Ankor Exclusive Residence">
<meta property="og:description" content="{d['title_plain']}">
<meta property="og:image" content="../assets/img/{d['hero']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="../assets/img/{d['hero']}" fetchpriority="high">
<link rel="stylesheet" href="../assets/css/style.css?v={V}">
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-N2VF7FVX');</script>
{GTAG}
<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','279593157240250');fbq('track','PageView');fbq('track','ViewContent',{{content_name:'Cobertura {u}'}});</script>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-N2VF7FVX" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

<header class="header">
  <div class="container header__inner">
    <a href="../" class="logo logo--lg" aria-label="Voltar ao site do Ankor"><img src="../assets/brand/ankor-logo.png" alt="Ankor Exclusive Residence" width="310" height="58"></a>
    <button class="nav-toggle" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu"><span></span></button>
    <nav class="nav" id="menu" aria-label="Cobertura {u}">
      <a href="#destaques">Destaques</a>
      <a href="#galeria">Galeria</a>
      <a href="#vista">Vista</a>
      <a href="#planta">Planta</a>
      <a href="#faq">Dúvidas</a>
      <a href="#agendar" class="btn btn--peach" data-goal="Agendar apresentação privativa">Agendar apresentação</a>
    </nav>
  </div>
</header>

<main>
<!-- 1. HERO -->
<section class="lp-hero">
  <div class="container lp-hero__content">
    <div class="lp-hero__grid">
      <div class="lp-hero__text">
        <p class="eyebrow">Cobertura {u} · Ankor Exclusive Residence</p>
        <h1 class="h1">{d['title']}</h1>
        <p class="lp-hero__sub">{d['sub']}</p>
      </div>
      <figure class="lp-hero__photo" style="--pos:{d['hero_pos']};--zoom:{d['hero_zoom']}">
        <img src="../assets/img/{d['hero']}" alt="Vista para o mar a partir do solarium da Cobertura {u}" width="{d['hero_wh'][0]}" height="{d['hero_wh'][1]}" fetchpriority="high">
        <span class="photo-note">Foto real · vista do solarium</span>
      </figure>
    </div>
    <div class="spec-bar">
      <div class="spec-bar__price"><small>Valor</small><strong>{d['price']}</strong></div>
      <ul class="spec-bar__list">
        <li>{d['area']} m² privativos</li><li>3 suítes</li><li>Varanda gourmet</li><li>Solarium com infraestrutura para jacuzzi</li><li>2 vagas</li><li>Armário náutico</li>
      </ul>
      <a href="#agendar" class="btn btn--peach" data-goal="Agendar apresentação privativa">Agendar uma apresentação privativa {ARROW}</a>
    </div>
  </div>
</section>

<!-- 2. APRESENTAÇÃO -->
<section class="section section--sand">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">A cobertura</p>
      <h2 class="h2">Um espaço para viver Ubatuba com <em>mais conforto</em></h2>
      <p style="margin-top:24px">Mais do que uma cobertura, o Ankor oferece um ambiente pensado para aproveitar o litoral com tranquilidade, privacidade e sofisticação. A integração entre os espaços sociais, a amplitude dos ambientes e a presença da varanda gourmet criam novas possibilidades para viver, relaxar e receber a família e os amigos.</p>
      <p>O solarium amplia a experiência da cobertura e proporciona momentos especiais de contemplação, com vista para o mar e a atmosfera única de Ubatuba.</p>
      <a href="#agendar" class="btn btn--primary" style="margin-top:12px" data-goal="Agendar apresentação privativa">Agendar uma apresentação privativa {ARROW}</a>
    </div>
    <figure class="split__media reveal reveal-d1" style="margin:0">
      <img src="../assets/img/{d['intro']}" alt="{d.get('intro_alt', 'Living amplo da Cobertura {u} com acesso ao solarium').replace('{u}', u)}" loading="lazy" width="1280" height="720">
      <span class="tag">Foto real · unidade sem decoração</span>
    </figure>
  </div>
</section>

<!-- 3. DESTAQUES -->
<section class="section" id="destaques">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Destaques da unidade</p>
      <h2 class="h2">Cada ambiente pensado para tornar a <em>experiência única</em></h2>
    </div>
    <div class="highlights">
      <article class="hl reveal"><div class="hl__icon">{icon('area')}</div><h3>Área privativa</h3><p><strong>{d['area']} m² de área privativa</strong> para viver com amplitude, conforto e liberdade de composição.</p></article>
      <article class="hl reveal reveal-d1"><div class="hl__icon">{icon('bed')}</div><h3>Suítes</h3><p><strong>3 suítes</strong>, incluindo suíte master, para preservar a privacidade e acomodar a família com conforto.</p></article>
      <article class="hl reveal reveal-d2"><div class="hl__icon">{icon('sofa')}</div><h3>Living</h3><p><strong>Living amplo e integrado à cozinha</strong>, favorecendo a convivência, a iluminação natural e a fluidez dos ambientes.</p></article>
      <article class="hl reveal"><div class="hl__icon">{icon('grill')}</div><h3>Varanda gourmet</h3><p><strong>Varanda gourmet com churrasqueira a gás</strong>, criada para receber bem em todos os momentos.</p></article>
      <article class="hl reveal reveal-d1"><div class="hl__icon">{icon('sun')}</div><h3>Solarium</h3><p><strong>Solarium com infraestrutura para jacuzzi</strong>, um espaço reservado para relaxar e contemplar a vista para o mar.</p></article>
      <article class="hl reveal reveal-d2"><div class="hl__icon">{icon('car')}</div><h3>Garagem</h3><p><strong>2 vagas amplas</strong>, com praticidade para moradores e convidados.</p></article>
      <article class="hl reveal"><div class="hl__icon">{icon('anchor')}</div><h3>Armário náutico</h3><p><strong>Armário náutico espaçoso</strong>, pensado para acompanhar o estilo de vida de quem aproveita o litoral e as atividades no mar.</p></article>
      <article class="hl hl--accent reveal reveal-d1"><div><h3>Quer ver de perto?</h3><p>Agende uma visita presencial ou por videochamada.</p></div><a href="#agendar" class="btn btn--peach" data-goal="Agendar apresentação privativa">Agendar {ARROW}</a></article>
    </div>
  </div>
</section>

<!-- 4. GALERIA -->
<section class="section section--sand" id="galeria">
  <div class="container" data-inline-gallery="{u}" data-limit="6">
    <div class="section-head reveal">
      <p class="eyebrow">Galeria de ambientes</p>
      <h2 class="h2">Uma cobertura feita para ser <em>vivida em todos os detalhes</em></h2>
      <p class="lead">Ambientes bem elaborados, materiais selecionados e uma arquitetura que valoriza a integração com a natureza.</p>
    </div>
    <div class="tabs" role="tablist" aria-label="Filtrar ambientes"></div>
    <div class="lp-gallery" data-lb-group></div>
    <div class="gallery-actions">
      <p>Fotos reais da unidade, entregue sem decoração.</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <button class="btn btn--ghost" data-open-gallery="{u}">Ver todas as imagens</button>
        <a href="#agendar" class="btn btn--primary" data-goal="Agendar apresentação privativa">Agendar uma apresentação privativa</a>
      </div>
    </div>
  </div>
</section>

<!-- 5. VISTA E IMPLANTAÇÃO -->
<section class="section section--dark" id="vista">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Vista para o mar e implantação</p>
      <h2 class="h2">Uma perspectiva <em>singular de Ubatuba</em></h2>
      <p class="lead">A localização da cobertura na parte posterior do edifício proporciona uma perspectiva própria e surpreendente da paisagem de Ubatuba. A vista se abre para o mar e para as montanhas, pelas laterais do apartamento, criando um cenário amplo e privilegiado.</p>
      <p class="lead">A implantação do edifício e as imagens reais da cobertura permitem visualizar sua orientação e comprovar a amplitude dessa vista.</p>
    </div>
    <div class="view">
      <div class="implant reveal">
        {implant(u)}
        <div class="implant__legend">
          <span><i style="background:#c9823b"></i>Cobertura {u}</span>
          <span><i style="border:1px solid rgba(255,229,212,.4)"></i>Cobertura {o}</span>
          <span>Esquema ilustrativo, sem escala</span>
        </div>
      </div>
      <div class="reveal reveal-d1">
        <figure class="view__photo" data-lb-group>
          <button class="g-item" data-img="{d['view'].split('/')[1][:-5]}" style="border-radius:0"><img src="../assets/img/{d['view']}" alt="Vista lateral para o mar a partir da Cobertura {u}" loading="lazy" width="1280" height="720"></button>
          <span class="tag">Foto real da vista</span>
        </figure>
        <a href="#agendar" class="btn btn--peach" style="margin-top:24px" data-goal="Conhecer a vista da cobertura">Quero conhecer a vista da cobertura {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<!-- 6. PLANTA -->
<section class="section" id="planta">
  <div class="container plan">
    <div class="reveal" data-lb-group>
      <button class="plan__img" data-img="planta-{u}" aria-label="Ampliar planta da Cobertura {u}">
        <img src="../assets/img/{d['plan']}" alt="Planta humanizada da Cobertura {u}" loading="lazy" width="1212" height="668">
        <span class="icon-btn plan__zoom" aria-hidden="true">{icon('zoom')}</span>
      </button>
      <p style="font-size:12.5px;color:var(--muted);margin:12px 4px 0">Planta humanizada ilustrativa. O mobiliário é sugestão de ambientação e não faz parte da entrega. Toque para ampliar.</p>
    </div>
    <div class="reveal reveal-d1">
      <p class="eyebrow">Planta e distribuição</p>
      <h2 class="h2">Uma planta que valoriza a <em>convivência e a privacidade</em></h2>
      <ul class="plan-list">
        <li>{d['area']} m² privativos</li><li>3 suítes</li><li>Lavabo</li><li>Living integrado</li><li>Cozinha</li><li>Lavanderia reservada</li><li>Varanda gourmet</li><li>Solarium</li><li>2 vagas de garagem</li><li>Armário náutico</li>
      </ul>
      <p style="color:var(--muted)">A distribuição dos ambientes foi pensada para equilibrar espaços de convivência e áreas reservadas. O living integrado amplia a sensação de espaço, enquanto as suítes oferecem conforto e privacidade para moradores e convidados.</p>
      <a href="#agendar" class="btn btn--primary" data-goal="Agendar apresentação privativa">Agendar uma apresentação privativa {ARROW}</a>
    </div>
  </div>
</section>

<!-- 8. DIFERENCIAIS DO ANKOR -->
<section class="section" id="diferenciais">
  <div class="container">
    <div class="head-row">
      <div class="section-head reveal">
        <p class="eyebrow">Diferenciais do Ankor</p>
        <h2 class="h2">Um empreendimento pensado para <em>viver bem</em></h2>
      </div>
      <a href="../#diferenciais" class="btn btn--ghost">Conhecer todos os diferenciais</a>
    </div>
    <div class="diffs">
      <article class="diff reveal"><span class="tile__num">01</span><h3>Convivência</h3><p>Espaços de uso comum integrados e ambientes preparados para receber a família e os amigos.</p></article>
      <article class="diff reveal reveal-d1"><span class="tile__num">02</span><h3>Lazer</h3><p>Piscinas, spa, sauna, fitness, espaço gourmet, lounge, espaço kids e áreas para convivência.</p></article>
      <article class="diff reveal reveal-d2"><span class="tile__num">03</span><h3>Praticidade</h3><p>Infraestrutura para internet por fibra óptica, duas vagas e armário náutico associado à unidade.</p></article>
      <article class="diff reveal reveal-d3"><span class="tile__num">04</span><h3>Exclusividade residencial</h3><p>Um ambiente destinado ao uso residencial, com regras que não permitem locação de temporada.</p><small>Ideal para uso próprio e tranquilidade; não atende quem busca renda com aluguel de curta duração.</small></article>
    </div>
  </div>
</section>

<!-- 9. FAQ -->
<section class="section section--sand" id="faq">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <p class="eyebrow">Perguntas frequentes</p>
      <h2 class="h2">Tudo sobre a <em>Cobertura {u}</em></h2>
    </div>
    <div class="faq reveal">
      <details><summary>A cobertura tem vista para o mar?</summary><p>Sim. A unidade está localizada na parte posterior do prédio e possui vista para o mar. Consulte as imagens reais e o esquema de implantação para conhecer a orientação e o campo visual da cobertura.</p></details>
      <details><summary>A cobertura fica de frente para a praia?</summary><p>Não. A cobertura está na parte posterior do edifício. A comunicação correta é vista para o mar, conforme apresentado na planta e nas imagens da unidade.</p></details>
      <details><summary>Qual é a área privativa?</summary><p>A Cobertura {u} possui {d['area']} m² de área privativa.</p></details>
      <details><summary>Quantas suítes possui?</summary><p>A unidade possui 3 suítes, incluindo uma suíte master.</p></details>
      <details><summary>A cobertura possui varanda gourmet?</summary><p>Sim. A unidade possui varanda gourmet com churrasqueira a gás.</p></details>
      <details><summary>Existe infraestrutura para jacuzzi?</summary><p>Sim. O solarium possui infraestrutura para jacuzzi. A instalação e as condições técnicas devem ser confirmadas com a equipe responsável.</p></details>
      <details><summary>Quantas vagas de garagem estão incluídas?</summary><p>A unidade possui 2 vagas de garagem amplas.</p></details>
      <details><summary>Existe armário náutico?</summary><p>Sim, conforme as condições específicas da unidade e da documentação comercial.</p></details>
      <details><summary>É permitida locação de temporada?</summary><p>Não. O empreendimento possui uso residencial e não permite locação de temporada.</p></details>
      <details><summary>Posso visitar a cobertura?</summary><p>Sim. A equipe pode agendar uma apresentação presencial ou por videochamada, conforme disponibilidade.</p></details>
      <details><summary>Qual é o valor?</summary><p>O valor anunciado da Cobertura {u} é de {d['price']}. Consulte a equipe comercial para confirmar a disponibilidade e as condições vigentes.</p></details>
    </div>
    <div class="faq-cta">
      <p>Ainda ficou com alguma dúvida?</p>
      <a href="#agendar" class="btn btn--primary" data-goal="Falar com um consultor">Fale com um consultor</a>
    </div>
  </div>
</section>

<!-- Outra unidade -->
<section class="section section--tight">
  <div class="container">
    <a class="other-unit reveal" href="../cobertura-{o}/">
      <img src="../assets/img/{d['other_img']}" alt="" loading="lazy" width="720" height="405">
      <div><small>Conheça também</small><h3>Cobertura {o}</h3><p>{d['other_area']} m² privativos · 3 suítes · {d['other_price']}</p></div>
      <span class="btn btn--ghost">Ver cobertura {ARROW}</span>
    </a>
  </div>
</section>
{VIDEO}

{LOCATION}

<!-- 10. CTA FINAL + FORMULÁRIO -->
<section class="section section--dark" id="agendar">
  <div class="container contact">
    <div class="reveal">
      <p class="eyebrow">Apresentação privativa</p>
      <h2 class="h2">Uma cobertura para viver Ubatuba com mais <em>espaço, conforto e sofisticação</em></h2>
      <p class="lead" style="margin-top:20px">Conheça a planta, veja as imagens reais, entenda a implantação e descubra todos os detalhes da Cobertura {u}.</p>
    </div>
    <div class="form-embed reveal reveal-d1">
      <iframe data-respondi src="https://form.respondi.app/JDCmWvqf?embed=true" title="Formulário de contato do Ankor" loading="lazy" allow="clipboard-write"></iframe>
    </div>
  </div>
</section>
</main>

<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <a href="../" class="logo" aria-label="Ankor Exclusive Residence"><img src="../assets/brand/ankor-logo.png" alt="Ankor Exclusive Residence" width="310" height="58" loading="lazy"></a>
      <nav class="footer__links" aria-label="Rodapé">
        <a href="../">Site do Ankor</a>
        <a href="../cobertura-{o}/">Cobertura {o}</a>
        <a href="#" data-book hidden target="_blank" rel="noopener">Book do empreendimento</a>
        <a href="#agendar">Contato</a>
      </nav>
      <a class="footer__by" href="https://construtoraconvenio.com.br" target="_blank" rel="noopener"><img src="../assets/brand/convenio.svg" alt="" width="44" height="38" loading="lazy">Construtora Convênio</a>
    </div>
    <p class="footer__addr">Av. Leovigildo Dias Vieira, 1724 · Itaguá · Ubatuba — SP</p>
    <p class="footer__legal">Fotos reais da Cobertura {u}, entregue sem decoração. A planta humanizada é ilustrativa, com mobiliário sugerido que não faz parte da entrega. O esquema de implantação é ilustrativo e sem escala. Valor anunciado sujeito a confirmação de disponibilidade e condições vigentes. Empreendimento de uso exclusivamente residencial: não é permitida locação de temporada.</p>
  </div>
</footer>

<div class="mobile-bar" aria-label="Ações rápidas">
  <a href="#agendar" class="btn btn--peach" data-goal="Agendar apresentação privativa">Agendar apresentação</a>
  <a href="#" class="btn btn--primary" data-whatsapp="Olá! Tenho interesse na Cobertura {u} do Ankor." hidden>WhatsApp</a>
</div>

<script src="../assets/js/config.js?v={V}"></script>
<script src="../assets/js/data.js?v={V}"></script>
<script src="../assets/js/main.js?v={V}"></script>
</body>
</html>
'''


# Páginas de obrigado (destino do formulário depois do envio).
#   obrigado/          leads das coberturas: dispara a conversão do Google Ads e o Lead do Meta
#   obrigado-contato/  outros empreendimentos e corretores: sem conversão
THANKS = {
  'obrigado': dict(
    title='Obrigado · Ankor Exclusive Residence', eyebrow='Formulário recebido',
    h1='Obrigado pelo <em>seu interesse</em>.',
    text='Em breve um de nossos consultores entrará em contato para agendar a sua apresentação privativa da cobertura.',
    extra=CONVERSAO_ADS, pixel="fbq('track','Lead');",
    links=[('../', 'Voltar ao site do Ankor', 'btn--peach'), ('../#coberturas', 'Ver as coberturas', 'btn--ghost-light')]),
  'obrigado-contato': dict(
    title='Contato recebido · Ankor Exclusive Residence', eyebrow='Formulário recebido',
    h1='Agradecemos o <em>seu contato</em>.',
    text='Em breve a equipe da Construtora Convênio entrará em contato com você.',
    extra='', pixel='',
    links=[('../', 'Voltar ao site do Ankor', 'btn--peach'), ('https://construtoraconvenio.com.br', 'Conhecer a Construtora Convênio', 'btn--ghost-light')]),
}

def thanks_page(d):
    links = '\n        '.join(
        f'<a href="{href}" class="btn {cls}"{" target=\"_blank\" rel=\"noopener\"" if href.startswith("http") else ""}>{label}</a>'
        for href, label, cls in d['links'])
    return f'''<!doctype html>
<html lang="pt-BR" data-base="../">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{d['title']}</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#2e2f2a">
<link rel="icon" href="../assets/brand/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/style.css?v={V}">
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-N2VF7FVX');</script>
{GTAG}
{d['extra']}
<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','279593157240250');fbq('track','PageView');{d['pixel']}</script>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-N2VF7FVX" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

<header class="header">
  <div class="container header__inner">
    <a href="../" class="logo logo--lg" aria-label="Voltar ao site do Ankor"><img src="../assets/brand/ankor-logo.png" alt="Ankor Exclusive Residence" width="310" height="58"></a>
  </div>
</header>

<main class="lp-hero thanks">
  <div class="container lp-hero__content">
    <div class="lp-hero__grid">
      <div class="lp-hero__text">
        <p class="eyebrow">{d['eyebrow']}</p>
        <h1 class="h1">{d['h1']}</h1>
        <p class="lp-hero__sub">{d['text']}</p>
        <div class="thanks__actions">
        {links}
        </div>
      </div>
      <figure class="lp-hero__photo" style="--pos:50% 60%">
        <img src="../assets/img/hero/hero-1.webp" alt="Fachada do Ankor Exclusive Residence, no Itaguá, em Ubatuba" width="1184" height="864">
      </figure>
    </div>
  </div>
</main>

<footer class="footer footer--slim">
  <div class="container">
    <div class="footer__top">
      <a href="../" class="logo" aria-label="Ankor Exclusive Residence"><img src="../assets/brand/ankor-logo.png" alt="Ankor Exclusive Residence" width="310" height="58" loading="lazy"></a>
      <a class="footer__by" href="https://construtoraconvenio.com.br" target="_blank" rel="noopener"><img src="../assets/brand/convenio.svg" alt="" width="44" height="38" loading="lazy">Construtora Convênio</a>
    </div>
    <p class="footer__addr">Av. Leovigildo Dias Vieira, 1724 · Itaguá · Ubatuba — SP</p>
  </div>
</footer>
</body>
</html>
'''

for u, d in UNITS.items():
    os.makedirs(f'{ROOT}/cobertura-{u}', exist_ok=True)
    with open(f'{ROOT}/cobertura-{u}/index.html', 'w') as f:
        f.write(page(u, d))
for slug, d in THANKS.items():
    os.makedirs(f'{ROOT}/{slug}', exist_ok=True)
    with open(f'{ROOT}/{slug}/index.html', 'w') as f:
        f.write(thanks_page(d))
print('ok')
