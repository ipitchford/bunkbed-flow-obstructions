# Response to the supplied v0.3 referee review

Revision: v0.3.1 candidate, 30 September 2026. The supplied assessment is
model-assisted, not external human peer review. Its prospective REF rating is
not an official REF assessment and does not increase the assurance status.

| Request | Disposition |
| --- | --- |
| Consolidate earlier ranges, models and quantifiers | Added the comparison paragraph in Section 1: ALR's 0.56–1.43 range, fixed-post weighted starting point, full/unweighted extensions, and the present every-prescribed-p formulation are distinct. Alpha is explicitly not a record lower endpoint. |
| Display the q=1 remainder | Section 7 now displays the C(x)(1+L) bound and its O_x(L^-5) normalised decay. Constants need not be uniform in x. |
| Minimal exact identity route | Section 6 gives bidegree bookkeeping (17,12); code/check_below_identity.py uses only integers and standard-library Python at 234 points. Its altered-coefficient negative control is optimisation-safe. |
| Update Hollom | Bibliography cites EJC 128 (2025), 104188, DOI 10.1016/j.ejc.2025.104188, retaining arXiv:2406.01790. |
| Remove date-history digression | Removed from Section 1. Provenance clarification: ALR arXiv:2509.18788v1 was submitted 23 September 2025; this is not a September 2026 first submission. |
| Fixed-parameter asymptotic constants | Explicit convention added to Section 1, with narrower x-dependence at the exceptional point. |
| Theorem-first presentation | Anonymous byline and scientific abstract retained; short candidate disclosure retained for this public candidate rather than implying external validation. |
| Licences and durable deposit | Publication obligations: original prose/data CC0-1.0, original code MIT; third-party material retains its own status. Deposits are not yet claimed by this response. Final public identifiers must be recorded at publication. |
| Stronger future research | Smaller graphs and wider intervals are open directions, not unfulfilled corrections. No new theorem is claimed. |

The main transfer theorem and parameter window are unchanged. The current
revision retains the distinction between universal written arguments, finite
certificate checking, producer-side reconstruction, independently written
model-assisted checks, formal verification and external specialist review.
The latter two are not established. The q=2 positive theorem is prior work;
integer q>=3 and a global parameter classification remain unresolved.

The ALR v1 Lemma A.1 objection concerns edge occupation, not connectivity;
neither this revision nor the supplied review claims to refute ALR's headline
counterexample theorem. Fixed-core pendant minimality is not global minimality.

Local execution of the added checker and its -O negative control passed on
30 September 2026. The complete revised-package reconstruction is recorded
separately; this sentence does not assert its completion.
