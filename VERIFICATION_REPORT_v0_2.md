# Executed verification report — v0.2

**Evidence Press bunkbed candidate v0.2.0 — 30 September 2026.** Environment: Linux x86-64, Python 3.11.15, sympy 1.14.0, numpy 2.4.4, g++ 13.3. Timings are descriptive.

## Consolidated exact checks (`code/certify_v02.py`)

| # | check | result |
|---|---|---|
| 1 | Γ* flow polynomial recomputed by a third algorithm (frontier DP) equals the v0.1 vector; P=F/(q−1) has exactly two real roots; certified negative on [2.0232, 2.2730]; v0.1 Bernstein certificate on [21/10, 9/4] reproduced | PASS |
| 2 | Word identity at random rational (q, λ): brute-force two-layer hypergraph numerator = q^{t+2}∏λ F/(q−1) | PASS |
| 2b | Thickened-triangle closed form vs DP (ℓ = 2,4,6; four q incl. q=1/3); F_{4C₃}(3/2) = −71/1024 | PASS |
| 3 | Own conditioned-post DP = brute force on tiny cores; = v0.1 stored (ABC)^4, L=20 numerator exactly; negative | PASS |
| 4 | Amplification lemma ingredients: N(y) DP = brute force; a_t = N^T; pendant reduction (D, r, y_k) by brute force | PASS |
| 5 | K_{4,b} closed form vs DP (b = 2,…,10; six q incl. a negative one); q_c isolated to 10⁻¹⁵; factorisations used in the dominance proof | PASS |
| 6 | 16 witnesses above 2: Eulerian, loopless; each stored certificate re-verified (P(a)<0, P(b)<0, zero roots in (a,b) by exact Sturm count); polynomials recomputed for n ≤ 20 (all, with `--full`) | PASS |
| 7 | Union argument: every certified interval reaching beyond q_c starts below q_c ⇒ certified failure set above 2 is (2, 691/250] | PASS |
| 8 | Explicit q=3/2 witness: stored cubic N(y) has a₃ = recomputed N^T < 0, a₀,a₁,a₂ > 0; k = 3565 is the exact minimum (N(y_k) < 0 ≤ N(y_{k−1})); cubic recomputed with `--full` | PASS |
| 9 | q<1 fan limit: exact signs in Q(√Δ) at 8 points for the doubled triangle and 3 for 10C₃, matching the expected pattern | PASS |
| 10 | Seven finite q<1 certificates: exact N^T_{(ABC)^2,L}(q,x) < 0 | PASS |
| 11 | Explicit q=9/10 witness: stored cubic's leading coefficient = recomputed N^T; minimal k = 1099 verified; cubic recomputed with `--full` | PASS |

Receipts: `checks/executed_checks_v02.json` (default mode, 12 checks, 57 s) and `checks/executed_checks_v02_full.json` (`--full`, 788 s; run before check 2b was added, so it lists 11 checks).

## Supporting scripts and logs

| script | what it did | log / data |
|---|---|---|
| `audit_flow_witness.py` | Γ* recomputation, roots, F′(2) = −47, structural identification (asymmetric, non-planar) | `logs/audit_flow_witness.log`, `data/flow_witness_audit.json` |
| `audit_word_and_core.py` | 22 word-identity points; own DP vs brute force; convergence tables at (q,x) = (3/2,1), (21/10,1), (3/2,1/3) | `logs/audit_word_and_core.log`, `data/word_core_audit.json` |
| `audit_amplification.py` | N(y) vs brute force (3 cores × 4 y), a_t = N^T, pendant reduction with 1 and 2 pendants | `logs/audit_amplification.log` |
| `fanbound.py` | v0.1 Appendix A bound implemented for any word; 86 exact comparisons, no violation | `logs/fanbound_test.log`, `data/fanbound_test.json` |
| `scan_q32_cores.py` | smallest negative ℓC₃ cores at q=3/2, x=1: (ℓ,L) = (4,19), (6,16), (8,15) | `logs/scan_q32_cores.log` |
| `explicit_q32.py`, `explicit_q09.py` | exact cubics N(y), minimal pendant counts (3565; 3740 for L=20; 1099 at q=9/10) | `data/explicit_q32_L19.json`, `_L20.json`, `data/explicit_q09_L21.json` |
| `families.py`, `families2.py`, `families3.py`, `families4.py` | structured-family scans (wheels, antiprisms, K_n, K_{a,b}, circulants, tori, blow-ups); root isolation | `logs/families*.log`, `data/families*.json` |
| `witness_table.py`, `c32.py` | certified table above 2 | `data/witnesses_above2.json`, `data/witness_C32.json` |
| `flowsearch.py`, `run_flowsearch.py` | annealing over words t ≤ 10 (float discovery) | `logs/flowsearch_A.log`, `_B.log`, `data/flowsearch_*.json` |
| `explore_qlt1*.py` | exact finite-L signs below q=1 | `logs/explore_qlt1*.log`, `logs/qlt1_map_*.log`, `data/explore_qlt1*.json` |
| `qlt1_limit.py`, `qlt1_map_limit.py` | float q<1 limit and map (discovery) | `logs/qlt1_limit_check.log`, `logs/qlt1_limit_map.log` |
| `qlt1_exact.py`, `qlt1_exact_map.py` | exact q<1 limit signs and threshold brackets | `logs/qlt1_exact_map.log`, `data/qlt1_exact_map.json` |
| `crosscheck_manuscript.py` | 32 mechanised comparisons of manuscript numbers vs data | `logs/crosscheck_manuscript.log` |
| `v0_1/code/run_all.py` | original v0.1 suite (re-run here, PASS, 3.9 s) | `logs/run_all_v01.log` |

## What this does not establish

No external referee; no proof assistant. The written proofs (v0.1 transfer theorem; v0.2 Theorems 4.1–4.2, 5.1; Proposition 7.1) were each read by one agent other than their author. The q<1 statements are exact only at the listed points. Discovery used floating point; nothing floating enters a certificate.
