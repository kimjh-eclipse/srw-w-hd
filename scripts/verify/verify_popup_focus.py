"""Check Tcl-only combobox grabs cannot crash focus or receive game input."""
import json,sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_emulator import EmulatorWindow
from gpu_display import GPUDisplay


class Tcl:
    def __init__(self,focus,grab):self.focus=focus;self.grab=grab
    def call(self,name,*args):return self.focus if name=='focus' else self.grab


class Root:
    _w='.'
    def __init__(self,focus,grab):self.tk=Tcl(focus,grab)
    def focus_get(self):raise KeyError('popdown')
    def focus_displayof(self):raise KeyError('popdown')


def main():
    rows=[]
    for focus,grab,popup in (('.!canvas','',False),('.!combobox.popdown.f.l','',True),('.!combobox','.!combobox.popdown',True)):
        app=SimpleNamespace(root=Root(focus,grab),gpu=None,dialog=None,loaded=True)
        app.focus_path=lambda:EmulatorWindow.focus_path(app)
        app.ui_popup_active=lambda:EmulatorWindow.ui_popup_active(app)
        assert app.ui_popup_active()==popup
        if popup:
            assert not EmulatorWindow.has_input_focus(app)
            # The game pointer poll must return before querying canvas
            # coordinates or moving focus away from the popup listbox.
            display=SimpleNamespace(pointer_api=SimpleNamespace(GetAsyncKeyState=lambda key:0),pointer_tracking=False,pointer_down=False,focused=lambda:True)
            GPUDisplay.events(display,app)
            assert not display.pointer_tracking
        rows.append(dict(focus=focus,grab=grab,popup=popup))
    report=dict(passed=True,cases=rows,python_focus_conversion_not_used=True)
    out=ROOT/'test_current/gui/unit_review';out.mkdir(parents=True,exist_ok=True)
    (out/'popup_verification.json').write_text(json.dumps(report,indent=2));print('Passed focus and popup pointer isolation:',len(rows),'cases')


if __name__=='__main__':main()
