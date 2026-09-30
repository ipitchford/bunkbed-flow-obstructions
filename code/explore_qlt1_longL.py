import json,time,sys
from fractions import Fraction as Fr
from bb_tools import *
rows=[];t0=time.time()
wd=[0,1,2]*2
for q in (Fr(1,2),Fr(9,10)):
    for x in (Fr(1),Fr(1,3)):
        signs=[]
        for L in list(range(9,41,3)):
            N=core_numerator(wd,L,q,x); signs.append((L,int(N>0)-int(N<0)))
            print("q=%s x=%s L=%d sign=%+d (%.0fs)"%(q,x,L,signs[-1][1],time.time()-t0),flush=True)
        rows.append({'word':wd,'q':str(q),'x':str(x),'signs':signs})
json.dump(rows,open('/home/claude/bunkbed/v02/data/explore_qlt1_longL.json','w'),indent=1)
