"""Validate shipped current edge lists and generators, without large materialisation."""
import hashlib,json
from pathlib import Path
from generate_release_graph import recipe,edges
from validate_release_inputs import graph_check
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for name in ['9_10','3_2']:
    rec=recipe(name);p=ROOT/'graphs'/f'q_{name}_base_v03.edges'
    with p.open() as src:
        n,m=map(int,src.readline().split())
        actual=[tuple(map(int,line.split())) for line in src]
    if (n,m)!=(rec['base_vertices'],rec['base_edges']) or len(actual)!=m or actual!=list(edges(rec)):
        raise ValueError('Edge list differs from recipe '+name)
    graph_check(n,actual)
    full=list(edges(rec,True));graph_check(rec['full_vertices'],full)
    if len(full)!=rec['full_edges']:raise ValueError('Full generator edge count')
    if rec['full_source']==rec['full_same_target']:raise ValueError('Identical endpoints')
    rows.append({'name':name,'base_vertices':n,'base_edges':m,
                 'full_vertices':rec['full_vertices'],'full_edges':len(full),
                 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
large=recipe('21_10')
print(json.dumps({'status':'PASS','small_graphs':rows,'large_recipe_checked':large,
                  'large_graph_materialised':False}))
