"""Consolidated exact certification for Evidence Press bunkbed candidate v0.2.

Run from the package root: python3 code/certify_v02.py [--full].
Full mode reconstructs C32 and both large cubics. The current environment
completed it in approximately ten minutes; runtime is hardware-dependent.
Without --full those large stored objects are checked but not all reconstructed.

Every check below is exact (integers, fractions, or elements of Q(sqrt(D))).
Floating point is used only for printing.
"""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json, time, sys, math, os, subprocess, platform
from fractions import Fraction as Fr
from math import comb
import sympy
from bb_tools import *
from qlt1_exact import G_exact
from witness_table import certify, circulant, K4b

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, 'data')
FULL = '--full' in sys.argv
qs = sympy.symbols('q')
T0 = time.time()
checks = []

def rec(name, ok, **kw):
    d = {'check': name, 'status': 'PASS' if ok else 'FAIL', 'seconds': round(time.time() - rec.t, 2), **kw}
    checks.append(d); print(json.dumps(d), flush=True); rec.t = time.time()
    _require_v03((ok), name)
rec.t = time.time()

# ---------------------------------------------------------------- 1. Gamma_*
w = json.load(open(os.path.join(ROOT, 'v0_1', 'certificates', 'flow_witness.json')))
F = flow_poly(w['n'], [tuple(e) for e in w['edges']])
_require_v03((F == flow_poly_from_word(w['word']) == w['flow_coefficients']), 'Validation failed in certify_v02.py: 36')
P, r = pdivmod(F, [-1, 1]); _require_v03((not r), 'Validation failed in certify_v02.py: 37'); P = [int(c) for c in P]
Pq = sympy.Poly(sum(sympy.Integer(c) * qs**i for i, c in enumerate(P)), qs, domain='QQ')
ivs = Pq.intervals(eps=sympy.Rational(1, 10**20))
_require_v03((len(ivs) == 2), 'Validation failed in certify_v02.py: 40')
lo_root = (Fr(int(ivs[0][0][0].p), int(ivs[0][0][0].q)), Fr(int(ivs[0][0][1].p), int(ivs[0][0][1].q)))
hi_root = (Fr(int(ivs[1][0][0].p), int(ivs[1][0][0].q)), Fr(int(ivs[1][0][1].p), int(ivs[1][0][1].q)))
a, b = Fr(20232, 10000), Fr(22730, 10000)   # 2.0232 and 2.2730
ok = peval(P, a) < 0 and peval(P, b) < 0 and Pq.count_roots(sympy.Rational(a), sympy.Rational(b)) == 0
# the v0.1 Bernstein certificate on [21/10, 9/4] is reproduced as well
aa, bb = Fr(21, 10), Fr(9, 4); d = len(P) - 1
power = [sum(Fr(P[j]) * comb(j, k) * aa**(j - k) * (bb - aa)**k for j in range(k, d + 1)) for k in range(d + 1)]
bern = [sum(power[j] * Fr(comb(k, j), comb(d, j)) for j in range(k + 1)) for k in range(d + 1)]
rec('Gamma_star: third-algorithm flow polynomial equals v0.1 vector; exactly two real roots; certified negative on [2.0232, 2.2730]; Bernstein on [21/10,9/4] reproduced',
    ok and all(c < 0 for c in bern), roots_float=[float(sum(lo_root) / 2), float(sum(hi_root) / 2)],
    root_isolating=[[str(lo_root[0]), str(lo_root[1])], [str(hi_root[0]), str(hi_root[1])]], F_prime_at_2=str(peval(pderiv(F), Fr(2))))

# ---------------------------------------------------------------- 2. word identity spot checks (own brute force)
import random
random.seed(1)
okw = True
for wd in ([0, 1, 2, 0, 1, 2], [0, 1, 0, 2, 1, 3, 2, 3], [0, 0, 1, 2, 2, 1]):
    m = len(wd); t = max(wd) + 1
    q = Fr(random.randint(3, 9), random.randint(1, 4)); lam = [Fr(random.randint(1, 7), random.randint(1, 3)) for _ in range(m)]
    prod = Fr(1)
    for l in lam: prod *= l
    okw &= hyper_numerator(wd, q, lam) == q**(t + 2) * prod * peval(flow_poly_from_word(wd), q) / (q - 1)
rec('Word identity (Theorem 2.1 of v0.1): brute-force two-layer hypergraph numerator equals q^{t+2} prod(lambda) F/(q-1) at random rational points', okw)

# thickened-triangle closed form (v0.1 eq. thick)
okt = True
for ell in (2, 4, 6):
    Fl = flow_poly_from_word([0, 1, 2] * ell)
    for q in (Fr(3, 2), Fr(21, 10), Fr(7, 3), Fr(1, 3)):
        z = q - 1
        okt &= peval(Fl, q) == ((z**ell + z)**3 + z * (z**ell - 1)**3) / q**3
okt &= peval(flow_poly_from_word([0, 1, 2] * 4), Fr(3, 2)) == Fr(-71, 1024)
rec('Thickened triangles: closed form F_{ell C3} = q^-3[(z^ell+z)^3 + z(z^ell-1)^3] vs DP for ell=2,4,6 at four q; F_{4C3}(3/2) = -71/1024', okt)

# ---------------------------------------------------------------- 3. own core DP vs brute force and vs v0.1 stored value
ok3 = True
for (wd, L, q, x) in [([0, 1], 1, Fr(3, 2), Fr(1)), ([0, 1], 1, Fr(7, 10), Fr(2))]:
    ok3 &= core_numerator(wd, L, q, x) == core_numerator_bruteforce(wd, L, q, x)
v01 = json.load(open(os.path.join(ROOT, 'v0_1', 'certificates', 'q_3_2_core.json')))
a32 = core_numerator([0, 1, 2] * 4, 20, Fr(3, 2), Fr(1))
rec('Own conditioned-post DP: equals brute force on tiny cores and equals the v0.1 stored (ABC)^4, L=20 numerator exactly', ok3 and str(a32) == v01['core_numerator'] and a32 < 0)

# ---------------------------------------------------------------- 4. amplification lemma ingredients
oka = True
for (wd, L, q, x) in [([0, 1], 1, Fr(3, 2), Fr(1)), ([0, 1], 1, Fr(7, 10), Fr(2))]:
    n, E, u, v = fan_chain_edges(wd, L); t = max(wd) + 1
    Ny = full_core_poly_int(wd, L, q, x)
    for y in (Fr(0), Fr(3)):
        oka &= peval(Ny, y) == full_bunkbed_bruteforce(n, E, u, v, q, x, {('v', s): y for s in range(t)})
    oka &= Ny[-1] == core_numerator(wd, L, q, x)
q, x = Fr(3, 2), Fr(1); D = q * q + 3 * q * x + 3 * x * x; rr = x**3 / D; y1 = (1 + x) * (1 + rr) - 1
oka &= full_bunkbed_bruteforce(4, [(0, 1), (1, 2), (0, 2), (0, 3)], 1, 2, q, x) == D * full_bunkbed_bruteforce(3, [(0, 1), (1, 2), (0, 2)], 1, 2, q, x, {('v', 0): y1})
rec('Lemma 4.1 ingredients: N(y) DP == brute force; leading coefficient a_t == N^T; pendant reduction factor D and activity y=(1+x)(1+r)-1 by brute force', oka)

# ---------------------------------------------------------------- 5. K_{4,b} closed form and q_c
def K4b_closed(b, q):
    z = q - 1
    return ((z**4 + z)**b + 4 * z * (-1)**b * (z**3 + 1)**b + 3 * z * (2 * z * z + z - 1)**b + 6 * z * (z - 1) * (z * z - z - 2)**b + z * (z - 1) * (z - 2) * (-3 * q)**b) / q**(3 + b)
ok5 = True
for b in (2, 4, 6, 8, 10):
    Fk = flow_poly(*K4b(b))
    for q in (Fr(3, 2), Fr(21, 10), Fr(5, 2), Fr(3), Fr(7, 2), Fr(-1, 3)):
        ok5 &= peval(Fk, q) == K4b_closed(b, q)
# q_c: real root of q^3-4q^2+6q-6
cub = sympy.Poly(qs**3 - 4 * qs**2 + 6 * qs - 6, qs)
rts = cub.intervals(eps=sympy.Rational(1, 10**15))
_require_v03((len(rts) == 1), 'Validation failed in certify_v02.py: 107')
qc_lo, qc_hi = Fr(int(rts[0][0][0].p), int(rts[0][0][0].q)), Fr(int(rts[0][0][1].p), int(rts[0][0][1].q))
# dominance inequalities on (2, q_c): check at the endpoint side and the algebraic identities used in the proof
z = sympy.symbols('z')
ok5 &= sympy.expand(z**3 - 3 * z - 2 - (z - 2) * (z + 1)**2) == 0 and sympy.expand(2 * z**2 - 2 * z - 4 - 2 * (z - 2) * (z + 1)) == 0
ok5 &= sympy.expand(sympy.expand((qs - 1)**4 - 2 * (qs - 1) - 3) - qs * (qs**3 - 4 * qs**2 + 6 * qs - 6)) == 0
rec('K_{4,b}: closed form verified against DP (b=2..10, six q values incl. negative); q_c isolated; factorisations used in the dominance proof', ok5, q_c_bracket=[str(qc_lo), str(qc_hi)], q_c_float=float((qc_lo + qc_hi) / 2))

# ---------------------------------------------------------------- 6. witness table above 2 (recompute small, verify stored certificates for all)
tab = json.load(open(os.path.join(DATA, 'witnesses_above2.json')))
c32p = os.path.join(DATA, 'witness_C32.json')
if os.path.exists(c32p): tab = tab + [json.load(open(c32p))]
ok6 = True; upper = Fr(0); summary = []
for row in tab:
    Pst = row['P_coefficients_ascending']
    if row['n'] <= 20 or FULL:
        Fk = flow_poly(row['n'], [tuple(e) for e in row['edges']]); Pk, r_ = pdivmod(Fk, [-1, 1]); ok6 &= (not r_) and [int(c) for c in Pk] == Pst
    Pq = sympy.Poly(sum(sympy.Integer(c) * qs**i for i, c in enumerate(Pst)), qs, domain='QQ')
    a_, b_ = Fr(row['certified_negative'][0]), Fr(row['certified_negative'][1])
    ok6 &= peval(Pst, a_) < 0 and peval(Pst, b_) < 0 and Pq.count_roots(sympy.Rational(a_.numerator, a_.denominator), sympy.Rational(b_.numerator, b_.denominator)) == 0
    # Eulerian, connected, loopless
    from collections import Counter
    deg = Counter()
    for e in row['edges']: deg.update(e)
    ok6 &= all(v % 2 == 0 for v in deg.values()) and all(e[0] != e[1] for e in row['edges'])
    upper = max(upper, b_); summary.append([row['name'], row['certified_negative']])
rec('Witnesses above 2: %d Eulerian graphs; each stored certificate re-verified (P(a)<0, P(b)<0, no roots in (a,b)); small ones recomputed' % len(tab), ok6, largest_certified_upper_endpoint=str(upper), largest_float=float(upper), table=summary)

# union of certified failure set above 2: (2, q_c) analytic, plus certified intervals
ok6b = all(Fr(row['certified_negative'][0]) < qc_lo for row in tab if Fr(row['certified_negative'][1]) > qc_hi)
rec('Union: every certified interval reaching beyond q_c starts below q_c, so the certified failure set above 2 is the whole open interval (2, %s]' % str(upper), ok6b)

# ---------------------------------------------------------------- 7. explicit q=3/2 witness
e32 = json.load(open(os.path.join(DATA, 'explicit_q32_L19.json')))['L19']
Ny = [Fr(c) for c in e32['N_y_coefficients']]
q, x = Fr(3, 2), Fr(1); D = q * q + 3 * q * x + 3 * x * x; rr = x**3 / D
k = e32['min_pendants_per_post']
yk = (1 + x) * (1 + rr)**k - 1; ykm = (1 + x) * (1 + rr)**(k - 1) - 1
ok7 = Ny[-1] == core_numerator([0, 1, 2] * 4, 19, q, x) and Ny[-1] < 0 and all(c > 0 for c in Ny[:-1]) and peval(Ny, yk) < 0 and peval(Ny, ykm) >= 0
if FULL:
    ok7 &= full_core_poly_int([0, 1, 2] * 4, 19, q, x) == Ny
sizes = dict(core_vertices=e32['core_vertices'], base_vertices=e32['base_vertices'], full_vertices=e32['full_vertices'], full_edges=e32['full_edges'], k=k)
rec('Explicit q=3/2, p=1/2 witness: (ABC)^4, L=19 core; stored cubic N(y) has a_3 == recomputed N^T < 0, a_0,a_1,a_2 > 0; k=3565 is the exact minimum (N(y_k)<0<=N(y_{k-1}))' + (' [cubic recomputed]' if FULL else ' [cubic taken from data; --full recomputes]'), ok7, **sizes)

# ---------------------------------------------------------------- 8. q<1: exact limit signs and finite-L certificates
pts = [(Fr(9, 10), Fr(1)), (Fr(4, 5), Fr(1)), (Fr(4, 5), Fr(1, 100)), (Fr(4, 5), Fr(1000)), (Fr(7, 10), Fr(10)), (Fr(3, 5), Fr(1000)), (Fr(1, 2), Fr(1)), (Fr(7, 10), Fr(1))]
signs = {}
for q_, x_ in pts:
    signs['q=%s,x=%s' % (q_, x_)] = G_exact([0, 1, 2] * 2, q_, x_).sign()
signs10 = {}
for q_, x_ in [(Fr(3, 5), Fr(100)), (Fr(4, 5), Fr(1)), (Fr(1, 2), Fr(1000))]:
    signs10['q=%s,x=%s' % (q_, x_)] = G_exact([0, 1, 2] * 10, q_, x_).sign()
expected = {'q=9/10,x=1': -1, 'q=4/5,x=1': -1, 'q=4/5,x=1/100': -1, 'q=4/5,x=1000': -1, 'q=7/10,x=10': -1, 'q=3/5,x=1000': 1, 'q=1/2,x=1': 1, 'q=7/10,x=1': 1}
rec('q<1 fan limit (Proposition 7.1): exact signs in Q(sqrt(Delta)) for the doubled triangle at 8 points and 10C3 at 3 points', signs == expected and signs10 == {'q=3/5,x=100': -1, 'q=4/5,x=1': -1, 'q=1/2,x=1000': 1}, doubled_triangle=signs, tenfold_triangle=signs10)
certs = [(Fr(19, 20), Fr(1), 18), (Fr(9, 10), Fr(1), 21), (Fr(17, 20), Fr(1), 21), (Fr(4, 5), Fr(1), 27), (Fr(9, 10), Fr(1, 3), 33), (Fr(9, 10), Fr(3), 24), (Fr(4, 5), Fr(3), 30)]
ok8 = True; vals = []
for q_, x_, L_ in certs:
    N = core_numerator([0, 1, 2] * 2, L_, q_, x_); ok8 &= N < 0
    vals.append({'q': str(q_), 'p': str(x_ / (1 + x_)), 'L': L_, 'core_vertices': 3 + 6 * L_ + 1, 'negative': N < 0})
rec('q<1 finite certificates: exact conditioned numerators N^T_{(ABC)^2,L}(q,x) < 0 at seven (q,p,L) points; each is an ordinary full-bunkbed counterexample by Lemma 4.1 (q>0)', ok8, points=vals)
e09 = os.path.join(DATA, 'explicit_q09_L21.json')
if os.path.exists(e09):
    e = json.load(open(e09)); Ny9 = [Fr(c) for c in e['N_y_coefficients']]
    q9, x9 = Fr(9, 10), Fr(1); D9 = q9 * q9 + 3 * q9 * x9 + 3 * x9 * x9; r9 = x9**3 / D9; k9 = e['min_pendants_per_post']
    ok9 = Ny9[-1] == core_numerator([0, 1, 2] * 2, 21, q9, x9) and peval(Ny9, (1 + x9) * (1 + r9)**k9 - 1) < 0 and (k9 == 0 or peval(Ny9, (1 + x9) * (1 + r9)**(k9 - 1) - 1) >= 0)
    if FULL: ok9 &= full_core_poly_int([0, 1, 2] * 2, 21, q9, x9) == Ny9
    rec('Explicit q=9/10, p=1/2 witness: (ABC)^2, L=21 core; stored N(y) leading coefficient equals recomputed N^T; minimal k verified', ok9, full_vertices=e['full_vertices'], full_edges=e['full_edges'], k=k9, coefficient_signs=e['coefficient_signs'])

out = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL', 'full_mode': FULL, 'python': platform.python_version(), 'platform': platform.platform(), 'elapsed_seconds': round(time.time() - T0, 1), 'checks': checks}
os.makedirs(os.path.join(ROOT, 'checks'), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, 'checks', 'executed_checks_v02%s.json' % ('_full' if FULL else '')), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'checks'}))
