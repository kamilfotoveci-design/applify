"""Translate Pyrus UI text while keeping provider data and user input intact."""
import json
from pathlib import Path
import xbmc
import xbmcgui
try:
    STRINGS=json.loads(Path(__file__).with_name('pyrus_strings.json').read_text(encoding='utf-8'))
except (OSError,ValueError):STRINGS={}
def text(value):
    key=STRINGS.get(value)
    if key is None:return value
    translated=xbmc.getLocalizedString(key)
    return translated or value
class LocalizedDialog:
    def __init__(self):self.dialog=xbmcgui.Dialog()
    def __getattr__(self,name):
        method=getattr(self.dialog,name)
        def call(*args,**kwargs):
            args=list(args)
            indexes={'select':(0,1),'multiselect':(0,1),'contextmenu':(0,),
                     'ok':(0,1),'yesno':(0,1),'yesnocustom':(0,1),
                     'input':(0,),'notification':(0,1),'textviewer':(0,1),
                     'browseSingle':(1,),'browse':(1,)}.get(name,())
            for i in indexes:
                if i<len(args):
                    v=args[i]
                    if isinstance(v,str):args[i]=text(v)
                    elif isinstance(v,(tuple,list)):args[i]=[text(x) if isinstance(x,str) else x for x in v]
            for key in ('heading','message','yeslabel','nolabel','customlabel'):
                if key in kwargs:kwargs[key]=text(kwargs[key])
            return method(*args,**kwargs)
        return call
