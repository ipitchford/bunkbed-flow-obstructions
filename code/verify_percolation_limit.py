#!/usr/bin/env python3
"""Exact symbolic identities for the q=1 fan limit, plus finite cross-checks."""
from __future__ import annotations
import argparse,json,itertools
from pathlib import Path
from fractions import Fraction as F
import sympy as S
from bb_tools import core_numerator
from percolation_jets import exact as numerator_jets
from verify_below_universal import compound,contraction,require
ROOT=Path(__file__).resolve().parents[1]

def factored(A):
    return A.applyfunc(S.factor)

def matrix_checks():
    x=S.symbols('x',positive=True)
    f=1+x
    gap=f*f-x
    kappa=x/gap
    total=0
    rows=[]
    for pi in [(0,0,1),(0,1,0),(0,1,1),(0,1,2)]:
        r=max(pi)+1
        n=r+1
        v,w=S.ones(n,1),S.Matrix([1]*r+[1-r])
        operators={}
        for s in set(pi):
            e=S.eye(n)[:,s]
            D=S.eye(n)+x*e*e.T
            T=(v*w.T+x*S.eye(n))*D
            U=T-x*S.eye(n)
            E=factored(U*U/gap**2)
            Q=S.eye(n)-E
            require(factored(E*E-E)==S.zeros(n),'Top projector identity')
            require(factored(T*E-f*f*E)==S.zeros(n),'Top eigenvalue identity')
            require(factored(U*U*Q)==S.zeros(n),'Bottom nilpotence identity')
            A=factored(D*E)
            C=factored(D*U*Q/x)
            AC,pairs=compound(A+C)
            AA,_=compound(A)
            CC,_=compound(C)
            mixed=factored(AC-AA-CC)
            vr=S.Matrix([v[i]*e[j]-v[j]*e[i] for i,j in pairs])
            wr=S.Matrix([w[i]*e[j]-w[j]*e[i] for i,j in pairs])
            R=vr*wr.T
            require(AA==S.zeros(len(pairs)),'Top rank-one compound')
            require(factored(mixed-f*kappa*R)==S.zeros(len(pairs)),
                    'Jordan mixed compound coefficient')
            operators[s]=R
        X=S.eye(len(pairs))
        for s in pi*2:
            X=X*operators[s]
        value=contraction(X,pairs,w,v)
        factor=1 if r==2 else -1
        total+=factor*value
        rows.append({'partition':list(pi),'falling_factorial_derivative_at_1':factor,
                     'rank_one_product_contraction':int(value)})
    require(total==-1,'Leading percolation coefficient is not -1')
    return rows

def make_certificate():
    rows=matrix_checks()
    tests=[]
    for x in [F(1,2),F(1),F(2)]:
        for L in [1,2,3]:
            exact=numerator_jets(L,x)
            alternate=core_numerator([0,1,2]*2,L,F(1),x)
            require(exact==alternate,f'Jet/frontier mismatch {(L,x)}')
            tests.append({'x':str(x),'L':L,'exact_numerator':str(exact),'matches_frontier':True})
    negatives=[]
    for x in [F(1,2),F(1),F(2)]:
        f=1+x
        kappa=x/(x*x+x+1)
        for L in [50,100]:
            value=numerator_jets(L,x)
            norm=(f*kappa*L)**6*(f*f*x)**(6*L)
            require(value<0,f'Claimed negative percolation core failed {(x,L)}')
            negatives.append({'x':str(x),'L':L,'normalised_exact_numerator':str(value/S.Rational(norm))})
    return {'schema':'evidence-press-percolation-fan-v03',
            'word':[0,1,2,0,1,2],
            'normalisation':'((1+x)*x/(x*x+x+1)*L)^6 * ((1+x)^2*x)^(6*L)',
            'limit':'-1','symbolic_partition_checks':rows,
            'finite_jet_frontier_comparisons':tests,
            'negative_finite_cores':negatives,
            'scope':'Each fixed x>0; not a uniform-in-x convergence assertion. The one-block derivative remainder is bounded in the written proof.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificate',action='store_true')
    args=parser.parse_args()
    result=make_certificate()
    path=ROOT/'data'/'percolation_limit_v03.json'
    if args.write_certificate:
        path.write_text(json.dumps(result,indent=2)+'\n')
        print('AUTHORING: q=1 certificate written from exact reconstruction.')
    else:
        require(result==json.loads(path.read_text()),'Stored q=1 certificate differs')
        print(json.dumps({'check':'q=1 Jordan matrix identities, leading coefficient -1, 9 jet/frontier comparisons, 6 finite negative cores','status':'PASS'}))
if __name__=='__main__':
    main()
