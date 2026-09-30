"""Run the complete exact-arithmetic certificate suite; exit nonzero on failure."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json,subprocess,sys,time,platform,hashlib
from pathlib import Path
from fractions import Fraction as F
sys.set_int_max_str_digits(1000000)
ROOT=Path(__file__).resolve().parents[1]

def comparable(obj):
    if isinstance(obj,dict):return {k:comparable(v) for k,v in obj.items() if k!='elapsed_seconds'}
    if isinstance(obj,list):return [comparable(x) for x in obj]
    return obj

def edge_probability(n,edges,target,q,x):
    numerator=denominator=F(0)
    for mask in range(1<<len(edges)):
        par=list(range(n))
        def find(a):
            while par[a]!=a:a=par[a]
            return a
        for i,(a,b) in enumerate(edges):
            if mask>>i&1:par[find(a)]=find(b)
        w=q**len({find(a) for a in range(n)})*x**mask.bit_count()
        denominator+=w
        if mask>>target&1:numerator+=w
    return numerator/denominator

def main():
    start=time.time();steps=[]
    for script,stored in [('verify_words.py','word_verification.json'),
                          ('verify_flow.py','flow_verification.json'),
                          ('verify_core.py','q_3_2_core.json'),
                          ('verify_asymptotic.py','q_21_10_bound.json')]:
        tick=time.time()
        flags = ['-O'] if sys.flags.optimize == 1 else (['-OO'] if sys.flags.optimize >= 2 else [])
        raw=subprocess.check_output([sys.executable,*flags,str(ROOT/'code'/script)],text=True)
        got=json.loads(raw);expected=json.load(open(ROOT/'certificates'/stored))
        _require_v03((comparable(got)==comparable(expected)), (script,'stored receipt mismatch'))
        _require_v03((got['status']=='PASS'), 'Validation failed in run_all.py: 37')
        steps.append({'check':script,'status':'PASS','seconds':time.time()-tick})
    # Independent direct-enumeration audit of ALR Lemma A.1 as printed.
    p0=edge_probability(3,[(0,1)],0,F(2),F(1))
    p1=edge_probability(3,[(0,1),(0,2),(1,2)],0,F(2),F(1))
    _require_v03((p0==F(1,3) and p1==F(5,14) and p0!=p1), 'Validation failed in run_all.py: 42')
    steps.append({'check':'ALR_A1_literal_counterexample','status':'PASS',
                  'common_edges':0,'single_edge_probability':str(p0),'triangle_marginal_probability':str(p1)})
    # The shipped edge list is exactly the certified recipe, with no duplicate edges.
    from generate_graph import graph
    rec=json.load(open(ROOT/'certificates/q_3_2_core.json'))
    n,m,u,v,stream=graph(rec)
    file=ROOT/'graphs/q_3_2_base.edges'
    with file.open() as f:
        header = tuple(map(int, f.readline().split()))
        _require_v03(header == (n,m), 'Edge-list header differs from graph recipe')
        edges=[tuple(map(int,line.split())) for line in f]
    _require_v03((edges==list(stream()) and len(edges)==m and len(set(tuple(sorted(e)) for e in edges))==m), 'Validation failed in run_all.py: 53')
    par=list(range(n))
    def find(a):
        while par[a]!=a:par[a]=par[par[a]];a=par[a]
        return a
    for a,b in edges:
        _require_v03((0<=a<n and 0<=b<n and a!=b), 'Validation failed in run_all.py: 59')
        par[find(a)]=find(b)
    _require_v03((len({find(a) for a in range(n)})==1 and u!=v), 'Validation failed in run_all.py: 61')
    steps.append({'check':'shipped_small_graph_matches_recipe_and_is_connected_simple',
                  'status':'PASS','vertices':n,'edges':m,
                  'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
    out={'status':'PASS','all_exact_checks_passed':True,'full_parameter_classification_completed':False,
         'external_peer_review_completed':False,'formal_proof_assistant_verification':False,
         'proof_depends_on_floating_point':False,'python':sys.version.split()[0],
         'platform':platform.platform(),'checks':steps,'elapsed_seconds':time.time()-start}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
