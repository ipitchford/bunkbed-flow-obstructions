"""Reconstruct a flow polynomial twice and verify its negative interval.
C++ enumerates subsets and colour partitions. Python uses exact integers and
fractions to reconstruct the polynomials and check a Bernstein certificate.
The optional --python-partitions flag avoids C++ for the colour enumeration.
"""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json,subprocess,tempfile,sys,time,os
from pathlib import Path
from fractions import Fraction as F
from math import comb
from collections import Counter

def add(a,b):
    out=[0]*max(len(a),len(b))
    for i,v in enumerate(a):out[i]+=v
    for i,v in enumerate(b):out[i]+=v
    return out

def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):out[i+j]+=u*v
    return out

def value(a,q):
    s=F(0)
    for c in reversed(a):s=s*q+c
    return s

def python_partition_histogram(n,edges):
    prior=[0]*n
    for a,b in edges:
        a,b=sorted((a,b));prior[b]|=1<<a
    hist=Counter();blocks=[0]*n
    def rec(i,r,h):
        if i==n:hist[r,h]+=1;return
        for b in range(r):
            z=(prior[i]&blocks[b]).bit_count();blocks[b]|=1<<i
            rec(i+1,r,h+z);blocks[b]^=1<<i
        blocks[r]=1<<i;rec(i+1,r+1,h);blocks[r]=0
    rec(0,0,0);return hist

def run():
    root=Path(__file__).resolve().parents[1];w=json.load(open(root/'certificates/flow_witness.json'))
    n=w['n'];E=w['edges'];m=len(E);word=w['word'];expected=w['flow_coefficients']
    _require_v03((len({tuple(sorted(e)) for e in E})==m), 'Validation failed in verify_flow.py: 45')
    _require_v03((Counter(tuple(sorted((word[i],word[(i+1)%m]))) for i in range(m))==Counter(tuple(sorted(e)) for e in E)), 'Validation failed in verify_flow.py: 46')
    _require_v03(([sum(i in e for e in E) for i in range(n)]==[4]*n), 'Validation failed in verify_flow.py: 47')
    text=f'{n} {m}\n'+''.join(f'{a} {b}\n' for a,b in E)
    with tempfile.TemporaryDirectory() as d:
        exe=Path(d)/'enumerate_flow'
        subprocess.run([os.environ.get('CXX','c++'),'-O3','-std=c++17',str(root/'code/enumerate_flow.cpp'),'-o',str(exe)],check=True)
        sub=subprocess.check_output([str(exe),'subsets'],input=text,text=True)
        co=[0]*(m+1)
        for line in sub.splitlines():i,c=map(int,line.split());co[i]=c
        if '--python-partitions' in sys.argv:hist=python_partition_histogram(n,E)
        else:
            part=subprocess.check_output([str(exe),'partitions'],input=text,text=True)
            hist={(int(r),int(h)):int(c) for r,h,c in map(str.split,part.splitlines())}
    while co and co[-1]==0:co.pop()
    _require_v03((co==expected), 'Validation failed in verify_flow.py: 60')
    fallings=[[1]]
    for r in range(1,n+1):fallings.append(mul(fallings[-1],[-(r-1),1]))
    numerator=[0]
    for (r,h),count in hist.items():
        term=mul(fallings[r],[comb(h,j)*(-1)**(h-j) for j in range(h+1)])
        term=[v*count*(-1)**(m-h) for v in term];numerator=add(numerator,term)
    _require_v03((numerator[:n]==[0]*n), 'Validation failed in verify_flow.py: 67')
    other=numerator[n:]
    while other and other[-1]==0:other.pop()
    _require_v03((other==expected), 'Validation failed in verify_flow.py: 70')
    _require_v03((sum(hist.values())==4213597), 'Validation failed in verify_flow.py: 71')
    # Exact division F(q)/(q-1).
    P=[0]*(len(co)-1);P[-1]=co[-1]
    for k in range(len(P)-2,-1,-1):P[k]=co[k+1]+P[k+1]
    _require_v03((mul(P,[-1,1])==co), 'Validation failed in verify_flow.py: 75')
    a,b=F(21,10),F(9,4);d=len(P)-1
    # Power coefficients of P(a+(b-a)z), then Bernstein coefficients.
    power=[sum(F(P[j])*comb(j,k)*a**(j-k)*(b-a)**k for j in range(k,d+1)) for k in range(d+1)]
    bern=[sum(power[j]*F(comb(k,j),comb(d,j)) for j in range(k+1)) for k in range(d+1)]
    _require_v03((all(c<0 for c in bern)), 'Validation failed in verify_flow.py: 80')
    # Verify change of basis by reconstruction, not just formula evaluation.
    recon=[F(0)]*(d+1)
    for k,c in enumerate(bern):
        for j in range(d-k+1):recon[k+j]+=c*comb(d,k)*comb(d-k,j)*(-1)**j
    _require_v03((recon==power), 'Validation failed in verify_flow.py: 85')
    _require_v03((value(co,a)==F(-20868388946779,10**13)), 'Validation failed in verify_flow.py: 86')
    _require_v03((value(co,b)==F(-57285175,67108864)), 'Validation failed in verify_flow.py: 87')
    return {'status':'PASS','edge_subsets_enumerated':2**m,'vertex_partitions_enumerated':sum(hist.values()),
            'independent_polynomials_agree':True,'flow_coefficients_ascending':co,
            'quotient_coefficients_ascending':P,'negative_interval':['21/10','9/4'],
            'bernstein_coefficients':[str(c) for c in bern],
            'flow_at_21_10':str(value(co,a)),'flow_at_9_4':str(value(co,b)),
            'histogram':[[r,h,c] for (r,h),c in sorted(hist.items())]}
if __name__=='__main__':
    start=time.time();receipt=run();receipt['elapsed_seconds']=time.time()-start
    print(json.dumps(receipt,indent=2))
