"""Exhaustive finite checks of the attachment-interface component identity."""
import itertools,json

def partitions(n):
    def rec(seq):
        if len(seq)==n:yield tuple(seq);return
        for a in range(max(seq)+2):yield from rec(seq+[a])
    yield from rec([0])

def components(n,edges):
    par=list(range(n))
    def find(a):
        while a!=par[a]:a=par[a]
        return a
    for a,b in edges:par[find(a)]=find(b)
    return len({find(a) for a in range(n)})

def star_realisation(p,b,offset):
    return [(i,offset+p[i]) for i in range(b)]

rows=[]
for b in range(1,7):
    pp=list(partitions(b));count=0
    for p,r in itertools.product(pp,repeat=2):
        np,nr=max(p)+1,max(r)+1
        incidence=[(p[i],np+r[i]) for i in range(b)]
        join=components(np+nr,incidence)
        ell=b-np-nr+join
        if not 0<=ell<=b-1:raise ValueError('Interface cycle-rank bound')
        # Independently realise each block as a star on new internal vertices.
        # Their union is an explicit graph, with exactly the b boundary vertices shared.
        edges=star_realisation(p,b,b)+star_realisation(r,b,b+np)
        union_components=components(b+np+nr,edges)
        if union_components!=np+nr-b+ell:raise ValueError('Component-count gluing formula')
        count+=1
    rows.append({'interface_vertices':b,'partition_pairs':count})
print(json.dumps({'status':'PASS','checks':rows,'total_pairs':sum(r['partition_pairs'] for r in rows),
                  'scope':'Finite component identity checks; density bound is proved in the paper.'}))
