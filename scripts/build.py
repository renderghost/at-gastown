"""Inject the event snapshot in data/ into src/town.template.html and write index.html."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(root / 'data/sprites.json'))
nos = json.load(open(root / 'data/nosprite.json'))
people = [{'h': p['handle'], 's': 'g' if p['status'] == 'going' else 'i', 'png': p['png']} for p in d['people']]
# RSVPs without a sprite aren't shown, so only their count goes in the page
ev = d['event']
ev['cid'] = 'bafyreicp23kbjrn6qrvfuzy5anrnjv64jk76f4lwptbxglws7nfeoth42a'
c = d['rsvpCounts']
data = {'event': ev, 'counts': {'going': c['going'], 'interested': c['interested'] + c.get('unknown', 0)},
        'withSprite': len(d['people']) + 1, 'fetchedAt': d['fetchedAt'],
        'hidden': len(nos),
        'me': {'h': d['me']['handle'], 'did': d['me']['did'], 'png': d['me']['png']}, 'people': people}
t = (root / 'src/town.template.html').read_text()
(root / 'index.html').write_text(t.replace('/*__DATA__*/null', json.dumps(data, separators=(',', ':'))))
print(f'index.html written: {len(people) + 1} people')
