# Audit ledger — v0.1 claims and v0.2 additions

Each row states what was checked, by what independent means, and the outcome. "Hand" means the proof was re-derived line by line in this session; "code" names the independent script (all in `code/`, all exact arithmetic unless marked float).

## v0.1 claims (ids from `v0_1/claims.json`)

| id | claim | hand | code | outcome |
|---|---|---|---|---|
| C1 | word identity N_w = q^{t+2} ∏λ_i F_{Γ_w}(q)/(q−1) | exterior-square steps re-derived, including the closing-transition sum Σ_a(qδ−1)(qδ−1)=q(qδ−1) | `audit_word_and_core.py`: brute-force hypergraph enumerator + own flow DP at 22 random rational points, 11 words incl. loops | stands |
| C2 | Eulerian-flow transfer (q>1): fan limit + amplification | fan spectral ordering (char. poly at x = x²(q−1)), reduced representation, C₂(MP_s)=a_L R_s, contraction, limit; amplification involution and pendant reduction | `audit_word_and_core.py` (convergence of N^T/a_L^m with own DP), `audit_amplification.py` (N(y) DP vs brute force, a_t=N^T, pendant factor), `fanbound.py` (86 tests of Appendix A bound) | stands; two presentational gaps closed (canonical choice of swapped vertex; u≠v non-posts) |
| C3 | all q∈(1,2) fail at every p | ℓC_3 closed form re-derived from bundle transfer | `audit_word_and_core.py` closed-form vs DP, ℓ=2,4,6 | stands |
| C4 | all q∈[21/10,9/4] fail at every p | — | `audit_flow_witness.py`: third-algorithm flow polynomial equals v0.1 vector; Bernstein certificate reproduced | stands; strengthened to (2.02317, 2.27308) exactly |
| C5 | q=2 least universal q>1; universal set not upward-closed | FKG argument re-read | — | stands; strengthened: universal set ∩ (1, 2.764] = {2} |
| C6 | q=2 universal (Häggström) | credited prior result via ALR Thm 1.5; FPSAC PDF not fetchable here | — | credited |
| C7 | ALR Lemma A.1 literal counterexample | re-derived 1/3 vs 5/14 | `v0_1/code/run_all.py` | stands; note added that ALR's application (m=3 attachment gadgets) is consistent with a corrected lemma |

## v0.2 claims

| id | claim | proof/certificate | code | status |
|---|---|---|---|---|
| N1 | Γ_* quotient P has exactly two real roots ρ₁=2.02316…, ρ₂=2.27307…; F<0 on (ρ₁,ρ₂); certified on [2.0232, 2.2730] | Sturm root isolation, exact endpoint signs | `audit_flow_witness.py`, `certify_v02.py` §1 | proved (exact) |
| N2 | closed form of F_{K_{4,b}} (Theorem 4.1) | colour-sum derivation (paper) | `certify_v02.py` §5 (b=2..10, six q incl. negative) | proved |
| N3 | every q∈(2,q_c), q_c root of q³−4q²+6q−6, fails at every p (Theorem 4.2) | dominance of −z(z−1)(2−z)(3q)^b for even b; factorisations checked | `certify_v02.py` §5 | proved |
| N4 | certified circulant witnesses; failure for every q∈(2, 2.764] at every p (Theorem 5.1) | exact Sturm certificates on stored polynomials; union argument | `witness_table.py`, `c32.py`, `certify_v02.py` §6 | proved (exact) |
| N5 | explicit q=3/2, p=1/2 witness: (ABC)^4, L=19, k=3565, 21,854 vertices | exact cubic N(y); a₃=N^T<0; N(y_k)<0≤N(y_{k−1}) | `explicit_q32.py`, `certify_v02.py` §7 (`--full` recomputes the cubic) | proved (exact) |
| N6 | q<1 fan limit G_w(q,x) (Proposition 7.1) | proof in paper §7.1 (same finite representation; different dominant compound mode) | `qlt1_limit.py` (float check vs exact finite-L values), `qlt1_exact.py` (exact signs) | proved; numerically validated |
| N7 | exact signs of G on the (q,x) grid; thresholds q₀^{(ℓ)}(x) (Table 2) | exact bisection in Q(√Δ) | `qlt1_exact_map.py`, `certify_v02.py` §8 (11 spot points) | proved at grid points |
| N8 | seven finite q<1 certificates (Table in §7.3) and explicit (9/10, 1/2) witness with 6,854 vertices | exact conditioned numerators; exact cubic; minimal k | `explore_qlt1_map.py`, `explicit_q09.py`, `certify_v02.py` §8 | proved (exact) |
| N9 | negative search evidence: no Eulerian witness above 2.77 or above 3 in the searched families and words | — | `run_flowsearch.py` (float discovery), `families*.py` | evidence only |

## Cross-reference

`code/crosscheck_manuscript.py` compares every number quoted in the manuscript's tables and key sentences with `data/` and `checks/`; its log (`logs/crosscheck_manuscript.log`) lists 32 comparisons, all OK.
