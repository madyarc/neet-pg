"""set one landmark's view + pixel: edit.py <file> <name> <dir> <x> <y>  (then re-run bone_views.py pick)"""
import json, sys
f, name, d, x, y = sys.argv[1:6]
L = json.load(open(f)); it = next((i for i in L if i['name'] == name), None)
if not it: it = {'name': name}; L.append(it)
it.update(dir=d, xy=[int(x), int(y)]); it.pop('p', None)
json.dump(L, open(f, 'w'), indent=1)
