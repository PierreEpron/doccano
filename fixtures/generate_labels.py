import json
from pathlib import Path


items = [json.loads(line) for line in Path('fixtures/crs_ents.jsonl').read_text(encoding='utf-8').split('\n')]
labels = []
for item in items:
    for label in item['labels']:
        labels.append(label[2])

labels = list(set(labels))
keys = '0123456789abcdefghijklmnopqrstuvwxyz'
colors = []


Path('fixtures/crs_ents_labels.json').write_text(json.dumps([{
    "text": labels[i],
    "suffix_key": keys[i],
    "background_color": "#FF0000",
    "text_color": "#ffffff"
} for i in range(len(labels))]), encoding='utf-8')
'#%02x%02x%02x' % (0, 128, 64)