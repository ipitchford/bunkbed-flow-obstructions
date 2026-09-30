"""Search for connected loopless Eulerian multigraphs (given as cyclic words)
whose flow polynomial is negative at real q > 2.

Fast evaluation uses the exact colour-partition formula
    q^t F(q) = sum_{pi in Pi_t} (q)_{|pi|} (-1)^{m-h(pi)} (q-1)^{h(pi)},
where h(pi) counts edges inside blocks.  Set partitions are tabulated once as
restricted-growth strings (numpy int8), the (r,h) histogram is formed with
bincount, and F is then evaluated on a grid of q values in floating point.
Floating point is used only for *discovery*; every witness is re-certified
with exact integer arithmetic (bb_tools.flow_poly) and exact root isolation.
"""
import numpy as np, random, math, json, time, sys
from fractions import Fraction as Fr

_PART = {}

def partitions_rgs(t):
    """All restricted growth strings of length t as an (Bell(t), t) int8 array,
    plus the number of blocks for each."""
    if t in _PART:
        return _PART[t]
    P = np.zeros((1, 1), dtype=np.int8)
    mx = np.zeros(1, dtype=np.int8)
    for k in range(1, t):
        counts = mx.astype(np.int64) + 2          # labels 0..mx+1
        rep = np.repeat(np.arange(len(P)), counts)
        offs = np.arange(rep.size) - np.repeat(np.cumsum(counts) - counts, counts)
        newcol = offs.astype(np.int8)
        P = np.concatenate([P[rep], newcol[:, None]], axis=1)
        mx = np.maximum(mx[rep], newcol)
    r = (mx.astype(np.int64) + 1)
    _PART[t] = (P, r)
    return _PART[t]


def word_edges(word):
    m = len(word)
    return [(word[i], word[(i + 1) % m]) for i in range(m)]


def rh_hist(t, edges):
    P, r = partitions_rgs(t)
    m = len(edges)
    h = np.zeros(len(P), dtype=np.int64)
    for a, b in edges:
        h += (P[:, a] == P[:, b])
    key = r * (m + 1) + h
    hist = np.bincount(key, minlength=(t + 1) * (m + 1)).reshape(t + 1, m + 1)
    return hist  # hist[r, h]


def F_from_hist(hist, qs, t, m):
    qs = np.asarray(qs, dtype=np.float64)
    out = np.zeros_like(qs)
    ff = np.ones_like(qs)  # falling factorial (q)_r
    z = qs - 1.0
    for r in range(0, t + 1):
        if r > 0:
            ff = ff * (qs - (r - 1))
        row = hist[r]
        if r == 0 or not row.any():
            continue
        acc = np.zeros_like(qs)
        for h in np.nonzero(row)[0]:
            acc += row[h] * ((-1.0) ** (m - h)) * z ** h
        out += ff * acc
    return out / qs ** t


def F_eval(word, qs):
    t = max(word) + 1
    edges = word_edges(word)
    return F_from_hist(rh_hist(t, edges), qs, t, len(edges))


def valid_word(word, t):
    m = len(word)
    if len(set(word)) != t:
        return False
    if any(word[i] == word[(i + 1) % m] for i in range(m)):
        return False
    # connectivity of transition graph
    adj = {v: set() for v in range(t)}
    for a, b in word_edges(word):
        adj[a].add(b); adj[b].add(a)
    seen = {0}; stack = [0]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w); stack.append(w)
    return len(seen) == t


def random_word(t, m, rng):
    while True:
        w = [rng.randrange(t) for _ in range(m)]
        if valid_word(w, t):
            return w


def mutate(word, t, rng):
    w = list(word)
    m = len(w)
    for _ in range(50):
        r = rng.random()
        if r < 0.5:
            i = rng.randrange(m); w[i] = rng.randrange(t)
        elif r < 0.8:
            i, j = rng.randrange(m), rng.randrange(m); w[i], w[j] = w[j], w[i]
        else:
            i = rng.randrange(m); j = rng.randrange(m)
            seg = w[min(i, j):max(i, j) + 1]; seg.reverse(); w[min(i, j):max(i, j) + 1] = seg
        if valid_word(w, t):
            return w
        w = list(word)
    return list(word)


def anneal(t, m, q0, rng, steps=4000, T0=1.0, grid=None, log=None):
    """Minimise F(q0) over words; returns best word and its value.  Also scans
    a q-grid at every improvement and records any negative point."""
    w = random_word(t, m, rng)
    f = float(F_eval(w, [q0])[0])
    best = (f, w)
    found = []
    for s in range(steps):
        T = T0 * (1 - s / steps) + 1e-3
        w2 = mutate(w, t, rng)
        f2 = float(F_eval(w2, [q0])[0])
        # scale-free acceptance: compare log-magnitudes with sign
        d = f2 - f
        scale = max(abs(f), abs(f2), 1e-9)
        if d <= 0 or rng.random() < math.exp(-d / (scale * T)):
            w, f = w2, f2
            if f < best[0]:
                best = (f, list(w))
                if grid is not None:
                    vals = F_eval(w, grid)
                    neg = grid[vals < 0]
                    if neg.size:
                        found.append((list(w), float(neg.min()), float(neg.max())))
                        if log:
                            log(f"  negative on grid: word={w} q in [{neg.min():.4f},{neg.max():.4f}] F(q0)={f:.4g}")
            if f < 0:
                break
    return best, found
