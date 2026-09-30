#!/usr/bin/env python3
"""Exact grid certificate for the cleared doubled-triangle identity.

MIT. Uses only Python integers and the standard library. The manuscript proves
the bidegree bound (17,12); the coefficient file is an input, not a derivation.
The referee's independent grid check suggested this minimal public route.
"""
import argparse
import json
from itertools import combinations
from pathlib import Path


def product(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def minor(a, i, j, k, l):
    return a[i][k] * a[j][l] - a[i][l] * a[j][k]


def evaluate(q, h):
    total = 0
    for labels in ((0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 1, 2)):
        r = max(labels) + 1
        n = r + 1
        weights = [1] * r + [q - r]
        pairs = list(combinations(range(n), 2))
        pair_index = {pair: i for i, pair in enumerate(pairs)}
        a_product, l_product = identity(n), identity(len(pairs))
        for s in labels * 2:
            a = [[(1 + h * (i == s)) * (weights[j] + h * (j == s))
                  for j in range(n)] for i in range(n)]
            b = [[(q - 1) * ((i == j) - (i == s and j == s))
                  - (i != s) * (weights[j] - (j == s))
                  for j in range(n)] for i in range(n)]
            ab = [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]
            mixed = [[minor(ab, i, j, k, l) - minor(a, i, j, k, l)
                      - minor(b, i, j, k, l) for k, l in pairs] for i, j in pairs]
            a_product = product(a_product, a)
            l_product = product(l_product, mixed)
        contraction = 0
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if i == j or k == j:
                        continue
                    row = pair_index[tuple(sorted((i, j)))]
                    col = pair_index[tuple(sorted((k, j)))]
                    sign = (1 if i < j else -1) * (1 if k < j else -1)
                    contraction += weights[i] * sign * l_product[row][col]
        z = sum(weights[i] * sum(a_product[i]) for i in range(n))
        falling = 1
        for j in range(r):
            falling *= q - j
        total += falling * (contraction + (q - 1)**6 * (q - r - 1) * z)
    return total


def verify(coefficients):
    if len(coefficients) != 11 or any(len(row) > 13 for row in coefficients):
        raise ValueError('Coefficient dimensions violate the advertised degree bound')
    count = 0
    for q in range(3, 21):
        for h in range(13):
            p = sum(c * q**i * h**j for j, row in enumerate(coefficients)
                    for i, c in enumerate(row))
            if evaluate(q, h) != q * (h + q)**2 * (q - 2) * (q - 1) * p:
                raise ValueError(f'Identity mismatch at q={q}, h={h}')
            count += 1
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative-control', action='store_true')
    args = parser.parse_args()
    path = Path(__file__).resolve().parents[1] / 'data/below_universal_v03.json'
    coefficients = json.loads(path.read_text())['P_coefficients_h_ascending_q_ascending']
    if args.negative_control:
        coefficients[0][0] += 1
        try:
            verify(coefficients)
        except ValueError:
            print(json.dumps({'status': 'PASS', 'corrupted_constant_rejected': True}))
        else:
            raise RuntimeError('Corrupted polynomial was accepted')
    else:
        print(json.dumps({'status': 'PASS', 'exact_grid_points': verify(coefficients),
                          'bidegree_bound': [17, 12], 'formal_verification': False}))
