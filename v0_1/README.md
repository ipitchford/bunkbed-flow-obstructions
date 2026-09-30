# Flow-polynomial obstructions to the random-cluster bunkbed inequality

**Evidence Press candidate v0.1.0 — 30 September 2026**

## Result and scope

This is a **partial resolution**, not a complete solution of Ayyer–Linusson–Ravichandran Problem 1.4 (Problem 8 in the supplied research brief).

For every prescribed homogeneous edge probability **0 < p < 1**, the candidate proves the existence of a finite connected simple full bunkbed counterexample at every **1 < q < 2**, and at every **21/10 ≤ q ≤ 9/4**. The central result transfers a negative Eulerian flow-polynomial evaluation at any real q > 1 to an ordinary homogeneous full bunkbed counterexample. Combined with Häggström’s known positive theorem at q = 2, this makes **2 the least universal q > 1** and proves that universal validity is **not upward-closed in q**.

The construction depends on p and q. There is no assertion that one finite graph works for all these parameters. The twelve-vertex flow witness is an **auxiliary graph**, not a twelve-vertex bunkbed counterexample.

The full classification remains unclosed. In particular, the candidate does not settle all low-q parameters, most q > 2, or integer q ≥ 3. A hypergraph-only obstruction is not substituted for an ordinary-graph result; the paper supplies the transfer and its real-q justification.

## Start here

`paper/manuscript.pdf` is the 12-page paper, including the complete argument, rational error bound, interval certificate, and scope statement. `paper/manuscript.tex` is its source. `claims.json` and `stop_receipt.json` record the status of the requested full classification.

Run all proof-related computational checks from this folder:

```sh
python3 code/run_all.py
```

Requirements: Python 3.11 or newer and a C++17 compiler available as `c++`. No third-party Python package is needed. The checks took approximately a few seconds in the execution environment; timing is recorded in `checks/executed_checks.json` and is not a performance guarantee.

The scripts do not update the stored certificate files when run normally. They recompute the claims and compare their results to those files. A failed assertion or failed subprocess exits nonzero.

## Evidence included

| File | What it establishes |
|---|---|
| `code/verify_words.py` | Exact multivariate word identity checks for ten words; explicit even-thickening choices below 2. |
| `code/enumerate_flow.cpp` and `code/verify_flow.py` | Independent edge-subset and vertex-partition reconstructions of the twelve-vertex flow polynomial; exact Bernstein sign certificate. |
| `code/verify_core.py` | Independent connectivity-frontier and rational Potts-transfer computations for the q = 3/2 conditioned core; direct-enumeration cross-checks of four small cases. |
| `code/verify_asymptotic.py` | A fully rational finite error bound and post-amplification certificate for q = 21/10. |
| `code/generate_graph.py` | Deterministic edge-list generator for either full counterexample, with explicit vertex conventions. |
| `certificates/` | Exact polynomial coefficients, rational certificate data and construction parameters. |
| `graphs/q_3_2_base.edges` | Explicit smaller base graph, 28,354 vertices and 28,602 edges. Its full bunkbed has 56,708 vertices. |
| `graphs/q_21_10_recipe.json` | Summary for the larger exact construction. The base graph has 18,211,525 vertices; its full bunkbed has 36,423,050 vertices. |

To print a construction summary without writing a large graph:

```sh
python3 code/generate_graph.py 21_10
```

To stream an edge list (the large case is optional and potentially hundreds of megabytes):

```sh
python3 code/generate_graph.py 21_10 --output large_base.edges
python3 code/generate_graph.py 3_2 --full --output smaller_full_bunkbed.edges
```

The first edge-list line is `number_of_vertices number_of_edges`. Subsequent lines contain zero-based unordered endpoint pairs. Full bunkbed vertex `(a, layer)` has integer label `2*a + layer`. The recipes give the source and the same-layer and cross-layer targets. Every edge has p = 1/2 in the two finite examples shipped here; arbitrary prescribed p is covered by the theorem and its parameter-dependent construction, not by these fixed numerical recipes.

## What is and is not certified

The certificates use exact integer or rational arithmetic. No Monte Carlo estimate, numerical root finder, or floating-point eigensolver is a proof dependency. The general theorem still depends on the written mathematical argument; it is not Lean- or Coq-verified. “Independent” describes different algorithms, not an external human referee or an independent research team.

The large graph is certified by the analytic reduction and a rational error bound; its astronomical set of edge configurations was not enumerated. The graph sizes are deliberately conservative, and no minimality claim is made. The smaller conditioned core was checked by two independent exact methods, and its promotion to the full graph uses the proved amplification lemma.

The paper identifies a literal counterexample to ALR Lemma A.1 as printed in the inspected arXiv version. It does **not** infer that their theorem is false. The new transfer avoids that marginal-distortion lemma.

## Provenance and release gates

The research brief identified the problem and cited arXiv:2509.18788. The original paper, GPZ construction, and flow-polynomial literature were consulted on 30 September 2026. The cubic for the doubled triangle and the positive Ising point are prior results, not new discoveries claimed by this release.

A focused external priority review and external adversarial examination of the real-q transfer remain necessary. This bundle is not externally peer reviewed, does not prove the full classification, and has not been uploaded or published to evidencepress.org. No individual user authorship is assigned.

`SHA256SUMS` covers the distributed files, except itself. Use `sha256sum -c SHA256SUMS` on Linux, or `shasum -a 256 -c SHA256SUMS` on macOS. To rebuild the PDF, run `pdflatex manuscript.tex` twice inside `paper/` with a standard TeX distribution.
