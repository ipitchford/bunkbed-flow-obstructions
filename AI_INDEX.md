# AI index: flow-polynomial bunkbed obstructions

Version: 0.3.1 candidate. Scholarly creator: Anonymous.
Read this before reusing any claim. This is an unrefereed mathematical candidate,
not an end-to-end formally verified theorem or complete parameter classification.

## Exact claims and scope

For each fixed 0<p<1, let U_p be the positive cluster weights q for which the
random-cluster bunkbed inequality holds for every finite simple base graph and
every pair of vertices. The main claim is U_p intersect [alpha,691/250] = {2},
where alpha is the unique real root of
q^5-7q^4+19q^3-28q^2+26q-10 and alpha≈0.78742286547463336.
Every negative case uses a finite connected simple **full** bunkbed with the
same p on every edge. The graph may depend on both p and q.

The reusable transfer theorem: for a connected loopless Eulerian multigraph
Gamma and q>1 with F_Gamma(q)<0, every prescribed p in (0,1) admits such a
counterexample. The auxiliary multigraph is not the final simple graph.

## Claim-to-evidence map

| Claim | Written argument | Executable/data evidence | Boundary |
| --- | --- | --- | --- |
| Word identity and flow transfer | paper/manuscript_v0_3.tex, Sections 2–4 and Appendix A | v0_1/code/run_all.py | Finite checks support, not replace, the universal proof. |
| q in (1,2) fails at every p | Thickened-triangle construction, Section 5 | data/flow_witness_audit.json | Graph size depends on parameters. |
| q in (2,691/250] fails | K_(4,b) family and overlapping C32 certificate, Section 5 | code/certify_v02.py --full; data/witness_C32.json | No claim of maximal endpoint. |
| alpha<=q<1 fails at every p | Second spectral limit and positivity, Section 6 | code/verify_below_universal.py; data/below_universal_v03.json | Alpha is not a record lower endpoint versus ALR. |
| Cleared bivariate identity | Equation labelled eq:belowidentity; degree bound (17,12) | code/check_below_identity.py | 234 exact evaluations certify this identity, not the whole theorem. |
| q=1 exceptional limit | Section 7; displayed remainder bound | code/verify_percolation_limit.py | Earlier q=1 disproof is credited to GPZ. |
| Finite graph recipes | Section 8 | code/verify_graph_files.py; graphs/ | Large q=2.1 graph uses analytic bounds, not exhaustive full-state enumeration. |
| ALR v1 attachment-lemma issue | Appendix D | code/verify_interface.py | Edge-occupation counterexample; not a disproof of ALR's headline theorem. |

## Reproduction

Install Python and a C++17 compiler; install requirements.txt (SymPy 1.14.0).
From the repository root:

```sh
python3 -m pip install -r requirements.txt
python3 code/check_below_identity.py
python3 -O code/check_below_identity.py --negative-control
python3 -O code/verify_release.py
```

The last command performs full graph-polynomial and core reconstruction and
writes runs/full/opt1/receipt.json plus stage logs. Its --quick option does not
reconstruct all large objects. Explicit exceptions preserve critical checks
under optimisation. code/test_negative_cases.py requires ten corruptions to
be rejected. Manifest agreement establishes byte identity, not proof truth.

## Dependencies, objections and safe reuse

The written bridge includes finite real-q continuation before limits, spectral
ordering, exact post amplification and sign-certificate coverage. These remain
semantic proof obligations outside a proof assistant. Ising positivity at q=2
is prior work, restated with its assumptions. Consult NOVELTY_REPORT.md and
RESPONSE_TO_V03_REVIEW.md before asserting novelty.

There is no global classification below alpha or above 2.764, and integer
q>=3 is unresolved here. Eulerian negative-flow witnesses cannot settle those
integers. Pendant minimality is only for the stated fixed core with equal
numbers of pendants per post. A model-assisted referee audit and separately
written checks are not authenticated unaffiliated reproduction or human review.

## Navigation, provenance and licences

Direct package entry points: [manuscript](paper/manuscript_v0_3.pdf),
[LaTeX](paper/manuscript_v0_3.tex), [claim ledger](claims_v0_3.json),
[full verifier](code/verify_release.py), [identity checker](code/check_below_identity.py),
[review response](RESPONSE_TO_V03_REVIEW.md), [assurance](ASSURANCE.md),
[replay receipt](REPLAY_RECEIPT.md), [sources](SOURCES.md),
[provenance](PROVENANCE.md) and [licence map](LICENSES.md).

- paper/manuscript_v0_3.tex and .pdf: current revised scientific paper; filename
  retained for the existing cross-checker, displayed version 0.3.1.
- claims_v0_3.json: supplied claim ledger; revisions clarify rather than enlarge claims.
- RESPONSE_TO_V03_REVIEW.md: current review dispositions.
- README.md, NOVELTY_REPORT.md, AUDIT_LEDGER.md: original package context.
- history/: preserved historical inputs, not the current claim authority.
- LICENSES.md: component-level reuse boundaries.

Original prose, diagrams and original data: CC0-1.0. Original code: MIT.
Third-party material keeps its upstream terms. Publication identifiers and
current replay status must be read from the final release receipt; this index
does not itself establish that an upload, DOI, CI run or deployment succeeded.
