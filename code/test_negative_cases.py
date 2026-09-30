"""Deliberately corrupt temporary copies. Every invalid case must exit nonzero."""
import json,os,sys,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run():
    results=[]
    with tempfile.TemporaryDirectory(prefix='bunkbed-negative-') as td:
        work=Path(td)/'candidate'
        shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('history','__pycache__','runs','*.pdf'))
        def case(name,script,mutate=None,restore=None,optimise=False,extra_env=None):
            if mutate:mutate()
            try:
                env=os.environ.copy();env.update(extra_env or {})
                flags=['-O'] if optimise else []
                command=[sys.executable,*flags,str(work/script)]
                p=subprocess.run(command,cwd=work,env=env,text=True,capture_output=True,timeout=180)
                # Failures must not end by falsely certifying the affected script.
                if p.returncode==0:
                    raise RuntimeError('Invalid case was accepted: '+name+'\n'+p.stdout)
                results.append({'case':name,'returncode':p.returncode,'rejected':True,
                                'diagnostic_tail':p.stderr.splitlines()[-1] if p.stderr else p.stdout.splitlines()[-1]})
            finally:
                if restore:restore()
        def json_mutation(path,fn):
            file=work/path;old=file.read_text()
            def modify():
                obj=json.loads(old);fn(obj);file.write_text(json.dumps(obj))
            return modify,lambda:file.write_text(old)
        for opt in (False,True):
            m,r=json_mutation(Path('v0_1/certificates/flow_witness.json'),lambda d:d['flow_coefficients'].__setitem__(0,d['flow_coefficients'][0]+1))
            case('wrong flow constant coefficient'+(' under -O' if opt else ''),Path('v0_1/code/verify_flow.py'),m,r,opt)
        m,r=json_mutation(Path('data/explicit_q32_L19.json'),lambda d:d['L19'].__setitem__('full_vertices',21855))
        case('wrong full-graph recipe count',Path('code/validate_release_inputs.py'),m,r,True)
        m,r=json_mutation(Path('data/witness_C32.json'),lambda d:d['edges'].__setitem__(0,[0,0]))
        case('loop in Eulerian witness',Path('code/validate_release_inputs.py'),m,r,True)
        m,r=json_mutation(Path('data/below_universal_v03.json'),lambda d:d['P_coefficients_h_ascending_q_ascending'][0].__setitem__(0,1))
        case('wrong doubled-triangle coefficient under -O',Path('code/verify_below_universal.py'),m,r,True)
        m,r=json_mutation(Path('data/percolation_limit_v03.json'),lambda d:d.__setitem__('limit','1'))
        case('wrong q=1 limit sign under -O',Path('code/verify_percolation_limit.py'),m,r,True)
        file=work/'data/witness_C32.json';old=file.read_text()
        case('missing C32 certificate',Path('code/validate_release_inputs.py'),lambda:file.unlink(),lambda:file.write_text(old),True)
        case('compiler cannot be invoked',Path('v0_1/code/verify_flow.py'),optimise=True,extra_env={'CXX':'/nonexistent/bunkbed-cxx'})
        # Historical presentation checker must fail even though its comparisons are not proofs.
        file=work/'paper/manuscript_v0_2.md';old=file.read_text()
        case('altered historical manuscript table',Path('code/crosscheck_manuscript.py'),lambda:file.write_text(old.replace('$C_{10}(1,4)$','$C_{10}(1,9)$')),lambda:file.write_text(old),True)
        file=work/'paper/manuscript_v0_3.tex';old=file.read_text()
        case('altered current printed coefficient',Path('code/crosscheck_v03.py'),lambda:file.write_text(old.replace('-657q^4','-656q^4')),lambda:file.write_text(old),True)
    return {'status':'PASS','negative_tests':results,'count':len(results),
            'scope':'Corruptions occur only in temporary copies; no check relies on Python assert.'}
if __name__=='__main__':print(json.dumps(run(),indent=2))
