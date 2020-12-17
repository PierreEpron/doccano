import json, re, functools 
from pathlib import Path
from glob import glob

bp_0 = 'service de médecine nucléaire hôpital de brabois'
bp_1 = 'installation répertoriée sous le n'
re_bp = re.compile(rf'{bp_0}|{bp_1}', re.I)

cr_prefix =  '''Service de Médecine Nucléaire Hôpital de Brabois
Secrétariat prise de rendez-vous 03 83 15 39 11
Télécopie Demande dexamen IRM 03 83 15 38 39
Télécopie Demande dexamen MN 03 83 15 52 05
Télécopie Demande dexamen TEP 03 83 15 44 78
Vandoeuvre, le mercredi 30 septembre 2020
Professeur G. KARCHER	03 83 15 39 05
Professeur P.Y. MARIE	03 83 15 39 09
Professeur P. OLIVIER	03 83 15 76 31
Docteur A. VERGER 03 83 15 55 67
Docteur S. PARIS-GRANDPIERRE 03 83 15 40 36
Docteur F. ATLANI-NETTER 03 83 15 40 40
Docteur M. PERRIN 03 83 15 41 56
Docteur E. CHEVALIER 03 83 15 74 02
Docteur M.CLAUDIN 03 83 15 43 33
Installation répertoriée sous le n° M540008 Autorisation CODEP-STR-2020-037740					
VEREOS N° identification 900007 PHILIPS année 2017
AVCodes CCAM ZZQL016
'''

def construct_cr(content):
    #  return cr_prefix + re.sub(r'\n+', '\n', content)
    return re.sub(r'\n{3,}', '\n', content)

def skip(txt, storage):
    pass

def keep(txt, storage):
    storage.append(construct_cr(txt))

def keep_wo_refs(txt, storage):
    keep('\n\n'.join(txt.split('\n\n')[1:]), storage)

scrap_contents_funcs = {
    bp_0 : {
        '' : keep,
        bp_0 : keep,
        bp_1 : skip
    },
    bp_1 : {
        '' : keep_wo_refs,
        bp_0 : keep_wo_refs,
        bp_1 : keep_wo_refs
    }
}

def scrap_cr(txt):
    txt = re.sub(r'\n{3,}', '\n\n', txt)

    result = []
    
    last_i, current_i = 0, 0
    last_m, current_m = None, None
    while current_i < len(txt):
        current_m = re_bp.search(txt[current_i:])

        if current_m == None:
            end = step = len(txt)
            current_str = ''
        else:
            end = current_i + current_m.start()
            step = current_m.end()
            current_str = current_m.group(0).lower()
        
        if last_m != None:
            start = last_i + last_m.end()
            scrap_contents_funcs[last_m.group(0).lower()][current_str](txt[start:end], result)

        last_i = current_i
        last_m = current_m
        current_i += step

    return result    

paths = [path for path in glob('fixtures/txt/*.txt')]
txts = [Path(path).read_text(encoding='utf-8') for path in paths]
crs = functools.reduce(lambda a, b: a + b, [scrap_cr(txt) for txt in txts])
result = '\n'.join([json.dumps({'text':cr}) for cr in crs])
print(len(result.split('\n')))
Path('fixtures/jsonl/crs.jsonl').write_text(result, encoding='utf-8')