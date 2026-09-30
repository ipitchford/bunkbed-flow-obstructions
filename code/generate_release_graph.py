#!/usr/bin/env python3
"""Stream a certified base graph or full bunkbed; default prints recipe only.

Examples:
  python code/generate_release_graph.py 3_2
  python code/generate_release_graph.py 9_10 --output base.edges
  python code/generate_release_graph.py 3_2 --full --output bunkbed.edges
The 21_10 full graph is deliberately not materialised during verification.
Labels of a full vertex (a, layer) are 2*a+layer. Edge files begin with n m.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Iterator
from bb_tools import fan_chain_edges
ROOT=Path(__file__).resolve().parents[1]

def recipe(name: str) -> dict:
    if name == '3_2':
        row=json.loads((ROOT/'data/explicit_q32_L19.json').read_text())['L19']
        word=[0,1,2]*4; k=row['min_pendants_per_post']; q='3/2'
    elif name == '9_10':
        row=json.loads((ROOT/'data/explicit_q09_L21.json').read_text())
        word=[0,1,2]*2; k=row['min_pendants_per_post']; q='9/10'
    elif name == '21_10':
        data=json.loads((ROOT/'v0_1/certificates/q_21_10_bound.json').read_text())
        row={**data,**data['amplification']};word=data['word'];k=row['k_per_post'];q='21/10'
    else:
        raise ValueError('Unknown certified construction')
    n,edges,u,v=fan_chain_edges(word,row['L']); t=len(set(word));N=n+t*k;M=len(edges)+t*k
    for key,val in [('base_vertices',N),('base_edges',M),('full_vertices',2*N),('full_edges',2*M+N)]:
        if row[key]!=val:raise ValueError('Stored graph recipe mismatch: '+key)
    return {'name':name,'q':q,'p':'1/2','word':word,'L':row['L'],'k':k,'posts':t,
            'core_vertices':n,'core_edges':len(edges),'base_vertices':N,'base_edges':M,
            'full_vertices':2*N,'full_edges':2*M+N,'base_u':u,'base_v':v,
            'full_source':2*u,'full_same_target':2*v,'full_cross_target':2*v+1,
            'full_vertex_convention':'(a,layer) -> 2*a+layer'}

def edges(rec:dict, full:bool=False) -> Iterator[tuple[int,int]]:
    n,core,_,_=fan_chain_edges(rec['word'],rec['L'])
    def base():
        yield from core
        for s in range(rec['posts']):
            for j in range(rec['k']):yield s,n+s*rec['k']+j
    if full:
        for a,b in base():
            yield 2*a,2*b
            yield 2*a+1,2*b+1
        for a in range(rec['base_vertices']):yield 2*a,2*a+1
    else:yield from base()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('construction',choices=['9_10','3_2','21_10'])
    ap.add_argument('--full',action='store_true')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();rec=recipe(args.construction)
    if args.output is None:
        print(json.dumps(rec,indent=2));return
    if args.output.exists():raise FileExistsError('Refusing to overwrite '+str(args.output))
    n=rec['full_vertices'] if args.full else rec['base_vertices']
    m=rec['full_edges'] if args.full else rec['base_edges']
    count=0
    with args.output.open('x',encoding='ascii') as out:
        out.write(f'{n} {m}\n')
        for a,b in edges(rec,args.full):out.write(f'{a} {b}\n');count+=1
    if count!=m:raise ValueError('Generated edge count differs from recipe')
    print(json.dumps({'status':'WRITTEN','path':str(args.output),'vertices':n,'edges':m}))
if __name__=='__main__':main()
