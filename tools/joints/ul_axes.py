"""Pivots and axes for the moving joints of the upper-limb joints page, fitted to the bone surfaces.
usage: python -I ul_axes.py -> anatomy/models/ul-joints/motions.json (same format as general_axes.py).
Frame: BodyParts3D (mm; +x = body's left, +y = posterior, +z = up). The limb is the right one (x < 0).
Arcs show the kind of movement only, not normal ranges."""
import os
MODEL = 'ul-joints'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fitlib.py')).read())

unit = lambda v: (np.asarray(v, float) / np.linalg.norm(v)).round(4).tolist()
R = lambda v: np.round(v, 2).tolist()
FREE = ['humerus', 'radius', 'ulna'] + HAND          # the free limb
M, info = {}, {}

# sternoclavicular: the clavicle (with the scapula and the free limb) moves on the sternum
X = near('clavicle', ['manubrium', 'cc1_r'], 4.0); c = X.mean(0)
M['sternoclavicular'] = {'moving': ['clavicle', 'scapula'] + FREE, 'pivot': R(c), 'moves': [
    {'name': 'Elevation and depression', 'axis': [0, 1, 0], 'arc': [-5, 25]},
    {'name': 'Protraction and retraction', 'axis': [0, 0, 1], 'arc': [-15, 15]}]}
info['sternoclavicular'] = f'{len(X)} clavicle vertices facing the sternum'

# acromioclavicular: the scapula (with the free limb) glides and turns on the clavicle
X = near('scapula', 'clavicle', 3.0); c = X.mean(0)
M['acromioclavicular'] = {'moving': ['scapula'] + FREE, 'pivot': R(c), 'moves': [
    {'name': 'Rotation of the scapula', 'axis': [0, 1, 0], 'arc': [-12, 12]}]}
info['acromioclavicular'] = f'{len(X)} acromion vertices facing the clavicle'

# shoulder (glenohumeral): ball and socket; centre of the humeral head
X = near('humerus', 'scapula', 4.0); c, r = sphere(X)
elb = near('humerus', ['ulna', 'radius'], 5.0).mean(0)
M['shoulder'] = {'moving': FREE, 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-90, 40]},
    {'name': 'Abduction and adduction', 'axis': [0, 1, 0], 'arc': [-10, 90]},
    {'name': 'Medial and lateral rotation', 'axis': unit(c - elb), 'arc': [-60, 60]}]}
info['shoulder'] = f'humeral head sphere r={r:.1f} mm from {len(X)} vertices'

# elbow: hinge (humero-ulnar); forearm and hand move
X = near('humerus', ['ulna', 'radius'], 5.0); c, r = circle(X, [1, 0, 0])
M['elbow'] = {'moving': ['ulna', 'radius'] + HAND, 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-140, 0]}]}
info['elbow'] = f'trochlea circle r={r:.1f} mm'

# radio-ulnar: the radius (and hand) turns about the line from the radial head to the ulnar head
rz, uz = P['radius'][:, 2], P['ulna'][:, 2]
head = near('radius', 'ulna', 2.0); head = head[head[:, 2] > rz.max() - 30]
uh = near('ulna', 'radius', 2.0); uh = uh[uh[:, 2] < uz.min() + 30]
a, b = head.mean(0), uh.mean(0)
M['radioulnar'] = {'moving': ['radius'] + HAND, 'pivot': R(a), 'moves': [
    {'name': 'Pronation and supination', 'axis': unit(a - b), 'arc': [0, 150]}]}

# wrist: ellipsoid; the hand moves about the head of the capitate
cap = near('capitate', ['lunate', 'scaphoid'], 2.0).mean(0)
M['wrist'] = {'moving': HAND, 'pivot': R(cap), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-70, 60]},
    {'name': 'Abduction and adduction (radial and ulnar deviation)', 'axis': [0, 1, 0], 'arc': [-30, 15]}]}

# thumb carpometacarpal: saddle
X = near('trapezium', 'mc1', 1.5); c = X.mean(0)
l = pca(P['mc1'])[0]; l = l if l @ (P['mc1'].mean(0) - c) > 0 else -l
n = np.array([0, -1.0, 0])
abd = np.cross(l, n); abd /= np.linalg.norm(abd); flex = n - (n @ l) * l; flex /= np.linalg.norm(flex)
M['thumb'] = {'moving': ['mc1', 'pp1', 'dp1'], 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': unit(flex), 'arc': [-20, 35]},
    {'name': 'Abduction and adduction', 'axis': unit(abd), 'arc': [-5, 35]}]}

# metacarpophalangeal (index finger): head of the second metacarpal
X = near('mc2', 'pp2', 4.0); c, r = sphere(X)
M['mcp'] = {'moving': ['pp2', 'mp2', 'dp2'], 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-90, 20]},
    {'name': 'Abduction and adduction', 'axis': [0, 1, 0], 'arc': [-15, 20]}]}
info['mcp'] = f'head of 2nd metacarpal sphere r={r:.1f} mm from {len(X)} vertices'

# proximal interphalangeal (index finger): hinge
X = near('pp2', 'mp2', 4.0); c, r = circle(X, [1, 0, 0])
M['ip'] = {'moving': ['mp2', 'dp2'], 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-100, 0]}]}
info['ip'] = f'head of proximal phalanx circle r={r:.1f} mm from {len(X)} vertices'

json.dump({'note': 'written by tools/joints/ul_axes.py; pivots fitted to the joint surfaces (approximate); '
                   'arcs show the kind of movement only, not normal ranges', 'motions': M},
          open(os.path.join(OUT, 'motions.json'), 'w'), indent=1)
for k, v in info.items(): print(k, v, M[k]['pivot'])
