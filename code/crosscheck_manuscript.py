"""Historical v0.2 presentation check of 32 selected assertions, not all numbers.
Exits nonzero on any mismatch. Not a mathematical proof checker."""
import re,json,os
from fractions import Fraction as Fr
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
md=open(os.path.join(ROOT,'paper','manuscript_v0_2.md')).read()
data=lambda f: json.load(open(os.path.join(ROOT,'data',f)))
problems=[]
def chk(cond,msg):
    print(('OK   ' if cond else 'FAIL ')+msg)
    if not cond: problems.append(msg)
# Table 1: circulant witnesses
tab=data('witnesses_above2.json')+[data('witness_C32.json')]
byname={r['name']:r for r in tab}
rows=re.findall(r'\| \$C_\{(\d+)\}\((\d),(\d)\)\$ \| (\d+) \| (\d+) \| ([\d.]+), ([\d.]+) \| \$\[([\d.]+),\\ ([\d.]+)\]\$ \|',md)
chk(len(rows)==11,"Table 1 has 11 circulant rows (found %d)"%len(rows))
for n,a,b,nn,mm,r1,r2,c1,c2 in rows:
    name='C%s(%s,%s)'%(n,a,b); r=byname[name]
    ok=int(nn)==r['n'] and int(mm)==r['m'] and abs(float(r1)-r['roots_float'][0])<6e-8 and abs(float(r2)-r['roots_float'][1])<6e-8
    ca,cb=Fr(r['certified_negative'][0]),Fr(r['certified_negative'][1])
    ok&= abs(float(c1)-float(ca))<1e-7 and abs(float(c2)-float(cb))<1e-7 and Fr(c1)>=ca and Fr(c2)<=cb
    chk(ok,"Table 1 row %s matches data (roots %s %s, certificate [%s,%s])"%(name,r['roots_float'][0],r['roots_float'][1],ca,cb))
# K4b intervals sentence
k=[byname['K4,6'],byname['K4,8'],byname['K4,12'],byname['K4,16']]
for row,(lo,hi) in zip(k,[(2.01252,2.35620),(2.00124,2.45834),(2.0000151,2.52162),(2.0000002,2.53945)]):
    chk(abs(row['roots_float'][0]-lo)<6e-6 and abs(row['roots_float'][1]-hi)<6e-6,"K4b interval %s quoted (%s,%s) vs data %s"%(row['name'],lo,hi,row['roots_float']))
# Gamma_* roots and F'(2)
g=data('flow_witness_audit.json')
chk(abs(g['real_roots_float'][0]-2.0231663356188748)<1e-12 and abs(g['real_roots_float'][1]-2.2730755356098221)<1e-12,"Gamma_* roots quoted match data %s"%g['real_roots_float'])
chk(g['F_prime_at_2']=='-47',"F'(2)=-47")
# q_c
ex=json.load(open(os.path.join(ROOT,'checks','executed_checks_v02.json')))
qc=[c for c in ex['checks'] if c['check'].startswith('K_{4,b}')][0]['q_c_float']
chk(abs(qc-2.574743073887)<2e-12,"q_c quoted 2.574743073887 vs computed %.15f"%qc)
# Table 2 thresholds
m2=data('qlt1_exact_map.json')
for name,key in (('2','2C3'),('6','6C3'),('10','10C3')):
    row=re.search(r'\| \$q_0\^\{\(%s\)\}\(x\)\$ \| (.*?) \|\n'%name,md).group(1).split(' | ')
    vals=[float(v) for v in row]
    xs=['1/100','1/10','1/4','1/2','1','2','4','10','100','1000']
    ok=True
    for v,x in zip(vals,xs):
        br=m2[key]['boundary_brackets'][x]; hi=float(Fr(br[1])); lo=float(Fr(br[0]))
        ok&= abs(v-hi)<6e-5
    chk(ok,"Table 2 row ell=%s matches exact bisection upper brackets"%name)
# explicit q=3/2
e=data('explicit_q32_L19.json')['L19']
chk(e['min_pendants_per_post']==3565 and e['full_vertices']==21854 and e['full_edges']==33253 and e['base_vertices']==10927 and e['base_edges']==11163 and e['core_vertices']==232 and e['core_edges']==468,"explicit q=3/2 sizes")
e20=data('explicit_q32_L20.json')['L20']; chk(e20['min_pendants_per_post']==3740,"L=20 exact minimum k=3740")
e9=data('explicit_q09_L21.json'); chk(e9['min_pendants_per_post']==1099 and e9['full_vertices']==6854 and e9['full_edges']==10537 and e9['core_vertices']==130,"explicit q=9/10 sizes")
# smallest cores scan
sc=data('scan_q32_cores.json'); neg={(r['ell'],r['L']) for r in sc if r['sign']<0}; pos={(r['ell'],r['L']) for r in sc if r['sign']>0}
chk((4,19) in neg and (4,18) in pos and (6,16) in neg and (6,15) in pos and (8,15) in neg and (8,14) in pos,"smallest negative cores (4,19),(6,16),(8,15)")
# fan bound test count
fb=data('fanbound_test.json'); chk(len(fb)==86 and all(r['holds'] for r in fb),"86 error-bound instances, none violated")
# convergence numbers at q=21/10
wc=data('word_core_audit.json'); conv=[c for c in wc['convergence'] if c['q']=='21/10'][0]
quoted=[59.81,56.81,53.07,50.21,49.62,49.50]
chk(all(abs(r['ratio']-v)<6e-3 for r,v in zip(conv['rows'],quoted)) and abs(conv['limit']-49.458)<1e-3,"convergence sequence at q=21/10 quoted correctly")
conv2=[c for c in wc['convergence'] if c['q']=='3/2'][0]
# q<1 normalised values quoted 1616.5,1834.5,1852.0 and limit 1853.64 : from log
log=open(os.path.join(ROOT,'logs','qlt1_limit_check.log')).read()
chk('1616.54' in log and '1834.51' in log and '1852.04' in log and '1853.64' in log,"q<1 convergence values quoted from log")
# finite certificates
fc=[c for c in ex['checks'] if c['check'].startswith('q<1 finite')][0]['points']
want={('19/20','1/2',18),('9/10','1/2',21),('17/20','1/2',21),('4/5','1/2',27),('9/10','1/4',33),('9/10','3/4',24),('4/5','3/4',30)}
chk({(p['q'],p['p'],p['L']) for p in fc}==want and all(p['negative'] for p in fc),"seven finite q<1 certificates")
# C_n(1,5) upper endpoints sequence
seq=[2.6187,2.6822,2.7079,2.7156,2.7451,2.7508,2.7641]
f4=data('families4_30_32_36_40.json'); f2=data('families2.json'); 
got={20:2.61865,28:2.7451}; 
src={r['family']:r for r in f2}
c=[src['C20(1,5)']['roots_above_2'][1]]
fl=open(os.path.join(ROOT,'logs','families3.log')).read()
for n in (22,24,26,28):
    c.append(float(re.search(r'C%d\(1,5\)\s+n=%d m=\s*\d+\s+neg>2: \[\(2\.\d+, ([\d.]+)\)\]'%(n,n),fl).group(1)))
c.append(f4[0]['neg_float'][0][1]); c.append(f4[1]['neg_float'][0][1])
chk(all(abs(a-b)<6e-5 for a,b in zip(seq,c)),"C_n(1,5) upper endpoint sequence %s vs data %s"%(seq,[round(v,4) for v in c]))
# random search claims
fa=data('flowsearch_A.json'); fb_=data('flowsearch_B.json')
chk(len(fa)==0 and all(r['t']==10 for r in fb_) and all(2.04<=r['grid_neg_lo'] and r['grid_neg_hi']<=2.145 for r in fb_ if 'grid_neg_lo' in r) and all(r.get('q0')==2.05 for r in fb_ if r.get('best')),"random search: negatives only for t=10 inside (2.04,2.145); none for t<=8")
print("\nPROBLEMS:",problems if problems else "none")

if problems:
    raise SystemExit(1)
