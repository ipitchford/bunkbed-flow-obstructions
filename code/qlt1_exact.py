"""Exact evaluation of the q<1 fan limit G_w(q,x) in the quadratic field
Q(sqrt(Delta)), Delta = tau^2 - 4d, for words with few posts.

Numbers are pairs (a, b) representing a + b*sqrt(Delta) with rational a, b.
The sign of a + b*sqrt(Delta) is decided exactly.
"""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

from fractions import Fraction as Fr
import itertools

class QF:
    __slots__ = ('a', 'b', 'D')
    def __init__(self, a, b=0, D=None):
        self.a = Fr(a); self.b = Fr(b); self.D = D
    def _D(self, o):
        return self.D if self.D is not None else o.D
    def __add__(self, o):
        if not isinstance(o, QF): o = QF(o, 0, self.D)
        return QF(self.a + o.a, self.b + o.b, self._D(o))
    __radd__ = __add__
    def __neg__(self): return QF(-self.a, -self.b, self.D)
    def __sub__(self, o):
        if not isinstance(o, QF): o = QF(o, 0, self.D)
        return self + (-o)
    def __rsub__(self, o): return QF(o, 0, self.D) - self
    def __mul__(self, o):
        if not isinstance(o, QF): o = QF(o, 0, self.D)
        D = self._D(o)
        return QF(self.a * o.a + self.b * o.b * D, self.a * o.b + self.b * o.a, D)
    __rmul__ = __mul__
    def inv(self):
        D = self.D; n = self.a * self.a - self.b * self.b * D
        _require_v03((n != 0), 'Validation failed in qlt1_exact.py: 32')
        return QF(self.a / n, -self.b / n, D)
    def __truediv__(self, o):
        if not isinstance(o, QF): o = QF(o, 0, self.D)
        return self * o.inv()
    def sign(self):
        """exact sign of a + b sqrt(D), D > 0 not a square assumed (works also if square)."""
        a, b, D = self.a, self.b, self.D
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        # compare a with -b sqrt(D)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        # opposite signs: sign = sign(a) if a^2 > b^2 D else sign(b)
        if a * a > b * b * D: return 1 if a > 0 else -1
        if a * a < b * b * D: return 1 if b > 0 else -1
        return 0
    def __float__(self):
        import math
        return float(self.a) + float(self.b) * math.sqrt(float(self.D))
    def __repr__(self): return f"({self.a} + {self.b}*sqrt({self.D}))"


def zeros(n, m, D): return [[QF(0, 0, D) for _ in range(m)] for _ in range(n)]
def eye(n, D):
    I = zeros(n, n, D)
    for i in range(n): I[i][i] = QF(1, 0, D)
    return I
def mm(A, B):
    n, k, m = len(A), len(B), len(B[0])
    out = zeros(n, m, A[0][0].D)
    for i in range(n):
        for j in range(m):
            s = QF(0, 0, A[0][0].D)
            for l in range(k): s = s + A[i][l] * B[l][j]
            out[i][j] = s
    return out
def madd(A, B): return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def msub(A, B): return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def outer(u, v): return [[u[i] * v[j] for j in range(len(v))] for i in range(len(u))]

def compound2(A):
    n = len(A); idx = list(itertools.combinations(range(n), 2)); N = len(idx)
    C = zeros(N, N, A[0][0].D)
    for I, (i, j) in enumerate(idx):
        for J, (k, l) in enumerate(idx):
            C[I][J] = A[i][k] * A[j][l] - A[i][l] * A[j][k]
    return C, idx

def partitions(t):
    def rec(a, r):
        if len(a) == t: yield tuple(a); return
        for s in range(r + 1): yield from rec(a + [s], max(r, s + 1))
    yield from rec([0], 1)

def G_exact(word, q, x):
    """Exact q<1 fan limit  lim N^T_{w,L}/(lambda_+ x)^{Lm}  as an element of Q(sqrt(Delta))."""
    q, x = Fr(q), Fr(x); f = 1 + x
    tau = x * x + 3 * x + q; d = f * x * (q + x); Dl = tau * tau - 4 * d
    _require_v03((Dl > 0), 'Validation failed in qlt1_exact.py: 91')
    lp = QF(tau / 2, Fr(1, 2), Dl)          # lambda_+
    t = max(word) + 1; m = len(word)
    total = QF(0, 0, Dl)
    for pi in partitions(t):
        r = max(pi) + 1; n = r + 1
        v = [QF(1, 0, Dl)] * n
        w = [QF(1, 0, Dl)] * r + [QF(q - r, 0, Dl)]
        Lam = {}; chain = {}; idx = None
        for s in range(r):
            es = [QF(int(i == s), 0, Dl) for i in range(n)]
            D_s = eye(n, Dl); D_s[s][s] = QF(f, 0, Dl)
            # right eigenvector of R D_s for lambda_+ : x^2 e_s + (lambda_+ - f x) v
            lplus = [QF(x * x, 0, Dl) * es[i] + (lp - f * x) * v[i] for i in range(n)]
            # left eigenvector: r_i = wtilde_i / (lambda_+ - x d_i), wtilde = w + x e_s
            rplus = [(w[i] + QF(x, 0, Dl) * es[i]) / (lp - QF(x, 0, Dl) * (QF(f, 0, Dl) if i == s else QF(1, 0, Dl))) for i in range(n)]
            norm = QF(0, 0, Dl)
            for i in range(n): norm = norm + rplus[i] * lplus[i]
            rplus = [ri / norm for ri in rplus]
            a = [D_s[i][i] * lplus[i] for i in range(n)]
            # sanity: (R D_s) lplus = lambda_+ lplus
            R = [[w[j] + (QF(x, 0, Dl) if i == j else QF(0, 0, Dl)) for j in range(n)] for i in range(n)]
            RD = mm(R, D_s)
            chk = mm(RD, [[l] for l in lplus])
            for i in range(n):
                _require_v03(((chk[i][0] - lp * lplus[i]).a == 0 and (chk[i][0] - lp * lplus[i]).b == 0), 'Validation failed in qlt1_exact.py: 116')
            # projector onto W_s along the plane
            vm = [v[i] - es[i] for i in range(n)]; wm = [w[i] - es[i] for i in range(n)]
            Ps = madd(outer(es, es), [[vm[i] * wm[j] / (q - 1) for j in range(n)] for i in range(n)])
            Pi = msub(eye(n, Dl), Ps)
            C1, idx = compound2(madd(outer(a, rplus), Pi)); C0, _ = compound2(Pi)
            Lam[s] = msub(C1, C0)
            chain[s] = outer(a, rplus)
        X = eye(len(idx), Dl)
        for c in word: X = mm(X, Lam[pi[c]])
        # contraction sum_a <w ^ e_a, X (v ^ e_a)>
        def wedge(pv, u):
            return [pv[i] * u[j] - pv[j] * u[i] for (i, j) in idx]
        term = QF(0, 0, Dl)
        for aa in range(n):
            ea = [QF(int(i == aa), 0, Dl) for i in range(n)]
            lhs = wedge(w, ea); rhs = wedge(v, ea)
            Xr = mm(X, [[val] for val in rhs])
            for I in range(len(idx)): term = term + lhs[I] * Xr[I][0]
        K = eye(n, Dl)
        for c in word: K = mm(K, chain[pi[c]])
        z = QF(0, 0, Dl)
        for i in range(n):
            for j in range(n): z = z + w[i] * K[i][j] * v[j]
        term = term + QF(q - r - 1, 0, Dl) * z
        falling = Fr(1)
        for j in range(r): falling *= q - j
        total = total + QF(falling, 0, Dl) * term
    return QF(q / (q - 1), 0, Dl) * total

if __name__ == '__main__':
    import json, sys
    from qlt1_limit import G_limit
    w2 = [0, 1, 2] * 2
    for q, x in [(Fr(9, 10), Fr(1)), (Fr(1, 2), Fr(1)), (Fr(7, 10), Fr(10))]:
        g = G_exact(w2, q, x)
        print(q, x, "exact sign", g.sign(), "float", float(g), "numpy version", G_limit(w2, float(q), float(x)))
