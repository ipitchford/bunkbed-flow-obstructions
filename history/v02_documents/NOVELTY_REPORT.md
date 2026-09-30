# Novelty report (bounded search) — v0.2

**Search date:** 30 September 2026. **Searcher:** second agent session (this release), independent of the v0.1 session.

## Frozen claims (narrowest statements that would count as success)

1. *Statement + proof:* for real q>1 and every p∈(0,1), a negative Eulerian flow value F_Γ(q)<0 yields an ordinary homogeneous full-bunkbed counterexample (v0.1 Theorem 1.1).
2. *Statement + proof:* failure at every p for every q∈(1,2) (v0.1) and every q∈(2,q_c), q_c≈2.5747 (v0.2, analytic), and every q∈(2,2.764] (v0.2, certified).
3. *Identification (bridge):* the two-layer post-word hypergraph numerator equals q^{t+2}∏λ F_{Γ_w}(q)/(q−1) — i.e. Tutte's flow polynomial / the Potts model at v=−q (v0.1 Theorem 2.1).
4. *Statement + proof:* the q<1 fan limit G_w(q,x) (v0.2 Proposition 7.1) and pointwise counterexamples below q=1 on homogeneous unweighted graphs.
5. *Computation/verification artefacts:* exact certificates, explicit witnesses, third-algorithm recomputation.

## Normalisation

Bunkbed inequality as in ALR (2) with G̃ = G□K₂ ("full bunkbed", all posts present); random-cluster weight p^{|A|}(1−p)^{m−|A|}q^{k(A)} ≡ x^{|A|}q^{k(A)} with x=p/(1−p). Flow polynomial in Tutte's normalisation F_Γ(q)=Σ_B(−1)^{m−|B|}q^{|B|−t+k(B)} = (−1)^m q^{−t} Z_Γ(q, v=−q). The doubled triangle 2C₃ has F=(q−1)(q³−5q²+10q−7); its real root 1.4301597… is Dong's ξ₃.

## Fingerprints searched

* Sequence: coefficient vector of F_{Γ_*} (−57709, 261521, −554231, …, 1) — not a named sequence; Γ_* is asymmetric and not isomorphic to Chvátal, cuboctahedron, C₁₂(a,b), C₃□C₄ (networkx isomorphism tests).
* Constants: 1.430159709 (ALR endpoint; Dong 2015 ξ₃ — collision, credited); q_c = 2.574743073887…, root of q³−4q²+6q−6 (no source found); 32/27 (Wakelin/Jackson zero-free bound, background only).
* Formula: q^{3+b}F_{K_{4,b}} = (z⁴+z)^b + 4z(−1)^b(z³+1)^b + 3z(2z²+z−1)^b + 6z(z−1)(z²−z−2)^b + z(z−1)(z−2)(−3q)^b — a routine colour-sum evaluation; not searched for as such, no novelty claimed for the formula itself, only for its use.

## Rings searched

1. **Original source and citing papers.** ALR arXiv:2509.18788 v1 (23 Sep 2025) read in full: Problem 1.4, Theorem 1.5 (Häggström), Theorem 1.6 (0.56<q<1.43 at p=1/100, weighted GPZ gadget, series–parallel sketch), Appendix A incl. Lemma A.1 and the closing remark computing q³−5q²+10q−7 for Hollom's hypergraph. arXiv API listing of all papers matching "bunkbed" (20 entries, newest 2511.13589, 17 Nov 2025): none concerns the random-cluster q-classification after ALR. Abstracts inspected: Gladkov–Pak–Zimin (2410.02545), Hollom (2406.01790), Meunier–Pournajafi (2410.08957, v2 7 Jun 2026), Przybyłowski (2506.22284), Denart (2506.09264), Donderwinkel–Jorritsma–Perarnau (2511.13589), Tang (2502.06237).
2. **Formula/constant searches.** Web search "bunkbed conjecture random cluster model q counterexample 2026"; "bunkbed inequality Potts model flow polynomial Eulerian arXiv"; "Häggström Probability on bunkbed graphs random-cluster q=2 Theorem". No hit connecting bunkbed to flow polynomials.
3. **Aliases.** Potts model at v=−q (flow polynomial) is classical (Tutte; Sokal 2005 survey found in search results) — the bridge object is known on the flow side; the identification with the bunkbed hypergraph numerator was not found.
4. **Not done:** MathSciNet/zbMATH, Google Scholar citation lists of ALR (one year old; the arXiv listing is the proxy), author enquiry.

## Adjudication by contribution unit

| unit | outcome | permitted language |
|---|---|---|
| 1 transfer theorem (v0.1) | CLEAR within the boundary | "not found in the bounded search described here" |
| 2 parameter exclusions (1,2), (2,q_c), (2,2.764] | CLEAR within the boundary; ALR's (0.56,1.43) at p=1/100 is prior and credited; (1.43,2) and everything above 2 not found | as above |
| 3 word identity | BRIDGE (both sides known; identification not found); 2C₃ case is ALR's closing remark | "the general identity was not found; the doubled-triangle case appears in ALR" |
| 4 q<1 limit and pointwise counterexamples | CLEAR within the boundary; ALR's Theorem 1.6 already excludes q∈(0.56,1) at p=1/100 (weighted gadget, sketch); the homogeneous fan certificates and the limit object were not found | as above; do not claim to exclude any q<1 that ALR does not already exclude |
| 5 artefacts | not a novelty question | — |

## Limits of this report

Negative search evidence only. A referee with database access should re-run ring 4. The Häggström FPSAC paper was not retrievable (TLS certificate mismatch on the host); it is cited through ALR Theorem 1.5.
