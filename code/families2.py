
# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json, time, sys
from fractions import Fraction as Fr
from bb_tools import *
import numpy as np

def roots_interval(F):
    """exact: largest certified negative interval of F above 2 (rational bounds), via root isolation of F/(q-1)"""
    P,r=pdivmod(F,[-1,1]); _require_v03((not r), 'Validation failed in families2.py: 8')
    P=[int(c) for c in P]
    negs,roots=negative_intervals(P,Fr(2),Fr(20),eps=Fr(1,10**12))
    return [(float(a),float(b)) for a,b in negs], [float((a+b)/2) for a,b in roots if a>=2]

def complete_bip(a,b):
    return a+b,[(i,a+j) for j in range(b) for i in range(a)]   # right-vertex-major order keeps frontier small
def circulant(n,S):
    E=[]
    for i in range(n):
        for s in S:
            j=(i+s)%n; E.append((min(i,j),max(i,j)))
    E=sorted(set(E)); return n,E

rows=[]
def do(name,n,E):
    t1=time.time(); F=flow_poly(n,E); negs,rts=roots_interval(F)
    rows.append({'family':name,'n':n,'m':len(E),'neg_intervals':negs,'roots_above_2':rts,'F':F})
    print("%-22s n=%2d m=%3d  neg: %s  roots>2: %s (%.1fs)"%(name,n,len(E),[(round(a,5),round(b,5)) for a,b in negs],[round(x,5) for x in rts],time.time()-t1),flush=True)

for b in (6,8,10,12,14,16,20):
    do(f'K4,{b}',*complete_bip(4,b))
for b in (6,8,10,12):
    do(f'K6,{b}',*complete_bip(6,b))
for b in (8,10):
    do(f'K8,{b}',*complete_bip(8,b))
for n in (14,16,18,20,24,28):
    do(f'C{n}(1,3)',*circulant(n,(1,3)))
for n in (14,16,18,20):
    do(f'C{n}(2,3)',*circulant(n,(2,3)))
for n in (16,18,20):
    do(f'C{n}(1,5)',*circulant(n,(1,5)))
json.dump(rows,open('/home/claude/bunkbed/v02/data/families2.json','w'),indent=1)
