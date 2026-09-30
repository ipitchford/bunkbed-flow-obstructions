# Flow-polynomial obstructions to the random-cluster bunkbed inequality

**Evidence Press candidate v0.2.0 — 30 September 2026**

This release develops the v0.1 candidate (included unchanged in `v0_1/`). It is a **partial resolution** of Ayyer–Linusson–Ravichandran Problem 1.4, not a full classification of the pairs (p, q).

## What v0.2 establishes

For every edge probability 0 < p < 1, the random-cluster bunkbed inequality fails on some finite connected simple full bunkbed graph for every

* q in (1, 2)  — v0.1 (evenly thickened triangles), independently re-verified here;
* q in (2, q_c) with q_c = 2.574743… the real root of q³ − 4q² + 6q − 6 — **new, analytic** (closed-form flow polynomial of K_{4,b});
* q in (2, 2.764] — **new, certified** (exact Sturm certificates for 4-regular circulant witnesses up to C_32(1,5)).

So within (1, 2.764] the set of universal q is exactly {2} (Häggström's Ising point), which is therefore an isolated universal point.

Below q = 1 the v0.1 argument does not apply, but a second fan limit exists (Proposition 7.1 of the paper) whose sign is an exactly computable algebraic number; with it and with exact finite certificates the release gives ordinary-graph counterexamples at, for example, (q, p) = (9/10, 1/2), (4/5, 1/2), (9/10, 1/4), (9/10, 3/4), and an explicit full bunkbed counterexample at (9/10, 1/2) with 6,854 vertices. These q < 1 results are pointwise in p.

Also new: the exact negativity interval (2.02317, 2.27308) of the v0.1 twelve-vertex witness; a smaller explicit witness at q = 3/2, p = 1/2 with 21,854 bunkbed vertices (v0.1: 56,708), with the exact minimal pendant count; a ten-vertex 4-regular witness C_10(1,4); an audit closing two presentational gaps in the v0.1 amplification lemma; and an 86-instance test of the v0.1 rational error bound.

## Start here

* `paper/manuscript_v0_2.pdf` (also `.md`): the paper. Sections 3 (audit), 4–5 (above 2), 6 (explicit witness), 7 (below 1), 9 (bounded novelty search), 10 (open).
* `AUDIT_LEDGER.md`: v0.1 claims C1–C7 with what was re-derived and re-computed, plus the new claims N1–N9.
* `VERIFICATION_REPORT_v0_2.md`: executed checks and timings.
* `NOVELTY_REPORT.md`: the bounded priority search (queries, corpus, outcome per contribution unit).
* `claims_v0_2.json`, `stop_receipt_v0_2.json`, `provenance_v0_2.json`: machine-readable ledger.

## Reproduce

```sh
cd code
python3 certify_v02.py          # about 1 minute: every exact check the paper relies on
python3 certify_v02.py --full   # about 15 minutes: also recomputes the stored large objects
python3 crosscheck_manuscript.py  # every number quoted in the paper vs the data files
cd ../v0_1 && python3 code/run_all.py   # the original v0.1 suite (needs a C++17 compiler as `c++`)
```

Requirements: Python 3.11+, `sympy` (exact root isolation/counting), `numpy` (discovery scripts only). No floating-point quantity is a proof dependency; the discovery scripts (`flowsearch.py`, `run_flowsearch.py`, `families*.py`, `explore_qlt1*.py`, `qlt1_limit.py`, `qlt1_map_limit.py`) are included with their logs for transparency.

## Layout

| Path | Contents |
|---|---|
| `code/bb_tools.py` | independent exact tools: frontier-DP flow polynomial, Sturm root isolation, hypergraph brute force, conditioned-post DP, full-bunkbed DP with symbolic y |
| `code/audit_*.py` | audit scripts for the v0.1 claims |
| `code/witness_table.py`, `code/c32.py` | certified witnesses above 2 |
| `code/qlt1_exact.py`, `code/qlt1_limit.py` | the q<1 fan limit, exact (Q(√Δ)) and floating versions |
| `code/explicit_q32.py`, `code/explicit_q09.py`, `code/scan_q32_cores.py` | explicit witnesses |
| `code/fanbound.py` | general implementation and test of the v0.1 Appendix A bound |
| `data/` | all computed certificates and tables (JSON) |
| `logs/` | execution logs of every script |
| `checks/` | executed consolidated receipts |
| `v0_1/` | the unmodified v0.1 bundle |

## What is and is not certified

Exact: all flow polynomials, root isolations, interval certificates, conditioned and full numerators, minimal pendant counts, the K_{4,b} closed form, the q<1 limit signs on the grid. Written mathematics: the v0.1 transfer theorem (re-derived here), the K_{4,b} theorem and the q<1 limit proposition (proved in the paper). Not done: external refereeing, proof-assistant verification, a proof that the q<1 limit is negative for *all* p at any q, any statement for integer q ≥ 3 or for q > 2.764.

`SHA256SUMS` covers every distributed file except itself.
