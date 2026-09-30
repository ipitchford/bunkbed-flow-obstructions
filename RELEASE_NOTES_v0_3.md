# v0.3 changes and claim boundary

## New research

1. **All-p failure below one.** The second fan limit for ABCABC has an explicit degree-ten polynomial in a positive parameter h. Its first two coefficients are q^7 g(q) and 10 q^6 g(q); the other nine are positive on [787/1000,1] by exact Bernstein certificates. This proves counterexamples for every alpha <= q < 1 and every 0 < p < 1. The algebraic endpoint is included.
2. **The q=1 boundary.** An exact Jordan decomposition gives the normalised limit -1 for every fixed positive activity x. This establishes a direct all-p construction at q=1 within the same fan framework. The original disproof of Bernoulli bunkbed percolation remains credited to Gladkov–Pak–Zimin.
3. **Exact local classification.** Together with the retained above-one results and Häggström's positive q=2 theorem, U_p intersect [alpha,2.764] is exactly {2}, for each interior p.
4. **A corrected interface estimate.** For edge-disjoint graphs meeting in b vertices, the marginal random-cluster density is bounded between R^{-(b-1)} and R^{b-1}, R=max(q,1/q). This clarifies the version-specific ALR appendix issue without disputing their main theorem or relying on their printed lemma.

## Retained, reproduced v0.2 contributions

The Eulerian-flow transfer, the entire interval (1,2), the K_{4,b} analytic interval (2,q_c), the exact circulant endpoint 2.764, all pointwise below-one certificates, and the improved 21,854-vertex q=3/2 graph remain in the candidate. The full developed reconstruction passed both before and after verifier hardening. The historical v0.1 interval and 56,708-vertex graph remain in the archived record; they are no longer the current best bounds.

## Repairs

Proof-critical `assert` statements were replaced by explicit exceptions (75 replacements in 19 active Python files). The side-effecting header read was separated from validation. Optimisation flags propagate to baseline subprocesses. Missing compiler/certificate errors remain fatal. The historical manuscript checker now exits nonzero on detected inconsistency. Approximate root metadata is labelled as discovery-only. The new runner checks file integrity, graph structure, current manuscript data and deliberate corruptions.

## What the release does not establish

Alpha is not a global bunkbed threshold. It is sharp only for all-p negativity of the particular doubled-triangle limiting test. The endpoint 2.764 is a certified stopping point, not a maximum. No statement here settles integer q>=3. Search failure does not prove universal validity. No single graph is asserted to work at every p. Fixed-core minimum pendant counts are not globally minimal graph orders. The large q=21/10 full partition function has not been enumerated. New theorems have not undergone external human review or proof-assistant formalisation.
