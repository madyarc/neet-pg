"""Pivots and axes for the moving joints of the lower-limb joints page, fitted to the bone surfaces.
usage: python -I ll_axes.py -> anatomy/models/ll-joints/motions.json (same format as general_axes.py).
Frame: BodyParts3D (mm; +x = body's left, +y = posterior, +z = up). The limb is the right one (x < 0).
Arcs show the kind of movement only, not normal ranges."""
import os
MODEL = 'll-joints'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fitlib.py')).read())

unit = lambda v: (np.asarray(v, float) / np.linalg.norm(v)).round(4).tolist()
R = lambda v: np.round(v, 2).tolist()
FOOT = ['talus', 'calcaneus', 'navicular', 'cun_med', 'cun_int', 'cun_lat', 'cuboid', 'mt1', 'mt2', 'mt3', 'mt4', 'mt5',
        'pp1', 'dp1', 'pp2', 'mp2', 'dp2', 'pp3', 'mp3', 'dp3', 'pp4', 'mp4', 'dp4', 'pp5', 'mp5', 'dp5']
SOFT_KNEE = ['medial_meniscus', 'lateral_meniscus']
M, info = {}, {}

# hip: ball and socket; centre of the femoral head
X = near('femur', 'hip', 4.0); c, r = sphere(X)
knee = P['femur'][P['femur'][:, 2] < P['femur'][:, 2].min() + 15].mean(0)
LEG = ['femur', 'patella', 'tibia', 'fibula'] + FOOT
M['hip'] = {'moving': LEG, 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-100, 20]},
    {'name': 'Abduction and adduction', 'axis': [0, 1, 0], 'arc': [-20, 40]},
    {'name': 'Medial and lateral rotation', 'axis': unit(c - knee), 'arc': [-35, 35]}]}
info['hip'] = f'femoral head sphere r={r:.1f} mm from {len(X)} vertices'

# knee: flexion centre fitted to the outline of the femoral condyles seen from the side (as in general_axes.py)
F = P['femur']; zmin = F[:, 2].min(); D = F[F[:, 2] < zmin + 45]; yc, zc = D[:, 1].mean(), zmin + 25
ang = np.degrees(np.arctan2(D[:, 2] - zc, D[:, 1] - yc)); rr = np.hypot(D[:, 2] - zc, D[:, 1] - yc)
X = np.array([D[m][rr[m].argmax()] for a0 in range(-90, 30, 6) for m in [(ang >= a0) & (ang < a0 + 6)] if m.any()])
c, r = circle(X, [1, 0, 0])
# the patella stays still: turning it with the tibia (or by a fraction of the angle) leaves it floating off the femur
M['knee'] = {'moving': ['tibia', 'fibula'] + FOOT + SOFT_KNEE, 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [0, 120]}]}
info['knee'] = f'condyle outline circle r={r:.1f} mm, {c[2] - zmin:.1f} mm above the lowest point'

# ankle: hinge; circle fitted to the trochlea of the talus (the surface facing the tibia) seen from the side
# (the facing surfaces alone give too small a circle: they include the malleolar facets), so the dome outline is used
T = P['talus']; zt = T[:, 2].max(); D = T[T[:, 2] > zt - 18]; yc, zc = D[:, 1].mean(), zt - 18
ang = np.degrees(np.arctan2(D[:, 2] - zc, D[:, 1] - yc)); rr = np.hypot(D[:, 2] - zc, D[:, 1] - yc)
X = np.array([D[m][rr[m].argmax()] for a0 in range(30, 150, 6) for m in [(ang >= a0) & (ang < a0 + 6)] if m.any()])
c, r = circle(X, [1, 0, 0])
M['ankle'] = {'moving': FOOT, 'pivot': R(c), 'moves': [
    {'name': 'Dorsiflexion and plantarflexion', 'axis': [1, 0, 0], 'arc': [-20, 45]}]}
info['ankle'] = f'talar dome outline circle r={r:.1f} mm from {len(X)} points'

# subtalar + transverse tarsal: inversion and eversion of the foot below the talus. The axis is placed schematically:
# through the talocalcaneal contact, rising forwards and medially (approximate)
X = near('talus', 'calcaneus', 3.0); c = X.mean(0)
M['subtalar'] = {'moving': [k for k in FOOT if k != 'talus'], 'pivot': R(c), 'moves': [
    {'name': 'Inversion and eversion', 'axis': unit([0.2, -0.71, 0.67]), 'arc': [-15, 25]}]}
info['subtalar'] = f'talocalcaneal contact {len(X)} vertices'

# metatarsophalangeal joint of the big toe
X = near('mt1', 'pp1', 4.0); c, r = sphere(X)
M['mtp'] = {'moving': ['pp1', 'dp1'], 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-60, 30]}]}
info['mtp'] = f'head of 1st metatarsal sphere r={r:.1f} mm from {len(X)} vertices'

json.dump({'note': 'written by tools/joints/ll_axes.py; pivots fitted to the joint surfaces (approximate); '
                   'arcs show the kind of movement only, not normal ranges', 'motions': M},
          open(os.path.join(OUT, 'motions.json'), 'w'), indent=1)
for k, v in info.items(): print(k, v, M[k]['pivot'])
