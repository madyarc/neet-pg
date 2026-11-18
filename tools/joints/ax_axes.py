"""Pivots and axes for the joints of the jaw, spine and pelvis page, fitted to the bone surfaces.
usage: python -I ax_axes.py -> anatomy/models/ax-joints/motions.json (format as general_axes.py; a move may also have
"glide": [x, y, z] mm per degree beyond "glideFrom" degrees, a translation added to the rotation: the jaw first turns, then its condyle glides forward).
Frame: BodyParts3D (mm; +x = body's left, +y = posterior, +z = up). Arcs show the kind of movement only."""
import os
MODEL = 'ax-joints'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fitlib.py')).read())

unit = lambda v: (np.asarray(v, float) / np.linalg.norm(v)).round(4).tolist()
R = lambda v: np.round(v, 2).tolist()
M, info = {}, {}
VERT = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7'] + ['t%d' % i for i in range(1, 13)] + ['l1', 'l2', 'l3', 'l4', 'l5']
DISCS = [k for k in P if k.startswith('disc_')]
SKULL = ['temporal_r', 'temporal_l', 'occipital', 'sphenoid', 'mandible']

# temporomandibular: the mandible turns about the line through both condyles and the condyles glide forward
cr = near('mandible', 'temporal_r', 3.0).mean(0); cl = near('mandible', 'temporal_l', 3.0).mean(0)
c = (cr + cl) / 2; ax = cl - cr
M['tmj'] = {'moving': ['mandible'], 'pivot': R(c), 'moves': [
    {'name': 'Opening and closing (depression and elevation)', 'axis': unit(ax), 'arc': [0, 25], 'glide': [0, -0.8, -0.2], 'glideFrom': 8},
    {'name': 'Protrusion and retraction', 'slide': [0, -1, 0], 'mm': 8}]}
info['tmj'] = f'condyles {np.round(cr, 1)} / {np.round(cl, 1)}'

# atlanto-occipital: the skull nods on the atlas, about a transverse line through the occipital condyles
X = near('occipital', 'c1', 3.0); c = X.mean(0); c[0] = 0.0   # on the midline (both condyles)
M['atlantooccipital'] = {'moving': SKULL, 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension (nodding)', 'axis': [1, 0, 0], 'arc': [-15, 15]}]}
info['atlantooccipital'] = f'occipital condyle contact {len(X)} vertices'

# atlanto-axial: the atlas (with the skull) turns about a vertical line through the dens
D = P['c2'][P['c2'][:, 2] > P['c2'][:, 2].max() - 12]
M['atlantoaxial'] = {'moving': ['c1'] + SKULL, 'pivot': R(D.mean(0)), 'moves': [
    {'name': 'Rotation (turning the head)', 'axis': [0, 0, 1], 'arc': [-35, 35]}]}

# intervertebral (L4 on L5): the column above the L4–L5 disc moves about the centre of the disc
c = P['disc_l4'].mean(0)
above = [v for v in VERT if v != 'l5'] + [d for d in DISCS if d not in ('disc_l4', 'disc_l5')]
M['lumbar'] = {'moving': above, 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-5, 8]},
    {'name': 'Lateral flexion', 'axis': [0, 1, 0], 'arc': [-6, 6]}]}

# sacro-iliac: the sacrum tips (nutation) about a transverse line through the joints (very small movement)
X = near('sacrum', ['hip', 'hip_l'], 4.0); c = X.mean(0); c[0] = 0.0   # on the midline (both joints)
M['sacroiliac'] = {'moving': ['sacrum', 'l5'], 'pivot': R(c), 'moves': [
    {'name': 'Nutation and counternutation (tipping of the sacrum)', 'axis': [1, 0, 0], 'arc': [-4, 4]}]}
info['sacroiliac'] = f'auricular contact {len(X)} vertices'

json.dump({'note': 'written by tools/joints/ax_axes.py; pivots fitted to the joint surfaces (approximate); '
                   'arcs show the kind of movement only, not normal ranges', 'motions': M},
          open(os.path.join(OUT, 'motions.json'), 'w'), indent=1)
for k, v in info.items(): print(k, v, M[k]['pivot'])
