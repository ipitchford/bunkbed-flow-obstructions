"""Stream either certified base graph, or its full bunkbed, as an edge list.
The q=21/10 graph is large. It is supplied as a compact, exact recipe by default.
"""
import argparse,json
from pathlib import Path
from verify_core import core_edges

def graph(recipe):
    word=recipe['word'];L=recipe['L'];k=recipe['amplification']['k_per_post']
    n,E,T,u,v=core_edges(word,L);new_n=n+len(T)*k;new_m=len(E)+len(T)*k
    def stream():
        yield from E
        for a in T:
            for j in range(k):yield a,n+a*k+j
    return new_n,new_m,u,v,stream

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('case',choices=['3_2','21_10'])
    ap.add_argument('--output',type=Path,help='Write the base edge list; without this, print the recipe summary only.')
    ap.add_argument('--full',action='store_true',help='Write the full bunkbed instead of the base graph.')
    args=ap.parse_args();root=Path(__file__).resolve().parents[1]
    fn='q_3_2_core.json' if args.case=='3_2' else 'q_21_10_bound.json'
    recipe=json.load(open(root/'certificates'/fn));n,m,u,v,stream=graph(recipe)
    print(json.dumps({'q':recipe['q'],'p':'1/2','base_vertices':n,'base_edges':m,
                      'base_u':u,'base_v':v,'full_source':2*u,'full_same_target':2*v,
                      'full_cross_target':2*v+1,'vertex_convention':'full copy (a,layer) has label 2*a+layer'},indent=2))
    if args.output:
        with args.output.open('w') as f:
            if not args.full:
                f.write(f'{n} {m}\n')
                for a,b in stream():f.write(f'{a} {b}\n')
            else:
                f.write(f'{2*n} {2*m+n}\n')
                for a,b in stream():
                    f.write(f'{2*a} {2*b}\n{2*a+1} {2*b+1}\n')
                for a in range(n):f.write(f'{2*a} {2*a+1}\n')
