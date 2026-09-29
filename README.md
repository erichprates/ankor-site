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

**Publicar uma atualização da prévia** (GitHub Pages atualiza em cerca de 1 a 2 minutos):
```
git add -A && git commit -m "Descrição do ajuste" && git push
```

**Publicação definitiva:** envie o conteúdo da pasta para o servidor da Convênio, **sem** as
pastas `_originais/` e `_ferramentas/`. Todos os caminhos são relativos, então o site funciona
em qualquer pasta (por exemplo, `construtoraconvenio.com.br/ankor/`).

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

---

## 8. Piloto: Tour 360° Cobertura 303 (em aprovação com o cliente, 28/09/2026)

Pasta `tour-303/` (não linkada no site). Ambientes prontos: **Terraço**, **Living e jantar**, **Cozinha**.

**Como é feito (fluxo aprovado):**
1. Modelo 3D no Blender (`_ferramentas/tour303/cena_living.py`) seguindo a **planta humanizada**, com medidas do DWG
   (`17-268-REM-ITAUB_EST.18_R00_V21.dwg`): esquadrias 2,60 m de altura, porta living/terraço 3,60 m, cobertura ~3,9 m, pé-direito 2,80 m.
2. Paisagem 360° (`_originais/vista303/paisagem_360.png`) gerada por IA a partir das fotos reais do terraço,
   usada como "mundo" do 3D (centro da imagem = saída do living para o terraço: serra e cidade; esquerda = parque e morro).
   `vista_pano.py` posiciona as fotos por direção (guia para a IA). **Trocar por foto 360° real quando houver.**
3. Render equirretangular "sem acabamento" no Blender (~2 min por ambiente):
   `Blender -b -P cena_living.py -- --out render/vX --samples 48 --res 2688 --only terraco_360,living_360,cozinha_360`
4. Refinamento "IA única" na Higgsfield (GPT Image 2.5, 21:9, qualidade alta, ~2,75 créditos/ambiente),
   usando a versão refinada anterior como referência de estilo.
5. Exportar em WebP 4096×2048 para `tour-303/img/<ambiente>.webp`. Visualizador: Pannellum (CDN); no celular roda só na horizontal.

**Publicado para o cliente:** https://erichprates.github.io/ankor-site/tour-303/ (sem link no site, sem nota de "ilustrativo" a pedido).

**Recursos do visualizador:** começa no Terraço; pré-carrega todos os ambientes em segundo plano (troca ~0,3 s);
gira sozinho a 2°/s, para quando a pessoa toca/arrasta e volta após 8 s parado; no celular só na horizontal.

**Ajustes manuais:** `tour-303/img/terraco.webp` teve a "porta" do muro removida no Photoshop
(cópia em `_ferramentas/tour303/render/v4/terraco_final_photoshop.webp`). Ao refazer o terraço, **tirar o
painel de pedra do modelo** para não voltar.

**Pendências:** retorno do cliente; deck com jacuzzi, 3 suítes e banheiros; foto 360° real do terraço.
