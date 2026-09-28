"""
Piloto tour 360 — Cobertura 303: living + jantar + cozinha.

Gera a cena no Blender a partir das cotas da planta humanizada (planta303.png) e
renderiza panoramas equirretangulares e vistas em perspectiva.

Uso:
  /Applications/Blender.app/Contents/MacOS/Blender -b -P cena_living.py -- \
      --out <pasta> [--samples 256] [--res 4096] [--only living_360,cozinha_360] [--save cena.blend]

Coordenadas: "planta" em metros, origem no canto interno sup-esq do living
(parede da suíte 3 x fachada frontal). x cresce para a direita, y cresce para
baixo na planta (Blender: Y = -y). Pé-direito 2,80 m.
"""
import bpy, math, os, sys, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default
OUT = arg('--out', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render'))
SAMPLES = int(arg('--samples', '256'))
RES = int(arg('--res', '4096'))
ONLY = [s for s in arg('--only', '').split(',') if s]
SAVE = arg('--save', '')
HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.abspath(os.path.join(HERE, '..', '..', '_originais'))
os.makedirs(OUT, exist_ok=True)
random.seed(7)

H = 2.80          # pé-direito
WT = 0.15         # espessura de parede

# ------------------------------------------------------------------ limpeza
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col = scene.collection

# ------------------------------------------------------------------ materiais
def mat(name, color=(0.8, 0.8, 0.8), rough=0.5, metal=0.0, **kw):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    for k, v in kw.items():
        b.inputs[k].default_value = v
    return m

def srgb(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)

def node_mat(name, build):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    build(nt, nt.nodes['Principled BSDF'])
    return m

def tex_coord(nt):
    tc = nt.nodes.new('ShaderNodeTexCoord')
    return tc.outputs['Object']

def wood_build(base, dark, scale=(1, 18, 1), gloss=0.35):
    def build(nt, b):
        mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = scale
        nt.links.new(tex_coord(nt), mp.inputs['Vector'])
        wv = nt.nodes.new('ShaderNodeTexWave')
        wv.wave_type = 'RINGS'
        wv.inputs['Scale'].default_value = 1.2
        wv.inputs['Distortion'].default_value = 6
        wv.inputs['Detail'].default_value = 3
        nt.links.new(mp.outputs['Vector'], wv.inputs['Vector'])
        nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 40
        nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'
        mx.inputs['Factor'].default_value = 0.35
        nt.links.new(wv.outputs['Fac'], mx.inputs['Factor'])
        mx.inputs[6].default_value = (*srgb(base), 1)
        mx.inputs[7].default_value = (*srgb(dark), 1)
        nt.links.new(mx.outputs[2], b.inputs['Base Color'])
        b.inputs['Roughness'].default_value = gloss
        bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.05
        nt.links.new(nz.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return build

def slat_ceiling(nt, b):
    # forro de madeira ripado (tauari/cumaru), ripas ao longo de x
    mp = nt.nodes.new('ShaderNodeMapping')
    nt.links.new(tex_coord(nt), mp.inputs['Vector'])
    wv = nt.nodes.new('ShaderNodeTexWave')
    wv.wave_type = 'BANDS'; wv.bands_direction = 'Y'; wv.wave_profile = 'SAW'
    wv.inputs['Scale'].default_value = 7.5  # ~13 cm por ripa
    nt.links.new(mp.outputs['Vector'], wv.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.9
    ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    ramp.color_ramp.elements[1].position = 0.93
    ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
    nt.links.new(wv.outputs['Fac'], ramp.inputs['Fac'])
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 3; nz.inputs['Detail'].default_value = 8
    mpn = nt.nodes.new('ShaderNodeMapping'); mpn.inputs['Scale'].default_value = (0.4, 12, 1)
    nt.links.new(tex_coord(nt), mpn.inputs['Vector'])
    nt.links.new(mpn.outputs['Vector'], nz.inputs['Vector'])
    wood = nt.nodes.new('ShaderNodeMix'); wood.data_type = 'RGBA'
    nt.links.new(nz.outputs['Fac'], wood.inputs['Factor'])
    wood.inputs[6].default_value = (*srgb('#7a4326'), 1)
    wood.inputs[7].default_value = (*srgb('#a4643c'), 1)
    gap = nt.nodes.new('ShaderNodeMix'); gap.data_type = 'RGBA'
    nt.links.new(ramp.outputs['Color'], gap.inputs['Factor'])
    gap.inputs[6].default_value = (*srgb('#1d100a'), 1)
    nt.links.new(wood.outputs[2], gap.inputs[7])
    nt.links.new(gap.outputs[2], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.45
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.4
    nt.links.new(ramp.outputs['Color'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

def porcelain_floor(nt, b):
    # porcelanato 120x120 bege claro acetinado
    br = nt.nodes.new('ShaderNodeTexBrick')
    br.offset = 0.0
    br.inputs['Scale'].default_value = 1 / 1.2
    br.inputs['Mortar Size'].default_value = 0.0025
    br.inputs['Brick Width'].default_value = 1.0
    br.inputs['Row Height'].default_value = 1.0
    br.inputs['Color1'].default_value = (*srgb('#d8d0c4'), 1)
    br.inputs['Color2'].default_value = (*srgb('#d3cabd'), 1)
    br.inputs['Mortar'].default_value = (*srgb('#b9ad9d'), 1)
    nt.links.new(tex_coord(nt), br.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6
    nt.links.new(tex_coord(nt), nz.inputs['Vector'])
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
    mx.inputs['Factor'].default_value = 0.08
    nt.links.new(br.outputs['Color'], mx.inputs[6]); nt.links.new(nz.outputs['Color'], mx.inputs[7])
    nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.22
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.2
    nt.links.new(br.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

def marble(nt, b):
    # mármore branco com veios cinza (Calacatta)
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.2, 1.2, 1.2)
    nt.links.new(tex_coord(nt), mp.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.6; nz.inputs['Detail'].default_value = 12
    nz.inputs['Distortion'].default_value = 1.8
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    wv = nt.nodes.new('ShaderNodeTexWave')
    wv.inputs['Scale'].default_value = 0.9; wv.inputs['Distortion'].default_value = 6
    wv.inputs['Detail'].default_value = 10
    nt.links.new(nz.outputs['Color'], wv.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    e = ramp.color_ramp.elements
    e[0].position = 0.44; e[0].color = (*srgb('#f4f2ef'), 1)
    e[1].position = 0.5; e[1].color = (*srgb('#a3a09c'), 1)
    e3 = ramp.color_ramp.elements.new(0.56); e3.color = (*srgb('#f4f2ef'), 1)
    nt.links.new(wv.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.12
    b.inputs['Coat Weight'].default_value = 0.4

def plaster(nt, b):
    # parede em cimento queimado/terracota suave (parede da TV)
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 3.5; nz.inputs['Detail'].default_value = 14; nz.inputs['Roughness'].default_value = 0.65
    nt.links.new(tex_coord(nt), nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    e = ramp.color_ramp.elements
    e[0].position = 0.35; e[0].color = (*srgb('#b89c86'), 1)
    e[1].position = 0.7; e[1].color = (*srgb('#d2bba6'), 1)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.85
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.15
    nt.links.new(nz.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

def jute(nt, b):
    # tapete de juta/sisal espinha de peixe
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (22, 22, 22)
    nt.links.new(tex_coord(nt), mp.inputs['Vector'])
    br = nt.nodes.new('ShaderNodeTexBrick')
    br.inputs['Color1'].default_value = (*srgb('#b59f81'), 1)
    br.inputs['Color2'].default_value = (*srgb('#a58e70'), 1)
    br.inputs['Mortar'].default_value = (*srgb('#8a7458'), 1)
    br.inputs['Mortar Size'].default_value = 0.03
    br.inputs['Brick Width'].default_value = 0.8
    br.inputs['Row Height'].default_value = 0.2
    nt.links.new(mp.outputs['Vector'], br.inputs['Vector'])
    nt.links.new(br.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.95
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.6
    nt.links.new(br.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

def cane(nt, b):
    # palhinha / rattan trançado
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (60, 60, 60)
    nt.links.new(tex_coord(nt), mp.inputs['Vector'])
    ck = nt.nodes.new('ShaderNodeTexChecker')
    ck.inputs['Color1'].default_value = (*srgb('#d8bf98'), 1)
    ck.inputs['Color2'].default_value = (*srgb('#b09068'), 1)
    nt.links.new(mp.outputs['Vector'], ck.inputs['Vector'])
    nt.links.new(ck.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.7
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.5
    nt.links.new(ck.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])

def velvet(color):
    def build(nt, b):
        b.inputs['Base Color'].default_value = (*srgb(color), 1)
        b.inputs['Roughness'].default_value = 0.85
        b.inputs['Sheen Weight'].default_value = 1.0
        b.inputs['Sheen Tint'].default_value = (*srgb('#8fa4c4'), 1)
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 90
        nt.links.new(tex_coord(nt), nz.inputs['Vector'])
        bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.08
        nt.links.new(nz.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return build

def sheer(nt, b):
    # cortina de voil translúcida
    out = nt.nodes['Material Output']
    tr = nt.nodes.new('ShaderNodeBsdfTranslucent'); tr.inputs['Color'].default_value = (*srgb('#f4efe6'), 1)
    tp = nt.nodes.new('ShaderNodeBsdfTransparent')
    mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = 0.45
    nt.links.new(tp.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])

def glass_mat(nt, b):
    b.inputs['Base Color'].default_value = (0.9, 0.95, 0.95, 1)
    b.inputs['Roughness'].default_value = 0.0
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['IOR'].default_value = 1.45

def photo_emit(path, strength=1.0):
    def build(nt, b):
        out = nt.nodes['Material Output']
        im = nt.nodes.new('ShaderNodeTexImage')
        im.image = bpy.data.images.load(path)
        im.extension = 'EXTEND'
        em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = strength
        nt.links.new(im.outputs['Color'], em.inputs['Color'])
        nt.links.new(em.outputs[0], out.inputs['Surface'])
    return build

M = dict(
    wall=mat('parede', srgb('#ebe4da'), 0.9),
    ceiling=node_mat('forro_madeira', slat_ceiling),
    plaster_white=mat('gesso', srgb('#f0ebe4'), 0.9),
    floor=node_mat('porcelanato', porcelain_floor),
    ext_floor=mat('piso_externo', srgb('#bdb6ab'), 0.6),
    marble=node_mat('marmore', marble),
    wood=node_mat('madeira_freijo', wood_build('#9a6a43', '#6d4428')),
    wood_dark=node_mat('madeira_escura', wood_build('#5a3521', '#3a2114', gloss=0.4)),
    slat=node_mat('ripado', wood_build('#8a5534', '#5e3620', scale=(1, 1, 18))),
    plaster=node_mat('parede_tv', plaster),
    navy=node_mat('veludo_marinho', velvet('#1b2a44')),
    linen=node_mat('linho', velvet('#cdbfa9')),
    cushion_rust=node_mat('almofada', velvet('#9b5a36')),
    jute=node_mat('juta', jute),
    cane=node_mat('palhinha', cane),
    lacquer=mat('laca_azul_petroleo', srgb('#1e3640'), 0.28, **{'Coat Weight': 0.5}),
    steel=mat('inox', srgb('#d4d6d8'), 0.32, 1.0),
    black=mat('preto_fosco', srgb('#151515'), 0.5),
    black_glass=mat('vidro_preto', srgb('#050505'), 0.05),
    brass=mat('latao', srgb('#b08a4e'), 0.3, 1.0),
    frame=mat('esquadria', srgb('#dcdcdc'), 0.4, 0.6),
    glass=node_mat('vidro', glass_mat),
    sheer=node_mat('voil', sheer),
    leaf=mat('folha', srgb('#2f5a2c'), 0.55, **{'Subsurface Weight': 0.2}),
    pot=mat('vaso', srgb('#d9d2c6'), 0.7),
    ceramic=mat('ceramica', srgb('#2e5d57'), 0.2),
    book=mat('livro', srgb('#e0d4c0'), 0.8),
)

# ------------------------------------------------------------------ geometria
def box(name, x0, x1, y0, y1, z0, z1, m, bevel=0.0):
    """Caixa em coordenadas de planta (y para baixo)."""
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.active_object
    o.name = name
    o.location = ((x0 + x1) / 2, -(y0 + y1) / 2, (z0 + z1) / 2)
    o.scale = (abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    if bevel:
        bv = o.modifiers.new('bevel', 'BEVEL'); bv.width = bevel; bv.segments = 4
        bpy.ops.object.shade_smooth()
    return o

def cyl(name, x, y, z0, z1, r, m, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=z1 - z0, location=(x, -y, (z0 + z1) / 2))
    o = bpy.context.active_object; o.name = name; o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    return o

def sphere(name, x, y, z, r, m, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=r, location=(x, -y, z))
    o = bpy.context.active_object; o.name = name; o.scale = scale; o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    return o

# ---- piso e forro
box('piso', -1.6, 6.0, 0.0, 9.05, -0.05, 0.0, M['floor'])
box('forro', -1.6, 6.0, 0.0, 9.05, H, H + 0.05, M['ceiling'])
# sanca de gesso junto às paredes (tabica)
box('tabica_frente', -1.6, 6.0, 0.0, 0.25, H - 0.18, H, M['plaster_white'])

# ---- paredes (y planta; espessura para fora)
def wall_x(x, y0, y1, openings=(), side=-1, m=None):
    """Parede vertical na planta ao longo de y, na coordenada x. side=-1: espessura para x menor."""
    xa, xb = (x - WT, x) if side < 0 else (x, x + WT)
    pts = [y0] + [v for o in openings for v in (o[0], o[1])] + [y1]
    for i in range(0, len(pts), 2):
        if pts[i + 1] > pts[i]:
            box('parede', xa, xb, pts[i], pts[i + 1], 0, H, m or M['wall'])
    for (a, b, zt, zb) in openings:  # verga e peitoril
        if zt < H: box('verga', xa, xb, a, b, zt, H, m or M['wall'])
        if zb > 0: box('peitoril', xa, xb, a, b, 0, zb, m or M['wall'])

def wall_y(y, x0, x1, openings=(), side=-1, m=None):
    ya, yb = (y - WT, y) if side < 0 else (y, y + WT)
    pts = [x0] + [v for o in openings for v in (o[0], o[1])] + [x1]
    for i in range(0, len(pts), 2):
        if pts[i + 1] > pts[i]:
            box('parede', pts[i], pts[i + 1], ya, yb, 0, H, m or M['wall'])
    for (a, b, zt, zb) in openings:
        if zt < H: box('verga', a, b, ya, yb, zt, H, m or M['wall'])
        if zb > 0: box('peitoril', a, b, ya, yb, 0, zb, m or M['wall'])

DOOR_H = 2.55
# fachada frontal (y=0): esquadria de piso a teto ao longo do living
wall_y(0.0, -0.15, 4.9, openings=[(0.25, 4.5, DOOR_H, 0)])
# lateral direita (x=4.75): vidro para a varanda gourmet
wall_x(4.75, 0.0, 7.35, openings=[(0.9, 4.25, DOOR_H, 0)], side=1)
# nicho da cozinha / shaft
wall_y(7.35, 4.75, 5.9, side=-1)
wall_x(5.9, 7.35, 9.05, side=1)
# fundo da cozinha
wall_y(9.05, -1.6, 6.05, side=1)
# esquerda: parede da suíte 3 / banho e passagem para o corredor
wall_x(0.0, 0.0, 6.13)
wall_y(6.13, -1.6, 0.0, side=1)
wall_x(-1.45, 6.13, 9.05, openings=[(6.45, 7.55, 2.2, 0)])
# corredor escuro atrás da passagem
box('corredor_piso', -4.0, -1.6, 6.3, 7.7, -0.05, 0, M['floor'])
box('corredor_fundo', -4.1, -4.0, 6.3, 7.7, 0, H, M['wall'])
box('corredor_teto', -4.0, -1.6, 6.3, 7.7, H - 0.2, H - 0.15, M['plaster_white'])
box('porta_suite', -3.2, -2.3, 6.25, 6.3, 0, 2.2, M['wood'])

# ---- esquadrias de correr (montantes + vidro)
def slider_y(y, x0, x1, n):
    box('marco_sup', x0, x1, y - 0.07, y - 0.02, DOOR_H - 0.05, DOOR_H, M['frame'])
    box('trilho', x0, x1, y - 0.07, y - 0.02, 0, 0.02, M['frame'])
    w = (x1 - x0) / n
    for i in range(n + 1):
        x = x0 + i * w
        box('montante', x - 0.025, x + 0.025, y - 0.08, y - 0.01, 0, DOOR_H, M['frame'])
    box('vidro', x0, x1, y - 0.05, y - 0.04, 0.02, DOOR_H - 0.05, M['glass'])

def slider_x(x, y0, y1, n):
    box('marco_sup', x + 0.02, x + 0.07, y0, y1, DOOR_H - 0.05, DOOR_H, M['frame'])
    box('trilho', x + 0.02, x + 0.07, y0, y1, 0, 0.02, M['frame'])
    w = (y1 - y0) / n
    for i in range(n + 1):
        y = y0 + i * w
        box('montante', x + 0.01, x + 0.08, y - 0.025, y + 0.025, 0, DOOR_H, M['frame'])
    box('vidro', x + 0.04, x + 0.05, y0, y1, 0.02, DOOR_H - 0.05, M['glass'])

slider_y(0.0, 0.25, 4.5, 4)
slider_x(4.75, 0.9, 4.25, 3)

# ---- exterior: varanda frontal e varanda gourmet/solarium
box('varanda_frontal', -1.6, 6.0, -1.55, -0.15, -0.06, -0.01, M['ext_floor'])
box('forro_varanda', -1.6, 6.0, -1.55, -0.15, H, H + 0.05, M['ceiling'])
box('guarda_corpo', -1.6, 6.0, -1.55, -1.53, 0, 1.1, M['glass'])
box('corrimao', -1.6, 6.0, -1.56, -1.52, 1.1, 1.13, M['steel'])
box('terraco', 4.9, 13.0, -1.55, 9.0, -0.06, -0.01, M['ext_floor'])
box('guarda_corpo_terraco', 12.98, 13.0, -1.55, 9.0, 0, 1.1, M['glass'])
box('corrimao_terraco', 12.97, 13.01, -1.55, 9.0, 1.1, 1.13, M['steel'])
box('beiral_terraco', 4.9, 8.5, -1.55, 9.0, H, H + 0.25, M['plaster_white'])
box('forro_terraco', 4.9, 8.5, -1.55, 9.0, H - 0.02, H, M['ceiling'])
# mesa da varanda gourmet (planta: mesa 10 lugares)
box('mesa_gourmet', 6.2, 7.2, 0.9, 3.4, 0.72, 0.77, M['wood_dark'], bevel=0.01)
for yy in (1.1, 3.2):
    box('pe_mesa_g', 6.3, 7.1, yy - 0.05, yy + 0.05, 0, 0.72, M['black'])

# fundos com fotos reais da vista da 303 (sem IA)
def backdrop(name, path, center, size, rot_z, crop=None, strength=1.0):
    img_path = path
    if crop:
        import subprocess
        img_path = os.path.join(OUT, name + '.png')
        if not os.path.exists(img_path):
            im = bpy.data.images.load(path)
            w, h = im.size
            x0, y0, x1, y1 = crop
            import numpy as np
            px = np.array(im.pixels[:]).reshape(h, w, 4)[::-1]
            sub = px[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)][::-1]
            out = bpy.data.images.new(name, sub.shape[1], sub.shape[0])
            out.pixels = sub.flatten().tolist()
            out.filepath_raw = img_path; out.file_format = 'PNG'; out.save()
    bpy.ops.mesh.primitive_plane_add(size=1, location=center)
    o = bpy.context.active_object; o.name = name
    o.scale = (size[0], size[1], 1)
    o.rotation_euler = (math.radians(90), 0, math.radians(rot_z))
    o.data.materials.append(node_mat(name, photo_emit(img_path, strength)))
    o.visible_shadow = False
    return o

VIEW_A = os.path.join(ORIG, 'WhatsApp-Image-2026-02-09-at-11.46.07.jpeg')    # baía (varanda)
VIEW_B = os.path.join(ORIG, 'WhatsApp-Image-2026-02-09-at-11.46.10-3.jpeg')  # baía + morro (solarium)
backdrop('vista_frente', VIEW_A, (2.4, 32.0, 6.0), (70, 32), 180, crop=(0.2, 0.0, 0.95, 0.72), strength=1.15)
backdrop('vista_lateral', VIEW_B, (45.0, -4.0, 5.0), (80, 36), 90, crop=(0.55, 0.15, 1.0, 0.85), strength=1.15)

# ================================================================== LIVING
# parede da TV: ripado de madeira em toda a parede esquerda do living
for i in range(int(3.9 / 0.06)):
    y = 0.35 + i * 0.06
    box('ripa', 0.0, 0.035, y, y + 0.035, 0, H, M['slat'])
box('fundo_ripado', 0.0, 0.01, 0.3, 4.3, 0, H, M['wood_dark'])
# painel em cimento/terracota atrás da TV
box('painel_tv', 0.035, 0.06, 1.35, 3.25, 0.0, H, M['plaster'])
# rack suspenso
box('rack', 0.06, 0.5, 0.9, 3.7, 0.28, 0.62, M['wood'], bevel=0.008)
for i in range(4):
    y = 0.9 + i * 0.7
    box('frente_gaveta', 0.5, 0.505, y + 0.02, y + 0.68, 0.3, 0.6, M['wood_dark'])
# TV
box('tv', 0.07, 0.11, 1.6, 3.0, 1.0, 1.8, M['black_glass'], bevel=0.005)
# prateleira com plantas pendentes (referência)
box('prateleira', 0.06, 0.3, 1.5, 3.1, 2.05, 2.09, M['wood'])
for yy in (1.8, 2.4, 2.8):
    cyl('vasinho', 0.18, yy, 2.09, 2.24, 0.08, M['pot'])
# objetos no rack
cyl('vaso_rack', 0.28, 1.15, 0.62, 0.95, 0.07, M['ceramic'])
box('livros_rack', 0.15, 0.42, 3.2, 3.5, 0.62, 0.7, M['book'])
sphere('escultura', 0.3, 3.35, 0.78, 0.08, M['brass'])

# tapete de juta
box('tapete', 0.62, 3.18, 0.6, 3.98, 0.0, 0.012, M['jute'])

# sofá marinho em L (chaise voltada para a janela), costas para o aparador
SX0, SX1, SY0, SY1 = 2.35, 3.4, 0.9, 3.35
box('sofa_base', SX0, SX1, SY0, SY1, 0.1, 0.42, M['navy'], bevel=0.04)
box('sofa_encosto', SX1 - 0.22, SX1, SY0, SY1, 0.42, 0.82, M['navy'], bevel=0.06)
box('sofa_chaise', 1.75, SX0 + 0.1, SY0, 1.65, 0.1, 0.42, M['navy'], bevel=0.04)
for y0, y1 in ((SY0, SY0 + 0.2), (SY1 - 0.2, SY1)):
    box('sofa_braco', SX0 + 0.1, SX1, y0, y1, 0.42, 0.62, M['navy'], bevel=0.05)
for i, (y0, y1) in enumerate(((1.15, 1.9), (1.9, 2.65), (2.65, 3.15))):
    box('assento', SX0 + 0.02, SX1 - 0.22, y0 + 0.01, y1 - 0.01, 0.42, 0.52, M['navy'], bevel=0.05)
    box('almofada_encosto', SX1 - 0.4, SX1 - 0.2, y0 + 0.02, y1 - 0.02, 0.52, 0.95, M['navy'], bevel=0.07)
for y, m_ in ((1.3, M['linen']), (2.2, M['cushion_rust']), (2.9, M['linen'])):
    o = box('almofada_decor', SX1 - 0.45, SX1 - 0.3, y - 0.22, y + 0.22, 0.55, 0.95, m_, bevel=0.07)
    o.rotation_euler = (0, math.radians(-12), 0)
for (x, y) in ((1.85, 0.97), (3.3, 0.97), (1.85, 3.28), (3.3, 3.28)):
    box('pe_sofa', x - 0.02, x + 0.02, y - 0.02, y + 0.02, 0, 0.1, M['black'])
# aparador atrás do sofá
box('aparador', 3.45, 3.9, 0.95, 3.3, 0.0, 0.72, M['wood'], bevel=0.008)
sphere('abajur_cupula', 3.68, 1.25, 1.05, 0.16, M['linen'], scale=(1, 1, 0.8))
cyl('abajur_pe', 3.68, 1.25, 0.72, 0.9, 0.06, M['ceramic'])

# mesa de centro: estrutura metálica quadrada + tampo redondo de madeira
box('mesa_centro_vidro', 0.85, 1.55, 2.0, 2.7, 0.36, 0.38, M['black_glass'])
for (x, y) in ((0.85, 2.0), (1.55, 2.0), (0.85, 2.7), (1.55, 2.7)):
    box('pe_centro', x - 0.012, x + 0.012, y - 0.012, y + 0.012, 0, 0.38, M['black'])
cyl('tampo_redondo', 1.25, 2.3, 0.38, 0.41, 0.3, M['wood'])
box('livros', 1.1, 1.4, 2.15, 2.4, 0.41, 0.47, M['book'])
cyl('suculenta', 1.35, 2.5, 0.41, 0.5, 0.06, M['pot'])
sphere('suculenta_f', 1.35, 2.5, 0.53, 0.06, M['leaf'], scale=(1, 1, 0.6))

# poltronas de palhinha (topo e base do tapete)
def armchair(cx, cy, facing):
    o = []
    o.append(box('poltrona_assento', cx - 0.36, cx + 0.36, cy - 0.34, cy + 0.34, 0.38, 0.46, M['linen'], bevel=0.03))
    back = (cy - 0.36, cy - 0.3) if facing > 0 else (cy + 0.3, cy + 0.36)
    o.append(box('poltrona_encosto', cx - 0.34, cx + 0.34, back[0], back[1], 0.46, 0.85, M['cane'], bevel=0.01))
    for sx in (-1, 1):
        o.append(box('poltrona_braco', cx + sx * 0.36 - 0.03, cx + sx * 0.36 + 0.03, cy - 0.34, cy + 0.34, 0.0, 0.62, M['wood'], bevel=0.01))
    return o
armchair(1.2, 0.8, +1)
armchair(1.2, 3.65, -1)

# luminária de chão em arco (preta)
cyl('luminaria_base', 3.75, 3.7, 0.0, 0.04, 0.16, M['black'])
cyl('luminaria_haste', 3.75, 3.7, 0.04, 1.75, 0.012, M['black'])
bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.24, radius2=0.12, depth=0.3, location=(3.4, -3.35, 1.62))
shade = bpy.context.active_object; shade.data.materials.append(M['black']); bpy.ops.object.shade_smooth()
shade.rotation_euler = (math.radians(180), 0, 0)
box('luminaria_braco', 3.4, 3.75, 3.35, 3.7, 1.74, 1.76, M['black'])

# planta grande no canto (costela-de-adão/ave-do-paraíso)
def plant(x, y, h=1.6, n=14):
    cyl('vaso_planta', x, y, 0, 0.45, 0.22, M['pot'])
    for i in range(n):
        a = random.uniform(0, 2 * math.pi); r = random.uniform(0.1, 0.35)
        z = random.uniform(0.7, h)
        lf = sphere('folha', x + r * math.cos(a), y + r * math.sin(a), z, 0.2, M['leaf'], scale=(1.6, 0.7, 0.06))
        lf.rotation_euler = (random.uniform(-0.6, 0.6), random.uniform(-0.5, 0.5), a)
        stem_h = z - 0.45
        cyl('haste', x + r * 0.5 * math.cos(a), y + r * 0.5 * math.sin(a), 0.45, 0.45 + stem_h, 0.008, M['leaf'])
plant(4.35, 0.45)
plant(0.45, 4.5, h=1.3, n=10)

# ================================================================== JANTAR
TX, TY = 2.09, 5.17
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.0, depth=0.05, location=(TX, -TY, 0.75))
tt = bpy.context.active_object; tt.name = 'mesa_jantar'; tt.scale = (1.1, 0.52, 1)
tt.data.materials.append(M['wood_dark']); bpy.ops.object.shade_smooth()
for dx in (-0.55, 0.55):
    box('pe_jantar', TX + dx - 0.06, TX + dx + 0.06, TY - 0.2, TY + 0.2, 0, 0.73, M['wood_dark'])
for i in range(3):
    for side in (-1, 1):
        cx = TX - 0.62 + i * 0.62
        cy = TY + side * 0.78
        box('cadeira_assento', cx - 0.23, cx + 0.23, cy - 0.22, cy + 0.22, 0.44, 0.49, M['cane'], bevel=0.01)
        by = cy + side * 0.2
        box('cadeira_encosto', cx - 0.22, cx + 0.22, by - 0.025, by + 0.025, 0.49, 0.88, M['cane'], bevel=0.01)
        for (px_, py_) in ((-0.2, -0.19), (0.2, -0.19), (-0.2, 0.19), (0.2, 0.19)):
            box('cadeira_pe', cx + px_ - 0.018, cx + px_ + 0.018, cy + py_ - 0.018, cy + py_ + 0.018, 0, 0.44, M['wood'])
for side in (-1, 1):
    cx = TX + side * 1.28
    box('cadeira_cab', cx - 0.22, cx + 0.22, TY - 0.23, TY + 0.23, 0.44, 0.49, M['cane'], bevel=0.01)
    box('cadeira_cab_enc', cx + side * 0.2 - 0.025, cx + side * 0.2 + 0.025, TY - 0.22, TY + 0.22, 0.49, 0.88, M['cane'], bevel=0.01)
# centro de mesa
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.22, depth=0.06, location=(TX, -TY, 0.8))
bowl = bpy.context.active_object; bowl.data.materials.append(M['ceramic']); bpy.ops.object.shade_smooth()
for k in range(6):
    sphere('folha_centro', TX + random.uniform(-0.12, 0.12), TY + random.uniform(-0.12, 0.12), 0.86, 0.08, M['leaf'], scale=(1.5, 0.6, 0.15))

# pendente de madeira ripada sobre o jantar (referência)
sphere('pendente_jantar', TX, TY, 2.05, 0.3, M['wood'], scale=(1, 1, 0.75))
cyl('fio_pendente', TX, TY, 2.25, H, 0.004, M['black'])

# ================================================================== COZINHA
KY0, KY1 = 8.35, 9.05
# coluna alta: geladeira inox side-by-side em nicho de madeira
box('nicho_madeira', 0.05, 1.2, KY0 - 0.05, KY1, 0, H - 0.2, M['wood_dark'])
box('geladeira', 0.12, 1.12, KY0 - 0.03, KY1, 0.02, 1.85, M['steel'], bevel=0.01)
box('geladeira_div', 0.615, 0.625, KY0 - 0.035, KY0 - 0.02, 0.05, 1.82, M['black'])
for x in (0.58, 0.66):
    box('puxador', x - 0.01, x + 0.01, KY0 - 0.07, KY0 - 0.04, 0.7, 1.5, M['steel'])
box('dispenser', 0.2, 0.42, KY0 - 0.035, KY0 - 0.02, 1.05, 1.4, M['black_glass'])
# torre quente (forno + micro-ondas)
box('torre', 1.2, 1.85, KY0, KY1, 0, H - 0.2, M['lacquer'])
box('forno', 1.25, 1.8, KY0 - 0.01, KY0, 0.8, 1.38, M['black_glass'])
box('micro', 1.25, 1.8, KY0 - 0.01, KY0, 1.45, 1.8, M['black_glass'])
# bancada inferior
box('armario_inf', 1.85, 5.85, KY0, KY1, 0.1, 0.88, M['lacquer'])
box('rodape', 1.85, 5.85, KY0 + 0.05, KY1, 0, 0.1, M['black'])
box('bancada', 1.85, 5.85, KY0 - 0.02, KY1, 0.88, 0.92, M['marble'])
for i in range(8):
    x = 1.85 + i * 0.5
    box('junta', x - 0.002, x + 0.002, KY0 - 0.001, KY0, 0.12, 0.86, M['black'])
box('backsplash', 1.85, 5.85, KY1 - 0.02, KY1, 0.92, 1.5, M['marble'])
box('armario_sup', 1.85, 5.85, KY1 - 0.36, KY1 - 0.02, 1.5, H - 0.2, M['lacquer'])
box('led_sup', 1.9, 5.8, KY1 - 0.35, KY1 - 0.32, 1.49, 1.5, M['brass'])
# cuba e cooktop (posições da planta)
box('cuba', 2.1, 2.85, KY0 + 0.1, KY1 - 0.12, 0.8, 0.921, M['steel'])
cyl('torneira', 2.47, KY1 - 0.08, 0.92, 1.25, 0.015, M['steel'])
box('cooktop', 3.75, 4.45, KY0 + 0.08, KY1 - 0.1, 0.92, 0.93, M['black_glass'])
box('coifa', 3.7, 4.5, KY1 - 0.42, KY1 - 0.02, 1.62, 1.72, M['steel'])
# objetos na bancada
cyl('garrafa', 3.2, KY1 - 0.12, 0.92, 1.2, 0.035, M['wood_dark'])
cyl('garrafa2', 3.3, KY1 - 0.12, 0.92, 1.25, 0.035, M['black'])
sphere('fruteira', 5.1, KY1 - 0.3, 0.97, 0.16, M['cane'], scale=(1, 1, 0.35))

# ripado vertical de madeira na parede lateral (entre living e cozinha)
for i in range(int(2.8 / 0.06)):
    y = 4.35 + i * 0.06
    box('ripa_lateral', 4.715, 4.75, y, y + 0.035, 0, H, M['slat'])

# balcão em L de mármore (bar com cascata + buffet junto à parede)
box('balcao_bar', 1.45, 4.7, 7.0, 7.45, 0.0, 1.0, M['marble'])
box('balcao_buffet', 4.15, 4.7, 4.3, 7.0, 0.0, 0.92, M['marble'])
box('balcao_base', 4.18, 4.68, 4.3, 7.0, 0.0, 0.1, M['black'])
# banquetas de madeira
for x in (1.95, 2.55, 3.15, 3.75):
    cyl('banqueta_assento', x, 6.72, 0.72, 0.76, 0.2, M['wood'])
    box('banqueta_encosto', x - 0.17, x + 0.17, 6.53, 6.56, 0.76, 0.95, M['wood'], bevel=0.01)
    for (px_, py_) in ((-0.13, -0.13), (0.13, -0.13), (-0.13, 0.13), (0.13, 0.13)):
        o = box('banqueta_pe', x + px_ - 0.015, x + px_ + 0.015, 6.72 + py_ - 0.015, 6.72 + py_ + 0.015, 0, 0.72, M['wood'])
    box('apoio_pe', x - 0.14, x + 0.14, 6.83, 6.86, 0.28, 0.3, M['wood'])
# objetos no balcão
cyl('xicara', 2.2, 7.2, 1.0, 1.07, 0.04, M['pot'])
cyl('cafeteira', 3.4, 7.2, 1.0, 1.2, 0.06, M['steel'])
cyl('vaso_buffet', 4.42, 5.3, 0.92, 1.25, 0.08, M['ceramic'])
for k in range(8):
    sphere('folha_buffet', 4.42 + random.uniform(-0.1, 0.1), 5.3 + random.uniform(-0.12, 0.12), 1.3 + k * 0.05, 0.08, M['leaf'], scale=(1.6, 0.5, 0.1))

# pendentes de vidro sobre o bar
glass_amber = mat('vidro_ambar', srgb('#f2d6a6'), 0.05, **{'Transmission Weight': 1.0, 'IOR': 1.45})
for x in (2.3, 3.4):
    cyl('fio', x, 7.22, 1.95, H, 0.004, M['black'])
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.11, radius2=0.05, depth=0.24, location=(x, -7.22, 1.83))
    c = bpy.context.active_object; c.data.materials.append(glass_amber); bpy.ops.object.shade_smooth()
    bpy.ops.object.light_add(type='POINT', location=(x, -7.22, 1.8))
    l = bpy.context.active_object; l.data.energy = 25; l.data.color = (1.0, 0.72, 0.45); l.data.shadow_soft_size = 0.03

# ================================================================== LUZ
# sol de fim de tarde entrando pela lateral (varanda gourmet)
bpy.ops.object.light_add(type='SUN', location=(10, 0, 10))
sun = bpy.context.active_object
sun.data.energy = 5.5
sun.data.angle = math.radians(1.5)
sun.data.color = (1.0, 0.86, 0.7)
sun.rotation_euler = (math.radians(62), 0, math.radians(75))

world = bpy.data.worlds.new('ceu'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (*srgb('#9ec3e6'), 1)
bg.inputs['Strength'].default_value = 2.2

# portais de luz nas esquadrias
def portal(loc, size, rot):
    bpy.ops.object.light_add(type='AREA', location=loc)
    p = bpy.context.active_object
    p.data.shape = 'RECTANGLE'; p.data.size = size[0]; p.data.size_y = size[1]
    p.data.cycles.is_portal = True
    p.rotation_euler = rot
portal((2.375, 0.05, 1.28), (4.3, 2.55), (math.radians(90), 0, 0))
portal((4.85, -2.575, 1.28), (3.4, 2.55), (math.radians(90), 0, math.radians(90)))

# spots embutidos no forro (luz quente 3000K)
spots = [(x, y) for x in (0.9, 2.2, 3.5) for y in (1.0, 2.4, 3.8)] + \
        [(x, 5.2) for x in (0.9, 3.3)] + [(x, 7.9) for x in (0.6, 1.8, 3.0, 4.2, 5.3)] + [(4.43, 4.8), (4.43, 6.0)]
for (x, y) in spots:
    cyl('spot_aro', x, y, H - 0.01, H, 0.045, M['black'])
    cyl('spot_led', x, y, H - 0.012, H - 0.01, 0.03, mat('led', (1, 1, 1), 0.5, **{'Emission Color': (1.0, 0.78, 0.55, 1), 'Emission Strength': 8.0}))
    bpy.ops.object.light_add(type='SPOT', location=(x, -y, H - 0.02))
    s = bpy.context.active_object
    s.data.energy = 40; s.data.color = (1.0, 0.8, 0.6)
    s.data.spot_size = math.radians(75); s.data.spot_blend = 0.6; s.data.shadow_soft_size = 0.02
bpy.ops.object.light_add(type='POINT', location=(TX, -TY, 2.02))
l = bpy.context.active_object; l.data.energy = 30; l.data.color = (1.0, 0.72, 0.45); l.data.shadow_soft_size = 0.1
bpy.ops.object.light_add(type='POINT', location=(3.68, -1.25, 1.05))
l = bpy.context.active_object; l.data.energy = 12; l.data.color = (1.0, 0.72, 0.45)
bpy.ops.object.light_add(type='POINT', location=(3.4, -3.35, 1.55))
l = bpy.context.active_object; l.data.energy = 15; l.data.color = (1.0, 0.72, 0.45)
bpy.ops.object.light_add(type='AREA', location=(3.85, -(KY1 - 0.3), 1.47))
l = bpy.context.active_object; l.data.energy = 30; l.data.size = 3.8; l.data.size_y = 0.08
l.data.color = (1.0, 0.78, 0.55); l.rotation_euler = (math.radians(180), 0, 0)

# ================================================================== CORTINAS (voil)
def curtain(x0, x1, y, z1=H - 0.02, axis='x', folds=18):
    L = abs(x1 - x0)
    bpy.ops.mesh.primitive_plane_add(size=1)
    o = bpy.context.active_object; o.name = 'voil'
    if axis == 'x':
        o.location = ((x0 + x1) / 2, -y, z1 / 2); o.rotation_euler = (math.radians(90), 0, 0)
    else:
        o.location = (y, -(x0 + x1) / 2, z1 / 2); o.rotation_euler = (math.radians(90), 0, math.radians(90))
    o.scale = (L, z1, 1)
    bpy.ops.object.transform_apply(scale=True)
    sub = o.modifiers.new('sub', 'SUBSURF'); sub.levels = 0
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.subdivide(number_cuts=folds * 4); bpy.ops.object.mode_set(mode='OBJECT')
    wave = o.modifiers.new('ondas', 'WAVE')
    wave.use_normal = True; wave.use_x = axis == 'x'; wave.use_y = axis != 'x'
    wave.height = 0.035; wave.width = L / folds; wave.narrowness = 1.2; wave.speed = 0
    o.data.materials.append(M['sheer'])
    return o
curtain(0.28, 0.95, 0.12)
curtain(3.8, 4.47, 0.12)
curtain(0.95, 1.55, 4.63, axis='y')
curtain(3.6, 4.2, 4.63, axis='y')
# trilho da cortina (cortineiro embutido)
box('cortineiro', -0.15, 4.75, 0.0, 0.2, H - 0.03, H, M['plaster_white'])

# ================================================================== RENDER
scene.render.engine = 'CYCLES'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'METAL'
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    scene.cycles.device = 'GPU'
except Exception as e:
    print('GPU indisponível, usando CPU:', e)
scene.cycles.samples = SAMPLES
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.02
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 10
scene.cycles.diffuse_bounces = 5
scene.cycles.glossy_bounces = 4
scene.cycles.transmission_bounces = 8
scene.cycles.transparent_max_bounces = 12
scene.cycles.sample_clamp_indirect = 8
scene.view_settings.view_transform = 'AgX'
try:
    scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    pass
scene.view_settings.exposure = 1.1
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_depth = '8'

def camera(name, loc, rot_deg, pano=False, lens=20):
    cd = bpy.data.cameras.new(name)
    if pano:
        cd.type = 'PANO'
        cd.panorama_type = 'EQUIRECTANGULAR'
    else:
        cd.lens = lens
    o = bpy.data.objects.new(name, cd); col.objects.link(o)
    o.location = (loc[0], -loc[1], loc[2])
    o.rotation_euler = tuple(math.radians(a) for a in rot_deg)
    return o

SHOTS = {
    # panoramas 360: câmera na altura dos olhos (1,60 m); yaw 90 = olhando para a fachada (y planta negativo)
    'living_360':  dict(loc=(1.95, 2.8, 1.6), rot=(90, 0, 90), pano=True),
    'cozinha_360': dict(loc=(2.9, 6.1, 1.6), rot=(90, 0, 90), pano=True),
    # perspectivas (para refinamento na Higgsfield e comparação)
    'living_persp':  dict(loc=(4.2, 4.6, 1.35), rot=(84, 0, 128), lens=16),
    'cozinha_persp': dict(loc=(0.9, 5.6, 1.4), rot=(80, 0, -145), lens=17),
}
for name, s in SHOTS.items():
    if ONLY and name not in ONLY:
        continue
    cam = camera(name, s['loc'], s['rot'], s.get('pano', False), s.get('lens', 20))
    scene.camera = cam
    if s.get('pano'):
        scene.render.resolution_x, scene.render.resolution_y = RES, RES // 2
    else:
        scene.render.resolution_x, scene.render.resolution_y = int(RES * 0.5), int(RES * 0.5 * 9 / 16)
    scene.render.resolution_percentage = 100
    scene.render.filepath = os.path.join(OUT, name + '.png')
    print('RENDER', name, scene.render.resolution_x, scene.render.resolution_y, flush=True)
    bpy.ops.render.render(write_still=True)

if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=SAVE)
print('FIM', flush=True)
