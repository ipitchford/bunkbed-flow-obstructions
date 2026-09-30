---
title: "Flow-polynomial obstructions to the random-cluster bunkbed inequality — version 0.2"
subtitle: "Independent verification of v0.1, analytic coverage of $(2,q_c)$ with $q_c\\approx 2.5747$, certified witnesses to $q=2.764$, and the regime below $q=1$"
author: "Evidence Press candidate release (no individual authorship assigned)"
date: "30 September 2026"
geometry: margin=24mm
fontsize: 11pt
header-includes:
  - \usepackage{amsmath,amssymb,amsthm,booktabs,longtable}
  - \newtheorem{theorem}{Theorem}[section]
  - \newtheorem{proposition}[theorem]{Proposition}
  - \newtheorem{lemma}[theorem]{Lemma}
  - \newtheorem{corollary}[theorem]{Corollary}
  - \theoremstyle{remark}\newtheorem{remark}[theorem]{Remark}
  - \DeclareMathOperator{\tr}{tr}
---

**Scope and assurance.** This is version 0.2 of a research candidate on Ayyer–Linusson–Ravichandran Problem 1.4. It is not a complete classification of the pairs $(p,q)$ for which the random-cluster bunkbed inequality holds on every finite graph. Everything computational in this release is exact arithmetic (integers, rationals, or elements of a real quadratic field); floating point was used only for discovery and for one descriptive map that is separately re-checked on an exact grid. The mathematics has been checked by a second, independent agent session (this one) against the first, but not by an external referee and not in a proof assistant. Novelty claims are bounded by the search described in Section 9.

# Summary of what changed between v0.1 and v0.2

Version 0.1 proved the *Eulerian-flow transfer theorem*: for real $q>1$, every connected loopless Eulerian multigraph $\Gamma$ with $F_\Gamma(q)<0$ yields, for every edge probability $p\in(0,1)$, a finite connected simple graph $G$ whose full bunkbed $G\square K_2$ violates the inequality $\mu(u_0\leftrightarrow v_0)\ge\mu(u_0\leftrightarrow v_1)$. It applied the theorem to evenly thickened triangles (all $q\in(1,2)$) and to one twelve-vertex graph $\Gamma_*$ certified negative on $[21/10,9/4]$.

Version 0.2 does five things.

1. **Audit.** Every claim in v0.1 (its ledger items C1–C7) was re-derived by hand and re-computed with independently written code, including a third algorithm for the flow polynomial and independent dynamic programmes for the conditioned and full bunkbed numerators. All claims stand. Two small presentational gaps in the proof of the amplification lemma are closed (Section 3). The explicit rational error bound of v0.1 Appendix A was tested against exact values in 86 instances and never violated.

2. **Exact interval for $\Gamma_*$.** Its quotient polynomial has exactly two real roots, at $2.023166\ldots$ and $2.273075\ldots$; so $\Gamma_*$ certifies failure on the whole open interval between them, not only on $[2.1,2.25]$.

3. **An analytic family above 2.** The complete bipartite graphs $K_{4,b}$ with $b$ even have a closed-form flow polynomial (Theorem 4.1). Its dominant term for large $b$ is negative exactly when $3q>(q-1)^4+(q-1)$, i.e. for $2<q<q_c$ where $q_c=2.574743\ldots$ is the real root of $q^3-4q^2+6q-6$. Hence the inequality fails for every $p\in(0,1)$ and every $q\in(2,q_c)$. Combined with the thickened triangles, **every $q\in(1,2)\cup(2,q_c)$ fails at every $p$**; the Ising point $q=2$ is an isolated universal point.

4. **Certified witnesses to $q=2.764$.** Four-regular circulant graphs $C_n(1,5)$, $C_n(3,4)$ and $C_n(2,5)$ have negative flow polynomials on intervals that widen with $n$; $C_{32}(1,5)$ is certified negative on $[2.0000001, 2.7640]$. Together with $q_c$, the certified failure set above 2 is the interval $(2, 2.764]$. A ten-vertex four-regular witness, $C_{10}(1,4)$, also exists; the v0.1 sampling of four-regular graphs on 8 and 10 vertices had missed it.

5. **The regime $0<q<1$.** For $q<1$ the ordering of the fan eigenvalues reverses ($\lambda_-<x<\lambda_+$), so the v0.1 limit does not apply, but a different limit exists (Proposition 7.1). Its sign is an exactly computable algebraic number. For the doubled triangle it is negative at every tested $p$ once $q\ge 0.79$, and for tenfold-thickened triangles once $q\gtrsim 0.575$ at $p$ near 1. Because the amplification lemma needs only $q>0$, any finite chain with a negative conditioned numerator is already a counterexample; seven such exact certificates are supplied, together with a fully specified full bunkbed counterexample at $(q,p)=(9/10,1/2)$ with $6{,}854$ vertices and $10{,}537$ edges.

A smaller explicit witness at $q=3/2$, $p=1/2$ is also given (21,854 bunkbed vertices instead of 56,708), with the exact minimal number of pendant vertices computed from the full cubic $N(y)$ rather than from the crude bound.

What remains open is stated in Section 10: integer $q\ge3$, all non-integer $q>2.764$ (no Eulerian witness was found above $2.77$ and none at all above 3), and the part of the region $q<1$ where the fan limit is positive.

# Setting and notation

For a finite simple graph $G=(V,E)$ write $G\square K_2$ for its full bunkbed, with vertex copies $u_0,u_1$. Fix $q>0$ and $0<p<1$ and put $x=p/(1-p)$. The random-cluster weight of an edge set $A\subseteq E(G\square K_2)$ is $q^{k(A)}x^{|A|}$, isolated vertices counting as components. The signed numerator
$$\mathcal N_G(q,x)=\sum_{A}q^{k(A)}x^{|A|}\big(\mathbf 1_{u_0\leftrightarrow v_0}-\mathbf 1_{u_0\leftrightarrow v_1}\big)$$
has the sign of $\mu(u_0\leftrightarrow v_0)-\mu(u_0\leftrightarrow v_1)$, so the inequality fails at $(p,q)$ exactly when $\mathcal N_G<0$ for some $G,u,v$.

For a multigraph $\Gamma$ with $t$ vertices and $m$ edges the flow polynomial is
$$F_\Gamma(q)=\sum_{B\subseteq E(\Gamma)}(-1)^{m-|B|}q^{|B|-t+k(B)}.$$
For Eulerian $\Gamma$ and every integer $k\ge2$, the constant assignment $1$ on an Eulerian orientation is a nowhere-zero $\mathbb Z_k$-flow, so $F_\Gamma(k)\ge k-1>0$; in particular $F_\Gamma(2)=1$ for every connected Eulerian $\Gamma$. Negative values of $F_\Gamma$ are therefore confined to open intervals between consecutive integers.

Two facts from the literature are used as black boxes. Häggström's theorem (ALR Theorem 1.5) says the inequality holds for every graph and every $p\in[0,1]$ at $q=2$. The v0.1 manuscript reproduces the standard FKG argument for it; that argument was re-read and is correct. Ayyer, Linusson and Ravichandran report failure for $0.56<q<1.43$ (their Theorem 1.6) via a weighted GPZ gadget at $p=1/100$; their closing remark computes the doubled-triangle polynomial $q^3-5q^2+10q-7$, which is the special case $\Gamma=2C_3$ of the v0.1 word identity.

# Audit of v0.1

The v0.1 bundle is included unchanged as `v0_1/`; its checksums verify and its check suite passes in about four seconds. The audit re-derived each proof and re-implemented each computation from scratch (`code/bb_tools.py`).

**Word identity (v0.1 Theorem 2.1, ledger C1).** The exterior-square computation was re-done by hand: $\bigwedge^2(J+\lambda e_se_s^{\top})=\lambda(\mathbf 1\wedge e_s)(\mathbf 1\wedge e_s)^{\top}$, $\langle\mathbf 1\wedge e_s,\mathbf 1\wedge e_a\rangle=q\delta_{sa}-1$, and $\sum_a(q\delta_{as_1}-1)(q\delta_{s_ma}-1)=q(q\delta_{s_1s_m}-1)$, which produces the closing transition of the cyclic word. The identity was also tested numerically: a brute-force enumeration of the two-layer hypergraph at random rational $(q,\lambda_1,\dots,\lambda_m)$ agrees with $q^{t+2}\prod\lambda_i\,F_{\Gamma_w}(q)/(q-1)$ for eleven words including loops and repeated labels (22 random points).

**Fan limit (v0.1 Proposition 3.1, part of C2).** The spectral facts were checked: on the invariant plane the matrix of $RD_s$ in the basis $(e_s,v)$ is $\begin{pmatrix}fx&x^2\\ f&q+2x\end{pmatrix}$ with trace $\tau=x^2+3x+q$, determinant $d=(1+x)x(q+x)$; the characteristic polynomial at $x$ equals $x^2(q-1)$, so for $q>1$ both eigenvalues exceed $x$. The reduced $(r{+}1)$-dimensional representation, the projector $P_s$, the exact identity $C_2(M_{s,L}P_s)=a_L\mathcal R_s$ and the contraction formula were verified line by line. Convergence of $\mathcal N^T_{w,L}/a_L^m$ to $q^{t+2}F/(q-1)$ was observed with an independently written frontier dynamic programme (Table 1 in `data/word_core_audit.json`); at $q=21/10,x=1$ the normalised numerator of $(ABC)^2$ moves $59.81,56.81,53.07,50.21,49.62,49.50$ towards the limit $49.458\ldots$ for $L=1,2,4,8,12,16$.

**Amplification lemma (v0.1 Lemma 4.1, part of C2).** Two presentational gaps were closed. (i) The involution must be defined with a canonical choice: let $y$ be the *first* non-post path vertex (from $u$) whose vertical edge is open, and swap the two layers on the path suffix strictly after $y$. This preserves the set of configurations with first open non-post vertical at $y$, preserves weights and component counts (it is an automorphism of the graph obtained by wiring all designated posts and the vertex $y$), and exchanges the two target events unless $y=v$, in which case the events coincide. (ii) The lemma needs $u\neq v$ and $u,v$ non-posts; both hold for fan chains with $m\ge1$. With these two additions the proof is complete. Independently: a full-bunkbed dynamic programme gives $N(y)$ as a polynomial in the designated-vertical activity $y$; on three tiny cores (including one with $q=7/10<1$) it agrees with brute-force enumeration at four values of $y$, and its leading coefficient equals the conditioned numerator $\mathcal N^T$ exactly. The pendant reduction (factor $D=q^2+3qx+3x^2$, activity $r=x^3/D$, parallel composition $y_k=(1+x)(1+r)^k-1$) was confirmed by brute force with one and two pendants.

**Thickened triangles (C3).** The closed form $F_{\ell C_3}(q)=q^{-3}[(z^\ell+z)^3+z(z^\ell-1)^3]$, $z=q-1$, was re-derived from the bundle transfer $N_\ell(0)=(z^\ell+z)/q$, $N_\ell(\ne0)=(z^\ell-1)/q$ for even $\ell$, and matched against the exact flow polynomials for $\ell=2,4,6$ at three values of $q$.

**The witness $\Gamma_*$ (C4).** Its flow polynomial was recomputed by a third algorithm (a set-partition frontier dynamic programme processing edges one at a time, distinct from the edge-subset and vertex-partition enumerations of v0.1) and agrees coefficient by coefficient. The Bernstein certificate on $[21/10,9/4]$ was reproduced. The graph is asymmetric (trivial automorphism group), non-planar, has three triangles and is not isomorphic to any of the named twelve-vertex four-regular graphs tried (Chvátal, cuboctahedron, the circulants $C_{12}(a,b)$, $C_3\square C_4$).

**Ising point and minimum (C5, C6).** The FKG argument in v0.1 Proposition 5.1 is the standard one and is correct; the conditional independence of the two layers given the post spins, and the fact that arbitrary-sign boundary fields do not disturb the FKG lattice condition of a ferromagnetic Ising model, are exactly what is needed.

**ALR Lemma A.1 (C7).** The counterexample was re-computed: at $q=2,p=1/2$ the single edge $ab$ is open with probability $1/3$ in the graph $\{ab\}$ and $5/14$ in the triangle, with no common edges. The literal statement is therefore false. We add that ALR's application of the lemma (with $m=3$, the three post verticals along which the pendant gadgets $K_t$ are attached) is consistent with a corrected statement in which $m$ counts the attachment gadgets, each of which meets the base graph in a single vertex pair and can merge at most one component; so the flaw is in the wording, not necessarily in ALR's Theorem 1.6. Neither v0.1 nor v0.2 depends on it.

**Error bound (v0.1 Appendix A).** The bound $E_L$ was implemented for an arbitrary word and compared with exact values of $|\mathcal N^T_{w,L}/a_L^m-\text{limit}|$ in 86 instances (three words, four pairs $(q,x)\in\{(3/2,1),(21/10,1),(5/2,1/2),(3,2)\}$, $L\le30$). Whenever the bound is defined ($\varepsilon_L\le1$) it exceeds the true error, typically by two to four orders of magnitude. This is evidence, not a proof; the proof in v0.1 Appendix A was read and no error was found.

**Outcome.** All seven ledger items keep their v0.1 status. The claims that depend on the general transfer theorem (C2–C5) now rest on two independent readings of the proof and on independent code.

# The exact interval of $\Gamma_*$ and an analytic family above 2

## Exact roots of the twelve-vertex witness

Write $F_{\Gamma_*}(q)=(q-1)P(q)$ with $P$ the degree-12 quotient from v0.1. Sturm-sequence root isolation over $\mathbb Q$ shows that $P$ has exactly two real roots,
$$\rho_1=2.0231663356188748\ldots,\qquad \rho_2=2.2730755356098221\ldots,$$
and $P<0$ precisely on $(\rho_1,\rho_2)$. A certificate with short rational endpoints: $P(2.0232)<0$, $P(2.2730)<0$ and $P$ has no root in $(2.0232,2.2730)$. Since $F(2)=1$ and $F'(2)=-47$, the first root lies close to $2+1/47$.

## Complete bipartite graphs $K_{4,b}$

\begin{theorem}[Closed form]
Let $b$ be a positive integer and $z=q-1$. Then
$$q^{3+b}F_{K_{4,b}}(q)=(z^4+z)^b+4z(-1)^b(z^3+1)^b+3z(2z^2+z-1)^b+6z(z-1)(z^2-z-2)^b+z(z-1)(z-2)(-3q)^b .$$
\end{theorem}

*Proof.* For integer $q\ge2$, $q^{a+b}F_{K_{a,b}}(q)=\sum_{\sigma\in[q]^a}g(\sigma)^b$ with $g(\sigma)=\sum_{c\in[q]}\prod_{i=1}^a(q\delta_{\sigma_i c}-1)$: this is the colour-sum form of the flow polynomial (each edge carries weight $q-1$ if its endpoints agree and $-1$ otherwise), with the $b$ right-hand vertices summed independently. If $\sigma$ has equality partition with block sizes $n_1,\dots,n_r$, then $g=(-1)^a\big[\sum_j(1-q)^{n_j}+q-r\big]$. For $a=4$ the five partition types $\{4\},\{3,1\},\{2,2\},\{2,1,1\},\{1,1,1,1\}$ occur $1,4,3,6,1$ times, are weighted by $(q)_r=q(q-1)\cdots(q-r+1)$, and give $g=z^4+z,\ -(z^3+1),\ 2z^2+z-1,\ z^2-z-2,\ -3q$ respectively. Summing and dividing by $q$ gives the display for every integer $q\ge2$; both sides are polynomials in $q$, so it holds identically. $\square$

The closed form was checked against the exact flow polynomial for $b=2,4,6,8,10$ at six values of $q$, including a negative one.

\begin{theorem}[Analytic coverage of $(2,q_c)$]
Let $q_c=2.574743073887\ldots$ be the unique real root of $q^3-4q^2+6q-6$. For every $q\in(2,q_c)$ there is an even $b$ with $F_{K_{4,b}}(q)<0$. Consequently, for every $p\in(0,1)$ and every $q\in(1,2)\cup(2,q_c)$, the random-cluster bunkbed inequality fails on some finite connected simple full bunkbed graph.
\end{theorem}

*Proof.* Let $z=q-1\in(1,z_c)$ with $z_c=q_c-1$. For even $b$ the closed form reads
$$q^{3+b}F=(z^4+z)^b+4z(z^3+1)^b+3z(2z^2+z-1)^b+6z(z-1)\big((2-z)(z+1)\big)^b-z(z-1)(2-z)(3q)^b .$$
The last coefficient $z(z-1)(2-z)$ is positive for $1<z<2$. The base $3q=3(z+1)$ strictly exceeds every other base in absolute value on this range: $z^4+z<3z+3$ is equivalent to $z^4-2z-3<0$, and $z^4-2z-3$ is increasing on $z>0.8$, negative at $z=1$, and vanishes at $z=z_c$ (indeed $(q-1)^4-2(q-1)-3=q(q^3-4q^2+6q-6)$); $z^3+1<3z+3$ is $(z-2)(z+1)^2<0$; $2z^2+z-1<3z+3$ is $2(z-2)(z+1)<0$; and $(2-z)(z+1)<3(z+1)$ is trivial. So the negative term dominates for all large even $b$, and $F_{K_{4,b}}(q)<0$. $K_{4,b}$ is connected, loopless and Eulerian for even $b$, so the v0.1 transfer theorem applies at every $p$. The interval $(1,2)$ is the v0.1 thickened-triangle result. $\square$

For orientation, the negativity intervals of the first members are $(2.01252,2.35620)$ for $K_{4,6}$, $(2.00124,2.45834)$ for $K_{4,8}$, $(2.0000151,2.52162)$ for $K_{4,12}$ and $(2.0000002,2.53945)$ for $K_{4,16}$; the upper endpoints increase towards $q_c$ and the lower endpoints collapse onto $2$.

The same colour-sum analysis explains why $K_{4,b}$ is the best of the "hub" families: for right-hand vertices of degree $s$ the competing bases are $(s-1)q$ (all hub colours distinct, coefficient sign $(-1)^{s-3}$ on $(2,3)$) and $z^s+z$ (hubs monochromatic), and $s=4$ gives the largest crossover. Above $q=3$ no hub family can work, because $(q)_s<0$ on $(3,4)$ only for odd $s$, which is incompatible with even degrees.

\begin{corollary}
Within $(1,q_c)$ the set of $q$ for which the inequality holds for all finite graphs and all $p$ is exactly $\{2\}$.
\end{corollary}

# Certified circulant witnesses beyond $q_c$

Four-regular circulants $C_n(a,b)$ (vertices $\mathbb Z_n$, $i\sim i\pm a,i\pm b$) were scanned exactly. For each graph the flow polynomial was computed by the frontier dynamic programme, its real roots above 2 were isolated exactly (there are always exactly two), and a certificate $[a,b]$ with short rational endpoints was verified: $P(a)<0$, $P(b)<0$, and no real root of $P$ in $(a,b)$ (exact Sturm count). Table 1 lists the certificates in `data/witnesses_above2.json`.

| graph | $n$ | $m$ | roots above 2 | certified negative on |
|---|---|---|---|---|
| $C_{10}(1,4)$ | 10 | 20 | 2.0416727, 2.2898825 | $[2.0416727,\ 2.2898]$ |
| $C_{10}(1,3)$ | 10 | 20 | 2.0779349, 2.1816214 | $[2.077935,\ 2.1816]$ |
| $C_{12}(2,3)$ | 12 | 24 | 2.0082964, 2.4319893 | $[2.0082965,\ 2.4319]$ |
| $C_{14}(1,3)$ | 14 | 28 | 2.0036336, 2.4528066 | $[2.0036336,\ 2.4528]$ |
| $C_{16}(2,3)$ | 16 | 32 | 2.0006060, 2.5655973 | $[2.0006061,\ 2.5655]$ |
| $C_{18}(1,5)$ | 18 | 36 | 2.0001330, 2.6353885 | $[2.000133,\ 2.6353]$ |
| $C_{20}(3,4)$ | 20 | 40 | 2.0000382, 2.6576665 | $[2.0000382,\ 2.6576]$ |
| $C_{24}(2,5)$ | 24 | 48 | 2.0000031, 2.7039901 | $[2.0000031,\ 2.7039]$ |
| $C_{24}(3,4)$ | 24 | 48 | 2.0000025, 2.7102185 | $[2.0000026,\ 2.7102]$ |
| $C_{28}(1,5)$ | 28 | 56 | 2.0000002, 2.7450789 | $[2.0000003,\ 2.7450]$ |
| $C_{32}(1,5)$ | 32 | 64 | 2.0000000, 2.7640992 | $[2.0000001,\ 2.7640]$ |

Table 1. Certified negative intervals of $P=F/(q-1)$ for circulant witnesses. Roots are given to seven decimals; the certificates are exact.

Since every certified interval that reaches beyond $q_c$ begins below $q_c$, the union of Theorem 4.2 with Table 1 is an interval:

\begin{theorem}
For every $p\in(0,1)$ and every $q\in(2,\,2.7640]$ the random-cluster bunkbed inequality fails on some finite connected simple full bunkbed graph.
\end{theorem}

The upper endpoints of $C_n(1,5)$ are $2.6187,2.6822,2.7079,2.7156,2.7451,2.7508,2.7641$ for $n=20,22,\dots,32$, still increasing; nothing in the present release says where the family's limit lies, and no Eulerian graph with a negative flow value above $2.77$ was found (Section 8). Other families behave similarly: $K_{6,b}$ and $K_{8,b}$ have crossover constants $2.49044\ldots$ and $2.40802\ldots$ (from the roots of $z^6-4z-5$ and $z^8-6z-7$, $z=q-1$), the tori $C_a\square C_b$ and the six-regular circulants $C_n(1,3,5)$ reach $2.5$–$2.63$ at $n\le20$.

The smallest four-regular witnesses found are the ten-vertex circulants $C_{10}(1,3)$ and $C_{10}(1,4)$; v0.1 had sampled four-regular graphs on 8 and 10 vertices without finding one, so the earlier remark that no such witness was found should be read as a statement about that sample.

# A smaller explicit witness at $q=3/2$, $p=1/2$

For $\ell C_3$ fan cores at $q=3/2$, $x=1$ the smallest core with a negative conditioned numerator, over $\ell\in\{4,6,8\}$ and $1\le L\le 25$, is $\ell=4$, $L=19$ (232 vertices, 468 edges; every smaller $L$ is positive). The next are $\ell=6,L=16$ (292 vertices) and $\ell=8,L=15$ (364 vertices). For the $L=19$ core the full-bunkbed numerator with the three designated verticals at activity $y$ is a cubic
$$N(y)=a_0+a_1y+a_2y^2+a_3y^3,\qquad a_0,a_1,a_2>0,\quad a_3=\mathcal N^T<0,$$
with $\log_{10}|a_j|\approx 339,339,316,165$. Its unique positive root is about $10^{151}$, and the exact minimal number of pendant vertices per post is $k=3565$ (with $y_k=2(43/39)^k-1$): $N(y_{3565})<0\le N(y_{3564})$, both evaluated exactly. The explicit counterexample is therefore the full bunkbed of the base graph with $10{,}927$ vertices and $11{,}163$ edges: $21{,}854$ vertices and $33{,}253$ edges. For comparison, v0.1's crude bound gave $k=9370$ for the $L=20$ core ($56{,}708$ bunkbed vertices); the exact minimum for that core is $k=3740$. The generator `v0_1/code/generate_graph.py` produces the edge list from the recipe with these parameters.

# Below $q=1$: the second fan limit

## Why the v0.1 argument stops at $q=1$, and what replaces it

For $0<q<1$ the discriminant $\tau^2-4d=x^4+2x^3+(5-2q)x^2+2qx+q^2$ is positive, so the plane eigenvalues $\lambda_\pm$ of $RD_s$ are real, and the characteristic polynomial at $x$ equals $x^2(q-1)<0$, so
$$0<\lambda_-<x<\lambda_+ .$$
The complementary subspace $W_s$ (dimension $r-1$ in the reduced representation), on which every fan factor acts as $x^L$, now outranks the second plane eigenvalue. The dominant second-compound mode of a fan factor is no longer $\bigwedge^2(\text{plane})$ with rate $d^L=(\lambda_+\lambda_-)^L$ but $(\text{top plane eigenvector})\wedge W_s$ with rate $(\lambda_+x)^L$.

On the reduced space write $(RD_s)^L=\lambda_+^{L}\ell_+r_+^{\top}+\lambda_-^{L}\ell_-r_-^{\top}+x^L\Pi_s$, where $\ell_\pm$ are right eigenvectors of $RD_s$, $r_\pm$ the dual left eigenvectors ($r_+^{\top}\ell_+=1$) and $\Pi_s=I-P_s$ is the projector onto $W_s$ along the plane. Explicitly $\ell_+=x^2e_s+(\lambda_+-fx)v$, and since $RD_s=v\tilde w^{\top}+xD_s$ with $\tilde w=w_r+xe_s$, the left eigenvector is $r_+\propto\big(\tilde w_i/(\lambda_+-x\,d_i)\big)_i$ with $d_i=1+x$ for $i=s$ and $d_i=1$ otherwise. Because $D_s$ acts as the identity on $W_s$, the fan factor is $M_{s,L}=D_s(RD_s)^L=\lambda_+^La_sb_s^{\top}+\lambda_-^LD_s\ell_-r_-^{\top}+x^L\Pi_s$ with $a_s=D_s\ell_+$, $b_s=r_+$. Put
$$\Lambda_s=C_2(a_sb_s^{\top}+\Pi_s)-C_2(\Pi_s),$$
the bilinear ("mixed") part of the second compound; then $C_2(M_{s,L})/(\lambda_+x)^L\to\Lambda_s$ because the omitted terms decay like $(\lambda_-/\lambda_+)^L$, $(\lambda_-/x)^L$ and $(x/\lambda_+)^L$.

\begin{proposition}[Fan limit for $0<q<1$]
Fix a word $w$ with loopless cyclic transition graph, $0<q<1$ and $x>0$. Then
$$\lim_{L\to\infty}\frac{\mathcal N^T_{w,L}(q,x)}{(\lambda_+x)^{Lm}}=G_w(q,x):=\frac{q}{q-1}\sum_{\pi\in\Pi_t}(q)_{|\pi|}\Big[\mathcal C_w\Big(\prod_{i=1}^m\Lambda_{\pi(c_i)}\Big)+(q-|\pi|-1)\,w_{|\pi|}^{\top}\Big(\prod_{i=1}^m a_{\pi(c_i)}b_{\pi(c_i)}^{\top}\Big)v\Big],$$
where $\mathcal C_w$ is the contraction $(w^{\top}Kv)\tr K-w^{\top}K^2v$ of v0.1 Section 3.3, read as a linear functional on second compounds. In particular, if $G_w(q,x)<0$ then $\mathcal N^T_{w,L}(q,x)<0$ for all large $L$, and by the amplification lemma (valid for all $q>0$) the bunkbed inequality fails at $(q,p)$, $p=x/(1+x)$, on a finite connected simple full bunkbed graph.
\end{proposition}

*Proof.* The finite post-colour representation of v0.1 Section 3.3 is a rational identity in $q$ valid for all $q\ne1$, so it may be used at $0<q<1$. In it, each partition contributes $z_\pi\big(\tr K_\pi+(q-r-1)x^{Lm}\big)-w_r^{\top}K_\pi^2v=\mathcal C_w(C_2(K_\pi))+(q-r-1)x^{Lm}z_\pi$. Divide by $(\lambda_+x)^{Lm}$. Since $C_2$ is multiplicative, $C_2(K_\pi)/(\lambda_+x)^{Lm}=\prod_i C_2(M_{\pi(c_i),L})/(\lambda_+x)^L\to\prod_i\Lambda_{\pi(c_i)}$ by the decomposition above. The second term is $(q-r-1)\,z_\pi/\lambda_+^{Lm}$, and $K_\pi/\lambda_+^{Lm}\to\prod_i a_{\pi(c_i)}b_{\pi(c_i)}^{\top}$ because each factor $M_{s,L}/\lambda_+^L\to a_sb_s^{\top}$. There are finitely many partitions, so the limit passes through the sum. The final sentence is the amplification lemma, whose proof uses only $q>0$, $x>0$. $\square$

Unlike the $q>1$ limit, $G_w$ depends on $x$ and is not a flow-polynomial evaluation; its value lies in the real quadratic field $\mathbb Q(\sqrt{\tau^2-4d})$, so its sign at rational $(q,x)$ can be decided exactly. The formula was validated against exact finite-$L$ values: for the doubled triangle at $q=1/2,x=1$ the normalised numerators $1616.5,1834.5,1852.0$ at $L=12,24,36$ approach $G=1853.64\ldots$, and at $q=9/10$ the sign change to negative occurs at the $L$ predicted by the negative limit.

## Where the limit is negative

For the thickened triangles $\ell C_3$ the exact sign of $G$ was computed on the grid $q\in\{1/20,\dots,19/20\}$, $x\in\{10^{-2},10^{-1},1/4,1/2,1,2,4,10,10^2,10^3\}$. For each $x$ the sign is positive for small $q$ and negative above a threshold $q_0^{(\ell)}(x)$, bracketed to $3\cdot10^{-4}$ by exact bisection:

| $x$ | $10^{-2}$ | $10^{-1}$ | $1/4$ | $1/2$ | $1$ | $2$ | $4$ | $10$ | $10^2$ | $10^3$ |
|---|---|---|---|---|---|---|---|---|---|---|
| $q_0^{(2)}(x)$ | 0.7876 | 0.7866 | 0.7821 | 0.7706 | 0.7460 | 0.7158 | 0.6952 | 0.6854 | 0.6830 | 0.6830 |
| $q_0^{(6)}(x)$ | 0.7706 | 0.7692 | 0.7627 | 0.7450 | 0.7067 | 0.6567 | 0.6201 | 0.6014 | 0.5969 | 0.5969 |
| $q_0^{(10)}(x)$ | 0.7677 | 0.7663 | 0.7594 | 0.7402 | 0.6986 | 0.6428 | 0.6014 | 0.5802 | 0.5746 | 0.5746 |

Table 2. Thresholds above which the $q<1$ fan limit of $\ell C_3$ is negative (exact bisection brackets, upper ends shown).

Thus, on the whole tested grid, every $q\in[4/5,1)$ is a failure point at every tested $p$ for the doubled triangle, and thicker triangles push the threshold down to about $0.57$ as $p\to1$. Even cycles behave differently: in a floating-point scan over $q\le3/4$ and $x\in\{0.1,1,10,100\}$, $2C_4$, $4C_4$, $K_{2,4}$, the doubled $K_4$ and the octahedron have positive limits at every point, while the doubled $C_5$ behaves like the doubled triangle. Two remarks on scope. First, the statements above are exact at the grid points; the claim "negative for all $x>0$ at $q=4/5$" is supported by the grid and by the monotone shape of the thresholds but is not proved. Second, this is the uniform-fan gadget only; ALR's weighted GPZ gadget reaches $q=0.56$ at $p=1/100$, where the fan limit is still positive, so the two gadgets have genuinely different limit objects.

## Finite exact certificates and an explicit graph at $q=9/10$

Independently of the limit, the exact conditioned numerator of the doubled-triangle chain is negative at
$$(q,p,L)\in\{(19/20,1/2,18),\ (9/10,1/2,21),\ (17/20,1/2,21),\ (4/5,1/2,27),\ (9/10,1/4,33),\ (9/10,3/4,24),\ (4/5,3/4,30)\},$$
each $L$ being the first negative value on a grid of step 3; each is a certified counterexample by the amplification lemma. For $(9/10,1/2,21)$ the full cubic $N(y)$ was computed exactly and the minimal pendant count determined, giving a cubic with coefficient signs $(+,+,+,-)$ and minimal pendant count $k=1099$ per post: a full bunkbed counterexample with $6{,}854$ vertices and $10{,}537$ edges (`data/explicit_q09_L21.json`). At $q\le 7/10$ and $x\in\{1,3\}$ the numerator stayed positive up to $L=42$–$48$, consistent with Table 2.

# Searches that found nothing

Simulated annealing over cyclic words (multigraphs with $t\le10$ posts and $m\le3t$ edges, floating-point evaluation by the colour-partition formula, exact re-certification of any hit) targeted $q_0\in\{2.05,2.3,2.5,2.7,2.9,3.5,4.5\}$ with 2000–3000 steps and two restarts per setting. Negative values were found only for $t=10$, on short intervals inside $(2.04,2.145)$. No word with $t\le10$ reached $q_0\ge2.5$, and nothing was negative above $3$. Structured families (wheels with doubled spokes, antiprisms, $K_5$, $K_7$, $K_{2,2k}$, tori, blow-ups, doubled wheels, $K_5\square C_n$, all circulants tried up to $n=32$) show negativity only inside $(2,2.77)$. Whether $F_\Gamma(q)>0$ for every Eulerian $\Gamma$ and every $q\ge3$ is left as a question; the corresponding statement is false for non-Eulerian graphs (odd wheels have $F<0$ on $(2,3)$, and there are flow roots above 4 in the literature).

# Priority and novelty (bounded search)

Search date 30 September 2026. Corpus: arXiv API listing of every paper matching "bunkbed" (20 entries, newest 17 November 2025), the ALR preprint (v1, 23 September 2025) read in full, the GPZ, Hollom, Meunier–Pournajafi, Przybyłowski, Denart and Donderwinkel–Jorritsma–Perarnau abstracts, and web searches for "bunkbed" with "random cluster", "Potts", "flow polynomial", "Eulerian". Outcome by contribution unit: (i) the word identity is a *bridge* between the two-layer hypergraph numerator and Tutte's flow polynomial (the Potts model at $v=-q$); its special case $2C_3$ appears in ALR's closing remark; the general identity was not found. (ii) The real-$q$ transfer at every $p$, the analytic $(2,q_c)$ family, the circulant certificates and the $q<1$ limit were not found in the bounded search. (iii) The cubic $q^3-5q^2+10q-7$ and its root $1.4301\ldots$ are Dong's constant $\xi_3$ for flow polynomials and ALR's endpoint; no novelty is claimed for them. (iv) Häggström's $q=2$ theorem is prior work; its FPSAC PDF could not be fetched from this environment (certificate mismatch on the host), so it is cited through ALR Theorem 1.5. No collision was found; this is negative search evidence, not a proof of priority. Language permitted in the paper: "not found in the bounded search described here". Language not permitted: "new", "first" without that qualifier.

# What remains open

1. Integer $q\ge3$: Eulerian flow polynomials are positive at integers, so no flow-witness argument can settle these points. No mechanism is offered.
2. Non-integer $q>2.764$: no witness was found; the circulant upper endpoints are still rising at $n=32$, so the true supremum of the flow-witness method is unknown, and nothing is known above $3$.
3. $0<q<1$: the fan limit gives failure only where $G_w<0$ (roughly $q\gtrsim0.57$ to $0.79$ depending on $p$ and $\ell$); the region below is untouched by this method, and ALR's $0.56$ at $p=1/100$ is not reproduced by it.
4. Universality for all $p$ at fixed $q<1$ is not proved for any $q$; the $q<1$ statements are pointwise in $p$.
5. Minimality of witnesses and the structure of the $q>2$ witness set (why $K_{4,b}$ and $C_n(1,5)$ but not $K_{2,b}$ or even cycles) are not addressed beyond the colour-sum heuristic in Section 4.

# Reproduction

From `code/`: `python3 certify_v02.py` (about one minute) re-runs every exact check that this manuscript relies on and writes `checks/executed_checks_v02.json`; `python3 certify_v02.py --full` also recomputes the two stored large objects (the $C_{32}(1,5)$ polynomial and the exact cubics $N(y)$), taking about a quarter of an hour. `python3 v0_1/code/run_all.py` (from the `v0_1/` folder) re-runs the original suite. Discovery scripts (`flowsearch.py`, `run_flowsearch.py`, `families*.py`, `explore_qlt1*.py`, `qlt1_map_limit.py`) are included with their logs; they use floating point and are not proof dependencies. Requirements: Python 3.11, `sympy` (root isolation and exact root counting), `numpy` (discovery only), a C++17 compiler for the v0.1 suite.
