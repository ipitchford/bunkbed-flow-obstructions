"""General implementation of the v0.1 Appendix A rational error bound for the
uniform fan limit (any word), plus a numerical test of the bound against exact
small-L values computed by the independent DP."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

from fractions import Fraction as Fr
from bb_tools import *

def stirling2_row(n):
    a=[0]*(n+1); a[0]=1
    for i in range(n):
        b=[0]*(n+1)
        for r in range(1,i+2): b[r]=a[r-1]+r*a[r]
        a=b
    return a

def sqrt_lower(v, iters=60):
    """rational g with g <= sqrt(v) (v>0), close."""
    v=Fr(v); lo=Fr(0); hi=v if v>=1 else Fr(1)
    for _ in range(iters):
        mid=(lo+hi)/2
        if mid*mid<=v: lo=mid
        else: hi=mid
    return lo

def fan_constants(word,q,x):
    q,x=Fr(q),Fr(x); f=1+x; t=max(word)+1; m=len(word)
    tau=f*(1+x)+q-1+x; d=f*x*(q+x)
    _require_v03((q>1 and x>0), 'Validation failed in fanbound.py: 27')
    disc=tau*tau-4*d; _require_v03((disc>0), 'Validation failed in fanbound.py: 28')
    g=sqrt_lower(disc)*Fr(999,1000)
    # rho: choose y=x/rho just below lambda_-: need y<tau/2 and y^2-tau*y+d>0 (then y<lambda_-)
    lam_minus_lower=(tau-sqrt_lower(disc)*Fr(1001,1000))/2   # slightly below lambda_-? careful: larger sqrt => smaller value => valid lower bound
    # certify y := lam_minus_lower satisfies y<tau/2 and y^2-tau*y+d>0
    y=lam_minus_lower; _require_v03((y<tau/2 and y*y-tau*y+d>0 and y>x), "need x<lambda_-")
    rho=x/y*Fr(1001,1000); _require_v03((rho<1), 'Validation failed in fanbound.py: 34')
    S=max(q,2*t-q); P0=max(Fr(1),(2*t-q-1)/(q-1)); W0=1+P0
    C=P0*(2*f*(S+x)+tau)/g; C0=(q-1)*(2*C*W0+W0*W0/f)
    A0=(q-1)*P0+1; H0=(q-1)*(C+W0/f); U=q+t+1
    St=stirling2_row(t); Bt=Fr(0); falling=Fr(1)
    for r in range(1,t+1):
        falling*=q-r+1; Bt+=St[r]*abs(falling)
    return dict(q=q,x=x,f=f,t=t,m=m,tau=tau,d=d,g=g,rho=rho,S=S,P0=P0,W0=W0,C=C,C0=C0,A0=A0,H0=H0,U=U,Bt=Bt)

def error_bound(c,L):
    eps=c['C0']*c['rho']**L
    if eps>1: return None
    m,t=c['m'],c['t']
    return c['q']/(c['q']-1)*c['Bt']*(t*c['S']*m*c['A0']**(m-1)*eps+c['U']*c['S']*c['H0']**m*c['rho']**(L*m))

def limit(word,q):
    t=max(word)+1; return Fr(q)**(t+2)*peval(flow_poly_from_word(word),Fr(q))/(Fr(q)-1)

def aL(c,L): return c['f']*c['d']**L/(c['q']-1)

if __name__=='__main__':
    import json,time
    out=[]
    for wd,q,x,Ls in [([0,1,2]*2,Fr(3,2),Fr(1),range(1,25)),([0,1,2]*2,Fr(21,10),Fr(1),range(1,21)),([0,1],Fr(5,2),Fr(1,2),range(1,31)),([0,1,0,2],Fr(3),Fr(2),range(1,13))]:
        c=fan_constants(wd,q,x); lim=limit(wd,q)
        for L in Ls:
            E=error_bound(c,L)
            N=core_numerator(wd,L,q,x); err=abs(N/aL(c,L)**c['m']-lim)
            ok=(E is None) or (err<=E)
            out.append({'word':wd,'q':str(q),'x':str(x),'L':L,'actual_error':float(err),'bound':None if E is None else float(E),'holds':ok})
            print("word %s q=%s x=%s L=%2d  |error|=%.3e  bound=%s  holds=%s"%(wd,q,x,L,float(err),'eps>1' if E is None else '%.3e'%float(E),ok),flush=True)
            _require_v03((ok), 'Validation failed in fanbound.py: 65')
    json.dump(out,open('/home/claude/bunkbed/v02/data/fanbound_test.json','w'),indent=1)
