# Flow-polynomial obstructions to the random-cluster bunkbed inequality
## Evidence Press candidate v0.3.1 — 30 September 2026

Start with [AI_INDEX.md](AI_INDEX.md) for exact claims, dependencies and safe reuse.
Reserved version DOI: https://doi.org/10.5281/zenodo.23063182.
Publication status is established by the public provider record, not this identifier alone.
See [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ASSURANCE.md](ASSURANCE.md) and
[RESPONSE_TO_V03_REVIEW.md](RESPONSE_TO_V03_REVIEW.md) for the current revision.

**Current paper:** `paper/manuscript_v0_3.pdf` (LaTeX source alongside it).

For each fixed `0 < p < 1`, let `U_p` consist of the positive q for which the random-cluster bunkbed inequality holds on every finite simple graph. This candidate proves

**U_p ∩ [alpha, 691/250] = {2},**

where alpha is the unique real root of
`q^5 - 7q^4 + 19q^3 - 28q^2 + 26q - 10`, approximately 0.78742286547463336.
The upper endpoint is exactly 2.764. Every exclusion concerns an ordinary finite connected simple full bunkbed, with the same p on every edge. The graph may depend on both p and q.

This is an exact local classification, not a complete solution of the parameter problem. The package does not classify all q below alpha or above 2.764, and does not settle integer q >= 3. It does not claim website publication, external human peer review, formal proof-assistant verification or exhaustive priority clearance.

### What changed

The supplied v0.2 results above one are retained. The new results are an all-p theorem for alpha <= q < 1, a separate q=1 Jordan-mode limit, and the resulting exact window. Seventy-five Python assertions were replaced by explicit validation, the side-effecting header read was removed, and current graph/statement checks and corruption tests were added. See `RESPONSE_TO_REVIEW.md` and `RELEASE_NOTES_v0_3.md`.

### Reproduce

Python 3.11 or newer is intended; the current publication replay used Python 3.14.7, SymPy 1.14.0 and a C++17 compiler. Earlier supplied receipts used Python 3.13.5. Install the pinned Python dependency:

```sh
python3 -m pip install -r requirements.txt
python3 code/verify_release.py
```

The default reconstructs the 32-vertex circulant polynomial and both full-core post-activity cubics, as well as running the baseline suite, new symbolic checks, graph checks and negative tests. Set `CXX` to a C++17 compiler executable when `c++` is unavailable. No internet connection is needed once the dependency and compiler are installed.

```sh
python3 -O code/verify_release.py --quick
```

Quick mode checks the stored large certificates without rebuilding every large object. Its receipt explicitly says `full_reconstruction: false`. It is not a substitute for the full reconstruction. The heavy developed stage took about ten minutes in this execution environment; other machines may differ substantially. All proof-critical validations remain active under Python optimisation. A failure raises an exception and exits nonzero.

The runner writes logs and receipts under `runs/`. `SHA256SUMS` covers fixed sources, certificates, current documents and graph files. Generated run logs are excluded. Checksums detect accidental change; they are not an external signature or a proof of mathematical truth.

### Graphs

The two current smaller base edge lists are in `graphs/`. Their full bunkbeds have 6,854 vertices at q=9/10 and 21,854 at q=3/2, both at p=1/2. The generator also supports the retained much larger q=21/10 example.

```sh
python3 code/generate_release_graph.py 3_2
python3 code/generate_release_graph.py 9_10 --full --output full_bunkbed.edges
```

The first command prints a recipe. Writing requires an explicit output path and refuses to overwrite an existing file. Files start with `number_of_vertices number_of_edges`; following lines contain endpoint pairs. Full vertices use label `2*a + layer`.

### Evidence map

`VERIFICATION_REPORT_v0_3.md` describes executed tests and their limits. `claims_v0_3.json` separates retained and new claims. `stop_receipt_v0_3.json` records the incomplete global classification. `provenance_v0_3.json` identifies the inputs and execution environment. `checks/` contains the frozen release evidence; `runs/` is for subsequent reproductions.

The original supplied v0.2 archive and referee archive are preserved byte-for-byte in `history/`. Active `v0_1/` code has documented software repairs and is not a byte-identical copy of the old release; the original is preserved inside the supplied v0.2 archive. The old papers, reports and ledgers remain historical records, not current statements of scope. The old 32-item presentation checker refers to the historical v0.2 manuscript; the current checker separately tests 42 specified formulas and table entries, not every sentence.

### Build the paper

Run `pdflatex -interaction=nonstopmode -halt-on-error manuscript_v0_3.tex` twice from `paper/`. The delivered PDF was rendered and visually inspected. The source uses standard TeX Live packages. No font files are distributed.
