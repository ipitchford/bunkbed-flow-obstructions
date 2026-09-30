"""Check specified current LaTeX formulas/tables against exact certificate data.

This is a structured consistency check, not verification of every sentence or proof.
It parses the printed eleven coefficient formulas as polynomial expressions.
"""
import json,re
from pathlib import Path
from fractions import Fraction as F
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
from generate_release_graph import recipe
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/'paper/manuscript_v0_3.tex').read_text()
cert=json.loads((ROOT/'data/below_universal_v03.json').read_text())
q,g=S.symbols('q g')
checks=[]
def require(ok,name):
    if not ok:raise ValueError('Current manuscript inconsistency: '+name)
    checks.append(name)

block=text.split(r'\section{The below-one polynomial and positivity certificates}',1)[1]
block=block.split(r'\begin{align*}',1)[1].split(r'\end{align*}',1)[0]
trans=standard_transformations+(implicit_multiplication_application,convert_xor)
gpoly=q**5-7*q**4+19*q**3-28*q**2+26*q-10
matches=re.findall(r'c_(?:\{(\d+)\}|(\d+))=\{\}&([^\n]+)',block)
require(len(matches)==11,'eleven printed coefficients')
for braced,plain,rhs in matches:
    k=int(braced or plain)
    rhs=rhs.replace('\\','').strip().rstrip(',.')
    expr=parse_expr(rhs,local_dict={'q':q,'g':g},transformations=trans).subs(g,gpoly)
    expected=sum(S.Integer(c)*q**j for j,c in enumerate(cert['P_coefficients_h_ascending_q_ascending'][k]))
    require(S.expand(expr-expected)==0,'printed coefficient c_'+str(k))

for key,label in [('core_vertices','Core base vertices'),('core_edges','Core base edges'),('k','Pendants per post'),
                  ('base_vertices','Final base vertices'),('base_edges','Final base edges'),
                  ('full_vertices','Full bunkbed vertices'),('full_edges','Full bunkbed edges')]:
    row=label+'&'+'&'.join(str(recipe(n)[key]) for n in ['9_10','3_2','21_10'])+r'\\'
    require(row in text,'graph table: '+label)

rows=json.loads((ROOT/'data/witnesses_above2.json').read_text())+[json.loads((ROOT/'data/witness_C32.json').read_text())]
for name in ['C10(1,4)','C16(2,3)','C24(3,4)','C28(1,5)','C32(1,5)']:
    row=next(r for r in rows if r['name']==name)
    n=int(name.split('(')[0][1:]);tail=name.split('(')[1]
    match=re.search(r'\$C_\{'+str(n)+r'\}\('+re.escape(tail)+r'\$\s*&\s*(\d+)\s*&\s*(\d+)\s*&\$\[([0-9.]+),\s*\\?\s*([0-9.]+)\]\$',text)
    require(match is not None,'circulant table row '+name)
    nn,mm,aa,bb=match.groups()
    require(int(nn)==row['n'] and int(mm)==row['m'] and [F(aa),F(bb)]==list(map(F,row['certified_negative'])),
            'circulant table data '+name)

require(r'\mathcal U_p\cap[\alpha,691/250]=\{2\}' in text,'main exact window')
require(r'\frac{787422865474633}{10^{15}}<\alpha<' in text and r'\frac{787422865474634}{10^{15}}' in text,'root bracket')
require(r'\frac{\N^T_{w,L}(1,x)}{(f\kappa L)^6(f^2x)^{6L}}=-1' in text,'q=1 limit and normalisation')
require(r'\frac{q^2(h+q)^2(q-2)}{s^6(q-1)^6}\,P(q,h)' in text,'below-one prefactor')

for j in range(2,11):
    betas=list(map(S.Rational,cert['bernstein_h2_to_h10'][str(j)]))
    lower=S.Rational(S.floor(min(betas)*1000),1000)
    literal=f'{j}&{len(betas)-1}&${S.latex(lower)}$'+r'\\'
    require(literal in text,'Bernstein lower-bound table row '+str(j))
print(json.dumps({'status':'PASS','checks':checks,'count':len(checks),
                  'scope':'Eleven printed polynomials, three tables, selected exact definitions/normalisations. Not every prose assertion.'}))
