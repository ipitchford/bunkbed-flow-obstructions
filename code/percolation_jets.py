"""Exact q=1 numerator from first-order polynomial jets in q-1.
This implementation does not use connectivity-state dynamic programming.
"""
import sys,json,time
from fractions import Fraction as F
import sympy as S
from bb_tools import core_numerator

def mul(A,B):return (A[0]*B[0],A[0]*B[1]+A[1]*B[0])
def mpow(A,k):
 B=(S.eye(A[0].rows),S.zeros(A[0].rows))
 while k:
  if k&1:B=mul(B,A)
  A=mul(A,A);k//=2
 return B

def exact(L,x):
 x=S.Rational(x);total=0;constant=0
 for pi in [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(0,1,2)]:
  r=max(pi)+1;n=r+1;v=S.ones(n,1);w=S.Matrix([1]*r+[1-r]);dw=S.Matrix([0]*r+[1]);R=v*w.T+x*S.eye(n);dR=v*dw.T;M={}
  for s in set(pi):
   D=S.eye(n);D[s,s]+=x;A=mpow((R*D,dR*D),L);M[s]=(D*A[0],D*A[1])
  K=(S.eye(n),S.zeros(n))
  for s in pi*2:K=mul(K,M[s])
  K2=mul(K,K);z=(w.T*K[0]*v)[0];dz=(dw.T*K[0]*v+w.T*K[1]*v)[0];tr=S.trace(K[0])+(1-r-1)*x**(6*L);dtr=S.trace(K[1])+x**(6*L)
  term=z*tr-(w.T*K2[0]*v)[0];dterm=dz*tr+z*dtr-(dw.T*K2[0]*v+w.T*K2[1]*v)[0]
  a=1 if r==1 else 0;b=1 if r in [1,2] else -1
  constant+=a*term;total+=b*term+a*dterm
 if constant!=0:raise ValueError('constant must vanish')
 return total
