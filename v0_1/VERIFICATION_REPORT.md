# Executed verification report

**Evidence Press bunkbed candidate v0.1.0 — 30 September 2026**

## Overall result

All released exact-arithmetic computational checks passed. **The requested full parameter classification was not completed.** The package proves a partial result and explicitly records the unclosed obligations.

## Checks executed

| Check | Result |
|---|---|
| Ten word-hypergraph identities, including repeated labels and loops | PASS |
| Independent enumeration of 16,777,216 edge subsets | PASS |
| Independent enumeration of 4,213,597 vertex partitions | PASS |
| Agreement of both integer flow-polynomial coefficient vectors | PASS |
| Thirteen strictly negative Bernstein coefficients on [21/10,9/4], including reverse basis reconstruction | PASS |
| Two exact methods for the q = 3/2, L = 20 conditioned core | PASS |
| Direct edge enumeration against both methods in four small cases | PASS |
| Rational q = 21/10, L = 1000 error bound below 10^-36 | PASS |
| Rational post-amplification inequalities for both finite full-graph recipes | PASS |
| Shipped 28,354-vertex base edge list matches its recipe and is simple and connected | PASS |
| Literal ALR Lemma A.1 counterexample: 1/3 versus 5/14, with zero common edges | PASS |

The consolidated execution took 4.87 seconds in this environment, excluding paper production and exploratory research. That timing is descriptive, not a requirement or a guarantee. The full execution metadata and individual times are in `checks/executed_checks.json`.

## What this does not establish

The general real-q transfer theorem still depends on the written proof; it is not formally verified by a proof assistant. Distinct algorithms were used, but no independent external referee or human research team reviewed the result. The larger full graph was not enumerated: its negativity follows from an analytic reduction plus exact sufficient bounds. No exhaustive novelty or graph-minimality claim is made.

The candidate excludes every 1 < q < 2 and every 21/10 ≤ q ≤ 9/4 at each prescribed 0 < p < 1. Combined with the credited Ising theorem, 2 is the least universal q > 1, and the universal-q set is not upward-closed. The remaining low-q parameter region and most q > 2, including integer q ≥ 3, are not classified by this work.

Reproduce with `python3 code/run_all.py` from the unzipped package root. Python 3.11 or newer and a C++17 compiler named `c++` are required; no third-party Python packages are used.
