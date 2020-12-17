import json, glob
from pathlib import Path

import chardet

# print(Path('fixtures/txt/brain_0.txt').read_text(encoding='utf-8')[:500])
# print(chardet.detect(Path('fixtures/txt/brain_0.txt').read_bytes()))


# Path('fixtures/prez_an.jsonl').write_text('\n'.join([json.dumps(line) for line in lines]), encoding='utf-8')

inputs = glob.glob('fixtures/*.txt')
output =  'fixtures/txt'

for i in inputs:
    path = Path(i)
    print(path.name)
    (Path(output) / path.name).write_text(path.read_text(encoding='Windows-1252'), encoding='utf-8')