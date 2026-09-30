# Response to the supplied v0.1 referee report
## Evidence Press candidate v0.3.0

The supplied report concerns v0.1. Its provisional REF judgement is not treated as an external review of the new v0.3 theorems. The supplied v0.2 development and the new work are distinguished in the claim ledger.

| Request | Action and evidence |
|---|---|
| Cite the precise least-q question | Introduction cites Gladkov–Pak–Zimin, published Section 8.5. It states the least-q conclusion and the failure of upward closure. |
| Delimit Sokal's suggestion | The 8 October 2024 author manuscript, footnote 3, is cited separately from the published paper. Integer q>=3 remains open here; no full noninteger classification is claimed. |
| Expand finite-L continuation | Section 3 has a separately identified lemma. It explains polynomial continuation at fixed L, the algebraic status of negative multiplicities, the compound contraction and decay of omitted colours. The q<1 and q=1 regimes each have their own proof. |
| Repair Python optimisation failures | Replaced 75 assertions in active Python code with explicit checks. Moved header-reading outside validation. Baseline and full developed reconstruction both passed under -O. Deliberate corruption of the expected flow constant was rejected normally and under -O. |
| Add negative tests | Ten invalid-input cases were rejected: wrong flow coefficient in two modes; wrong graph count; a loop in a witness; wrong new polynomial coefficient; wrong q=1 limit sign; a missing certificate; an unavailable compiler; an altered historical manuscript table; an altered current printed coefficient. |
| Clarify approximate root metadata | Active old witness metadata now uses `approximate_above_two_roots` and a discovery-only role. Exact interval proofs do not depend on floating-point roots. |
| Add a proof-dependency map | Section 1 traces the word identity, finite representation, fan limits, amplification and each parameter family. |
| Preserve quantifier warnings | Abstract, main theorem, README, ledgers and scope section state that G may depend on both q and p. |
| Keep ALR criticism version-specific | Appendix D refers to arXiv:2509.18788v1, Lemma A.1 as printed. It supplies a vertex-interface correction and explains compatibility with three two-terminal attachments. It does not claim ALR Theorem 1.6 is false or fully re-audit that theorem. |
| Clarify cancellation | The amplification lemma specifies distinct non-post endpoints. Its involution selects the first open non-post vertical along the ordered path, making the reversal canonical. |
| Reduce sizes or extend intervals when tractable | Retains the supplied v0.2 all-p interval up to 2.764 and smaller fixed-core graph. Adds the new all-p interval [alpha,1) and a separate q=1 limit, producing an exact local classification. |

## Evidential limits

The new symbolic polynomial is reconstructed from five ordered equality partitions; the three two-block partitions are not collapsed to one representative. Seven independently implemented quadratic-field evaluations agree exactly with the formula. The q=1 proof is supported by symbolic projector/nilpotence identities and exact jet/frontier comparisons, but those finite tests do not themselves prove a statement for every real x. The proof supplies that step.

The current LaTeX consistency checker examines 42 specified checks, including every printed coefficient polynomial, both numerical tables and selected normalisations. It is not a semantic proof checker. The historical presentation check is explicitly labelled historical. All archived source materials remain recoverable.
