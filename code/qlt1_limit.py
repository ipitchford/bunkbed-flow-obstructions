"""The q<1 fan limit (new): for 0<q<1 the fan matrix ordering is
lambda_- < x < lambda_+, so the dominant second-compound mode of each fan
factor is (top plane eigenvector) wedge (complement).  This module computes
the resulting limit
   G_w(q,x) = lim_{L->inf} N^T_{w,L}(q,x) / (lambda_+ x)^{L m}
numerically (float) from the finite reduced representation, for any word.
"""
import numpy as np, itertools, math
from fractions import Fraction as Fr

def partitions(t):
    def rec(a,r):
        if len(a)==t: yield tuple(a); return
        for s in range(r+1): yield from rec(a+[s],max(r,s+1))
    yield from rec([0],1)

def compound2(A):
    n=A.shape[0]; idx=list(itertools.combinations(range(n),2)); N=len(idx)
    C=np.zeros((N,N))
    for I,(i,j) in enumerate(idx):
        for J,(k,l) in enumerate(idx):
            C[I,J]=A[i,k]*A[j,l]-A[i,l]*A[j,k]
    return C,idx

def contraction(X,idx,w,v):
    """C_w(X) = sum_a <w ^ e_a, X (v ^ e_a)> for X a matrix on wedge^2 in basis idx."""
    n=len(w); pos={p:I for I,p in enumerate(idx)}
    def wedge_vec(p,u):
        out=np.zeros(len(idx))
        for I,(i,j) in enumerate(idx): out[I]=p[i]*u[j]-p[j]*u[i]
        return out
    tot=0.0
    for a in range(n):
        ea=np.zeros(n); ea[a]=1
        tot+=wedge_vec(w,ea)@X@wedge_vec(v,ea)
    return tot

def fan_modes(q,x,r,s):
    """reduced representation of size r+1; returns (lam_plus, a_s, b_s, Pi_x, plane info)."""
    n=r+1; v=np.ones(n); w=np.ones(n); w[-1]=q-r
    J=np.outer(v,w); R=J+x*np.eye(n); D=np.eye(n); D[s,s]=1+x
    A=R@D
    # plane basis e_s, v : matrix [[fx, x^2],[f, q+2x]]
    f=1+x; B=np.array([[f*x, x*x],[f, q+2*x]])
    tau=B.trace(); d=np.linalg.det(B); disc=tau*tau-4*d
    lp=(tau+math.sqrt(disc))/2; lm=(tau-math.sqrt(disc))/2
    es=np.zeros(n); es[s]=1
    def right_vec(lam): # in basis (e_s, v): (x^2, lam - f x)
        return x*x*es+(lam-f*x)*v
    lplus=right_vec(lp); lminus=right_vec(lm)
    # left eigenvectors of A for lp: solve r^T A = lp r^T within the dual of the plane; use full-matrix left eigen solve
    # simpler: left eigenvector of A restricted: use scipy-free approach: eig of A.T
    vals,vecs=np.linalg.eig(A.T)
    k=np.argmin(abs(vals-lp)); rplus=np.real(vecs[:,k]); rplus=rplus/(rplus@lplus)
    a=D@lplus; b=rplus
    # projector onto W_s (eigenvalue x) along the plane: Pi = I - P_s, P_s = e_s e_s^T + (v-e_s)(w-e_s)^T/(q-1)
    Ps=np.outer(es,es)+np.outer(v-es,w-es)/(q-1); Pi=np.eye(n)-Ps
    return lp,lm,a,b,Pi,v,w

def G_limit(word,q,x):
    t=max(word)+1; m=len(word); total=0.0
    for pi in partitions(t):
        r=max(pi)+1; n=r+1
        modes={}
        for s in range(r): modes[s]=fan_modes(q,x,r,s)
        lp=modes[0][0]
        v=modes[0][5]; w=modes[0][6]
        # Lambda_s = C2(a b^T + Pi) - C2(Pi)
        Lam={}; idx=None
        for s in range(r):
            _,_,a,b,Pi,_,_=modes[s]
            C1,idx=compound2(np.outer(a,b)+Pi); C0,_=compound2(Pi); Lam[s]=C1-C0
        X=np.eye(len(idx))
        for c in word: X=X@Lam[pi[c]]
        term=contraction(X,idx,w,v)
        # rank-one chain for the omitted-colour term
        chain=np.eye(n)
        for c in word:
            _,_,a,b,_,_,_=modes[pi[c]]; chain=chain@np.outer(a,b)
        term+=(q-r-1)*(w@chain@v)
        falling=1.0
        for j in range(r): falling*=q-j
        total+=falling*term
    return q/(q-1)*total

if __name__=='__main__':
    import json,sys,time
    from bb_tools import core_numerator
    w2=[0,1,2]*2
    # compare with exact finite-L values normalised by (lambda_+ x)^{Lm}
    for q,x in [(Fr(9,10),Fr(1)),(Fr(9,10),Fr(1,3)),(Fr(1,2),Fr(1))]:
        G=G_limit(w2,float(q),float(x))
        f=1+float(x); tau=float(x)**2+3*float(x)+float(q); d=f*float(x)*(float(q)+float(x)); lp=(tau+math.sqrt(tau*tau-4*d))/2
        print("q=%s x=%s  G_limit=%.6g"%(q,x,G))
        for L in (12,24,36):
            N=core_numerator(w2,L,q,x); val=float(Fr(N)/(Fr(1)))  if False else None
            # normalise in floating point via logs
            sgn=1 if N>0 else -1; mag=abs(N)
            logN=(len(str(mag.numerator))-len(str(mag.denominator)))*math.log(10)+math.log(float(Fr(mag.numerator,10**(len(str(mag.numerator))-1)))/float(Fr(mag.denominator,10**(len(str(mag.denominator))-1))))
            ratio=sgn*math.exp(logN-L*len(w2)*math.log(lp*float(x)))
            print("   L=%2d  N^T/(lambda_+ x)^{Lm} = %.6g"%(L,ratio))
