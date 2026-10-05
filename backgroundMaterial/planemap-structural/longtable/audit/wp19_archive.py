"""Losslessly archive released WP19 results, verifying replay bindings first."""
import argparse
import gzip
import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1024*1024):h.update(chunk)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('phases',nargs='+',choices=('P1','P2','P3'));a=p.parse_args()
    out={}
    for phase in a.phases:
        raw=ROOT/'wp19'/f'wp19-{phase}.json';replay=ROOT/'audit'/f'wp19-{phase}-math-replay.json'
        cert=ROOT/'wp19'/f'wp19-{phase}-certificate-check.json'
        r=json.loads(replay.read_text());c=json.loads(cert.read_text());sha=digest(raw)
        assert r['complete'] and r['phase']==phase and r['phase_sha256']==sha
        assert c['total_failures']==0
        archive=raw.with_suffix('.json.gz')
        with raw.open('rb') as src,archive.open('wb') as dst:
            with gzip.GzipFile(filename='',mode='wb',fileobj=dst,mtime=0,compresslevel=9) as z:shutil.copyfileobj(src,z)
        h=hashlib.sha256()
        with gzip.open(archive,'rb') as f:
            while chunk:=f.read(1024*1024):h.update(chunk)
        assert h.hexdigest()==sha
        out[phase]={'raw_file':raw.name,'raw_bytes':raw.stat().st_size,'raw_sha256':sha,
                    'archive_file':archive.name,'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive),
                    'replay_file':str(replay.relative_to(ROOT)),'replay_sha256':digest(replay),
                    'certificate_file':str(cert.relative_to(ROOT)),'certificate_sha256':digest(cert),
                    'lossless_roundtrip_verified':True}
        print(phase,'archived',raw.stat().st_size,'to',archive.stat().st_size,'bytes',flush=True)
    manifest=ROOT/'wp19'/'WP19-verified-output-manifest.json'
    old=json.loads(manifest.read_text()) if manifest.exists() else {}
    old.update(out);manifest.write_text(json.dumps(old,indent=2)+'\n')

if __name__=='__main__':main()
