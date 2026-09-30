# Verification report — Evidence Press bunkbed v0.3.0

**Date:** 30 September 2026. **Scope:** candidate proofs and exact arithmetic. This is not proof-assistant verification, external human peer review or an exhaustive priority audit.

## Full reconstruction and provenance

The supplied v0.2 manifest passed before modification. Its full reconstruction completed successfully in 594.2 seconds in the execution environment. After hardening, the full developed reconstruction passed under `python -O` in 601.2 seconds. Both logs are retained in `checks/v03/`. The hardened baseline suite also passed under `-O`, including its two different exact flow enumerations and stored-certificate comparisons.

The full developed stage reconstructs **all sixteen** flow witnesses, including C32(1,5), and **both** full-core post-activity cubics. It does not merely compare saved PASS receipts. The quicker mode explicitly omits some large reconstructions. A subsequent reproduction should use the default `code/verify_release.py` for full reconstruction.

## New exact checks

| Object | Executed evidence |
|---|---|
| Doubled-triangle limit polynomial | Reconstructed symbolically from all five ordered equality partitions; exact factorisation, degree ten and every coefficient compared to the certificate. |
| Algebraic lower endpoint | Exact Sturm count: the quintic has one real root; exact opposite signs at the rational bracket endpoints. |
| Positivity on [alpha,1) | Every Bernstein coefficient for c2,...,c10 is positive on [787/1000,1], with exact reverse reconstruction. c0 and c1 are positive multiples of the endpoint quintic. |
| Simpler [4/5,1) corollary | All eleven coefficient polynomials certified positive on [4/5,1]. |
| Alternate subunit calculation | Seven rational parameter pairs agree exactly with a distinct quadratic-field implementation, including cases with a positive rather than negative limit. |
| q=1 Jordan limit | Exact symbolic top projectors, bottom nilpotence and mixed-compound coefficients; four ordered partition contractions give the leading coefficient -1. |
| q=1 finite implementation | Nine first-order-jet calculations agree exactly with a connectivity-frontier recurrence. Six larger finite cores have exactly negative numerators. |
| Graph files | The two current small base lists match their recipes exactly. Both generated full graphs are connected and simple and have the certified edge counts. The large construction is checked as a recipe, without materialising its full graph. |
| Attachment-interface identity | 44,168 pairs of partitions on interfaces of size one through six pass a direct component-count check. This supports the written general density-bound proof. |
| Current manuscript consistency | 42 specified checks, including all eleven printed polynomial coefficients, graph/circulant tables and selected exact formulas. This does not validate every sentence. |

The q=1 one-block derivative remainder is controlled by the written spectral argument, not by the finite test grid. The general transfer and amplification proofs similarly remain written mathematical arguments. No number of successful finite checks substitutes for those quantifiers.

## Validation repairs and negative tests

Seventy-five Python assertions in nineteen active files were replaced with explicit exceptions, including all proof-critical checks. The side-effecting header read was moved outside validation. Optimisation settings propagate to the baseline subprocesses. The historical presentation checker now exits nonzero when it detects an inconsistency. Approximate root metadata is labelled non-certifying.

Ten deliberate invalid cases must be rejected, with the tested optimised variants shown in the raw receipt: a changed expected flow coefficient normally and under -O; a wrong graph count; a loop in a flow witness; a corrupt new polynomial coefficient; a wrong q=1 limit sign; a missing certificate; a missing compiler; an altered historical manuscript table; an altered current printed polynomial coefficient. Mutations take place only in temporary copies. Initial evidence for the first nine cases is preserved separately from the final ten-case run.

## Sanity checks and interpretation

The current q=3/2 base graph has 10,927 vertices and 11,163 edges, so its full bunkbed has 21,854 vertices and `2*11163+10927 = 33253` edges. The q=9/10 graph has `2*3427 = 6854` vertices and `2*3555+3427 = 10537` edges. These identities are checked against the actual generated edge lists. The old and new graph orders are not confused with the 32-vertex auxiliary flow witness.

Counterexamples exist for each interior p, with a graph allowed to depend on p and q. This does not contradict validity sufficiently close to p=1 for each fixed graph. The local classification does not imply a global lower threshold at alpha or an upper threshold at 2.764. Integer q>=3 remains unclassified here.

## Evidence boundaries

Algorithmic cross-checking is not independent human review. The 36,423,050-vertex example is verified by an analytic error certificate and exact amplification inequalities; its full partition function was not enumerated. The polynomial identity and small component tests are exact, but the complete theorem has not been translated into a proof assistant. The priority search was targeted. The new claims are therefore delivered as a candidate requiring external mathematical review.

## Reproduction entry point

The packaged runner performs a manifest check followed by baseline, developed, new symbolic, structural, graph, interface, current/historical manuscript and negative-test stages. It writes command lines, exit codes, timings and log hashes in `runs/`. The released consolidated evidence identifies which full constituent reconstructions and which integrated runner modes were actually executed; a quick run is never labelled full reconstruction.
