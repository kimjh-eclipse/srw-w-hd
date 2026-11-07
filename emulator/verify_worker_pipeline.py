"""Headless worker lifecycle/actions after moving HD composition off-process."""
import json
from verify_player import worker_checks,controls_checks,ROOT
from verify_player_actions import worker_checks as actions_checks

def main():
    result=dict(controls=controls_checks(),lifecycle=worker_checks(),actions=actions_checks())
    (ROOT/'test_current/gui/worker_pipeline.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':main()
