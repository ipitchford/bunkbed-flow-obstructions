#!/usr/bin/env python3
"""Reconstruct the doubled-triangle symbolic limit and certify its all-p sign.

Default: recompute the polynomial and compare every certificate field.
--write-certificate is an authoring command, not verification of existing data.
All sign decisions and polynomial identities are exact; no floating-point tests.
"""
from __future__ import annotations
import argparse
import itertools
import json
from math import comb
from pathlib import Path
from fractions import Fraction
import sympy as S
from qlt1_exact import QF, G_exact

ROOT = Path(__file__).resolve().parents[1]
q, h = S.symbols('q h')
PARTITIONS = ((0,0,0), (0,0,1), (0,1,0), (0,1,1), (0,1,2))

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def expand(A):
    return A.applyfunc(S.expand)

def multiply(A, B):
    return expand(A * B)

def compound(A):
    pairs = tuple(itertools.combinations(range(A.rows), 2))
    C = S.Matrix([[S.expand(A[i,u]*A[j,v]-A[i,v]*A[j,u])
                   for u,v in pairs] for i,j in pairs])
    return C, pairs

def contraction(X, pairs, w, v):
    result = 0
    for a in range(len(v)):
        left = S.Matrix([w[i]*int(j==a)-w[j]*int(i==a) for i,j in pairs])
        right = S.Matrix([v[i]*int(j==a)-v[j]*int(i==a) for i,j in pairs])
        result += (left.T * X * right)[0]
    return S.expand(result)

def derive_polynomial():
    """Five equality partitions are evaluated separately, never grouped by r."""
    total = 0
    for pi in PARTITIONS:
        r = max(pi)+1
        n = r+1
        v, w = S.ones(n,1), S.Matrix([1]*r+[q-r])
        matrices, rank_one = {}, {}
        for s in range(r):
            e = S.eye(n)[:,s]
            A = expand((v+h*e)*(w+h*e).T)
            B = expand((q-1)*(S.eye(n)-e*e.T)-(v-e)*(w-e).T)
            AB, pairs = compound(A+B)
            AA, _ = compound(A)
            BB, _ = compound(B)
            require(AA == S.zeros(len(pairs)), 'Rank-one compound is nonzero')
            matrices[s], rank_one[s] = expand(AB-AA-BB), A
        X, K = S.eye(len(pairs)), S.eye(n)
        for s in pi:
            X, K = multiply(X,matrices[s]), multiply(K,rank_one[s])
        # ABCABC: preserve the ordering of the three factors.
        X, K = multiply(X,X), multiply(K,K)
        term = contraction(X,pairs,w,v)+(q-1)**6*(q-r-1)*(w.T*K*v)[0]
        total += S.prod(q-i for i in range(r))*term
    total = S.Poly(S.expand(total),q,h)
    factor = S.Poly(q*(h+q)**2*(q-2)*(q-1),q,h)
    quotient, remainder = S.div(total,factor)
    require(remainder.is_zero, 'Doubled-triangle factorisation has a remainder')
    P = quotient.as_expr()
    require(S.Poly(P,h).degree()==10, 'Wrong degree in h')
    return P

def bernstein(poly, a, b):
    """Power-to-Bernstein conversion with an exact reverse reconstruction."""
    t = S.symbols('t')
    transformed = S.Poly(S.expand(poly.subs(q,a+(b-a)*t)),t)
    n = transformed.degree()
    coefficients = [sum(transformed.nth(j)*S.Rational(comb(i,j),comb(n,j))
                        for j in range(i+1)) for i in range(n+1)]
    reverse = sum(coefficients[i]*comb(n,i)*t**i*(1-t)**(n-i)
                  for i in range(n+1))
    require(S.expand(reverse-transformed.as_expr())==0, 'Bernstein reverse check failed')
    return coefficients

def field_power(a, n):
    result = 1
    for _ in range(n):
        result = result*a
    return result

def check_quadratic_field(P):
    cases = [(Fraction(4,5),Fraction(1)), (Fraction(4,5),Fraction(1,100)),
             (Fraction(9,10),Fraction(1000)), (Fraction(1,2),Fraction(1)),
             (Fraction(7,10),Fraction(10)), (Fraction(79,100),Fraction(1,1000)),
             (Fraction(999,1000),Fraction(3,7))]
    rows=[]
    for qq,x in cases:
        f=1+x
        tau=x*x+3*x+qq
        delta=tau*tau-4*f*x*(qq+x)
        lp=QF(tau/2,Fraction(1,2),delta)
        hh=x+QF(f*x*x,0,delta)/(lp-f*x)
        ss=qq-1+field_power(1+hh,2)/f
        value=QF(0,0,delta)
        for c in S.Poly(P.subs(q,S.Rational(qq.numerator,qq.denominator)),h).all_coeffs():
            value=value*hh+Fraction(int(c.p),int(c.q))
        actual=qq*qq*field_power(hh+qq,2)*(qq-2)*value/(field_power(ss,6)*(qq-1)**6)
        expected=G_exact([0,1,2]*2,qq,x)
        difference=actual-expected
        require(difference.a==0 and difference.b==0,
                f'Independent quadratic-field formula mismatch at {(qq,x)}')
        rows.append({'q':str(qq),'x':str(x),'sign':actual.sign(),'exact_match':True})
    return rows

def make_certificate():
    P=derive_polynomial()
    coeffs=[S.Poly(P,h).nth(k) for k in range(11)]
    g=q**5-7*q**4+19*q**3-28*q**2+26*q-10
    require(S.expand(coeffs[0]-q**7*g)==0,'Wrong constant coefficient')
    require(S.expand(coeffs[1]-10*q**6*g)==0,'Wrong linear coefficient')
    root_poly=S.Poly(g,q)
    a=S.Rational(787422865474633,10**15)
    b=S.Rational(787422865474634,10**15)
    require(root_poly.count_roots(-S.oo,S.oo)==1,'Quintic does not have one real root')
    require(root_poly.eval(a)<0<root_poly.eval(b),'Root bracket signs fail')
    require(S.Rational(787,1000)<a<b<S.Rational(4,5),'Root bracket ordering fails')
    bern={}
    for k in range(2,11):
        B=bernstein(coeffs[k],S.Rational(787,1000),S.Integer(1))
        require(all(c>0 for c in B),f'Nonpositive Bernstein coefficient, h^{k}')
        bern[str(k)]=[str(c) for c in B]
    # Also provide the shorter rational corollary independently of root isolation.
    simple={}
    for k in range(11):
        B=bernstein(coeffs[k],S.Rational(4,5),S.Integer(1))
        require(all(c>0 for c in B),f'Rational corollary fails for h^{k}')
        simple[str(k)]=[str(c) for c in B]
    return {
       'schema':'evidence-press-bunkbed-below-universal-v03',
       'word':[0,1,2,0,1,2],
       'equality_partitions':[list(pi) for pi in PARTITIONS],
       'P_coefficients_h_ascending_q_ascending':[
          [int(S.Poly(c,q).nth(j)) for j in range(S.Poly(c,q).degree()+1)] for c in coeffs],
       'quintic_q_ascending':[-10,26,-28,19,-7,1],
       'unique_real_root_bracket':[str(a),str(b)],
       'bernstein_interval':['787/1000','1'],
       'bernstein_h2_to_h10':bern,
       'rational_corollary_interval':['4/5','1'],
       'bernstein_h0_to_h10_rational_corollary':simple,
       'quadratic_field_crosschecks':check_quadratic_field(P),
       'mathematical_scope': 'All 0<p<1, alpha<=q<1; graph may depend on q and p. Alpha is sharp only for all-p negativity of this fixed doubled-triangle limiting test.'
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificate',action='store_true')
    args=parser.parse_args()
    result=make_certificate()
    destination=ROOT/'data'/'below_universal_v03.json'
    if args.write_certificate:
        destination.write_text(json.dumps(result,indent=2)+'\n')
        print('AUTHORING: certificate reconstructed and written; not a comparison with prior data.')
    else:
        expected=json.loads(destination.read_text())
        require(result==expected,'Stored below-q=1 certificate differs from exact reconstruction')
        print(json.dumps({'check':'all-p below-one theorem: symbolic five-partition identity, 9 Bernstein positivity polynomials, global quintic root isolation, 7 independent field comparisons','status':'PASS','root_bracket':result['unique_real_root_bracket']}))

if __name__=='__main__':
    main()
