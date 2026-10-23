"""On-demand, bounded repository checks. Never modifies playback settings."""
import hashlib
import json
import ssl
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
import xbmc
import xbmcgui
import xbmcvfs
from pyrus_l10n import text, LocalizedDialog
BASE='https://kamilfotoveci-design.github.io/applify/'
def fetch(name):
    # Use the normal verified HTTPS context. No credentials or provider URLs.
    request=Request(BASE+name,headers={'User-Agent':'Pyrus-Diagnostics/1.1.2'})
    with urlopen(request,timeout=5,context=ssl.create_default_context()) as response:
        data=response.read(2*1024*1024+1)
        if len(data)>2*1024*1024:raise ValueError('Repository response too large')
        return data

def repository_check():
    result={}
    try:
        index=fetch('addons.xml');root=ET.fromstring(index)
        if root.tag!='addons':raise ValueError('Invalid repository index')
        result['index']='ok'
        result['versions']={a.get('id'):a.get('version') for a in root.findall('addon') if a.get('id') in ('skin.applify','repository.applify')}
        for suffix,algorithm in [('md5',hashlib.md5),('sha256',hashlib.sha256)]:
            try:
                expected=fetch('addons.xml.'+suffix).decode('ascii').strip().lower()
                result[suffix]='ok' if expected==algorithm(index).hexdigest() else 'mismatch'
            except Exception as exc:result[suffix]=type(exc).__name__
    except Exception as exc:result['index']=type(exc).__name__
    return result

def run():
    progress=xbmcgui.DialogProgressBG();progress.create('Pyrus Skin',text('Checking repository…'))
    try:
        report={'skin':xbmc.getInfoLabel('System.AddonVersion(skin.applify)'),
                'kodi':xbmc.getInfoLabel('System.BuildVersion'),
                'os':xbmc.getInfoLabel('System.OSVersionInfo'),
                'repository':repository_check(),
                'playback':{key:xbmc.getInfoLabel(key) for key in (
                    'Player.Process(videodecoder)','Player.Process(pixfmt)',
                    'Player.Process(deintmethod)','Player.Process(amlogic.eoft_gamut)',
                    'VideoPlayer.HdrType','System.SupportedHDRTypes')}}
        folder='special://profile/addon_data/skin.applify/';xbmcvfs.mkdirs(folder)
        with xbmcvfs.File(folder+'diagnostics.json','w') as file:file.write(json.dumps(report,indent=2))
    finally:progress.close()
    LocalizedDialog().textviewer('Pyrus Skin',text('Diagnostics saved to userdata/addon_data/skin.applify/diagnostics.json')+'\n\n'+json.dumps(report,indent=2))
