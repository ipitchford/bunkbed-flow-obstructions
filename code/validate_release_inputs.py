"""Fast structural, recipe and exact interval checks; not full reconstruction."""
import json
from pathlib import Path
from fractions import Fraction as F
import sympy as S
from bb_tools import fan_chain_edges,peval
ROOT=Path(__file__).resolve().parents[1]

def require(ok,msg):
    if not ok:raise ValueError(msg)

def graph_check(n,edges):
    require(n>0,'Empty graph')
    seen=set()
    adjacency=[[] for _ in range(n)]
    for a,b in edges:
        require(0<=a<n and 0<=b<n and a!=b,'Invalid vertex or loop')
        require(tuple(sorted((a,b))) not in seen,'Duplicate edge')
        seen.add(tuple(sorted((a,b))))
        adjacency[a].append(b);adjacency[b].append(a)
    reached={0};stack=[0]
    while stack:
        for b in adjacency[stack.pop()]:
            if b not in reached:reached.add(b);stack.append(b)
    require(len(reached)==n,'Disconnected graph')
    return [len(a) for a in adjacency]

def recipes():
    a=json.loads((ROOT/'data/explicit_q32_L19.json').read_text())['L19']
    b=json.loads((ROOT/'data/explicit_q09_L21.json').read_text())
    result=[]
    for q,word,row in [(F(3,2),[0,1,2]*4,a),(F(9,10),[0,1,2]*2,b)]:
        n,edges,u,v=fan_chain_edges(word,row['L']);e=len(edges);t=len(set(word));k=row['min_pendants_per_post']
        graph_check(n,edges)
        expected={'core_vertices':n,'core_edges':e,'base_vertices':n+t*k,'base_edges':e+t*k,'full_vertices':2*(n+t*k),'full_edges':2*(e+t*k)+n+t*k}
        for name,value in expected.items():require(row[name]==value,f'Recipe {q}: {name} mismatch')
        coeffs=[F(c) for c in row['N_y_coefficients']]
        require(len(coeffs)==t+1 and all(c>0 for c in coeffs[:-1]) and coeffs[-1]<0,'Wrong cubic signs')
        x=F(1);r=x**3/(q*q+3*q*x+3*x*x)
        y=lambda j:(1+x)*(1+r)**j-1
        require(peval(coeffs,y(k))<0<=peval(coeffs,y(k-1)),'Pendant threshold invalid')
        result.append({'q':str(q),'word':word,'L':row['L'],'k':k,**expected})
    return result

def main():
    rows=json.loads((ROOT/'data/witnesses_above2.json').read_text())+[json.loads((ROOT/'data/witness_C32.json').read_text())]
    q=S.symbols('q')
    for row in rows:
        degrees=graph_check(row['n'],row['edges'])
        require(all(d%2==0 for d in degrees),'Flow witness not Eulerian')
        require(len(row['edges'])==row['m'],'Incorrect edge count')
        P=row['P_coefficients_ascending'];flow=row['flow_coefficients_ascending']
        require([int(c) for c in S.Poly((q-1)*sum(c*q**i for i,c in enumerate(P)),q).all_coeffs()[::-1]]==flow,'Flow quotient mismatch')
        a,b=map(F,row['certified_negative']);poly=S.Poly(sum(c*q**i for i,c in enumerate(P)),q)
        require(a<b and peval(P,a)<0 and peval(P,b)<0 and poly.count_roots(S.Rational(a),S.Rational(b))==0,'Invalid exact negative interval')
    print(json.dumps({'check':'connected simple Eulerian witnesses, exact interval checks, finite graph recipe arithmetic and pendant thresholds','status':'PASS','recipes':recipes()}))
if __name__=='__main__':main()
