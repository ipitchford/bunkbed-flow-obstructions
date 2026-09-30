"""Driver: annealing search for Eulerian words with negative flow values above 2."""
import sys, json, time, random, numpy as np
from flowsearch import *
tag=sys.argv[1]; ts=[int(a) for a in sys.argv[2].split(',')]; seed=int(sys.argv[3])
targets=[float(a) for a in sys.argv[4].split(',')]
steps=int(sys.argv[5]) if len(sys.argv)>5 else 3000
rng=random.Random(seed)
grid=np.round(np.arange(2.005,6.0,0.005),3)
out=[]; t0=time.time()
def log(s):
    print(s,flush=True)
for t in ts:
    for m in sorted({2*t,2*t+2,2*t+4,3*t}):
        for q0 in targets:
            for restart in range(2):
                (f,w),found=anneal(t,m,q0,rng,steps=steps,grid=grid,log=log)
                log(f"t={t} m={m} q0={q0} restart={restart}: best F(q0)={f:.4g} word={w} ({time.time()-t0:.0f}s)")
                for (ww,lo,hi) in found:
                    out.append({'t':t,'m':m,'q0':q0,'word':ww,'grid_neg_lo':lo,'grid_neg_hi':hi})
                if f<0: out.append({'t':t,'m':m,'q0':q0,'word':w,'F_q0':f,'best':True})
                json.dump(out,open(f'/home/claude/bunkbed/v02/data/flowsearch_{tag}.json','w'),indent=1)
log("done")
