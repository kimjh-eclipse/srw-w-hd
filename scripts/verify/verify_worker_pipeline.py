"""Headless worker lifecycle/actions after moving HD composition off-process."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
from scripts.verify.verify_player import worker_checks, controls_checks, ROOT
from scripts.verify.verify_player_actions import worker_checks as actions_checks

def main():
    result=dict(controls=controls_checks(),lifecycle=worker_checks(),actions=actions_checks())
    (ROOT/'test_current/gui/worker_pipeline.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':main()
