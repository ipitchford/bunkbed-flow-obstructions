# Producer-side replay receipt

On 30 September 2026, Python 3.14.7, SymPy 1.14.0, optimisation level 1:

`python3 -O code/verify_release.py`

All ten stages passed in 492.215 seconds, including the full C32 and core
polynomial reconstructions and deliberate corruption tests. The retained raw
receipt and stage logs are in publication_checks/full/opt1/. That receipt
records its original manifest identity, before final documentation and title
layout edits. It must not be described as replay of this final archive.

The final frozen archive is separately extracted and checked by the publication
gate; its exact-archive receipt is retained with the publication operational
record. Scientific sources and data are unchanged after the successful run.
The added standard-library identity checker passed 234 integer evaluations;
its altered-coefficient negative control passed under -O.

This is internal producer-coordinated execution, not formal verification,
external human peer review, or authenticated independent reproduction.
Full graph-polynomial reconstruction is distinct from --quick mode.
