import tomllib, json, os, sys, re
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'firs520','src','grf','lang','english.toml')
z=tomllib.load(open(SRC,'rb'))
def load(n,default=None):
    p=os.path.join(HERE,n)
    return json.load(open(p,encoding='utf-8')) if os.path.exists(p) else (default or {})
zc=load('zh520_cargo.json'); zi=load('zh520_ind.json'); zs=load('zh520_station.json'); zm=load('zh520_misc.json')
CODE=re.compile(r'\{[^{}]*\}')
def codes(s):
    out=[]
    for m in CODE.finditer(s or ''):
        if m.group(0).startswith('{P '): continue
        out.append(m.group(0))
    return sorted(out)
def unit(zh,name,en_unit):
    if not en_unit: return None
    if en_unit.startswith('{WEIGHT}'): return '{WEIGHT}'+name
    if en_unit.startswith('{VOLUME}'): return '{VOLUME}'+name
    m=re.match(r'^\{SIGNED_WORD\} (\w+)\{P 0 "" s\} of ',en_unit)
    if m:
        unitword={'sack':'袋','crate':'箱','bale':'捆','barrel':'桶','keg':'桶'}.get(m.group(1),m.group(1))
        return '{SIGNED_WORD}'+unitword+name
    return None
out=[]; miss=[]; bad=[]
for k,v in z.items():
    if not isinstance(v,dict): continue
    en=v.get('base')
    if en is None: continue
    zh=None
    if k=='STR_GRF_NAME': zh='FIRS 产业替换包'
    elif k in zi: zh=zi[k]
    elif k in zs: zh=zs[k]
    elif k in zm: zh=zm[k]
    elif k.startswith('STR_CARGO_NAME_') or k.startswith('STR_CARGO_UNIT_') or k.startswith('STR_CID_'):
        cid=k[len('STR_CARGO_NAME_'):] if k.startswith('STR_CARGO_NAME_') else (k[len('STR_CARGO_UNIT_'):] if k.startswith('STR_CARGO_UNIT_') else k[len('STR_CID_'):])
        ent=zc.get(cid)
        if ent: zh = ent[0] if k.startswith('STR_CARGO_NAME_') else (unit(ent[0],ent[0],en) if k.startswith('STR_CARGO_UNIT_') else en)
        elif k.startswith('STR_CID_'): zh=en
    if zh is None:
        miss.append(k); continue
    if codes(en)!=codes(zh): bad.append((k,en,zh)); continue
    out.append((k,zh))
with open(os.path.join(os.path.dirname(SRC),'schinese.toml'),'w',encoding='utf-8',newline='\n') as f:
    f.write('[GLOBAL_PRAGMA]\ngrflangid = "0x56"\nplural = "0"\n')
    for k,zh in out:
        f.write('\n[%s]\nbase = %s\n' % (k, json.dumps(zh,ensure_ascii=False)))
print('wrote',len(out),'missing',len(miss),'badcodes',len(bad))
for k,a,b in bad[:5]: print('BAD',k,a,'|',b)
