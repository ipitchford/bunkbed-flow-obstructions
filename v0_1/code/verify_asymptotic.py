"""Rational, finite certificate for the q=21/10 homogeneous construction.
Implements the explicitly proved norm bound, not numerical eigenvalue estimates.
"""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

from fractions import Fraction as F
from math import comb
import json,sys,time
from pathlib import Path
from verify_core import amplify
sys.set_int_max_str_digits(1000000)

def stirling(n):
    a=[0]*(n+1);a[0]=1
    for i in range(n):
        b=[0]*(n+1)
        for r in range(1,i+2):b[r]=a[r-1]+r*a[r]
        a=b
    return a

def horner(coefs,q):
    a=F(0)
    for c in reversed(coefs):a=a*q+c
    return a

def certificate(witness,L=1000):
    q=F(21,10);x=F(1);f=1+x;t=witness['n'];m=len(witness['edges'])
    _require_v03((t==12 and m==24), 'Validation failed in verify_asymptotic.py: 26')
    Fq=horner(witness['flow_coefficients'],q)
    _require_v03((Fq==F(-20868388946779,10**13)), 'Validation failed in verify_asymptotic.py: 28')
    tau=f*(1+x)+q-1+x;d=f*x*(q+x)
    g=F(3);rho=F(4,5);y=x/rho
    _require_v03((tau*tau-4*d>g*g and 0<rho<1), 'Validation failed in verify_asymptotic.py: 31')
    _require_v03((y<tau/2 and y*y-tau*y+d>0), 'Validation failed in verify_asymptotic.py: 32')
    # Thus y<lambda_minus, and x/lambda_minus<rho.
    S=max(q,2*t-q)
    P=max(F(1),(2*t-q-1)/(q-1));W=1+P;R0=S+x
    C=P*(2*f*R0+tau)/g
    C0=(q-1)*(2*C*W+W*W/f)
    epsilon=C0*rho**L
    A=(q-1)*P+1;H0=(q-1)*(C+W/f);U=q+t+1
    B=F(0);falling=F(1)
    for r,St in enumerate(stirling(t)):
        if r:falling*=q-r+1
        B+=St*abs(falling)
    error=q/(q-1)*B*(t*S*m*A**(m-1)*epsilon+U*S*H0**m*rho**(L*m))
    limit=q**(t+2)*Fq/(q-1)
    _require_v03((epsilon<1 and limit<0 and error<(-limit)/2), 'Validation failed in verify_asymptotic.py: 46')
    _require_v03((error<F(1,10**36)), 'Validation failed in verify_asymptotic.py: 47')  # Optional convenient human-readable bound.
    _require_v03((-limit>60000), 'Validation failed in verify_asymptotic.py: 48')
    a=f*d**L/(q-1);delta=(-limit)/2*a**m
    n=t+m*L+1;e=m*(2*L+1)
    amp=amplify(q,x,n,e,t,delta)
    return {'status':'PASS','q':str(q),'p':'1/2','x':str(x),'L':L,
            'word':witness['word'],'tau':str(tau),'d':str(d),
            'gap_lower_bound':str(g),'rho':str(rho),
            'limit':str(limit),'error_less_than':'1/10^36',
            'minus_limit_greater_than':60000,
            'epsilon_less_than_one':True,'error_less_than_minus_half_limit':True,
            'normalization_a':'(20/11)*(31/5)^1000',
            'delta_lower_bound_formula':'(-limit/2)*a^24',
            'core_vertices':n,'core_edges':e,'amplification':amp,
            'bound_constants':{k:str(v) for k,v in {
                'S':S,'P':P,'W':W,'C':C,'C0':C0,'A':A,'H0':H0,'U':U,'B_t':B}.items()}}

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    w=json.load(open(root/'certificates/flow_witness.json'))
    print(json.dumps(certificate(w),indent=2))
