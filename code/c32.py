
# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json,time
from witness_table import circulant,certify
from bb_tools import *
t1=time.time(); n,E=circulant(32,(1,5)); F=flow_poly(n,E); P,r=pdivmod(F,[-1,1]); _require_v03((not r), 'Validation failed in c32.py: 4'); P=[int(c) for c in P]
c=certify(P)
row={'name':'C32(1,5)','n':n,'m':len(E),'edges':E,'flow_coefficients_ascending':F,'P_coefficients_ascending':P,**c,'seconds':round(time.time()-t1,1)}
json.dump(row,open('/home/claude/bunkbed/v02/data/witness_C32.json','w'),indent=1)
print(row['name'],row['roots_float'],row['certified_negative'],row['seconds'])
