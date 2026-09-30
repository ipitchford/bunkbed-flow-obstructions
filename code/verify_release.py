#!/usr/bin/env python3
"""Run the v0.3 exact verification pipeline, failing on any error.

Default reconstructs the C32 flow polynomial and both full-core cubics.
--quick checks stored large objects without reconstructing them; the receipt
explicitly records this limitation. All other steps are unchanged.
Receipts and raw output are written under runs/ (excluded from source manifest).
The manifest protects sources, certificates, graph data and manuscript. It is
an integrity check, not an external signature or a proof of correctness.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,platform,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def verify_manifest():
    manifest=ROOT/'SHA256SUMS'
    entries=manifest.read_text(encoding='utf-8').splitlines();seen=set()
    for line in entries:
        expected,rel=line.split('  ',1)
        p=(ROOT/rel).resolve()
        if not p.is_relative_to(ROOT) or rel in seen:raise ValueError('Invalid manifest path')
        seen.add(rel)
        if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise ValueError('Manifest mismatch: '+rel)
    if not entries:raise ValueError('Empty manifest')
    return {'status':'PASS','covered_files':len(seen),'sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--quick',action='store_true');args=ap.parse_args()
    start=time.monotonic();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    folder=ROOT/'runs'/('quick' if args.quick else 'full')/('opt'+str(sys.flags.optimize))
    folder.mkdir(parents=True,exist_ok=True)
    receipt={'status':'RUNNING','started_utc':stamp,'full_reconstruction':not args.quick,
             'python':platform.python_version(),'sympy':__import__('sympy').__version__,
             'python_optimisation':sys.flags.optimize,'steps':[],
             'formal_proof_assistant_verification':False,'external_peer_review':False,
             'full_parameter_classification_completed':False}
    flags=['-O'] if sys.flags.optimize==1 else (['-OO'] if sys.flags.optimize>=2 else [])
    stages=[('baseline','v0_1/code/run_all.py',[]),
            ('developed','code/certify_v02.py',[] if args.quick else ['--full']),
            ('below_one','code/verify_below_universal.py',[]),
            ('percolation','code/verify_percolation_limit.py',[]),
            ('structure','code/validate_release_inputs.py',[]),
            ('graphs','code/verify_graph_files.py',[]),
            ('interface','code/verify_interface.py',[]),
            ('current_paper','code/crosscheck_v03.py',[]),
            ('historical_paper','code/crosscheck_manuscript.py',[]),
            ('negative_tests','code/test_negative_cases.py',[])]
    try:
        receipt['manifest']=verify_manifest()
        for name,script,extra in stages:
            tick=time.monotonic();command=[sys.executable,*flags,str(ROOT/script),*extra]
            result=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
            log=folder/(name+'.log');log.write_text(result.stdout+'\nSTDERR:\n'+result.stderr)
            step={'name':name,'command':[Path(sys.executable).name,*flags,script,*extra],
                  'returncode':result.returncode,'seconds':round(time.monotonic()-tick,3),
                  'log':str(log.relative_to(ROOT)),
                  'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
            receipt['steps'].append(step)
            if result.returncode!=0:raise RuntimeError('Verification failed at '+name+'; see '+str(log))
            print(json.dumps({'step':name,'status':'PASS','seconds':step['seconds']}),flush=True)
        receipt['status']='PASS'
    except Exception as exc:
        receipt['status']='FAIL';receipt['error']=str(exc)
        raise
    finally:
        receipt['elapsed_seconds']=round(time.monotonic()-start,3)
        (folder/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'PASS','full_reconstruction':not args.quick,'receipt':str(folder/'receipt.json')}))
if __name__=='__main__':main()
