# Suítes e banheiros da Cobertura 303 — executado por cena_living.py (usa box, cyl, wall_x, M etc. de lá).
#
# Layout pela planta humanizada (planta303.png); larguras e esquadrias conferidas no DWG
# (_originais/projeto/17-268-REM-ITAUB_EST.18_R00_V21.dwg): suítes 2,70 / 2,75 / 2,70 m de largura,
# esquadria de 2,60 m de altura em toda a largura de cada suíte, portas 0,80 e 0,70 x 2,10 m.
# Coordenadas como no arquivo principal: x negativo = à esquerda do living, y = 0 na fachada.

M['vinilico'] = node_mat('piso_vinilico', wood_build('#b08a62', '#8f6b47', scale=(1, 9, 1), gloss=0.3))
# Revestimentos REAIS dos banhos (fotos em _originais/referencias/303-banho-*.webp): porcelanato cinza-claro
# em placas grandes no piso e nas paredes, parede do fundo do box em azulejo quadrado brilhante
# (azul-marinho no banho da master, verde-acinzentado nos outros), bancada e moldura do nicho em granito claro.
def placa(nome, c1, c2, rejunte, larg, alt, eixo='xy', rough=0.45, junta=0.004, ondas=0.0):
    def build(nt, b):
        sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tex_coord(nt), sep.inputs[0])
        cmb = nt.nodes.new('ShaderNodeCombineXYZ')
        nt.links.new(sep.outputs['XYZ'.index(eixo[0].upper())], cmb.inputs[0])
        nt.links.new(sep.outputs['XYZ'.index(eixo[1].upper())], cmb.inputs[1])
        br = nt.nodes.new('ShaderNodeTexBrick'); br.offset = 0.0
        br.inputs['Scale'].default_value = 1.0
        br.inputs['Brick Width'].default_value = larg; br.inputs['Row Height'].default_value = alt
        br.inputs['Mortar Size'].default_value = junta
        br.inputs['Color1'].default_value = (*srgb(c1), 1); br.inputs['Color2'].default_value = (*srgb(c2), 1)
        br.inputs['Mortar'].default_value = (*srgb(rejunte), 1)
        nt.links.new(cmb.outputs[0], br.inputs['Vector'])
        nt.links.new(br.outputs['Color'], b.inputs['Base Color'])
        b.inputs['Roughness'].default_value = rough
        bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.25
        nt.links.new(br.outputs['Fac'], bump.inputs['Height'])
        if ondas:                                       # esmalte irregular do azulejo artesanal
            nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 9
            nt.links.new(tex_coord(nt), nz.inputs['Vector'])
            b2 = nt.nodes.new('ShaderNodeBump'); b2.inputs['Strength'].default_value = ondas; b2.inputs['Distance'].default_value = 0.02
            nt.links.new(nz.outputs['Fac'], b2.inputs['Height']); nt.links.new(bump.outputs['Normal'], b2.inputs['Normal'])
            bump = b2
            b.inputs['Coat Weight'].default_value = 0.6
        nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return node_mat(nome, build)
PORC = ('#cdc9c1', '#c8c4bc', '#b3afa7')
if APTO == '304':      # 304 (fotos assets/img/coberturas/304-banho*.webp): porcelanato marmorizado claro, com veios bege
    PORC = ('#e6e1d8', '#e1dbd0', '#cfc8bb')
M['banho_piso'] = placa('porcelanato_banho_piso', *PORC, 0.9, 0.9, 'xy')
M['banho_par_xz'] = placa('porcelanato_banho_parede_xz', *PORC, 1.2, 1.2, 'xz')
M['banho_par_yz'] = placa('porcelanato_banho_parede_yz', *PORC, 1.2, 1.2, 'yz')
M['azulejo_azul'] = placa('azulejo_azul_marinho', '#1d3c68', '#27497a', '#c9d0d6', 0.13, 0.13, 'xz', rough=0.07, junta=0.003, ondas=0.5)
M['azulejo_verde'] = placa('azulejo_verde_acinzentado', '#a3b3a8', '#99aa9f', '#c2c7c0', 0.13, 0.13, 'xz', rough=0.07, junta=0.003, ondas=0.5)
def _granito(nt, b):
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 220; nz.inputs['Detail'].default_value = 3
    nt.links.new(tex_coord(nt), nz.inputs['Vector'])
    rp = nt.nodes.new('ShaderNodeValToRGB')
    rp.color_ramp.elements[0].position = 0.35; rp.color_ramp.elements[0].color = (*srgb('#9d9a97'), 1)
    rp.color_ramp.elements[1].position = 0.6; rp.color_ramp.elements[1].color = (*srgb('#d6d3cf'), 1)
    nt.links.new(nz.outputs['Fac'], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.25
M['granito'] = node_mat('granito_claro', _granito)
M['louca'] = mat('louca', srgb('#f4f3f0'), 0.12, **{'Coat Weight': 0.6})
M['espelho'] = mat('espelho', (0.9, 0.9, 0.9), 0.02, 1.0)
M['roupa_cama'] = node_mat('roupa_cama', velvet('#ebe6dc'))
M['cabeceira'] = node_mat('cabeceira', velvet('#b9ad9b'))
M['tapete'] = node_mat('tapete_suite', velvet('#d8d4cc'))
M['parede_areia'] = mat('parede_areia', srgb('#d9c8b0'), 0.9)
M['abajur'] = mat('abajur', (1, 1, 1), 0.5, **{'Emission Color': (1.0, 0.8, 0.58, 1), 'Emission Strength': 4.0})
M['led_branco'] = mat('led_suite', (1, 1, 1), 0.5, **{'Emission Color': (1.0, 0.82, 0.62, 1), 'Emission Strength': 8.0})

# cores por cobertura, conforme as plantas humanizadas (manta da cama e paleta do quadro de cada suíte)
TELA_AZUL = ('#e9dfcf', '#c9a27a', '#8a5a3c', '#1b2a44'); TELA_VERDE = ('#ece4d6', '#b9c2a8', '#5f7d6e', '#2e5d57')
TELA_AREIA = ('#efe7da', '#cdb89a', '#9a7b5a', '#3a2f28')
TELA_MAR = ('#ece7dc', '#cfd9dc', '#8fb3c6', '#3f6f8f'); TELA_PRAIA = ('#efe9dd', '#dccdb4', '#a9c0c9', '#6f93a8')
if APTO == '304':      # 304 (referências de decoração): roupa de cama em linho, com azul-claro, areia e verde-sálvia
    M['azul_claro'] = node_mat('linho_azul_claro', velvet('#a9c6d6')); M['salvia'] = node_mat('linho_salvia', velvet('#a8b5a0'))
    COR_S1, COR_S2, COR_S3 = M['azul_claro'], M['linen'], M['salvia']; TELA_S2, TELA_S3 = TELA_PRAIA, TELA_MAR
    TELA_AREIA = TELA_MAR
else:                  # 303: master em tons de areia, suíte 2 verde, suíte 3 azul
    COR_S1, COR_S2, COR_S3 = M['linen'], M['ceramic'], M['navy']; TELA_S2, TELA_S3 = TELA_VERDE, TELA_AZUL

BATH_Y0, BATH_Y1 = 3.85, 6.13      # banho: 1,30 m de largura; fundo alinhado à parede do hall
DOOR = 2.10                        # portas internas 2,10 m (DWG)
Z0 = 0.004                         # piso das suítes um fio acima do contrapiso do living

def luz(x, y, z=H - 0.06, w=30, cor=(1.0, 0.82, 0.62)):
    bpy.ops.object.light_add(type='POINT', location=(x, -y, z))
    l = bpy.context.active_object; l.data.energy = w; l.data.color = cor; l.data.shadow_soft_size = 0.05

def spot_forro(x, y, w=11):
    cyl('spot_suite', x, y, H - 0.032, H - 0.03, 0.04, M['led_branco'])
    luz(x, y, H - 0.1, w)

def cama(xc, yc, lado, manta, larg=1.6, comp=2.0, pendente=False):
    """Cama de casal com a cabeceira na parede do lado `lado` (+1 = parede da direita/x maior)."""
    xh = xc + lado * comp / 2                       # x da cabeceira
    xa, xb = sorted((xh, xh - lado * comp))
    if APTO == '303':
        box('cama_base', xa + 0.03, xb - 0.03, yc - larg / 2, yc + larg / 2, 0.08, 0.3, M['wood'])
    else:      # 304: cama em plataforma baixa de madeira clara, mais larga que o colchão (referência)
        box('cama_plataforma', xa - 0.22 if lado > 0 else xa, xb if lado > 0 else xb + 0.22, yc - larg / 2 - 0.2, yc + larg / 2 + 0.2, 0.06, 0.3, M['wood'])
    box('colchao', xa, xb, yc - larg / 2 + 0.02, yc + larg / 2 - 0.02, 0.3, 0.55, M['roupa_cama'], bevel=0.05)
    ma, mb = sorted((xh - lado * 0.85, xh - lado * (comp + 0.02)))
    box('manta', ma, mb, yc - larg / 2 - 0.01, yc + larg / 2 + 0.01, 0.36, 0.575, manta, bevel=0.04)
    for dy in (-0.4, 0.4):
        pa, pb = sorted((xh - lado * 0.12, xh - lado * 0.55))
        box('travesseiro', pa, pb, yc + dy - 0.33, yc + dy + 0.33, 0.55, 0.69, M['roupa_cama'], bevel=0.06)
    ca, cb = sorted((xh - lado * 0.08, xh))
    box('cabeceira', ca, cb, yc - larg / 2 - 0.6, yc + larg / 2 + 0.6, 0.0, 1.25, M['cabeceira'], bevel=0.02)
    for s in (-1, 1):                                # criados-mudos com abajur
        yn = yc + s * (larg / 2 + 0.33)
        na, nb = sorted((xh - lado * 0.08, xh - lado * 0.5))
        box('criado', na, nb, yn - 0.25, yn + 0.25, 0.12, 0.48, M['wood'], bevel=0.005)
        xl = xh - lado * 0.29
        if pendente:                                 # pendente em vez de abajur (suíte master)
            cyl('pendente_fio', xl, yn, 1.25, H - 0.03, 0.003, M['black'])
            cyl('pendente_cupula', xl, yn, 1.05, 1.25, 0.07, M['brass'])
            cyl('pendente_luz', xl, yn, 1.04, 1.05, 0.06, M['abajur'])
            luz(xl, yn, 0.98, 2.5)
        else:
            cyl('abajur_pe', xl, yn, 0.48, 0.66, 0.012, M['brass'])
            cyl('abajur_cupula', xl, yn, 0.66, 0.86, 0.1, M['abajur'])
            luz(xl, yn, 0.95, 2.5)
    box('tapete', min(xa, xb) - 0.05 + (0.0 if lado > 0 else 0.5), max(xa, xb) + 0.05 - (0.5 if lado > 0 else 0.0),
        yc - larg / 2 - 0.55, yc + larg / 2 + 0.55, Z0, Z0 + 0.012, M['tapete'])

def armario(x0, x1, y0, y1):
    box('armario', x0, x1, y0, y1, 0.0, 2.55, M['plaster_white'])
    box('armario_rodateto', x0, x1, y0, y1, 2.55, H, M['plaster_white'])
    n = max(2, int(round(abs(y1 - y0) / 0.5)))
    xf = x1 if x1 > x0 else x0
    for i in range(1, n):                            # frisos das portas
        yy = y0 + (y1 - y0) * i / n
        box('friso', xf, xf + 0.004, yy - 0.003, yy + 0.003, 0.05, 2.5, M['black'])
    return xf

def banho(x0, x1, pia_lado, porta, azulejo):
    """Banho entre x0 e x1 (1,30 m). pia_lado: +1 = bancada e vaso na parede x1. porta: 'lado' ou 'topo'."""
    xo = x0 if pia_lado > 0 else x1                  # parede oposta à da bancada (onde fica a porta lateral)
    xp = x1 if pia_lado > 0 else x0                  # parede da bancada
    s = -pia_lado                                    # direção da parede da bancada para dentro do banho
    box('banho_piso', x0, x1, BATH_Y0, BATH_Y1, Z0, Z0 + 0.006, M['banho_piso'])
    box('banho_forro', x0, x1, BATH_Y0, BATH_Y1, 2.5, 2.52, M['plaster_white'])
    for xx in (x0 + 0.65,):
        for yy in (BATH_Y0 + 0.55, BATH_Y0 + 1.45):
            cyl('spot_banho', xx, yy, 2.497, 2.5, 0.04, M['led_branco']); luz(xx, yy, 2.42, 7, (1.0, 0.9, 0.78))
    # paredes: topo (y0), lateral da porta e forros das paredes vizinhas com revestimento
    T = 0.1
    if porta == 'topo':
        px0, px1 = x0 + 0.3, x0 + 1.0                # porta 0,70 no topo
        box('banho_par_topo', x0, px0, BATH_Y0 - T, BATH_Y0, 0, H, M['wall'])
        box('banho_par_topo', px1, x1 + T, BATH_Y0 - T, BATH_Y0, 0, H, M['wall'])
        box('banho_verga', px0, px1, BATH_Y0 - T, BATH_Y0, DOOR, H, M['wall'])
        box('banho_par_lado', xo, xo + T, BATH_Y0, BATH_Y1, 0, H, M['wall'])
        box('porta_banho', px1, px1 + 0.68, BATH_Y0 - T - 0.04, BATH_Y0 - T, 0, DOOR, M['wood'])       # de correr, aberta
        for (ra_, rb_, z0_) in ((x0, px0, 0), (px1, x1, 0), (px0, px1, DOOR)):
            box('rev_topo', ra_, rb_, BATH_Y0, BATH_Y0 + 0.008, z0_, 2.5, M['banho_par_xz'])
        la, lb = sorted((xo, xo + pia_lado * 0.008))
        box('rev_lado', la, lb, BATH_Y0, BATH_Y1, 0, 2.5, M['banho_par_yz'])
    else:
        py0, py1 = BATH_Y0 + 0.7, BATH_Y0 + 1.4      # porta 0,70 na lateral
        xa, xb = (xo - T, xo)
        box('banho_par_topo', x0 - T if pia_lado > 0 else x0, x1 if pia_lado > 0 else x1 + T, BATH_Y0 - T, BATH_Y0, 0, H, M['wall'])
        box('banho_par_lado', xa, xb, BATH_Y0, py0, 0, H, M['wall'])
        box('banho_par_lado', xa, xb, py1, BATH_Y1 + 0.15, 0, H, M['wall'])
        box('banho_verga', xa, xb, py0, py1, DOOR, H, M['wall'])
        box('porta_banho', xa - 0.04, xa, py0 - 0.68, py0, 0, DOOR, M['wood'])                           # de correr, aberta
        box('rev_topo', x0, x1, BATH_Y0, BATH_Y0 + 0.008, 0, 2.5, M['banho_par_xz'])
        la, lb = sorted((xo, xo + pia_lado * 0.008))
        for (ya_, yb_, z0_) in ((BATH_Y0, py0, 0), (py1, BATH_Y1, 0), (py0, py1, DOOR)):
            box('rev_lado', la, lb, ya_, yb_, z0_, 2.5, M['banho_par_yz'])
    box('banho_par_fundo', x0 - T, x1 + T, BATH_Y1, BATH_Y1 + 0.15, 0, H, M['wall'])
    # revestimento interno (placas finas sobre as paredes)
    box('rev_fundo', x0, x1, BATH_Y1 - 0.008, BATH_Y1, 0, 2.5, azulejo)
    ra, rb = sorted((xp, xp + s * 0.008))
    box('rev_pia', ra, rb, BATH_Y0, BATH_Y1, 0, 2.5, M['banho_par_yz'])
    # bancada com cuba, espelho e torneira
    ba, bb = sorted((xp, xp + s * 0.48))
    box('bancada_banho', ba, bb, BATH_Y0 + 0.05, BATH_Y0 + 0.85, 0.84, 0.88, M['granito'])
    fa, fb = sorted((xp + s * 0.008, xp + s * 0.03))
    box('rodabanca', fa, fb, BATH_Y0 + 0.05, BATH_Y0 + 0.85, 0.88, 0.96, M['granito'])
    box('gabinete_banho', ba, bb - 0.03 if s > 0 else bb, BATH_Y0 + 0.08, BATH_Y0 + 0.82, 0.35, 0.82, M['wood'])
    xc = xp + s * 0.25
    qa, qb = sorted((xp + s * 0.1, xp + s * 0.52))                # cuba retangular de semi-encaixe, como na foto
    ya, yb = BATH_Y0 + 0.17, BATH_Y0 + 0.73
    box('cuba_fundo', qa, qb, ya, yb, 0.8, 0.892, M['louca'])    # fundo acima do tampo de granito, que passa por baixo
    for (c0, c1, d0, d1) in ((qa, qa + 0.022, ya, yb), (qb - 0.022, qb, ya, yb), (qa + 0.022, qb - 0.022, ya, ya + 0.022), (qa + 0.022, qb - 0.022, yb - 0.022, yb)):
        box('cuba_borda', c0, c1, d0, d1, 0.892, 0.96, M['louca'])   # sem sobrepor faces (faces coincidentes saem pretas)                      # paredes: a cuba é oca
    cyl('cuba_valvula', (qa + qb) / 2, (ya + yb) / 2, 0.892, 0.895, 0.022, M['steel'])
    # misturador de bancada, atrás da cuba e centrado nela, com a bica sobre a cavidade
    xt = xp + s * 0.06; yt = (ya + yb) / 2
    cyl('torneira_corpo', xt, yt, 0.88, 1.05, 0.02, M['steel'])
    ba_, bb_ = sorted((xt, xp + s * 0.21))
    box('torneira_bica', ba_, bb_, yt - 0.013, yt + 0.013, 1.02, 1.045, M['steel'], bevel=0.004)
    box('torneira_alavanca', xt - 0.012, xt + 0.012, yt - 0.012, yt + 0.012, 1.05, 1.09, M['steel'], bevel=0.004)
    ea, eb = sorted((xp + s * 0.008, xp + s * 0.02))
    box('espelho', ea, eb, BATH_Y0 + 0.08, BATH_Y0 + 0.82, 1.05, 2.0, M['espelho'])
    # vaso
    va, vb = sorted((xp + s * 0.02, xp + s * 0.2))
    box('vaso_caixa', va, vb, BATH_Y0 + 0.95, BATH_Y0 + 1.31, 0.0, 0.8, M['louca'], bevel=0.02)
    ta, tb = sorted((xp + s * 0.2, xp + s * 0.62))
    box('vaso', ta, tb, BATH_Y0 + 0.96, BATH_Y0 + 1.30, 0.0, 0.42, M['louca'], bevel=0.08)
    # box de vidro no fundo
    yb = BATH_Y1 - 0.8
    box('box_vidro', x0 + 0.02, x1 - 0.55, yb, yb + 0.01, 0.0, 2.0, M['glass'])
    box('box_perfil', x0 + 0.02, x1 - 0.55, yb - 0.005, yb + 0.015, 2.0, 2.02, M['steel'])
    # chuveiro de parede: braço horizontal saindo da parede lateral, com a ducha na ponta, e registro abaixo
    yc = BATH_Y1 - 0.42
    aa, ab = sorted((xp + s * 0.008, xp + s * 0.36))
    box('chuveiro_braco', aa, ab, yc - 0.011, yc + 0.011, 2.1, 2.122, M['steel'])
    cyl('chuveiro_canopla', xp + s * 0.012, yc, 2.085, 2.137, 0.035, M['steel'])
    cyl('chuveiro_descida', xp + s * 0.35, yc, 2.06, 2.1, 0.011, M['steel'])
    cyl('chuveiro', xp + s * 0.35, yc, 2.04, 2.06, 0.11, M['steel'])
    ga, gb = sorted((xp + s * 0.008, xp + s * 0.04))
    box('registro', ga, gb, yc - 0.035, yc + 0.035, 1.1, 1.17, M['steel'], bevel=0.01)
    box('nicho_moldura', x0 + 0.3, x1 - 0.3, BATH_Y1 - 0.014, BATH_Y1 - 0.008, 1.0, 1.3, M['granito'])   # nicho com moldura de granito
    box('nicho_fundo', x0 + 0.33, x1 - 0.33, BATH_Y1 - 0.016, BATH_Y1 - 0.014, 1.03, 1.27, azulejo)

def suite(a, b, prof, cab_lado, manta, cam_bed_y, pendente=False):
    """Suíte entre as faces internas x=a e x=b, da fachada (y=0) até y=prof."""
    box('suite_piso', a, b, 0.0, prof, 0.0, Z0, M['vinilico'])
    box('suite_forro', a, b, 0.0, max(prof, BATH_Y1), H - 0.03, H - 0.02, M['plaster_white'])
    box('cortineiro_suite', a, b, 0.0, 0.2, H - 0.06, H - 0.03, M['plaster_white'])
    # esquadria em toda a largura (DWG: 2,70/2,75 x 2,60) com verga e voil nas pontas
    box('verga_suite', a, b, -WT, 0.0, DOOR_H, H, M['wall'])
    slider_y(0.0, a + 0.02, b - 0.02, 4)
    curtain(a + 0.03, a + 0.5, 0.12); curtain(b - 0.5, b - 0.03, 0.12)
    xh = b if cab_lado > 0 else a
    pa, pb = sorted((xh, xh - cab_lado * 0.02))                      # parede da cabeceira em cimento queimado
    box('painel_cabeceira', pa, pb, 0.2, min(prof, 3.75), 0, H - 0.03, M['plaster'])
    cama(xh - cab_lado * 1.0, cam_bed_y, cab_lado, manta, pendente=pendente)
    for (x, y) in ((a + 0.7, 1.0), (b - 0.7, 1.0), ((a + b) / 2, 2.6), (a + 0.7, prof - 0.9)):
        spot_forro(x, y)

def arte(nome, cores, escala=1.6, seed=0.0):
    """Tela abstrata (manchas largas em poucas cores) para os quadros."""
    def build(nt, b):
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Location'].default_value = (seed, seed * 0.7, seed * 1.3)
        nt.links.new(tex_coord(nt), mp.inputs['Vector'])
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = escala; nz.inputs['Detail'].default_value = 1.5
        nz.inputs['Distortion'].default_value = 1.2
        nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
        rp = nt.nodes.new('ShaderNodeValToRGB'); rp.color_ramp.interpolation = 'EASE'
        el = rp.color_ramp.elements
        el[0].position = 0.3; el[0].color = (*srgb(cores[0]), 1); el[1].position = 0.7; el[1].color = (*srgb(cores[-1]), 1)
        for i, c in enumerate(cores[1:-1]):
            e = el.new(0.3 + 0.4 * (i + 1) / (len(cores) - 1)); e.color = (*srgb(c), 1)
        nt.links.new(nz.outputs['Fac'], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs['Base Color'])
        b.inputs['Roughness'].default_value = 0.85
    return node_mat(nome, build)

def parede_decorada(a, tela, objeto, nome_tela='tela'):
    """Parede em frente à cama (a que fica diante da câmera): painel ripado iluminado, aparador de madeira suspenso
    com objetos e um quadro grande."""
    # 303: painel ripado; 304: parede lisa em tom de areia (como nas referências)
    box('ripado_parede', a + 0.001, a + 0.03, 0.2, 3.3, 0, 2.5, M['slat'] if APTO == '303' else M['parede_areia'])
    box('sanca_led_parede', a + 0.001, a + 0.045, 0.2, 3.3, 2.5, 2.52, M['led_branco'])
    box('aparador', a + 0.03, a + 0.4, 0.5, 2.9, 0.4, 0.72, M['wood'], bevel=0.004)
    box('aparador_tampo', a + 0.03, a + 0.41, 0.49, 2.91, 0.72, 0.745, M['marble'])
    # quadro grande com moldura fina preta e passe-partout claro
    if APTO == '303':      # um quadro grande, moldura preta fina e passe-partout claro
        quadros = [(0.95, 2.45, tela)]; mold = M['black']
    else:                  # 304: par de marinhas com moldura de madeira
        quadros = [(0.72, 1.6, tela), (1.8, 2.68, arte(nome_tela + '_b', TELA_PRAIA, seed=77.0))]; mold = M['wood']
    zq0, zq1 = 1.02, 2.12
    for yq0, yq1, tl in quadros:
        box('quadro_moldura', a + 0.03, a + 0.055, yq0, yq1, zq0, zq1, mold)
        box('quadro_passe', a + 0.055, a + 0.058, yq0 + 0.025, yq1 - 0.025, zq0 + 0.025, zq1 - 0.025, M['plaster_white'])
        m_ = 0.13 if APTO == '303' else 0.03
        box('quadro_tela', a + 0.058, a + 0.061, yq0 + m_, yq1 - m_, zq0 + m_, zq1 - m_, tl)
    # objetos sobre o aparador
    cyl('vaso_aparador', a + 0.22, 0.75, 0.745, 1.02, 0.07, objeto)
    sphere('vaso_aparador_boca', a + 0.22, 0.75, 1.02, 0.075, objeto, scale=(1, 1, 0.5))
    for i, (l, w) in enumerate(((0.3, 0.22), (0.26, 0.19), (0.22, 0.17))):
        box('livro_aparador', a + 0.1, a + 0.1 + w, 2.45 - l / 2, 2.45 + l / 2, 0.745 + i * 0.035, 0.778 + i * 0.035, M['book'] if i != 1 else objeto)
    cyl('abajur_aparador_pe', a + 0.22, 2.75, 0.745, 0.95, 0.012, M['brass'])
    cyl('abajur_aparador', a + 0.22, 2.75, 0.95, 1.15, 0.09, M['abajur'])
    luz(a + 0.3, 2.75, 1.25, 2.5)

# ---- divisórias entre as suítes (a parede suíte 3 / living em x -0,15..0 já existe no arquivo principal)
S3 = (-2.85, -0.15); S2 = (-5.75, -3.0); S1 = (-8.65, -5.95)
box('div_s3_s2', -3.0, -2.85, -WT, 6.28, 0, H, M['wall'])
box('div_s2_s1', -5.95, -5.75, -WT, 6.5, 0, H, M['wall'])
box('empena', -8.8, -8.65, -WT, 6.5, 0, H, M['wall'])

# ---- suíte 3 (ao lado do living): 2,70 x 5,40, cabeceira na parede do living
suite(*S3, 5.40, +1, COR_S3, 1.75)
banho(-1.45, -0.15, +1, 'lado', M['azulejo_verde'])                                   # suíte 3: verde nas duas coberturas
parede_decorada(S3[0], arte('tela_s3', TELA_S3, seed=3.0), COR_S3, 'tela_s3')
armario(S3[0], S3[0] + 0.55, 3.35, 5.25)
box('s3_fundo', S3[0], -1.55, 5.40, 5.50, 0, H, M['wall'])                    # fundo com a porta de entrada (fechada)
box('s3_porta', -2.2, -1.6, 5.38, 5.40, 0, DOOR, M['wood'])

# ---- suíte 2 (meio): 2,75 x 5,25, cabeceira na parede da direita, bancada de estudo sobre o banho
suite(*S2, 5.25, +1, COR_S2, 1.7)
banho(-4.3, -3.0, +1, 'lado', M['azulejo_verde'])   # igual nas duas coberturas (decisão do cliente em 07/10/2026; as fotos da 304 mostram dois banhos azuis)
parede_decorada(S2[0], arte('tela_s2', TELA_S2, seed=11.0), COR_S2 if APTO == '303' else M['ceramic'], 'tela_s2')
armario(S2[0], S2[0] + 0.55, 3.35, 5.1)
box('bancada_estudo', -4.3, -3.0, 3.35, 3.75, 0.72, 0.76, M['plaster_white'])
# (a cadeira fica à esquerda do criado-mudo, que ocupa x -3,5..-3,08 junto à cabeceira; antes os dois se sobrepunham)
box('cadeira_s2', -4.27, -3.82, 2.85, 3.3, 0.42, 0.47, M['ceramic'], bevel=0.02)
box('cadeira_s2_enc', -4.27, -3.82, 2.85, 2.9, 0.47, 0.85, M['ceramic'], bevel=0.02)
for (cx_, cy_) in ((-4.23, 2.89), (-3.86, 2.89), (-4.23, 3.26), (-3.86, 3.26)):
    cyl('cadeira_s2_pe', cx_, cy_, 0, 0.42, 0.012, M['black'])
box('s2_fundo', S2[0], -4.4, 5.25, 5.35, 0, H, M['wall'])
box('s2_porta', -5.05, -4.45, 5.23, 5.25, 0, DOOR, M['wood'])

# ---- suíte 1 (master, ponta): 2,70 x 6,35, cabeceira na empena, banho no fundo à esquerda
box('suite_piso', S1[0], S1[1], 3.75, 6.35, 0.0, Z0, M['vinilico'])
suite(*S1, 3.75, -1, COR_S1, 2.0, pendente=True)
box('suite_forro_fundo', S1[0], S1[1], BATH_Y1, 6.5, H - 0.03, H - 0.02, M['plaster_white'])
banho(-8.65, -7.35, -1, 'topo', M['azulejo_azul'])
# decoração da master (sem bancada, a pedido): painel ripado iluminado atrás da cama, pendentes de latão,
# painel de TV em madeira escura com rack suspenso e canto de leitura junto à janela
box('painel_ripado_s1', S1[0] + 0.02, S1[0] + 0.045, 0.2, 3.75, 0, 2.5, M['slat'] if APTO == '303' else M['parede_areia'])
box('sanca_led_s1', S1[0] + 0.02, S1[0] + 0.06, 0.2, 3.75, 2.5, 2.52, M['led_branco'])
box('painel_tv_s1', S1[1] - 0.04, S1[1], 1.5, 3.7, 0.0, H - 0.03, M['wood_dark'])
box('rack_s1', S1[1] - 0.3, S1[1] - 0.04, 1.6, 3.6, 0.3, 0.5, M['wood_dark'])
box('tv_s1', S1[1] - 0.07, S1[1] - 0.04, 2.0, 3.2, 1.0, 1.7, M['black_glass'])
cyl('vaso_rack_s1', S1[1] - 0.17, 1.85, 0.5, 0.72, 0.06, M['ceramic'])
armchair(-6.5, 0.75, +1)
if APTO == '304':
    oliveira(-6.2, 1.35, h=1.8)
# quadros na parede da direita: um de cada lado do painel da TV e outro mais perto da porta de entrada
def quadro_parede_x(xw, lado, yc, zc, larg, alt, tela, mold=None):
    """Quadro numa parede de x constante; lado = -1 se a face visível olha para x menor."""
    p = lambda d: xw + lado * d
    for nome, d0, d1, m, folga in (('quadro_moldura', 0.0, 0.025, mold or M['black'], 0.0), ('quadro_passe', 0.025, 0.028, M['plaster_white'], 0.02),
                                   ('quadro_tela', 0.028, 0.031, tela, 0.09)):
        xa, xb = sorted((p(d0), p(d1)))
        box(nome, xa, xb, yc - larg / 2 + folga, yc + larg / 2 - folga, zc - alt / 2 + folga, zc + alt / 2 - folga, m)
# parede atrás da cama: tela horizontal grande sobre a cabeceira, ladeada por duas arandelas, e prateleira com objetos
quadro_parede_x(S1[0] + 0.045, +1, 2.0, 1.88, 1.9, 0.8,
                arte('tela_s1_cama', ('#efe7da', '#d8c7ad', '#b08a4e', '#3a2f28') if APTO == '303' else TELA_MAR, escala=1.1, seed=58.0),
                mold=M['brass'] if APTO == '303' else M['wood'])
for ya_ in (0.72, 3.28):
    box('arandela_base', S1[0] + 0.045, S1[0] + 0.06, ya_ - 0.04, ya_ + 0.04, 1.7, 2.0, M['brass'])
    cyl('arandela_luz', S1[0] + 0.1, ya_, 1.78, 1.94, 0.035, M['abajur'])
    luz(S1[0] + 0.2, ya_, 1.86, 2.0)
if APTO == '304':      # 304: cabeceira em palha natural, como nas referências
    box('cabeceira_palha', S1[0] + 0.08, S1[0] + 0.095, 0.62, 3.38, 0.32, 1.23, M['cane'])
quadro_parede_x(S1[1], -1, 0.9, 1.6, 0.6, 0.85, arte('tela_s1c', ('#efe7da', '#c9b79c', '#7d6a55', '#2f3b3a') if APTO == '303' else TELA_MAR, seed=47.0))
quadro_parede_x(S1[1], -1, 4.3, 1.55, 0.6, 0.85, arte('tela_s1a', ('#efe7da', '#cdb89a', '#9a7b5a', '#3a2f28') if APTO == '303' else TELA_PRAIA, seed=21.0))
quadro_parede_x(S1[1], -1, 5.25, 1.55, 0.6, 0.85, arte('tela_s1b', ('#efe7da', '#d8c7ad', '#b08a4e', '#5a4636') if APTO == '303' else TELA_MAR, seed=34.0))
cyl('mesa_lateral_s1', -7.05, 0.5, 0.0, 0.5, 0.17, M['brass'])
cyl('luminaria_s1_haste', -6.1, 0.35, 0.0, 1.45, 0.01, M['black'])
cyl('luminaria_s1_cupula', -6.1, 0.35, 1.45, 1.65, 0.11, M['abajur'])
armario(-7.25, -6.7, 4.75, 6.3)
box('s1_fundo', S1[0], S1[1], 6.35, 6.5, 0, H, M['wall'])
box('s1_porta', -6.65, -6.0, 6.33, 6.35, 0, DOOR, M['wood'])
for (x, y) in ((-6.5, 4.4), (-6.5, 5.7)):
    spot_forro(x, y)
