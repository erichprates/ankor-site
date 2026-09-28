# Ankor Exclusive Residence — novo site

Site estático (HTML + CSS + JS, sem dependências) refeito a partir dos PDFs
"Ajustes site Ankor", "LP Ankor - Cobertura 303" e "LP Ankor - Cobertura 304".

```
index.html               Página principal (ordem recomendada no PDF)
cobertura-303/index.html Landing page da Cobertura 303
cobertura-304/index.html Landing page da Cobertura 304
assets/css/style.css     Estilos compartilhados
assets/js/config.js      >>> CONFIGURAR: destino do formulário, WhatsApp, e-mail
assets/js/data.js        Catálogo das 143 fotos (categoria, legenda, unidade)
assets/js/main.js        Galeria, lightbox, carrossel, vídeos, formulário
assets/img/              Fotos otimizadas em WebP (tamanho cheio + miniatura)
assets/brand/            Logo Ankor, logo Convênio, fotos dos consultores
_originais/              Fotos baixadas do site atual (fonte; não precisa subir)
```

## Antes de publicar

1. **Formulário**: em `assets/js/config.js`, preencha `formEndpoint` (CRM, RD Station,
   Formspree, webhook) e/ou `whatsapp` (ex.: `5512999999999`). Sem isso o formulário
   avisa que o envio não está configurado. Os campos enviados são: nome, email,
   whatsapp, cidade, interesse, objetivo, origem, formato, mensagem, consentimento, pagina.
2. **Fotos em alta**: as fotos do site atual têm no máximo 800–1600 px. Se houver os
   arquivos originais do fotógrafo, substitua mantendo o mesmo nome em `assets/img/`.
3. **Confirmar com o comercial**: armário náutico em cada unidade, pontos do mapa
   ("a poucos minutos"), posição 303/304 no esquema de implantação (baseado na
   miniatura das plantas) e a localização exata do pin no Google Maps.
4. Rastreamento: GTM `GTM-N2VF7FVX` e Meta Pixel `279593157240250` (os mesmos do site
   atual). Eventos no dataLayer: `lead_submit`, `gallery_open`, `video_play`.

## Ver localmente

```
cd ~/Documents/Sites/Ankor && python3 -m http.server 8765
```
Abra http://localhost:8765
