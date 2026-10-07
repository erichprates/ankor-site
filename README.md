# Manual do site — Ankor Exclusive Residence

Site estático (HTML + CSS + JavaScript puro, sem frameworks) da Construtora Convênio para o
Ankor Exclusive Residence, no Itaguá, em Ubatuba. Ele foi refeito a partir do site antigo
(construtoraconvenio.com.br/ankor) seguindo os documentos de briefing:

- **Ajustes site Ankor.pdf**: reorganização da página principal
- **LP Ankor - Cobertura 303.pdf** e **LP Ankor - Cobertura 304.pdf**: landing pages de cada unidade

| | |
|---|---|
| **Prévia pública** | https://erichprates.github.io/ankor-site/ |
| Cobertura 303 | https://erichprates.github.io/ankor-site/cobertura-303/ |
| Cobertura 304 | https://erichprates.github.io/ankor-site/cobertura-304/ |
| Repositório | https://github.com/erichprates/ankor-site (público, exigência do GitHub Pages gratuito) |
| Pasta local | `~/Documents/Sites/Ankor` |
| Backup das fotos originais | https://github.com/erichprates/ankor-originais (**privado**). Restaurar: `git clone https://github.com/erichprates/ankor-originais.git _originais` |
| Status | **Enviado ao cliente para aprovação em 28/09/2026.** Aguardando considerações. |

---

## 1. Estrutura de arquivos

```
index.html                     Página principal
cobertura-303/index.html       Landing page da Cobertura 303  (GERADA por script, não editar à mão)
cobertura-304/index.html       Landing page da Cobertura 304  (GERADA por script, não editar à mão)
assets/css/style.css           Todos os estilos (compartilhados entre as 3 páginas)
assets/js/config.js            >>> CONFIGURAÇÃO: destino do formulário, WhatsApp, e-mail, book
assets/js/data.js              Catálogo das fotos (GERADO por script)
assets/js/main.js              Interações: hero, galeria, lightbox, vídeos, mapa, formulário
assets/img/                    Fotos otimizadas em WebP
  hero/                          topo da home (hero-1…5) e topo das LPs (lp-303, lp-304)
  empreendimento/ lazer/ localizacao/ coberturas/ vista/ plantas/ videos/
assets/brand/                  Logo Ankor (PNG) e logo Convênio (SVG)
_ferramentas/                  Scripts que geram imagens e landing pages (ver seção 4)
_originais/                    Fotos em tamanho original (~104 MB). Fora deste repositório; backup no repo privado ankor-originais
```

---

## 2. Página principal (index.html): ordem das seções

1. **Topo (hero)**: painel escuro à esquerda com título "Viva o *exclusivo* no Itaguá" e o botão
   "Conhecer as coberturas". À direita, 5 fotos que se alternam sozinhas (fachada, vista aérea
   com a baía, piscina com o evento, acesso com o totem, piscina com deck) e o selo
   "100% entregue" em cobre.
2. **O Ankor**: apresentação curta, conceitos (conforto, sofisticação, integração, lazer, Marina),
   números e 3 fotos. A foto grande é a fachada frontal com o totem "K".
3. **Coberturas 303 e 304**: selo pulsante "Últimas unidades · direto com a construtora",
   a palavra "disponíveis" pulsando de leve e dois cards (área, preço, atributos,
   mini-implantação e botão para a LP). Os cards falam em "vista para o mar e para as
   montanhas pelas laterais"; a palavra "posterior" não aparece na home (pedido de 29/09).
4. **Vídeo institucional**: capa grande (foto da fachada) com play (YouTube `Oy8C2-HSCjQ`).
5. **Diferenciais**: 5 blocos (Lazer completo, Convivência, Praticidade, Padrão construtivo,
   Exclusividade residencial).
6. **Faixa de chamada**: "Venha conhecer o Ankor pessoalmente", com agendamento e book.
7. **O Ankor por quem faz**: título à esquerda e 4 depoimentos em grade 2×2 (Sergio Matos,
   Marcos Campos, Reginaldo e Ana Lucia). As capas ficam salvas em `assets/img/videos/`.
8. **Galeria**: 8 fotos do empreendimento e o botão **"Ver mais imagens"**, que abre a galeria
   completa com as abas Empreendimento, Lazer e Localização (96 fotos). **Fotos e plantas das
   coberturas não aparecem na home**, só nas landing pages.
9. **Localização**: texto no topo, foto aérea grande da baía com o pin do Ankor, endereço,
   botão "Ver no mapa" (abre o Google Maps no endereço) e **distâncias das praias** Sul/Norte.
10. **Formulário "Agende uma apresentação privativa"**, com escolha de interesse.
11. Rodapé com endereço e avisos legais.

No celular, uma barra fixa na parte de baixo mostra "Coberturas" e "Agendar visita" (e
"WhatsApp", quando configurado).

## 3. Landing pages (Cobertura 303 e 304): ordem das seções

Textos conforme os PDFs das LPs.

1. **Topo**: texto à esquerda e foto real num box arredondado à direita (no celular a foto
   vem primeiro), com faixa de preço, atributos e botão "Agendar uma apresentação privativa"
   embaixo. O recorte da foto é ajustado por `hero_pos` e `hero_zoom` no dicionário `UNITS`.
   - 303: `_originais/hero-cobertura-303.png` (terraço com a pilastra branca e a baía)
   - 304: `_originais/hero-cobertura-304.png` (solarium com a baía e a serra)
2. **A cobertura**: texto e foto (303: living com acesso ao solarium; 304: living integrado à cozinha).
3. **Destaques da unidade**: 7 cards com ícone.
4. **Galeria de ambientes**: abas Todas / Living e cozinha / Vista para o mar / Solarium e área
   gourmet / Suítes e banheiros, mais **Vista para a serra** (só na 303). O botão "Ver todas
   as imagens" abre a galeria completa da unidade.
5. **Vista para o mar e implantação**: esquema ilustrativo (SVG) com a unidade destacada e a
   vista lateral para o mar, ao lado da foto real da vista.
6. **Planta humanizada** (clique para ampliar) e lista de ambientes.
7. **Diferenciais do Ankor**: 4 blocos (a restrição de locação vem com a ressalva do PDF).
8. **Perguntas frequentes**: 11 perguntas do PDF.
9. **Conheça também** a outra cobertura.
10. **Vídeo institucional**: copiado automaticamente da home.
11. **Localização**: copiada automaticamente da home (foto aérea e distâncias das praias).
12. **Formulário de agendamento** (sempre por último). Ele já vai marcado com a unidade da página.

Posição das unidades (tirada da miniatura das plantas): a frente do prédio fica à esquerda;
a **303** ocupa a metade posterior de cima e a **304** a metade posterior de baixo.

---

## 4. Como fazer alterações

### Textos e seções da home
Edite `index.html` direto. Se mexer nas seções **Vídeo institucional** ou **Localização**,
rode também o gerador das LPs (abaixo) para as landing pages receberem a mudança.

### Landing pages
**Não edite `cobertura-303/index.html` nem `cobertura-304/index.html`**: eles são gerados.
Edite `_ferramentas/gerar_landing_pages.py` (dicionário `UNITS` para dados de cada unidade,
função `page()` para a estrutura) e rode:
```
python3 _ferramentas/gerar_landing_pages.py
```

### Fotos
As fotos em tamanho original ficam em `_originais/`, que é um repositório Git próprio (backup privado).
Depois de adicionar ou trocar originais, atualize o backup: `cd _originais && git add -A && git commit -m "..." && git push`.
Para trocar ou adicionar:
1. coloque o arquivo em `_originais/` (para substituir, use o mesmo nome);
2. se for foto nova, adicione uma linha na lista `M` de `_ferramentas/gerar_imagens.py`
   (arquivo, slug, categoria, legenda, unidade);
3. rode:
   ```
   python3 -m pip install pillow        # só na primeira vez
   python3 _ferramentas/gerar_imagens.py
   ```
   O script gera os WebP e reescreve `assets/js/data.js`. Legendas e categorias ficam na lista `M`.

Padrões de qualidade usados:

| Tipo de foto | Configuração |
|---|---|
| Fotos do catálogo | até 1600px, qualidade 90; miniatura até 1000px, qualidade 86 |
| Topo da home | versões de 1200px e 2400px; o navegador escolhe conforme a tela |
| Topos das LPs e aérea da localização | tamanho original, qualidade 88 |

### Estilos
Cores e fontes ficam no topo de `assets/css/style.css` (`:root`). Os ajustes finais pedidos
pelo cliente estão no fim do arquivo, em "Ajustes de finalização".

| Cor | Valor | Uso |
|---|---|---|
| Painel escuro | `#2e2f2a` | seções escuras e fundos |
| Pêssego | `#ffe5d4` | cor do logo, textos claros |
| Cobre | `#ac6620` | botões e textos de destaque |
| Cobre claro | `#c9823b` | selo "100% entregue", "exclusivo" em itálico |
| Areia | `#f5ede7` | seções claras |

Fontes: **Cormorant Garamond** (títulos) e **Manrope** (textos e preços), via Google Fonts.

**Cache:** o CSS e os JS são chamados com `?v=AAAAMMDD…`. Ao mudar `style.css` ou um JS, troque
esse número em `index.html` e na constante `V` do `gerar_landing_pages.py` (e gere as páginas),
senão celulares podem continuar mostrando a versão antiga.

**Rastreamento (todas as páginas):** GTM `GTM-N2VF7FVX`, GA4 `G-858ZVEWJJ1` e Google Ads
`AW-10869641873` (as duas últimas direto, como no WordPress antigo) e Meta Pixel `279593157240250`.

**Páginas de obrigado** (geradas pelo `gerar_landing_pages.py`, dicionário `THANKS`, com `noindex`):
- `obrigado/`: leads das coberturas 303/304. Dispara a conversão do Google Ads e o `Lead` do Pixel.
- `obrigado-contato/`: outros empreendimentos e corretores. Sem conversão.
O formulário (embed do respondi.app, a configurar) deve redirecionar para uma ou outra.

---

## 5. Ver localmente e publicar

**Ver no computador:**
```
cd ~/Documents/Sites/Ankor && python3 -m http.server 8765
```
Abra http://localhost:8765 (use Cmd+Shift+R para limpar o cache depois de mudanças).

**Site no ar:** https://construtoraconvenio.com.br/ankor/ (HostGator, pasta `public_html/ankor`,
desde 29/09/2026). O WordPress antigo do /ankor foi renomeado para `public_html/ankor_antigo`.
O GitHub Pages publica só o **tour 360°** (ramo `gh-pages`, que tem apenas `tour-303/`, a planta,
o logo e o favicon): https://erichprates.github.io/ankor-site/tour-303/ . A raiz da prévia
redireciona para o site oficial. Para atualizar o tour lá, copie os arquivos para o ramo `gh-pages`
(por exemplo com `git worktree add ../ghp gh-pages`), faça commit e push. O ramo `main` é o histórico do site.

**Publicar uma atualização:**
1. `sh _ferramentas/empacotar.sh` (gera as LPs e cria `_deploy/ankor.zip`, sem tour, ferramentas e originais).
2. No cPanel, Gerenciador de Arquivos, `public_html/ankor`: envie o zip, extraia sobrescrevendo e apague o zip.
3. Limpe o cache da HostGator (o servidor guarda páginas: cabeçalho `x-nginx-cache: WordPress`),
   senão a versão antiga pode continuar aparecendo por algumas horas.
4. `git add -A && git commit -m "..." && git push` para guardar o histórico.

O `.htaccess` redireciona os endereços do WordPress antigo (cobertura303, cobertura304,
obrigadocorretor, outroimovel, corretores) e manda endereços inexistentes para a home.

---

## 6. Pendências antes de ir ao ar

- [ ] **Formulário**: preencher `formEndpoint` (CRM, RD Station, webhook) e/ou `whatsapp`
      (ex.: `5512999999999`) em `assets/js/config.js`. Hoje o formulário mostra "envio ainda
      não configurado". Campos enviados: nome, email, whatsapp, cidade, interesse, objetivo,
      origem, formato, mensagem, consentimento, pagina.
- [ ] **Considerações do cliente** sobre a prévia (enviada em 28/09/2026).
- [ ] **Confirmar com o comercial**: armário náutico de cada unidade e a posição 303/304 no
      esquema de implantação.
- [ ] **Legendas de "vista a partir da varanda" da 304** (`304-vista-varanda`, `-2`): confirmar
      se também são da varanda de suíte.
- [ ] **Fotos em resolução maior** (opcional): as áreas comuns vieram do site antigo com 800px,
      as fotos das coberturas passaram pelo WhatsApp (1280px) e a fachada, a aérea e os topos das
      LPs têm cerca de 1200–1340px. Com os originais do fotógrafo, basta trocar em `_originais/`
      e rodar o script.
- [ ] **Rastreamento**: GTM `GTM-N2VF7FVX` e Meta Pixel `279593157240250` (os mesmos do site
      antigo) estão ativos, inclusive na prévia. Eventos enviados ao dataLayer: `lead_submit`,
      `gallery_open`, `video_play`.

---

## 7. Histórico de ajustes pedidos (28/09/2026)

- Selo "100% entregue" 30% maior, com fundo cobre.
- Logo 30% maior na home e nas landing pages.
- Selo "Últimas unidades" em destaque, com "disponíveis" pulsando.
- Aviso de posição das coberturas movido para baixo dos cards.
- Textos de Lazer ("refúgio de bem-estar…") e Praticidade (sem fibra óptica) reescritos.
- Vídeos: o tour saiu, o institucional virou seção grande abaixo das coberturas e os
  4 depoimentos ficaram em grade 2×2 com capas em HD, sem tarja preta.
- Localização com foto aérea nova e distâncias das praias (as praias do Norte em ordem crescente).
- Fotos e nomes dos consultores removidos.
- Topo da home com 5 fotos novas (pasta "fotos header").
- Foto da fachada frontal na seção "O Ankor".
- Galeria da home sem fotos e plantas das coberturas.
- Topos novos nas LPs 303 e 304; na 304, a foto da seção "A cobertura" virou o living com cozinha.
- 303: duas fotos passaram de "Vista para o mar" para a nova aba "Vista para a serra".
- 304: legenda "Vista a partir da suíte" na última foto de vista para o mar.
- LPs: localização igual à da home; vídeo institucional antes dela; formulário por último.
- Endereço: Av. Leovigildo Dias Vieira, 1724, Itaguá, Ubatuba, SP.

### Ajustes de 29/09/2026

- Menos ênfase em "posterior": seção de vista das LPs com o texto "Uma perspectiva singular
  de Ubatuba", sem a legenda repetida sob a foto; home sem a nota abaixo dos cards e com os
  cards falando só da vista. O FAQ das LPs mantém a explicação (decisão do cliente).
- Espaçamento entre seções menor no celular.
- Topo das LPs em duas colunas (texto + foto em box), para mostrar mar e montanhas em vez de céu.
- Preços em Manrope (números retos), no lugar da Cormorant.
- Site publicado em construtoraconvenio.com.br/ankor (HostGator), no lugar do WordPress do /ankor
  (guardado em `public_html/ankor_antigo`). GitHub Pages ficou só com o tour 360°.
- Formulário: embed do respondi.app (JDCmWvqf) na home e nas LPs, com as UTMs repassadas.
  Ele redireciona para `obrigado/` (coberturas, conversão do Ads + Lead do Pixel) ou
  `obrigado-contato/` (outros empreendimentos e corretores).
- Contato: texto ocupa a altura do formulário, com três pontos de atendimento embaixo
  (no celular os pontos vão depois do formulário).
- GA4 `G-858ZVEWJJ1` e Google Ads `AW-10869641873` em todas as páginas, como no WordPress antigo.
- Home: descrição de compartilhamento e subtítulo do topo sem destaque para a Marina
  ("na melhor localização do Itaguá").
- Fotos profissionais das coberturas (Confector, 03/2026; originais em `_originais/confector/`)
  no lugar das fotos de celular dos mesmos ambientes. Ficaram as antigas que mostram a vista.
- 303: topo com a varanda gourmet (foto profissional); seção "A cobertura" com a vista do solarium.
- 304: topo com a vista lateral para o mar; seção "A cobertura" com solarium e varanda gourmet;
  seção de vista com a vista a partir do solarium.
- Cache da HostGator: o `.htaccess` impede o proxy de guardar o HTML (cabeçalho `X-Accel-Expires: 0`).

### Tour 360° — sessão de 07/10/2026

- **Vista real** das coberturas como paisagem do 3D (panorâmica do terraço, versão ampla; no deck, a versão que pega o mar).
- **DWG do projeto** guardado em `_originais/projeto/` e conferido (medidas na seção 8).
- **Ambientes novos na 303:** deck e jacuzzi, suíte master, suítes 2 e 3 e os três WCs (10 pontos no total).
- **Banhos com os revestimentos reais** (fotos em `_originais/referencias/`); cubas ocas, misturador e chuveiro de parede.
- **Terraço:** ducha externa com revestimento no muro cinza, guarda-corpo contínuo por toda a fachada e na quina,
  pingadeira sobre as muretas, floreira terminando antes da ducha, água na jacuzzi.
- **Decoração:** master sem bancada, com painel ripado, pendentes e quadros; suítes 2 e 3 com ripado, quadro grande e aparador.
- **Página do tour refeita:** abre no living virado para o terraço; barra de ambientes no rodapé (com setas quando não cabe
  e botão de esconder); planta humanizada recortada num cartão ao lado da barra; "WC" no lugar de "Banho"; botões de
  navegação em pílula, centralizados na porta; zoom e tela cheia em vidro escuro; carregamento sem caixa.

**Próximo passo:** receber as vistas reais da 304 e dos quartos, refinar os ambientes das duas coberturas na Higgsfield
e publicar no GitHub Pages (seção 8).

---

## 8. Tour 360° das Coberturas 303 e 304 (em construção; piloto da 303 com 3 ambientes publicado em 28/09/2026)

Pasta `tour-303/` (não linkada no site). **No GitHub Pages** continuam os 3 ambientes refinados do piloto (Terraço, Living
e jantar, Cozinha). **No ramo `main`**, desde 07/10/2026, `tour-303/` tem a página nova e os 10 ambientes em **render cru do
Blender** (sem refinamento por IA): Living e jantar, Cozinha, Terraço, Deck e jacuzzi, Suíte master, Suíte 2, Suíte 3 e os
três WCs. As imagens refinadas antigas estão no histórico do Git e no ramo `gh-pages`. **Não publicar o `main` no Pages
antes do refinamento.**

**Para ver localmente:** `python3 -m http.server 8765` na pasta do site e abrir `http://127.0.0.1:8765/tour-303/`.
Ao trocar uma imagem, mudar o `?v=` na função `src()` da página, senão o navegador mostra a antiga.

**Tour da 304 (`tour-304/`, criado em 07/10/2026):** é o modelo da 303 **espelhado** (`--apto 304` no `cena_living.py`;
o espelho é aplicado no fim, as câmeras só têm a posição espelhada). Render:
`Blender -b -P cena_living.py -- --apto 304 --out render/304 --samples 48 --res 2688 --only <ambientes>`.
Cores pela planta humanizada da 304: master azul, suíte 2 areia, suíte 3 verde, sofá claro, poltronas verdes,
espreguiçadeiras claras. A página é cópia da 303 com os `yaw` de sinal trocado e os pontos na planta da 304.
Decoração própria ("litoral natural", referências em `_originais/referencias/decoracao304/`): linho e areia, madeira clara,
pedra clara na parede da TV, pares de marinhas, azul-claro/areia/sálvia nas camas; banhos em porcelanato marmorizado claro
(fotos `assets/img/coberturas/304-banho*.webp`), com azulejos como na 303 por decisão do cliente (as fotos da 304 mostram
dois banhos azuis e um verde). Terraço próprio da 304 pela planta: deck começa em x = 12,5 e é mais largo na fachada
(17,1 → 15,9 m, medido pela imagem), lareira com 4 poltronas escuras e sofá, 2 chaises no fundo, jacuzzi no canto da fachada.
**Decisão do cliente (07/10/2026):** forro de madeira do living e piso de madeira das suítes ficam como decoração nas duas
coberturas, embora nas fotos reais o forro seja branco e o piso das suítes seja porcelanato cinza.
**Vistas reais (07/10/2026):** `_originais/vista304/vista-304.png` (terraço), `vista2-304.png` (deck) e `janelas-304.png`
(janelas dos quartos); na 303, `vista303/janelas-303.png`. Entradas `304`, `304_deck`, `304_quartos` e `303_quartos` no
`vista_real.py` (rodar as três da 304 nessa ordem). A foto das janelas é reta e só entra na faixa da paisagem; quartos e
WC master usam `paisagem_360_real_quartos.png`, e na 304 também living e cozinha (objetos próximos, como a casa amarela,
mudam de direção entre a fachada dos quartos e o terraço; a calibração está comentada no script).
**Pendente na 304:** (1) cliente conferir a direção das vistas; (2) oliveira nas suítes 2 e 3 (sem espaço) e demais móveis das referências ficam para o refinamento;
(3) conferir a 304 no DWG; (4) conferir no navegador os pontos da planta e os botões entre ambientes.

**Regras aprendidas (valem para a 304):**
- Ponto do tour a menos de ~1,8 m de um guarda-corpo de vidro enxerga, pelo vidro, abaixo de onde a foto da vista termina
  (~35° abaixo do horizonte) e aparece uma faixa embaçada. Afastar o ponto ou pedir foto com mais área para baixo.
- A câmera não pode ficar na linha de uma parede: a porta que está nela some (aconteceu com o WC da master).
- Peças com faces coincidentes saem pretas no render (cuba, piso duplicado). Não sobrepor caixas no mesmo plano.
- Topo branco de mureta reflete o céu e parece fresta azul: usar pingadeira. Muretas descem até a laje.
- Hotspots do Pannellum ancoram pelo canto: o elemento tem tamanho zero e o conteúdo se centraliza com `translate(-50%,-50%)`.
- Direção dos botões: `yaw = atan2(-dy, -dx)` em coordenadas de planta da 303 (na 304, espelhada, o yaw troca de sinal).
- Não encadear renders com `pgrep` esperando outro Blender: duas filas ficaram esperando uma pela outra. Rodar um comando só.

**Fontes do projeto (em `_originais/`, fora do repositório do site):**
- `projeto/17-268-REM-ITAUB_EST.18_R00_V21.dwg`: projeto arquitetônico (todos os pavimentos; a cobertura é a planta
  mais à direita do desenho, a 303 é o apartamento de cima à esquerda). Para ler as cotas:
  `dwg2dxf -y -o planta.dxf <arquivo.dwg>` (LibreDWG, `brew install libredwg`) e abrir o DXF com `ezdxf` em Python.
- `planta303.png`: planta humanizada (material de venda). **É ela que define o layout e o mobiliário do tour.**
- `vista303/vista_303_real_ampla.webp`: panorâmica real tratada, tirada do terraço da 303, com área para baixo até ~37° do
  horizonte (07/10/2026). **É a base da paisagem de todos os ambientes.** Na mesma pasta ficam as versões anteriores
  (`vista_303_real.webp`, `vista_303_real_ext.png`) e a foto original nublada (`vista_303_original_nublada.jpg`).
- `referencias/303-banho-master.webp` e `303-banho-suites.webp`: fotos dos banhos como entregues. **Os revestimentos do tour
  têm de ser estes** (pedido do cliente): porcelanato cinza-claro em placas grandes no piso e nas paredes, fundo do box em
  azulejo quadrado brilhante (azul-marinho na master, verde-acinzentado nas suítes 2 e 3), bancada e moldura do nicho em
  granito claro, cuba retangular branca de semi-encaixe. A decoração entra por cima dessa base; no refinamento por IA,
  mandar a foto como referência e pedir para não trocar os revestimentos.
- `referencias/303-terraco-ducha-corredor.webp`: terraço como entregue. Mostra o **revestimento da ducha externa** no muro
  de divisa (obrigatório no tour; o muro é cinza), o forro de madeira do corredor da varanda com plafons pretos e a mureta com vidro.
- `vista303/vista_303_deck.jpg`: panorâmica mais aberta (pega o mar à esquerda) e com mais área para baixo (até ~34° abaixo
  do horizonte), usada **só no deck**. Substituiu `vista_303_aberta.png`, que ia só até ~21°.

**O que foi conferido no DWG:** living 4,85 m de fachada; suítes 2,70 / 2,75 / 2,70 m; esquadrias de 2,60 m de altura
em toda a largura das suítes (2,80 + 1,35 fixo no living, porta living/terraço 3,60 m); portas internas 0,80 e 0,70 x 2,10 m;
varanda da frente contínua por toda a fachada (da suíte 1 ao terraço), com ~1,26 m livres; projeção da cobertura gourmet ~3,9 m;
pé-direito 2,80 m. **Diferenças conhecidas:** no DWG o terraço é reto e mais comprido (~11,9 m) e os banhos das suítes têm
outra posição; o tour segue a planta humanizada (borda inclinada do deck, banhos ao fundo). Alturas de mureta (0,35 m) e
do vidro do guarda-corpo (até 1,25 m) **não estão na planta**: são estimativas pelas fotos.

**Como é feito (fluxo aprovado):**
1. Modelo 3D no Blender: `_ferramentas/tour303/cena_living.py` (living, cozinha, terraço, deck) + `cena_suites.py`
   (suítes e banhos; é executado pelo primeiro). Coordenadas em metros, origem no canto interno do living junto à suíte 3.
2. Paisagem 360° **real**: `python vista_real.py 303` projeta a panorâmica do terraço (cilíndrica, ~190° de largura,
   centro apontando 52° à esquerda da saída living→terraço) em `_originais/vista303/paisagem_360_real.png`, usada como
   "mundo" do 3D. O céu é continuado até o zênite; o que a foto não cobre (atrás do prédio) é espelho da própria foto.
   Para o deck: `python vista_real.py 303_deck` junta a vista mais aberta (à esquerda) com a do terraço (à direita) em
   `paisagem_360_real_deck.png`; o `deck_360` usa esse mundo (campo `mundo` em `SHOTS`) e fica na borda da frente, ao lado
   da jacuzzi, único ponto do deck de onde o prédio não esconde o lado do mar.
   A paisagem antiga gerada por IA (`paisagem_360.png`, via `vista_pano.py`) só é usada se a real não existir.
3. Render equirretangular "sem acabamento" (~1,5 min por ambiente):
   `Blender -b -P cena_living.py -- --out render/vX --samples 48 --res 2688 --only terraco_360,living_360,cozinha_360,deck_360,suite1_360,suite2_360,suite3_360,banho1_360,banho2_360,banho3_360`
4. Refinamento "IA única" na Higgsfield (GPT Image 2.5, 21:9, qualidade alta, ~2,75 créditos/ambiente),
   usando a versão refinada anterior como referência de estilo. **A IA redesenha a paisagem**: depois do refinamento,
   recolocar a vista real nas áreas de céu/paisagem (máscara tirada do próprio Blender).
5. Exportar em WebP 4096×2048 para `tour-303/img/<ambiente>.webp` e incluir o ambiente em `ROOMS` no `tour-303/index.html`.
   Visualizador: Pannellum (CDN); no celular roda só na horizontal.

**Publicado para o cliente:** https://erichprates.github.io/ankor-site/tour-303/ (sem link no site, sem nota de "ilustrativo" a pedido).
Ainda com a paisagem antiga de IA e só 3 ambientes; os renders novos estão em `_ferramentas/tour303/render/v5/` (fora do Git).

**Recursos do visualizador:** começa no Terraço; pré-carrega todos os ambientes em segundo plano (troca ~0,3 s);
gira sozinho a 2°/s, para quando a pessoa toca/arrasta e volta após 8 s parado; no celular só na horizontal.

**Ajustes no modelo em 07/10/2026:** vista real como mundo; o painel de pedra do muro do terraço é a **ducha externa**: voltou ao modelo com braço, ducha e
registros (sem eles o refinamento o transformava em "porta"); muro de divisa cinza; plafons pretos no corredor da varanda;
suíte master sem bancada, com painel ripado, pendentes e painel de TV em madeira escura; banhos com cuba oca e misturador; guarda-corpo, piso e forro da varanda estendidos por toda a fachada; muretas descem até a laje e ganharam
pingadeira de pedra clara (o topo branco refletia o céu e parecia uma fresta azul); vidro embutido na mureta.

**Pendências:** refinar na Higgsfield os 10 ambientes (conectar a conta nova em `/mcp`) e recolocar a vista real;
conferir no deck, pelo vidro do guarda-corpo, se ainda aparece a faixa lisa onde as fotos acabam (~34 a 37° abaixo do horizonte); vistas reais dos quartos (o usuário vai enviar);
vista real da 304 (`ap-304.jpg`) e tour da 304; lavabo e corredor não modelados; retorno do cliente.
