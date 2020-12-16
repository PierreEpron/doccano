import json
from pathlib import Path

lines = [json.loads(line) for line in Path('fixtures/prez.jsonl').read_text(encoding='ascii').split('\n')]
Path('fixtures/prez_an.jsonl').write_text('\n'.join([json.dumps(line) for line in lines]), encoding='utf-8')