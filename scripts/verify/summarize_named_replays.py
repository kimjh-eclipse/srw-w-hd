"""Summarize recorded native replays without promoting failed cases to coverage."""
import json,sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

def main():
    base=ROOT/'test_current/combat/named_attacks'
    rows=[r for path in sorted(base.glob('unit_*/report.json')) for r in json.loads(path.read_text(encoding='utf-8'))['rows']]
    counts=Counter(r.get('blocked_reason') or ('completed' if r.get('full_replay_verified') else 'not_started' if not r['battle_started'] else 'unfinished') for r in rows)
    failures=[dict(unit_id=r['unit_id'],name_ja=r['name_ja'],weapon_id=r['weapon_id'],weapon_name=r['weapon_name'],reason=r.get('blocked_reason') or ('not_started' if not r['battle_started'] else 'unfinished')) for r in rows if not r.get('full_replay_verified')]
    result=dict(scope=__doc__,attempted=len(rows),units=len({r['unit_id'] for r in rows}),counts=dict(counts),
        observed_cutin_ids=sorted({i for r in rows for i in r.get('cutin_ids',[])}),
        failures=failures,all_hd_poses_visually_verified=False,campaign_legality_verified=False)
    (base/'catalog_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    previews=[r for path in sorted(base.glob('unit_*/diagnostic_preview/report.json')) for r in json.loads(path.read_text(encoding='utf-8'))['rows']]
    preview_result=dict(scope='Separate locked-animation diagnostics, not normal menu/campaign coverage',attempted=len(previews),
        completed=sum(bool(r.get('animation_preview_verified') or r.get('full_replay_verified')) for r in previews),
        cutin_ids=sorted({i for r in previews for i in r.get('cutin_ids',[])}),
        cases=[dict(unit_id=r['unit_id'],weapon_id=r['weapon_id'],weapon_name=r['weapon_name'],completed=bool(r.get('animation_preview_verified') or r.get('full_replay_verified')),menu_entry_injected=r.get('native_menu_entry_injected',False)) for r in previews],
        normal_menu_legality_verified=False,all_hd_poses_visually_verified=False)
    (base/'preview_summary.json').write_text(json.dumps(preview_result,ensure_ascii=False,indent=2),encoding='utf-8')
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text());by_unit={}
    for row in rows:by_unit.setdefault(row['unit_id'],[]).append(row)
    groups={}
    for u in catalog['units']:
        if u['primary_image'] is None:continue
        s=groups.setdefault(u['series_ja'],dict(units=0,weapons=0,completed=0,secondary=set()))
        s['units']+=1;s['weapons']+=len(u['weapon_ids']);s['completed']+=sum(r.get('full_replay_verified',False) for r in by_unit.get(u['unit_id'],[]))
        if u.get('secondary_image'):s['secondary'].add(u['secondary_image'])
    lines=['# 작품별 연결·재생 검사 현황','','ROM의 적·변형·능력치 변형 레코드를 포함한 수치입니다. 고유 기체 수와 다릅니다.','',
        '주 기체 자세는 기존 검사 범위이며, 서브용 그림 322종은 별도 합성 검사를 통과했습니다. 아래 공격 완료 수는 진단용 게임 상태의 재생 결과로, 모든 HD 자세나 실제 캠페인 조건의 검증 완료를 뜻하지 않습니다.','',
        '| 작품 | 기체 레코드 | 서브 그림 | 무장 레코드 | 공격 재생 완료 |','|---|---:|---:|---:|---:|']
    for name,s in groups.items():lines.append(f"| {name} | {s['units']} | {len(s['secondary'])} | {s['weapons']} | {s['completed']} |")
    lines+=['',f"전체 재생 검사: {len(rows)}건. 분류: {dict(counts)}.",'',
        f"별도의 잠금 연출 검사: {preview_result['attempted']}건 중 {preview_result['completed']}건 재생 완료. 시험용 메뉴 항목을 주입한 경우가 포함되므로 정상 해금·캠페인 검증 수치에는 합산하지 않습니다.",'',
        '미완료 항목과 실제 관측 컷인 ID는 `test_current/combat/named_attacks/catalog_summary.json`에 기록합니다.']
    (ROOT/'docs/NAMED_COVERAGE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(dict(attempted=len(rows),counts=dict(counts),observed_cutins=len(result['observed_cutin_ids']))))

if __name__=='__main__':main()
