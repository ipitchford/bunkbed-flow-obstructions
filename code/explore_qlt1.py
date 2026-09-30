"""q<1 exploration: exact conditioned-post numerators of fan chains at finite L.
Any negative value is, via the (q>0) amplification lemma, a certified
counterexample at that (p,q) on a finite simple full bunkbed graph."""
import json,time
from fractions import Fraction as Fr
from bb_tools import *
rows=[]; t0=time.time()
for wd in ([0,1,2]*2,[0,1,2]*4):
    for q in (Fr(3,10),Fr(1,2),Fr(7,10),Fr(9,10)):
        for x in (Fr(1,4),Fr(1,2),Fr(1),Fr(2),Fr(4)):
            signs=[]
            for L in range(1,9):
                N=core_numerator(wd,L,q,x); signs.append(int(N>0)-int(N<0))
            rows.append({'word':wd,'q':str(q),'x':str(x),'signs_L1_8':signs})
            print("word len %2d q=%s x=%s signs(L=1..8): %s (%.0fs)"%(len(wd),q,x,signs,time.time()-t0),flush=True)
json.dump(rows,open('/home/claude/bunkbed/v02/data/explore_qlt1.json','w'),indent=1)
