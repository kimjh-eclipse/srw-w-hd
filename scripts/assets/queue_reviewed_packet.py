"""Queue a drawn packet after review: keep only the parts that passed
review_packet_candidate.py, write the filtered contract, fill the SHA-256s and
add the entry to docs/PENDING_ART_INSTALL_QUEUE.json (ready_candidates).

  py -3.11 -X utf8 scripts/assets/queue_reviewed_packet.py <folder> <tag>
expects contract_<tag>.json, candidate_<tag>.png, native_<tag>.png,
generated_<tag>.png, queue_entry_<tag>.json and review_candidate_<tag>.json.
"""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    folder=ROOT/sys.argv[1];tag=sys.argv[2]
    rows=json.loads((folder/f'contract_{tag}.json').read_text(encoding='utf-8'))
    review=json.loads((folder/f'review_candidate_{tag}.json').read_text(encoding='utf-8'))
    failed={(r['slot'],r['hash']) for r in review if r['bad']}
    keep=[r for r in rows if (r.get('slot'),r.get('hash')) not in failed]
    for k,r in enumerate(keep):r['slot']=k
    contract=f'contract_{tag}_reviewed.json';(folder/contract).write_text(json.dumps(keep,ensure_ascii=False),encoding='utf-8')
    entry=json.loads((folder/f'queue_entry_{tag}.json').read_text(encoding='utf-8'))
    entry.update(contract=contract,new_source_keys=[dict(hash=r['hash'],index_hash=r['index_hash']) for r in keep],
        file_sha256={k:sha(folder/entry[k] if k!='contract' else folder/contract) for k in ('contract','drawing','native','generated')},
        note=f"recolour packet {folder.name}/{tag}: {len(keep)} of {len(rows)} parts passed Claude review; held {sorted(s for s,_ in failed)}")
    qpath=ROOT/'docs/PENDING_ART_INSTALL_QUEUE.json';queue=json.loads(qpath.read_text(encoding='utf-8'))
    queue['ready_candidates']=[c for c in queue['ready_candidates'] if not (c.get('source')==entry['source'] and c.get('contract')==contract)]+[entry]
    qpath.write_text(json.dumps(queue,ensure_ascii=False,indent=1),encoding='utf-8')
    print('queued',entry['source'],contract,'parts',len(keep),'held',sorted(s for s,_ in failed))


if __name__=='__main__':main()
