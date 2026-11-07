"""Restore the verified Korean ROM at the one canonical game path."""
from pathlib import Path
import hashlib,json,zlib
ROOT=Path(__file__).resolve().parent
BASE='0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478'
target=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
data=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes()
assert hashlib.sha256(data).hexdigest()==BASE
temporary=target.with_suffix('.tmp');temporary.write_bytes(data)
assert hashlib.sha256(temporary.read_bytes()).hexdigest()==BASE
temporary.replace(target)
status=dict(voice_enabled=False,reason='User discontinued voice addition',rom_sha256=BASE,baseline='Korean 1.0.8',hd_assets_preserved=True)
(ROOT/'release_battle_v02/current_features.json').write_text(json.dumps(status,indent=2))
info=dict(path=str(target),size=len(data),sha256=BASE,crc32=f'{zlib.crc32(data):08X}')
(target.parent/'build_manifest.json').write_text(json.dumps(dict(source={**info,'path':str(ROOT/'baseline/SRWW_Korean_1.0.8.nds')},target=info,voice_enabled=False,validation='Byte-identical to verified Korean 1.0.8 baseline'),indent=2))
notice=target.parent/'읽어주세요.txt'
notice.write_text('슈퍼로봇대전 W HD — 현재 롬\n\n음성 추가는 중단했고 시험 음성 패치를 제거했습니다.\n현재 롬은 한글판 1.0.8 기준과 바이트 단위로 같습니다.\n기존 파일 경로를 유지하므로 파일명에는 BattleVoice가 남아 있습니다.\n\nHD 그림은 emulator/HD_게임실행.cmd에서 별도로 적용됩니다.\n이 폴더의 음성 미리보기·검증 자료는 과거 시험 기록입니다.\n',encoding='utf-8')
checks=[f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}' for p in sorted(target.parent.iterdir()) if p.is_file() and p.name!='SHA256SUMS.txt']
(target.parent/'SHA256SUMS.txt').write_text('\n'.join(checks)+'\n')
stamp=ROOT/'graphics/all_units/approved_prefix.json'
if stamp.exists():
    record=json.loads(stamp.read_text());record['rom_sha256']=BASE;stamp.write_text(json.dumps(record,indent=2))
print(json.dumps(status))
