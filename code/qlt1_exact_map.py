import json,time
from fractions import Fraction as Fr
from qlt1_exact import G_exact
t0=time.time(); out={}
qs=[Fr(k,20) for k in range(1,20)]
xs=[Fr(1,100),Fr(1,10),Fr(1,4),Fr(1,2),Fr(1),Fr(2),Fr(4),Fr(10),Fr(100),Fr(1000)]
for name,w in [('2C3',[0,1,2]*2),('6C3',[0,1,2]*6),('10C3',[0,1,2]*10)]:
    grid=[]
    for q in qs:
        row=[G_exact(w,q,x).sign() for x in xs]; grid.append(row)
        print("%-5s q=%5s  %s"%(name,q,''.join({1:'+',-1:'-',0:'0'}[s] for s in row)),flush=True)
    # boundary q0(x) by bisection (exact signs), assuming sign changes once in q
    bounds={}
    for x in xs:
        lo,hi=Fr(1,100),Fr(99,100)
        if G_exact(w,hi,x).sign()>=0: bounds[str(x)]=None; continue
        if G_exact(w,lo,x).sign()<0: bounds[str(x)]='<0.01'; continue
        for _ in range(12):
            mid=(lo+hi)/2
            if G_exact(w,mid,x).sign()<0: hi=mid
            else: lo=mid
        bounds[str(x)]=[str(lo),str(hi)]
    print(name,"boundary q0(x) brackets:",{k:(v if not isinstance(v,list) else "%.4f-%.4f"%(float(Fr(v[0])),float(Fr(v[1])))) for k,v in bounds.items()},flush=True)
    out[name]={'qs':[str(q) for q in qs],'xs':[str(x) for x in xs],'signs':grid,'boundary_brackets':bounds}
json.dump(out,open('/home/claude/bunkbed/v02/data/qlt1_exact_map.json','w'),indent=1)
print("elapsed %.0fs"%(time.time()-t0))
