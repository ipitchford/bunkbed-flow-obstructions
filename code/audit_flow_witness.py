"""Independent (third-algorithm) recomputation of the 12-vertex witness flow
polynomial, its Bernstein certificate on [21/10, 9/4], and exact isolation of
its real roots to obtain the maximal certified negativity interval."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json, time, sys
from fractions import Fraction as Fr
from math import comb
from bb_tools import *

ROOT = '/home/claude/bunkbed/v01/evidence_press_bunkbed_v0_1'
w = json.load(open(f'{ROOT}/certificates/flow_witness.json'))
t0 = time.time()
word = w['word']; edges = [tuple(e) for e in w['edges']]
n = w['n']; m = len(edges)
# structural checks
from collections import Counter
deg = Counter(); [deg.update(e) for e in edges]
_require_v03((set(deg.values()) == {4} and len(deg) == 12 and m == 24), 'Validation failed in audit_flow_witness.py: 17')
_require_v03((len(set(tuple(sorted(e)) for e in edges)) == 24), 'Validation failed in audit_flow_witness.py: 18')  # simple
wedges = Counter(tuple(sorted((word[i], word[(i+1) % m]))) for i in range(m))
_require_v03((wedges == Counter(tuple(sorted(e)) for e in edges)), 'Validation failed in audit_flow_witness.py: 20')
F = flow_poly(n, edges)
F2 = flow_poly_from_word(word)
_require_v03((F == F2), 'Validation failed in audit_flow_witness.py: 23')
print("frontier-DP flow polynomial (ascending):", F)
print("matches v0.1 coefficient vector:", F == w['flow_coefficients'])
P, r = pdivmod(F, [-1, 1])
_require_v03((not r), 'Validation failed in audit_flow_witness.py: 27')
P = [int(c) for c in P]
print("P = F/(q-1):", P)
# values
for q in (Fr(21,10), Fr(9,4), Fr(2), Fr(3)):
    print(f"F({q}) = {peval(F,q)}")
# Bernstein on [21/10, 9/4]
a, b = Fr(21,10), Fr(9,4); d = len(P)-1
power = [sum(Fr(P[j])*comb(j,k)*a**(j-k)*(b-a)**k for j in range(k,d+1)) for k in range(d+1)]
bern = [sum(power[j]*Fr(comb(k,j),comb(d,j)) for j in range(k+1)) for k in range(d+1)]
print("Bernstein coefficients all negative:", all(c < 0 for c in bern))
# Exact real-root isolation of P
roots = isolate_real_roots(P, eps=Fr(1,10**30))
print("number of distinct real roots of P:", len(roots))
for (lo,hi) in roots:
    print("  root in (%s, %s]  ~ %.20f" % (lo, hi, float((lo+hi)/2)))
negs, _ = negative_intervals(P, Fr(0), Fr(10), eps=Fr(1,10**30))
print("certified negative sub-intervals of [0,10] for P (hence for F on q>1):")
for (lo,hi) in negs:
    print("  [%s, %s]  ~ [%.15f, %.15f]" % (lo,hi,float(lo),float(hi)))
# also confirm P>0 at integers 2..6 and positive far right
print("P at 2,3,4,5,6:", [peval(P,Fr(k)) for k in (2,3,4,5,6)])
# derivative-based first-order estimate at 2
print("F'(2) =", peval(pderiv(F),Fr(2)))
# sympy cross-check of real roots
import sympy
q = sympy.symbols('q')
Pq = sum(sympy.Integer(c)*q**i for i,c in enumerate(P))
sr = sympy.Poly(Pq, q).real_roots()
print("sympy real roots:", [sympy.N(x, 25) for x in sr])
out = {'flow_coefficients_ascending': F, 'P_coefficients_ascending': P,
       'bernstein_all_negative': all(c<0 for c in bern),
       'real_roots_isolating': [[str(lo),str(hi)] for lo,hi in roots],
       'real_roots_float': [float((lo+hi)/2) for lo,hi in roots],
       'certified_negative_intervals': [[str(lo),str(hi)] for lo,hi in negs],
       'F_prime_at_2': str(peval(pderiv(F),Fr(2))),
       'elapsed_seconds': time.time()-t0}
json.dump(out, open('/home/claude/bunkbed/v02/data/flow_witness_audit.json','w'), indent=1)
print("elapsed", time.time()-t0)
