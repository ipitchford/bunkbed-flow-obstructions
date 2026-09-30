import json,numpy as np,math,time
from qlt1_limit import G_limit
words={'2C3':[0,1,2]*2,'4C3':[0,1,2]*4,'6C3':[0,1,2]*6,'K4_2? (word 0102)':[0,1,0,2],'C5 doubled? (01234)x2':[0,1,2,3,4]*2}
qs=[0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.85,0.9,0.95,0.98]
xs=[0.05,0.1,0.25,0.5,1,2,4,10,50]
out={}
t0=time.time()
for name,w in words.items():
    tab=[]
    for q in qs:
        row=[]
        for x in xs:
            G=G_limit(w,q,x); row.append(G)
        tab.append(row)
        print("%-24s q=%.2f  signs over x=%s : %s"%(name,q,xs,''.join('-' if g<0 else '+' for g in row)),flush=True)
    out[name]={'qs':qs,'xs':xs,'G':tab}
json.dump(out,open('/home/claude/bunkbed/v02/data/qlt1_limit_map.json','w'),indent=1)
print("elapsed %.0fs"%(time.time()-t0))
