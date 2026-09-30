"""Broader survey of Eulerian families: upper end of the negativity interval above 2."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json, time, sys, itertools
from fractions import Fraction as Fr
from bb_tools import *

def neg_above2(F):
    P,r=pdivmod(F,[-1,1]); _require_v03((not r), 'Validation failed in families3.py: 7')
    P=[int(c) for c in P]
    negs,roots=negative_intervals(P,Fr(2),Fr(20),eps=Fr(1,10**9))
    return [(float(a),float(b)) for a,b in negs]

def circulant(n,S):
    E=set()
    for i in range(n):
        for s in S:
            j=(i+s)%n
            if j!=i: E.add((min(i,j),max(i,j)))
    return n,sorted(E)
def torus(a,b):
    idx=lambda i,j:(i%a)*b+(j%b)
    E=set()
    for i in range(a):
        for j in range(b):
            E.add(tuple(sorted((idx(i,j),idx(i+1,j))))); E.add(tuple(sorted((idx(i,j),idx(i,j+1)))))
    return a*b,sorted(E)
def lex2(n,S):   # C_n(S)[2 independent copies]: each edge -> K_{2,2}
    _,E=circulant(n,S); out=[]
    for a,b in E:
        for u in (0,1):
            for v in (0,1): out.append((2*a+u,2*b+v))
    return 2*n,out
def cycle_bundle(n,k): # C_n with every edge k-fold (k even => Eulerian)
    return n,[(i,(i+1)%n) for i in range(n)]*k
def K4_times_Cn(n):  # K4 x C_n (degree 3+2=5 odd) -> skip; use K5 x C_n? degree 4+2=6
    E=[]
    for i in range(n):
        for a in range(5):
            for b in range(a+1,5): E.append((5*i+a,5*i+b))
            E.append((5*i+a,5*((i+1)%n)+a))
    return 5*n,E
def wheel_double_all(n):  # hub+cycle, all edges doubled -> Eulerian (deg 6 rim, 2n hub)
    E=[]
    for i in range(n): E+= [(i,(i+1)%n)]*2 + [(i,n)]*2
    return n+1,E
def moebius_kantor_like(n,k): return circulant(n,(1,k))
def cube_dual(n): return None

rows=[]
def do(name,n,E,tlim=400):
    t1=time.time()
    try:
        F=flow_poly(n,E)
    except Exception as e:
        print(name,'fail',e); return
    negs=neg_above2(F); up=max([b for a,b in negs],default=None)
    rows.append({'family':name,'n':n,'m':len(E),'neg_intervals':negs})
    print("%-26s n=%2d m=%3d  neg>2: %s (%.1fs)"%(name,n,len(E),[(round(a,4),round(b,4)) for a,b in negs],time.time()-t1),flush=True)

for n in (16,20,24,28,32):
    do(f'C{n}(2,3)',*circulant(n,(2,3)))
for n in (20,22,24,26,28):
    do(f'C{n}(1,5)',*circulant(n,(1,5)))
for n in (16,18,20,24):
    do(f'C{n}(2,5)',*circulant(n,(2,5)))
    do(f'C{n}(3,4)',*circulant(n,(3,4)))
    do(f'C{n}(1,7)',*circulant(n,(1,7)))
    do(f'C{n}(3,5)',*circulant(n,(3,5)))
for n in (12,14,16,18,20):
    do(f'C{n}(1,2,3)',*circulant(n,(1,2,3)))
    do(f'C{n}(1,3,5)',*circulant(n,(1,3,5)))
for a,b in ((3,4),(3,6),(4,4),(3,8),(4,6),(4,8),(5,6),(6,6)):
    do(f'torus C{a}xC{b}',*torus(a,b))
for n in (6,8,10,12):
    do(f'lex C{n}[2]',*lex2(n,(1,)))
for n in (5,7,9):
    do(f'lex C{n}(1,2)[2]? deg8',*lex2(n,(1,2)))
for n in (5,6,7,8,9,10):
    do(f'wheel W{n} all doubled',*wheel_double_all(n))
for n in (3,4,5,6):
    do(f'K5 x C{n}',*K4_times_Cn(n))
json.dump(rows,open('/home/claude/bunkbed/v02/data/families3.json','w'),indent=1)
