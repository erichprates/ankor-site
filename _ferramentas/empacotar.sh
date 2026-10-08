#!/bin/sh
# Gera _deploy/ankor.zip só com o que vai para construtoraconvenio.com.br/ankor/
# Uso (na pasta do site):  sh _ferramentas/empacotar.sh
set -e
cd "$(dirname "$0")/.."
python3 _ferramentas/gerar_landing_pages.py
mkdir -p _deploy
rm -f _deploy/ankor.zip
zip -rq _deploy/ankor.zip .htaccess index.html assets cobertura-303 cobertura-304 obrigado obrigado-contato tour-303 tour-304 -x '*.DS_Store'
ls -lh _deploy/ankor.zip
