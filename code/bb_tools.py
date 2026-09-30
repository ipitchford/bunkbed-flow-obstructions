"""Independent exact tools for the random-cluster bunkbed audit (Evidence Press v0.2).

Everything here was written independently of the v0.1 scripts.  Only the Python
standard library, ``fractions`` and (optionally) ``sympy`` for root isolation
are used.  All polynomial arithmetic is exact integer/rational arithmetic.

Contents
--------
flow_poly            frontier (set-partition) dynamic programme for the flow
                     polynomial of a loopless multigraph -- a third algorithm,
                     distinct from the v0.1 edge-subset and vertex-partition
                     enumerations.
poly helpers         add/mul/eval/divide for integer coefficient lists.
sturm_*              exact Sturm-sequence root counting and isolation.
negative_intervals   certified rational sub-intervals on which a polynomial is
                     strictly negative.
hyper_numerator      brute-force signed numerator of the two-layer word
                     hypergraph at rational (q, lambda).
core_numerator       own frontier DP for the conditioned-post fan chain.
full_core_poly       own frontier DP for the full bunkbed core with the
                     designated verticals at symbolic activity y (polynomial in y).
"""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

from fractions import Fraction as Fr
from collections import defaultdict
from itertools import product
import sys

sys.set_int_max_str_digits(0)

# --------------------------------------------------------------------------
# Integer/rational polynomial helpers (coefficient lists, ascending degree)
# --------------------------------------------------------------------------

def padd(a, b):
    n = max(len(a), len(b))
    out = [0] * n
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] += v
    return out


def pmul(a, b):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        if u == 0:
            continue
        for j, v in enumerate(b):
            out[i + j] += u * v
    return out


def pscale(a, c):
    return [c * v for v in a]


def ptrim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def peval(a, q):
    s = Fr(0)
    for c in reversed(a):
        s = s * q + c
    return s


def pderiv(a):
    return [i * a[i] for i in range(1, len(a))]


def pdivmod(a, b):
    """Exact division over the rationals; returns (quotient, remainder)."""
    a = [Fr(v) for v in ptrim(a)]
    b = [Fr(v) for v in ptrim(b)]
    q = [Fr(0)] * max(0, len(a) - len(b) + 1)
    r = a[:]
    while len(r) >= len(b) and r:
        c = r[-1] / b[-1]
        d = len(r) - len(b)
        q[d] = c
        for i, v in enumerate(b):
            r[d + i] -= c * v
        r = ptrim(r)
    return ptrim(q), r


# --------------------------------------------------------------------------
# Set-partition utilities
# --------------------------------------------------------------------------

def canon(p):
    """Relabel a block-label tuple in order of first appearance."""
    d = {}
    return tuple(d.setdefault(x, len(d)) for x in p)


def merge_labels(p, i, j):
    a, b = p[i], p[j]
    if a == b:
        return p
    lo, hi = min(a, b), max(a, b)
    return canon(tuple(lo if x == hi else x for x in p))


# --------------------------------------------------------------------------
# Flow polynomial by frontier DP (third algorithm)
# --------------------------------------------------------------------------

def flow_poly(t, edges):
    """Flow polynomial F(q) = sum_B (-1)^{m-|B|} q^{|B| - t + k(B)} of the
    loopless multigraph on vertices 0..t-1 with the given edge list.

    Edges are processed one at a time.  A state is the partition of the
    *active* vertices (those still incident to an unprocessed edge) induced
    by the chosen edge subset, together with an integer polynomial weight in q.
    Choosing an edge multiplies by q and merges; omitting it multiplies by -1.
    When a vertex's last edge has been processed it leaves the frontier; if it
    was alone in its block, that component is complete and contributes q.
    """
    m = len(edges)
    remaining = [0] * t
    for a, b in edges:
        _require_v03((a != b), "loops not supported here (multiply by q-1 per loop)")
        remaining[a] += 1
        remaining[b] += 1
    # state: (tuple of active vertex ids, block labels) -> poly
    active = tuple(v for v in range(t) if remaining[v] > 0)
    idx = {v: i for i, v in enumerate(active)}
    states = {tuple(range(len(active))): [1]}
    inactive_isolated = t - len(active)  # vertices with no edges at all
    for (a, b) in edges:
        ia, ib = idx[a], idx[b]
        new = defaultdict(lambda: [])
        for p, w in states.items():
            # omit edge: factor -1
            key = p
            new[key] = padd(new[key], pscale(w, -1))
            # include edge: factor q, merge
            key2 = merge_labels(p, ia, ib)
            new[key2] = padd(new[key2], [0] + w)
        states = dict(new)
        remaining[a] -= 1
        remaining[b] -= 1
        # retire finished vertices
        gone = [v for v in (a, b) if remaining[v] == 0]
        gone = sorted(set(gone))
        if gone:
            keep = [i for i, v in enumerate(active) if v not in gone]
            new = defaultdict(lambda: [])
            for p, w in states.items():
                pp = canon(tuple(p[i] for i in keep))
                factor = len(set(p)) - len(set(pp))  # blocks that vanish = completed components
                new[pp] = padd(new[pp], [0] * factor + w)
            states = dict(new)
            active = tuple(active[i] for i in keep)
            idx = {v: i for i, v in enumerate(active)}
    _require_v03((active == ()), 'Validation failed in bb_tools.py: 164')
    G = ptrim(states.get((), []))
    G = [0] * inactive_isolated + G  # each isolated vertex is its own component
    # F = G / q^t
    _require_v03((all(c == 0 for c in G[:t])), "not divisible by q^t")
    return ptrim(G[t:])


def flow_poly_from_word(word):
    """Cyclic transition multigraph of a word (labels 0..t-1) -> flow polynomial.
    Loops (consecutive equal labels, cyclically) contribute a factor (q-1) each."""
    m = len(word)
    t = max(word) + 1
    edges = []
    loops = 0
    for i in range(m):
        a, b = word[i], word[(i + 1) % m]
        if a == b:
            loops += 1
        else:
            edges.append((a, b))
    F = flow_poly(t, edges) if edges else ([1] if t == 1 else None)
    if F is None:
        raise ValueError("disconnected")
    for _ in range(loops):
        F = pmul(F, [-1, 1])
    return F


# --------------------------------------------------------------------------
# Exact Sturm sequences and root isolation
# --------------------------------------------------------------------------

def sturm_sequence(p):
    p = [Fr(v) for v in ptrim(p)]
    seq = [p, [Fr(v) for v in ptrim(pderiv(p))]]
    while len(seq[-1]) > 1 or (len(seq[-1]) == 1 and False):
        _, r = pdivmod(seq[-2], seq[-1])
        if not r:
            break
        seq.append([-v for v in r])
    return seq


def sign_changes(seq, x):
    signs = []
    for p in seq:
        v = peval(p, x)
        if v != 0:
            signs.append(1 if v > 0 else -1)
    return sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])


def count_roots(seq, a, b):
    """Number of distinct real roots in (a, b] (Sturm)."""
    return sign_changes(seq, a) - sign_changes(seq, b)


def cauchy_bound(p):
    p = ptrim(p)
    lead = abs(Fr(p[-1]))
    return 1 + max(abs(Fr(c)) / lead for c in p[:-1])


def isolate_real_roots(p, eps=Fr(1, 10**12)):
    """Isolating intervals (a,b] with b-a <= eps for each distinct real root."""
    seq = sturm_sequence(p)
    B = cauchy_bound(p)
    out = []
    stack = [(-B, B)]
    while stack:
        a, b = stack.pop()
        n = count_roots(seq, a, b)
        if n == 0:
            continue
        if n == 1 and b - a <= eps:
            out.append((a, b))
            continue
        mid = (a + b) / 2
        if peval(p, mid) == 0:
            # exact rational root: isolate it separately
            out.append((mid, mid))
            stack.append((a, mid - eps / 4))
            stack.append((mid + eps / 4, b))
            continue
        stack.append((a, mid))
        stack.append((mid, b))
    return sorted(out)


def negative_intervals(p, lo, hi, eps=Fr(1, 10**12)):
    """Certified rational sub-intervals of [lo, hi] on which p < 0 strictly.

    Returns a list of (a, b, root_left, root_right) where [a, b] is certified
    negative (p(a) < 0, p(b) < 0 and no real root in (a, b) by Sturm) and
    root_left/root_right are the isolating intervals of the bounding roots
    (None at lo/hi).
    """
    seq = sturm_sequence(p)
    roots = [r for r in isolate_real_roots(p, eps) if r[1] >= lo and r[0] <= hi]
    # sample points between consecutive isolating intervals
    cuts = [lo] + [r for r in roots] + [hi]
    pts = []
    prev = lo
    for r in roots:
        pts.append((prev, r[0]))
        prev = r[1]
    pts.append((prev, hi))
    out = []
    for (a, b) in pts:
        if b <= a:
            continue
        # certify: no roots in (a, b], and both endpoints negative
        if count_roots(seq, a, b) == 0 and peval(p, a) < 0 and peval(p, b) < 0:
            out.append((a, b))
    return out, roots


# --------------------------------------------------------------------------
# Brute-force two-layer word hypergraph numerator (Theorem 2.1 check)
# --------------------------------------------------------------------------

def hyper_numerator(word, q, lam):
    """Signed numerator N_w(q; lambda) by enumerating all 4^m hyperedge subsets.
    word: labels 0..t-1; lam: list of m activities (Fractions)."""
    m = len(word)
    t = max(word) + 1
    # vertices: posts 0..t-1 ; layer l path vertex i -> t + l*(m+1) + i
    def pv(l, i):
        return t + l * (m + 1) + i
    n = t + 2 * (m + 1)
    hyper = [(pv(l, i), pv(l, i + 1), word[i], i) for l in range(2) for i in range(m)]
    u, v0, v1 = pv(0, 0), pv(0, m), pv(1, m)
    total = Fr(0)
    for bits in product((0, 1), repeat=2 * m):
        p = list(range(n))
        w = Fr(1)
        def find(x):
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            return x
        for bit, (a, b, c, i) in zip(bits, hyper):
            if bit:
                w *= lam[i]
                for x, y in ((a, b), (b, c)):
                    rx, ry = find(x), find(y)
                    if rx != ry:
                        p[rx] = ry
        roots = {find(x) for x in range(n)}
        k = len(roots)
        s = int(find(u) == find(v0)) - int(find(u) == find(v1))
        if s:
            total += s * w * Fr(q) ** k
    return total


# --------------------------------------------------------------------------
# Own frontier DP for the conditioned-post fan chain (Section 3 of v0.1)
# --------------------------------------------------------------------------

def fan_chain_edges(word, L):
    """Base graph G_{w,L}: posts 0..t-1, path vertices t..t+mL.
    Returns (n, edges, u, v)."""
    m = len(word)
    t = max(word) + 1
    edges = []
    for i in range(m):
        post = word[i]
        base = t + i * L
        for j in range(L):
            edges.append((base + j, base + j + 1))  # rim
        for j in range(L + 1):
            edges.append((post, base + j))  # spokes
    edges = sorted(set(tuple(sorted(e)) for e in edges))
    n = t + m * L + 1
    return n, edges, t, t + m * L


def core_numerator(word, L, q, x):
    """Conditioned-post numerator N^T_{w,L}(q,x): posts wired across layers,
    no other vertical edges.  Exact rational.  Frontier = posts, u_0, and the
    current path vertex in each layer.  Processed path vertex by path vertex.
    """
    q, x = Fr(q), Fr(x)
    m = len(word)
    t = max(word) + 1
    N = m * L  # last path index
    # slots: 0..t-1 posts, t = u_0 (layer 0 copy of path vertex 0),
    # then current vertex layer0, layer1
    def spokes(j):
        if j == 0:
            return [word[0]]
        if j == N:
            return [word[-1]]
        i, r = divmod(j, L)
        return sorted({word[i - 1], word[i]}) if r == 0 else [word[i]]
    # initial: path vertex 0 in both layers; layer-0 copy is u_0 itself.
    # slots: posts (t), u0 (=cur0 at start), cur1
    states = {canon(tuple(range(t + 2))): Fr(1)}  # t posts, u0/cur0, cur1
    # spokes at vertex 0
    def apply_edge(states, a, b):
        new = defaultdict(Fr)
        for p, w in states.items():
            new[p] += w
            new[merge_labels(p, a, b)] += w * x
        return dict(new)
    for s in spokes(0):
        states = apply_edge(states, s, t)      # layer 0: u0
        states = apply_edge(states, s, t + 1)  # layer 1 copy of vertex 0
    # now slots: 0..t-1 posts, t = u0 (also cur0), t+1 = cur1
    cur0, cur1 = t, t + 1
    for j in range(1, N + 1):
        # add new vertices j in both layers: slots t+2, t+3
        new = {}
        for p, w in states.items():
            mx = max(p)
            new[p + (mx + 1, mx + 2)] = w
        states = new
        n0, n1 = (t + 2, t + 3) if j == 1 else (t + 3, t + 4)
        states = apply_edge(states, cur0, n0)
        states = apply_edge(states, cur1, n1)
        for s in spokes(j):
            states = apply_edge(states, s, n0)
            states = apply_edge(states, s, n1)
        # retire old cur0/cur1 unless cur0 is u0 (j==1: cur0 is u0, keep)
        if j == 1:
            # slots: posts, u0(t), cur1(t+1), n0(t+2), n1(t+3) -> keep u0, drop t+1
            keep = list(range(t + 1)) + [t + 2, t + 3]
            drop = [t + 1]
        else:
            # slots: posts, u0(t), cur0(t+1), cur1(t+2), n0(t+3), n1(t+4)
            keep = list(range(t + 1)) + [t + 3, t + 4]
            drop = [t + 1, t + 2]
        new = defaultdict(Fr)
        for p, w in states.items():
            pp = canon(tuple(p[k] for k in keep))
            factor = len(set(p)) - len(set(pp))
            new[pp] += w * q ** factor
        states = dict(new)
        if j == 1:
            cur0, cur1 = t + 1, t + 2
        else:
            cur0, cur1 = t + 1, t + 2
    # final: slots posts, u0, v0=cur0, v1=cur1
    total = Fr(0)
    for p, w in states.items():
        k = len(set(p))
        s = int(p[t] == p[cur0]) - int(p[t] == p[cur1])
        if s:
            total += s * w * q ** k
    return total


def core_numerator_bruteforce(word, L, q, x):
    n, E, u, v = fan_chain_edges(word, L)
    t = max(word) + 1
    def vert(a, layer):
        return a if a < t else t + 2 * (a - t) + layer
    edges = [(vert(a, l), vert(b, l)) for a, b in E for l in (0, 1)]
    nv = 2 * n - t
    total = Fr(0)
    q, x = Fr(q), Fr(x)
    for bits in product((0, 1), repeat=len(edges)):
        p = list(range(nv))
        def find(z):
            while p[z] != z:
                p[z] = p[p[z]]
                z = p[z]
            return z
        cnt = 0
        for bit, (a, b) in zip(bits, edges):
            if bit:
                cnt += 1
                ra, rb = find(a), find(b)
                if ra != rb:
                    p[ra] = rb
        k = len({find(z) for z in range(nv)})
        s = int(find(vert(u, 0)) == find(vert(v, 0))) - int(find(vert(u, 0)) == find(vert(v, 1)))
        if s:
            total += s * q ** k * x ** cnt
    return total


# --------------------------------------------------------------------------
# Own frontier DP for the FULL bunkbed core with designated verticals at y
# --------------------------------------------------------------------------

def full_core_poly(word, L, q, x, ydeg=None):
    """Numerator N(y) of the full bunkbed G_{w,L} x K2, all edges activity x
    except the t designated (post) verticals at activity y.  Non-post vertical
    edges are present with activity x.  Returns the polynomial in y as a list
    of Fractions (ascending).  Exact."""
    q, x = Fr(q), Fr(x)
    m = len(word)
    t = max(word) + 1
    N = m * L
    def spokes(j):
        if j == 0:
            return [word[0]]
        if j == N:
            return [word[-1]]
        i, r = divmod(j, L)
        return sorted({word[i - 1], word[i]}) if r == 0 else [word[i]]
    # slots: posts layer0: 0..t-1 ; posts layer1: t..2t-1 ; u0: 2t ; cur0, cur1
    T2 = 2 * t
    def apply_edge(states, a, b, act):
        """act: 'x' -> activity x ; 'y' -> polynomial y"""
        new = defaultdict(lambda: [])
        for p, w in states.items():
            new[p] = padd(new[p], w)
            pm = merge_labels(p, a, b)
            if act == 'x':
                new[pm] = padd(new[pm], pscale(w, x))
            else:
                new[pm] = padd(new[pm], [Fr(0)] + w)
        return dict(new)
    init = canon(tuple(range(T2 + 2)))  # posts0, posts1, u0(=cur0), cur1
    states = {init: [Fr(1)]}
    # designated verticals (y)
    for s in range(t):
        states = apply_edge(states, s, t + s, 'y')
    u0 = T2
    cur0, cur1 = T2, T2 + 1
    # vertex 0: spokes from post word[0] in both layers, vertical u0-cur1 at x
    for s in spokes(0):
        states = apply_edge(states, s, cur0, 'x')
        states = apply_edge(states, t + s, cur1, 'x')
    states = apply_edge(states, cur0, cur1, 'x')
    for j in range(1, N + 1):
        new = {}
        for p, w in states.items():
            mx = max(p)
            new[p + (mx + 1, mx + 2)] = w
        states = new
        # slot bookkeeping: for j==1 slots are posts0,posts1,u0,cur1,n0,n1
        # for j>=2 slots are posts0,posts1,u0,cur0,cur1,n0,n1
        if j == 1:
            n0, n1 = T2 + 2, T2 + 3
        else:
            n0, n1 = T2 + 3, T2 + 4
        states = apply_edge(states, cur0, n0, 'x')
        states = apply_edge(states, cur1, n1, 'x')
        for s in spokes(j):
            states = apply_edge(states, s, n0, 'x')
            states = apply_edge(states, t + s, n1, 'x')
        states = apply_edge(states, n0, n1, 'x')  # non-post vertical at x
        if j == 1:
            keep = list(range(T2 + 1)) + [T2 + 2, T2 + 3]
            drop = [T2 + 1]
        else:
            keep = list(range(T2 + 1)) + [T2 + 3, T2 + 4]
            drop = [T2 + 1, T2 + 2]
        new = defaultdict(lambda: [])
        for p, w in states.items():
            pp = canon(tuple(p[k] for k in keep))
            factor = len(set(p)) - len(set(pp))
            new[pp] = padd(new[pp], pscale(w, q ** factor))
        states = dict(new)
        cur0, cur1 = T2 + 1, T2 + 2
    total = []
    for p, w in states.items():
        k = len(set(p))
        s = int(p[u0] == p[cur0]) - int(p[u0] == p[cur1])
        if s:
            total = padd(total, pscale(w, s * q ** k))
    return [Fr(c) for c in total]


def full_bunkbed_bruteforce(n, base_edges, u, v, q, x, activities=None):
    """Brute-force RC numerator on the full bunkbed of a base graph.
    activities: optional dict mapping ('v', a) -> activity for vertical at a,
    default x for everything."""
    q, x = Fr(q), Fr(x)
    edges = []
    for a, b in base_edges:
        edges.append(((2 * a, 2 * b), x))
        edges.append(((2 * a + 1, 2 * b + 1), x))
    for a in range(n):
        act = x if activities is None else Fr(activities.get(('v', a), x))
        edges.append(((2 * a, 2 * a + 1), act))
    nv = 2 * n
    total = Fr(0)
    for bits in product((0, 1), repeat=len(edges)):
        p = list(range(nv))
        def find(z):
            while p[z] != z:
                p[z] = p[p[z]]
                z = p[z]
            return z
        w = Fr(1)
        for bit, ((a, b), act) in zip(bits, edges):
            if bit:
                w *= act
                ra, rb = find(a), find(b)
                if ra != rb:
                    p[ra] = rb
        k = len({find(z) for z in range(nv)})
        s = int(find(2 * u) == find(2 * v)) - int(find(2 * u) == find(2 * v + 1))
        if s:
            total += s * w * q ** k
    return total


# --------------------------------------------------------------------------
# Faster integer-scaled version of the full-core DP (same algorithm, weights
# kept as integer polynomial tuples; a global rational scale is divided out at
# the end).  Used for the explicit q=3/2 witness.
# --------------------------------------------------------------------------

def full_core_poly_int(word, L, q, x):
    q, x = Fr(q), Fr(x)
    qn, qd = q.numerator, q.denominator
    xn, xd = x.numerator, x.denominator
    m = len(word)
    t = max(word) + 1
    N = m * L
    T2 = 2 * t
    deg = t  # degree in y
    ZERO = (0,) * (deg + 1)
    scale = Fr(1)

    def spokes(j):
        if j == 0:
            return [word[0]]
        if j == N:
            return [word[-1]]
        i, r = divmod(j, L)
        return sorted({word[i - 1], word[i]}) if r == 0 else [word[i]]

    def edge_x(states, a, b):
        nonlocal scale
        new = {}
        for p, w in states.items():
            wc = tuple(c * xd for c in w)
            wo = tuple(c * xn for c in w)
            v = new.get(p)
            new[p] = wc if v is None else tuple(i + j for i, j in zip(v, wc))
            pm = merge_labels(p, a, b)
            v = new.get(pm)
            new[pm] = wo if v is None else tuple(i + j for i, j in zip(v, wo))
        scale *= xd
        return new

    def edge_y(states, a, b):
        new = {}
        for p, w in states.items():
            v = new.get(p)
            new[p] = w if v is None else tuple(i + j for i, j in zip(v, w))
            pm = merge_labels(p, a, b)
            wo = (0,) + w[:-1]
            v = new.get(pm)
            new[pm] = wo if v is None else tuple(i + j for i, j in zip(v, wo))
        return new

    init = canon(tuple(range(T2 + 2)))
    states = {init: (1,) + (0,) * deg}
    for s in range(t):
        states = edge_y(states, s, t + s)
    u0 = T2
    cur0, cur1 = T2, T2 + 1
    for s in spokes(0):
        states = edge_x(states, s, cur0)
        states = edge_x(states, t + s, cur1)
    states = edge_x(states, cur0, cur1)
    for j in range(1, N + 1):
        states = {p + (max(p) + 1, max(p) + 2): w for p, w in states.items()}
        if j == 1:
            n0, n1 = T2 + 2, T2 + 3
            keep = list(range(T2 + 1)) + [T2 + 2, T2 + 3]
        else:
            n0, n1 = T2 + 3, T2 + 4
            keep = list(range(T2 + 1)) + [T2 + 3, T2 + 4]
        states = edge_x(states, cur0, n0)
        states = edge_x(states, cur1, n1)
        for s in spokes(j):
            states = edge_x(states, s, n0)
            states = edge_x(states, t + s, n1)
        states = edge_x(states, n0, n1)
        # retire: at most 2 components complete; multiply all by qd^2, completed by qn per component
        new = {}
        for p, w in states.items():
            pp = canon(tuple(p[k] for k in keep))
            factor = len(set(p)) - len(set(pp))
            mult = qn ** factor * qd ** (2 - factor)
            w2 = tuple(c * mult for c in w)
            v = new.get(pp)
            new[pp] = w2 if v is None else tuple(i + j for i, j in zip(v, w2))
        states = new
        scale *= qd ** 2
        cur0, cur1 = T2 + 1, T2 + 2
    total = ZERO
    kmax = T2 + 3
    for p, w in states.items():
        k = len(set(p))
        s = int(p[u0] == p[cur0]) - int(p[u0] == p[cur1])
        if s:
            mult = s * qn ** k * qd ** (kmax - k)
            total = tuple(i + j * mult for i, j in zip(total, w))
    scale *= qd ** kmax
    return [Fr(c) / scale for c in total]
