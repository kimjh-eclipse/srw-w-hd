"""Keep ingesting arrived drawings until a deadline: run ingest_drawings.py, wait, repeat.

  py -3.11 -X utf8 scripts/assets/ingest_loop.py --until "2026-11-16 09:20" [--every 600]
Each pass prints its lines (prefixed with the time) to stdout.
"""
import argparse,datetime,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT


def main():
    p=argparse.ArgumentParser();p.add_argument('--until',required=True);p.add_argument('--every',type=int,default=600)
    a=p.parse_args();end=datetime.datetime.strptime(a.until,'%Y-%m-%d %H:%M')
    while datetime.datetime.now()<end:
        start=time.time()
        r=subprocess.run([sys.executable,'-X','utf8','scripts/assets/ingest_drawings.py','--workers','8'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        stamp=datetime.datetime.now().strftime('%H:%M')
        for line in r.stdout.splitlines():print(stamp,line,flush=True)
        rest=a.every-(time.time()-start)
        if rest>0 and datetime.datetime.now()+datetime.timedelta(seconds=rest)<end:time.sleep(rest)
    print('LOOP END',flush=True)


if __name__=='__main__':main()
