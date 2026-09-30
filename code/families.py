"""Exact flow polynomials of structured Eulerian families; scan for negative
values above q=2."""
import json, time
from fractions import Fraction as Fr
from bb_tools import *
import numpy as np

def scan(F, lo=2.0, hi=6.0, step=0.002):
    qs=np.arange(lo+step,hi,step); vals=np.array([float(peval(F,Fr(round(q,6)))) for q in qs])
    neg=qs[vals<0]
    return (float(neg.min()),float(neg.max()),int(len(neg))) if neg.size else None

def wheel_edges(n, spoke_mult=2, rim_mult=1):
    # hub = n, rim 0..n-1
    E=[]
    for i in range(n):
        E += [(i,(i+1)%n)]*rim_mult
        E += [(i,n)]*spoke_mult
    return n+1,E

def antiprism(n):
    E=[]
    for i in range(n):
        E += [(i,(i+1)%n),(n+i,n+(i+1)%n),(i,n+i),(i,n+(i+1)%n)]
    return 2*n,E

def complete(n):
    return n,[(i,j) for i in range(n) for j in range(i+1,n)]

def complete_bip(a,b):
    return a+b,[(i,a+j) for i in range(a) for j in range(b)]

def circulant(n,S):
    E=set()
    for i in range(n):
        for s in S: E.add(tuple(sorted((i,(i+s)%n))))
    return n,sorted(E)

def cube_like(n,mult):  # n-cycle with each edge multiplied by mult (Eulerian if mult even) 
    return n,[(i,(i+1)%n) for i in range(n)]*mult

fams=[]
for n in range(3,10): fams.append((f'wheel W{n} doubled spokes', wheel_edges(n,2,1)))
for n in range(3,8): fams.append((f'wheel W{n} tripled spokes doubled rim', wheel_edges(n,3,2)))
for n in range(3,9): fams.append((f'antiprism A{n}', antiprism(n)))
for n in (5,7): fams.append((f'K{n}', complete(n)))
for a,b in ((2,2),(2,4),(4,4),(2,6),(4,6)): fams.append((f'K{a},{b}', complete_bip(a,b)))
for n,S in ((8,(1,2)),(8,(1,3)),(9,(1,2)),(9,(1,3)),(9,(1,4)),(10,(1,2)),(10,(1,3)),(10,(1,4)),(10,(2,3)),(11,(1,2)),(11,(1,3)),(11,(1,4)),(11,(1,5)),(12,(1,2)),(12,(1,3)),(12,(1,4)),(12,(1,5)),(12,(2,3)),(12,(2,5)),(12,(3,4)),(13,(1,5)),(13,(2,3)),(14,(1,3)),(14,(1,5))):
    fams.append((f'circulant C{n}{S}', circulant(n,S)))
res=[]
for name,(n,E) in fams:
    t1=time.time()
    try:
        F=flow_poly(n,E)
    except AssertionError as e:
        print(name,"skip",e); continue
    s=scan(F)
    res.append({'family':name,'n':n,'m':len(E),'neg_scan':s,'F':F})
    print("%-40s n=%2d m=%3d  negative on grid: %s  (%.1fs)"%(name,n,len(E),s,time.time()-t1),flush=True)
json.dump(res,open('/home/claude/bunkbed/v02/data/families_scan.json','w'),indent=1)
