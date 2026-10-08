#!/usr/bin/env python3
# Publica o site em construtoraconvenio.com.br/ankor/ por SFTP (a conta não tem shell, só SFTP).
# Uso (na pasta do site):  python3 _ferramentas/publicar.py            envia o que mudou
#                          python3 _ferramentas/publicar.py --simular  só mostra o que enviaria
#
# Gera as LPs e envia: sempre os arquivos de texto (html, css, js, .htaccess) e, das imagens,
# só as que faltam no servidor ou têm tamanho diferente. Só grava dentro de public_html/ankor
# e nunca apaga nada lá (a pasta tem outras coisas: Antigo, antigo2...).
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = 'public_html/ankor'
SERVIDOR = 'con30882@162.241.63.49'
CHAVE = os.path.expanduser('~/.ssh/ankor_hostgator')
# o mesmo conteúdo do empacotar.sh
ITENS = ['.htaccess', 'index.html', 'assets', 'cobertura-303', 'cobertura-304',
         'obrigado', 'obrigado-contato', 'tour-303', 'tour-304']
TEXTO = ('.html', '.css', '.js', '.htaccess', '.json', '.txt', '.xml', '.svg')


def sftp(comandos):
    r = subprocess.run(
        ['sftp', '-q', '-i', CHAVE, '-o', 'IdentitiesOnly=yes', '-o', 'BatchMode=yes', '-P', '22', SERVIDOR],
        input='\n'.join(comandos) + '\n', capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def locais():
    arquivos = []
    for item in ITENS:
        caminho = os.path.join(ROOT, item)
        if os.path.isfile(caminho):
            arquivos.append(item)
        for pasta, _, nomes in os.walk(caminho):
            for n in nomes:
                if n != '.DS_Store':
                    arquivos.append(os.path.relpath(os.path.join(pasta, n), ROOT))
    return sorted(arquivos)


def tamanhos_no_servidor(pastas):
    # sem shell não há listagem recursiva: lista pasta por pasta ('-' ignora pasta que ainda não existe)
    _, saida = sftp(['-ls -la %s/%s' % (DESTINO, p) if p else '-ls -la ' + DESTINO for p in pastas])
    tam = {}
    for linha in saida.splitlines():
        campos = linha.split(None, 8)
        if len(campos) == 9 and campos[0].startswith('-') and campos[8].startswith(DESTINO + '/'):
            tam[campos[8][len(DESTINO) + 1:]] = int(campos[4])
    return tam


def main():
    simular = '--simular' in sys.argv
    subprocess.run([sys.executable, os.path.join(ROOT, '_ferramentas', 'gerar_landing_pages.py')], check=True)

    arquivos = locais()
    pastas = sorted({os.path.dirname(a) for a in arquivos})
    no_servidor = tamanhos_no_servidor(pastas)
    if '.htaccess' not in no_servidor and 'index.html' not in no_servidor:
        sys.exit('Não consegui listar %s no servidor; nada foi enviado.' % DESTINO)

    enviar = [a for a in arquivos
              if a.endswith(TEXTO) or no_servidor.get(a) != os.path.getsize(os.path.join(ROOT, a))]
    print('%d arquivos no site, %d para enviar:' % (len(arquivos), len(enviar)))
    for a in enviar:
        print('  ' + a)
    if simular or not enviar:
        return

    comandos = []
    criadas = set()
    for a in enviar:
        partes = os.path.dirname(a).split('/') if os.path.dirname(a) else []
        for i in range(1, len(partes) + 1):
            p = '/'.join(partes[:i])
            if p not in criadas:
                criadas.add(p)
                comandos.append('-mkdir "%s/%s"' % (DESTINO, p))
        comandos.append('put "%s" "%s/%s"' % (os.path.join(ROOT, a), DESTINO, a))
    codigo, saida = sftp(comandos)
    # a saída repete cada comando ('sftp> put ...'); pasta que já existe faz o mkdir reclamar, e tudo bem
    erros = [l for l in saida.splitlines()
             if l.strip() and not l.startswith('sftp>') and 'mkdir' not in l.lower()]
    if codigo != 0 or erros:
        print('\n'.join(erros))
        sys.exit('O envio falhou (código %d). Confira acima.' % codigo)
    print('Publicado em https://construtoraconvenio.com.br/ankor/')
    print('Lembre do cache da HostGator: a versão antiga pode aparecer por algumas horas.')


if __name__ == '__main__':
    main()
