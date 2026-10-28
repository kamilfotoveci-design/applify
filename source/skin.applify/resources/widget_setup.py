"""On-demand native Kodi home editor. No service, credentials, or provider URLs."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import xbmc
import xbmcgui
import xbmcvfs
from pyrus_l10n import text, LocalizedDialog
DIALOG=LocalizedDialog()
HOME_DEFAULTS={1:('special://skin/playlists/inprogress_movies.xsp','Up Next'),2:('videodb://recentlyaddedmovies/','Movies'),3:('videodb://recentlyaddedepisodes/','TV Shows'),4:('special://skin/playlists/inprogress_episodes.xsp','Continue Watching'),5:('','Row 5'),6:('','Row 6'),7:('','Row 7'),8:('','Row 8')}
PAGE_DEFAULTS={
 'home':HOME_DEFAULTS,
 'movies':{1:('videodb://movies/titles/','Movies'),2:('videodb://recentlyaddedmovies/','Recently Added Movies'),3:('special://skin/playlists/inprogress_movies.xsp','Continue Watching'),**{r:('','Row '+str(r)) for r in range(4,9)}},
 'tv':{1:('videodb://tvshows/titles/','TV Shows'),2:('videodb://recentlyaddedepisodes/','Recently Added Episodes'),3:('special://skin/playlists/inprogress_episodes.xsp','Continue Watching'),**{r:('','Row '+str(r)) for r in range(4,9)}}
}
DEFAULTS=HOME_DEFAULTS # Backward-compatible name for external editor tooling.
PAGES=('home','movies','tv','custom1','custom2','custom3')
for _page in PAGES[3:]:
    PAGE_DEFAULTS[_page]={r:('', 'Row '+str(r)) for r in range(1,9)}
SUFFIXES=('path','title','layout','limit')
def rpc(method,params):
    payload=json.loads(xbmc.executeJSONRPC(json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params})))
    if 'error' in payload:raise RuntimeError(payload['error'].get('message','Kodi request failed'))
    return payload.get('result',{})
def set_string(key,value):
    # Kodi's built-in parser accepts a quoted argument, including embedded commas.
    value=str(value).replace('\n',' ').replace('\r',' ').replace('"','\\"')
    xbmc.executebuiltin('Skin.SetString(%s,"%s")'%(key,value))
def setting(key):return xbmc.getInfoLabel('Skin.String('+key+')')
def flag(key):return xbmc.getCondVisibility('Skin.HasSetting('+key+')')
def set_flag(key,value):xbmc.executebuiltin(('Skin.SetBool(' if value else 'Skin.Reset(')+key+')')
def current_page():
    page=setting('orchard.page')
    return page if page in PAGES else 'home'
def row_key(row,page=None):
    page=page or current_page()
    return 'orchard.'+('' if page=='home' else page+'.')+'row'+str(row)
def page_defaults(page=None):return PAGE_DEFAULTS[page or current_page()]
def effective(row,suffix,page=None):
    if flag(row_key(row,page)+'.empty'):
        return {'path':'','title':'Empty Slot','layout':'landscape','limit':'12'}[suffix]
    value=setting(row_key(row,page)+'.'+suffix)
    fallback={'path':page_defaults(page)[row][0],'title':text(page_defaults(page)[row][1]),'layout':'landscape','limit':'12'}[suffix]
    return value or fallback
def reload_page():
    xbmc.executebuiltin('ActivateWindow(Home)',True)
    xbmc.executebuiltin('RunScript(special://skin/resources/home_hubs.py,restore)')
def switch_page(page,editing=False):
    if page not in PAGES:raise ValueError('Unknown page.')
    previous=current_page();changed=previous!=page
    # Directory providers track their native $VAR paths automatically. A full reload
    # is needed only when conditional landscape/poster geometry changes.
    needs_reload=any((effective(row,'layout',previous) in ('poster','ranked')) != (effective(row,'layout',page) in ('poster','ranked')) for row in range(1,9))
    if changed:
        set_string('orchard.page',page)
    if not editing:
        # Native activation keeps window history consistent when arriving from a library.
        if changed or not xbmc.getCondVisibility('Window.IsActive(Home)'):
            xbmc.executebuiltin('ActivateWindow(Home)')
        else:
            for row in range(1,9):
                control=PAGES.index(page)*10000+5100+row
                if xbmc.getCondVisibility('Integer.IsGreater(Container(%d).NumItems,0)'%control):
                    xbmc.executebuiltin('SetFocus(%d)'%control);return
            xbmc.executebuiltin('ActivateWindow(SkinSettings)');return
    if not editing:
        xbmc.executebuiltin('SetProperty(pyrus.hub,'+page+',Home)')
        xbmc.executebuiltin('SetProperty(pyrus.visited.'+page+',true,Home)')
        xbmc.executebuiltin('RunScript(special://skin/resources/home_hubs.py,geometry)')
def swap_rows(a,b):
    ae,be=flag(row_key(a)+'.empty'),flag(row_key(b)+'.empty')
    av={s:effective(a,s) for s in SUFFIXES};bv={s:effective(b,s) for s in SUFFIXES}
    ad,bd=flag(row_key(a)+'.disabled'),flag(row_key(b)+'.disabled')
    for row,values,disabled in [(a,bv,bd),(b,av,ad)]:
        for s,v in values.items():set_string(row_key(row)+'.'+s,v)
        set_flag(row_key(row)+'.disabled',disabled)
    set_flag(row_key(a)+'.empty',be)
    set_flag(row_key(b)+'.empty',ae)
def available_addons():
    addons=rpc('Addons.GetAddons',{'type':'xbmc.addon.video','enabled':True,'properties':['name']}).get('addons',[])
    return sorted(addons,key=lambda a:a.get('name','').casefold())
def validate_path(path,addons):
    path=path.strip()
    if not path:raise ValueError('The source path is empty.')
    if any(c in path for c in ('\n','\r','\x00','"')):raise ValueError('The path contains invalid characters.')
    if path.startswith('plugin://'):
        addon=urlparse(path).netloc
        if addon not in {a['addonid'] for a in addons}:raise ValueError('The video add-on is not installed or enabled.')
    elif path.startswith('videodb://'):pass
    elif path.lower().endswith('.xsp'):
        if not xbmcvfs.exists(path):raise ValueError('The smart playlist does not exist.')
    else:raise ValueError('Use a video add-on directory, videodb:// path, or an existing .xsp playlist.')
    return path

def choose_source():
    addons=available_addons()
    options=['Kodi Favourites','Local Library','Smart Playlist (.xsp)','Custom Directory Path']+[a.get('name',a['addonid']) for a in addons]
    picked=DIALOG.select('Choose Content Source',options)
    if picked<0:return None
    if picked==0:
        favs=rpc('Favourites.GetFavourites',{'properties':['path','window','windowparameter']}).get('favourites',[])
        favs=[f for f in favs if f.get('type') in (None,'window') and (f.get('windowparameter') or f.get('path','')).startswith(('plugin://','videodb://','special://'))]
        if not favs:DIALOG.ok('No Lists Found','Add a complete list to Kodi Favourites first.');return None
        idx=DIALOG.select('Kodi Favourites',[f['title'] for f in favs])
        if idx<0:return None
        f=favs[idx];return validate_path(f.get('windowparameter') or f['path'],addons),f['title']
    if picked==1:
        opts=[('Movies','videodb://movies/titles/'),('TV Shows','videodb://tvshows/titles/'),('Recently Added Movies','videodb://recentlyaddedmovies/'),('Recently Added Episodes','videodb://recentlyaddedepisodes/'),('In-progress Movies','special://skin/playlists/inprogress_movies.xsp'),('In-progress Episodes','special://skin/playlists/inprogress_episodes.xsp'),('Movie Collections','videodb://movies/sets/')]
        idx=DIALOG.select('Local Library',[x[0] for x in opts]);return (opts[idx][1],opts[idx][0]) if idx>=0 else None
    if picked==2:
        path=DIALOG.browseSingle(1,'Choose Smart Playlist','video','.xsp',False,False,'special://profile/playlists/video/')
        if not path:return None
        return validate_path(path,addons),path.replace('\\','/').rsplit('/',1)[-1].removesuffix('.xsp')
    if picked==3:
        path=DIALOG.input('Directory Path','plugin://')
        if not path:return None
        path=validate_path(path,addons)
        title=DIALOG.input('Row Name','My Collection')
        return (path,title.strip() or 'My Collection')
    addon=addons[picked-4]
    stack=[('plugin://'+addon['addonid']+'/',addon.get('name',addon['addonid']))]
    while stack:
        path,title=stack[-1]
        # A single explicit request per directory. Never resolve media or poll lists.
        data=rpc('Files.GetDirectory',{'directory':path,'media':'video','properties':[]})
        folders=[x for x in data.get('files',[]) if x.get('filetype')=='directory' and x.get('file','').startswith(('plugin://','videodb://','special://'))]
        idx=DIALOG.select(title,['Use This List','Back']+[x.get('label',x['file']) for x in folders])
        if idx<0:return None
        if idx==0:return path,title
        if idx==1:stack.pop()
        else:
            item=folders[idx-2];stack.append((item['file'],item.get('label','Collection')))
    return None

def save_source(key):
    result=choose_source()
    if not result:return False
    path,title=result
    set_flag(key+'.empty',False)
    set_string(key+'.path',path);set_string(key+'.title',title);set_flag(key+'.disabled',False)
    return True

def home_menu():
    """An on-demand shortcut; all rows remain scoped to the current page."""
    choice=DIALOG.select(PAGE_TITLES[current_page()],['Add widget','Customize this page','Kodi settings'])
    if choice==0:quick_setup()
    elif choice==1:xbmc.executebuiltin('ActivateWindow(1190)')
    elif choice==2:xbmc.executebuiltin('ActivateWindow(Settings)')

def quick_setup():
    """Collect the complete row before changing persistent skin settings."""
    page=current_page()
    free=[r for r in range(1,9) if not effective(r,'path',page)]
    if not free:
        if DIALOG.yesno('Page full','All eight widget slots are in use. Open the editor to replace or remove a row?'):
            xbmc.executebuiltin('ActivateWindow(1190)')
        return
    source=choose_source()
    if not source:return
    path,title=source
    title=DIALOG.input('Widget name',title).strip()
    if not title:return
    style=DIALOG.select('Artwork style',['Landscape','Poster','Top 10 posters'])
    if style<0:return
    key=row_key(free[0],page)
    set_flag(key+'.empty',False)
    for suffix,value in [('path',path),('title',title),('layout',('landscape','poster','ranked')[style]),('limit','12')]:
        set_string(key+'.'+suffix,value)
    set_flag(key+'.disabled',False)
    reload_page()

def open_videos(path):
    if any(c in path for c in ('\n','\r','\x00','"')):raise ValueError('Invalid directory path.')
    xbmc.executebuiltin('ActivateWindow(Videos,"'+path.replace('"','\\"')+'",return)')

def launch_addons():
    import addons_catalog
    addons_catalog.refresh(rpc)
    xbmc.executebuiltin('ActivateWindow(1192)')


SEARCH_ADDONS={'pov':('plugin.video.pov','POV'),'tmdb':('plugin.video.themoviedb.helper','TMDb Helper')}
def search_providers():
    enabled={a['addonid'] for a in available_addons()}
    return [key for key,(addonid,name) in SEARCH_ADDONS.items() if addonid in enabled]
def make_search_path(provider,kind,query):
    from urllib.parse import urlencode
    if provider not in SEARCH_ADDONS or kind not in ('movie','tv'):raise ValueError('Unknown search provider or media type.')
    if provider=='pov':
        args={'mode':'build_movie_list' if kind=='movie' else 'build_tvshow_list','action':'tmdb_movies_search' if kind=='movie' else 'tmdb_tv_search','query':query}
    else:args={'info':'search','tmdb_type':kind,'query':query}
    return 'plugin://'+SEARCH_ADDONS[provider][0]+'/?'+urlencode(args)
def search():
    providers=search_providers()
    if not providers:
        DIALOG.ok('Search','Install and enable POV or TMDb Helper first. Search results are played by that add-on.');return
    provider=setting('orchard.search.provider')
    if provider not in providers:provider=providers[0]
    kind=DIALOG.select('Search',['Movies','TV Shows'])
    if kind<0:return
    query=DIALOG.input('Search '+('Movies' if kind==0 else 'TV Shows')).strip()
    if not query:return
    open_videos(make_search_path(provider,'movie' if kind==0 else 'tv',query))
def search_settings():
    providers=search_providers()
    if not providers:
        DIALOG.ok('Search Provider','Install and enable POV or TMDb Helper first.');return
    selected=DIALOG.select('Search Provider',[SEARCH_ADDONS[p][1] for p in providers]+['Configure TMDb Helper Players','Autocomplete Settings'])
    if selected<0:return
    if selected==len(providers)+1:
        if not xbmc.getCondVisibility('System.AddonIsEnabled(plugin.program.autocompletion)'):
            DIALOG.ok('Autocomplete','AutoCompletion is not enabled.');return
        import xbmcaddon
        xbmcaddon.Addon('plugin.program.autocompletion').openSettings();return
    if selected==len(providers):
        if 'tmdb' not in providers:DIALOG.ok('TMDb Helper','TMDb Helper is not installed.');return
        import xbmcaddon
        xbmcaddon.Addon(SEARCH_ADDONS['tmdb'][0]).openSettings();return
    set_string('orchard.search.provider',providers[selected])
def more(row):
    if row not in range(1,9):raise ValueError('Invalid widget row.')
    if flag(row_key(row)+'.disabled'):return
    source=effective(row,'path')
    if source:open_videos(validate_path(source,available_addons()))

def pov_settings(pairs):
    # Validate the installed schema before touching a provider preference.
    import xbmcaddon
    addon=xbmcaddon.Addon('plugin.video.pov')
    schema=addon.getAddonInfo('path')+'/resources/settings.xml'
    with xbmcvfs.File(schema) as f:root=ET.fromstring(f.read())
    ids={s.get('id') for s in root.iter('setting')}
    for key,value in pairs:
        if key not in ids:raise ValueError('This POV version does not expose '+key+'.')
    for key,value in pairs:addon.setSetting(key,value)

def set_artwork_cache(resolution):
    """Merge native artwork limits; preserve unrelated settings and a backup."""
    if resolution not in (1080,1440,2160):raise ValueError('Unsupported artwork cache resolution.')
    import os
    from pathlib import Path
    path=Path(xbmcvfs.translatePath('special://profile/advancedsettings.xml'))
    existing=path.read_bytes() if path.exists() else None
    parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    try:root=ET.fromstring(existing,parser=parser) if existing is not None else ET.Element('advancedsettings')
    except ET.ParseError:raise ValueError('advancedsettings.xml is invalid. It was not changed.')
    if root.tag!='advancedsettings':raise ValueError('Unexpected advancedsettings.xml root. It was not changed.')
    elements=root.findall('fanartres')
    if not elements:elements=[ET.SubElement(root,'fanartres')]
    for element in elements:element.text=str(resolution)
    images=root.findall('imageres')
    if not images:images=[ET.SubElement(root,'imageres')]
    for element in images:element.text='1080' if resolution>1080 else '720'
    backup=path.with_name('advancedsettings.orchard-artwork-backup.xml')
    if existing is not None and not backup.exists():
        with backup.open('xb') as f:f.write(existing)
    temporary=path.with_name('advancedsettings.orchard-new.xml')
    path.parent.mkdir(parents=True,exist_ok=True)
    try:
        temporary.write_bytes(ET.tostring(root,encoding='utf-8',xml_declaration=True))
        os.replace(temporary,path)
    finally:
        if temporary.exists():temporary.unlink()

def artwork_settings():
    choices=['POV: Original artwork (sharpest, larger downloads)','POV: High artwork (less data)','POV: Remove Next Episodes date','Show Current Artwork URL','Fanart cache: 1440p (restart required)','Fanart cache: 2160p / 4K (restart required)','Fanart cache: 1080p (lower memory)','POV: Refresh artwork metadata (confirm in POV)']
    selected=DIALOG.select('Artwork and Episode Titles',choices)
    if selected<0:return
    if selected==7:
        if 'pov' not in search_providers():DIALOG.ok('POV','POV is not installed or enabled.');return
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.pov/?mode=clear_cache&cache=meta)')
        return
    if selected>=4:
        set_artwork_cache({4:1440,5:2160,6:1080}[selected])
        DIALOG.ok('Artwork Cache','Restart Kodi to apply. Existing cached images may need refreshing. Original artwork and matching GUI resolution are also required; this does not upscale missing detail.')
        return
    if selected==3:
        xbmc.executebuiltin('ActivateWindow(Home)',True)
        xbmc.sleep(350)
        art=xbmc.getInfoLabel('$VAR[OrchardHeroArt]')
        resolution=xbmc.getInfoLabel('System.ScreenResolution')
        pov='Not installed'
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.pov)'):
            import xbmcaddon
            pov=xbmcaddon.Addon('plugin.video.pov').getSetting('image_resolutions')
        message='GUI: '+resolution+'\nPOV image_resolutions: '+pov+' (3 = Original)\n\nFanart URL:\n'+(art or 'No fanart reported.')
        folder='special://profile/addon_data/skin.applify/'
        xbmcvfs.mkdirs(folder)
        with xbmcvfs.File(folder+'artwork-diagnostics.txt','w') as f:f.write(message)
        DIALOG.textviewer('Current Artwork',message)
        return
    if 'pov' not in search_providers():DIALOG.ok('POV','POV is not installed or enabled.');return
    pairs=[('image_resolutions','3' if selected==0 else '2')] if selected<2 else [('nextep.include_airdate','false')]
    pov_settings(pairs)
    xbmc.executebuiltin('ReloadSkin()')

def configure_pov_titles():
    if flag('orchard.pov.cleanlabels'):return
    if not xbmc.getCondVisibility('System.HasAddon(plugin.video.pov)'):return
    try:pov_settings([('nextep.include_airdate','false')])
    except (RuntimeError,ValueError,OSError,ET.ParseError):return
    set_flag('orchard.pov.cleanlabels',True)

PAGE_TITLES={p:text(n) for p,n in zip(PAGES,('Watch Now','Movies','TV Shows','Custom Hub 1','Custom Hub 2','Custom Hub 3'))}
APPEARANCE=[('Reduce animations','orchard.reducedanimations'),('Hide hero text','orchard.hidehero'),('Hide all card captions','orchard.hidecardtitles'),('Use title instead of clearlogo','orchard.hideherologo'),('Hide synopsis','orchard.hideheroplot'),('Hide year / genre','orchard.hideherometa'),('Hide watched progress bars','orchard.hideprogress')]
PLAYBACK=[('Hide passive timeline while paused','orchard.hidepausedosd'),('Show chapters in playback controls','orchard.osdchapters'),('Show clock in playback controls','orchard.osdclock')]
def reset_page(page):
    for row in range(1,9):
        for suffix in (*SUFFIXES,'disabled','empty'):xbmc.executebuiltin('Skin.Reset('+row_key(row,page)+'.'+suffix+')')
BACKUP_STRINGS=('orchard.backdropdim', 'orchard.cardcaptions', 'orchard.page', 'pyrus.hub.addons.label', 'pyrus.hub.addons.path', 'pyrus.hub.addons.sub1.label', 'pyrus.hub.addons.sub1.path', 'pyrus.hub.addons.sub2.label', 'pyrus.hub.addons.sub2.path', 'pyrus.hub.addons.sub3.label', 'pyrus.hub.addons.sub3.path', 'pyrus.hub.addons.sub4.label', 'pyrus.hub.addons.sub4.path', 'pyrus.hub.addons.sub5.label', 'pyrus.hub.addons.sub5.path', 'pyrus.hub.addons.sub6.label', 'pyrus.hub.addons.sub6.path', 'pyrus.hub.custom1.label', 'pyrus.hub.custom1.path', 'pyrus.hub.custom1.sub1.label', 'pyrus.hub.custom1.sub1.path', 'pyrus.hub.custom1.sub2.label', 'pyrus.hub.custom1.sub2.path', 'pyrus.hub.custom1.sub3.label', 'pyrus.hub.custom1.sub3.path', 'pyrus.hub.custom1.sub4.label', 'pyrus.hub.custom1.sub4.path', 'pyrus.hub.custom1.sub5.label', 'pyrus.hub.custom1.sub5.path', 'pyrus.hub.custom1.sub6.label', 'pyrus.hub.custom1.sub6.path', 'pyrus.hub.custom2.label', 'pyrus.hub.custom2.path', 'pyrus.hub.custom2.sub1.label', 'pyrus.hub.custom2.sub1.path', 'pyrus.hub.custom2.sub2.label', 'pyrus.hub.custom2.sub2.path', 'pyrus.hub.custom2.sub3.label', 'pyrus.hub.custom2.sub3.path', 'pyrus.hub.custom2.sub4.label', 'pyrus.hub.custom2.sub4.path', 'pyrus.hub.custom2.sub5.label', 'pyrus.hub.custom2.sub5.path', 'pyrus.hub.custom2.sub6.label', 'pyrus.hub.custom2.sub6.path', 'pyrus.hub.custom3.label', 'pyrus.hub.custom3.path', 'pyrus.hub.custom3.sub1.label', 'pyrus.hub.custom3.sub1.path', 'pyrus.hub.custom3.sub2.label', 'pyrus.hub.custom3.sub2.path', 'pyrus.hub.custom3.sub3.label', 'pyrus.hub.custom3.sub3.path', 'pyrus.hub.custom3.sub4.label', 'pyrus.hub.custom3.sub4.path', 'pyrus.hub.custom3.sub5.label', 'pyrus.hub.custom3.sub5.path', 'pyrus.hub.custom3.sub6.label', 'pyrus.hub.custom3.sub6.path', 'pyrus.hub.home.label', 'pyrus.hub.home.path', 'pyrus.hub.home.sub1.label', 'pyrus.hub.home.sub1.path', 'pyrus.hub.home.sub2.label', 'pyrus.hub.home.sub2.path', 'pyrus.hub.home.sub3.label', 'pyrus.hub.home.sub3.path', 'pyrus.hub.home.sub4.label', 'pyrus.hub.home.sub4.path', 'pyrus.hub.home.sub5.label', 'pyrus.hub.home.sub5.path', 'pyrus.hub.home.sub6.label', 'pyrus.hub.home.sub6.path', 'pyrus.hub.livetv.label', 'pyrus.hub.livetv.path', 'pyrus.hub.livetv.sub1.label', 'pyrus.hub.livetv.sub1.path', 'pyrus.hub.livetv.sub2.label', 'pyrus.hub.livetv.sub2.path', 'pyrus.hub.livetv.sub3.label', 'pyrus.hub.livetv.sub3.path', 'pyrus.hub.livetv.sub4.label', 'pyrus.hub.livetv.sub4.path', 'pyrus.hub.livetv.sub5.label', 'pyrus.hub.livetv.sub5.path', 'pyrus.hub.livetv.sub6.label', 'pyrus.hub.livetv.sub6.path', 'pyrus.hub.movies.label', 'pyrus.hub.movies.path', 'pyrus.hub.movies.sub1.label', 'pyrus.hub.movies.sub1.path', 'pyrus.hub.movies.sub2.label', 'pyrus.hub.movies.sub2.path', 'pyrus.hub.movies.sub3.label', 'pyrus.hub.movies.sub3.path', 'pyrus.hub.movies.sub4.label', 'pyrus.hub.movies.sub4.path', 'pyrus.hub.movies.sub5.label', 'pyrus.hub.movies.sub5.path', 'pyrus.hub.movies.sub6.label', 'pyrus.hub.movies.sub6.path', 'pyrus.hub.tv.label', 'pyrus.hub.tv.path', 'pyrus.hub.tv.sub1.label', 'pyrus.hub.tv.sub1.path', 'pyrus.hub.tv.sub2.label', 'pyrus.hub.tv.sub2.path', 'pyrus.hub.tv.sub3.label', 'pyrus.hub.tv.sub3.path', 'pyrus.hub.tv.sub4.label', 'pyrus.hub.tv.sub4.path', 'pyrus.hub.tv.sub5.label', 'pyrus.hub.tv.sub5.path', 'pyrus.hub.tv.sub6.label', 'pyrus.hub.tv.sub6.path')
BACKUP_FLAGS=('orchard.hidecardtitles', 'orchard.hidehero', 'orchard.hideherologo', 'orchard.hideherometa', 'orchard.hideheroplot', 'orchard.hidepausedosd', 'orchard.hideprogress', 'orchard.migrated', 'orchard.osdchapters', 'orchard.osdclock', 'orchard.pov.cleanlabels', 'orchard.reducedanimations', 'pyrus.hideratings', 'pyrus.hub.custom1.enabled', 'pyrus.hub.custom2.enabled', 'pyrus.hub.custom3.enabled', 'pyrus.showlivetv')

def backup_preferences():
    return {'strings':{key:setting(key) for key in BACKUP_STRINGS},
            'flags':{key:flag(key) for key in (*BACKUP_FLAGS,'pyrus.hidewatchnow')}}

def validate_preferences(data):
    if not isinstance(data,dict) or set(data)!={'strings','flags'}:
        raise ValueError('Invalid menu and appearance backup.')
    if not isinstance(data['flags'],dict):raise ValueError('Invalid backup flags.')
    data['flags'].setdefault('pyrus.hidewatchnow',False)
    for kind,allowed in (('strings',BACKUP_STRINGS),('flags',(*BACKUP_FLAGS,'pyrus.hidewatchnow'))):
        values=data[kind]
        if not isinstance(values,dict) or set(values)!=set(allowed):
            raise ValueError('Invalid menu and appearance backup.')
        for key,value in values.items():
            if kind=='flags':
                if not isinstance(value,bool):raise ValueError('Invalid setting visibility.')
            elif not isinstance(value,str) or len(value)>4096 or any(c in value for c in ('\n','\r','\x00')):
                raise ValueError('Invalid menu setting.')
            elif key.endswith('.label') and len(value)>60:
                raise ValueError('Use a name of up to 60 characters.')
            elif key.endswith('.path') and value:
                if '"' in value:raise ValueError('Invalid source path.')
                parsed=urlparse(value)
                if parsed.scheme=='pyrus':
                    if value not in ('pyrus://guide','pyrus://channels','pyrus://radio','pyrus://recordings'):raise ValueError('Invalid source path.')
                elif parsed.scheme=='addon':
                    if not re.fullmatch(r'addon://[A-Za-z0-9_.-]+',value):raise ValueError('Invalid source path.')
                elif parsed.scheme=='plugin':
                    if not re.fullmatch(r'[A-Za-z0-9_.-]+',parsed.netloc):raise ValueError('Invalid source path.')
                else:validate_path(value,available_addons())
    if data['strings'].get('orchard.page') not in ('',*PAGES):raise ValueError('Unknown page.')
    return data

def export_widgets():
    folder='special://profile/addon_data/skin.applify/'
    xbmcvfs.mkdirs(folder)
    data={'version':2,'preferences':backup_preferences(),'pages':{page:[{**{s:effective(row,s,page) for s in SUFFIXES},'disabled':flag(row_key(row,page)+'.disabled'),'empty':flag(row_key(row,page)+'.empty')} for row in range(1,9)] for page in PAGES}}
    temporary=folder+'widget-backup.tmp.json'
    with xbmcvfs.File(temporary,'w') as f:f.write(json.dumps(data,ensure_ascii=False,indent=2))
    if not xbmcvfs.rename(temporary,folder+'widget-backup.json'):
        raise OSError('Could not save the backup.')
    DIALOG.ok('Widgets Exported','Saved to userdata/addon_data/skin.applify/widget-backup.json')
def import_widgets():
    path=DIALOG.browseSingle(1,'Import Widget Settings','files','.json',False,False,'special://profile/addon_data/skin.applify/')
    if not path:return False
    with xbmcvfs.File(path) as f:data=json.loads(f.read())
    if not isinstance(data,dict) or data.get('version') not in (1,2) or not isinstance(data.get('pages'),dict):raise ValueError('Not a valid Pyrus / Applify widget backup.')
    addons=available_addons();pending=[];missing=0
    preferences=validate_preferences(data.get('preferences',{})) if data['version']==2 else None
    # Validate the complete backup before changing any settings.
    for page in PAGES:
        rows=data['pages'].get(page)
        if rows is None and page.startswith('custom'):continue
        if not isinstance(rows,list) or len(rows)!=8:raise ValueError('Each page must contain exactly eight rows.')
        for row,entry in enumerate(rows,1):
            if not isinstance(entry,dict) or any(not isinstance(entry.get(s),str) for s in SUFFIXES):raise ValueError('Invalid row fields.')
            if entry['layout'] not in ('landscape','poster','ranked') or entry['limit'] not in ('6','10','12','20','24') or len(entry['title'])>200:raise ValueError('Invalid row style, item limit or title.')
            if not isinstance(entry.get('disabled'),bool):raise ValueError('Invalid row visibility.')
            if not isinstance(entry.get('empty',False),bool):raise ValueError('Invalid empty slot.')
            disabled=entry['disabled'];source=entry['path']
            if source:
                if any(c in source for c in ('\n','\r','\x00','"')):raise ValueError('Invalid source path.')
                try:validate_path(source,addons)
                except ValueError:
                    # Keep missing add-on paths for later recovery; do not activate them.
                    if source.startswith('plugin://') and urlparse(source).netloc and urlparse(source).netloc not in {a['addonid'] for a in addons}:disabled=True;missing+=1
                    else:raise
            pending.append((row_key(row,page),entry,disabled))
    if not DIALOG.yesno('Import Widgets','Replace the widget rows on all included pages?'):return False
    for key,entry,disabled in pending:
        for suffix in SUFFIXES:set_string(key+'.'+suffix,entry[suffix])
        set_flag(key+'.disabled',disabled)
        set_flag(key+'.empty',entry.get('empty',False))
    if preferences is not None:
        for key,value in preferences['strings'].items():set_string(key,value)
        for key,value in preferences['flags'].items():set_flag(key,value)
        HOME=xbmcgui.Window(10000);HOME.clearProperty('pyrus.nav.initialized');HOME.clearProperty('pyrus.hub')
    if missing:DIALOG.ok('Widgets Imported',text('{count} rows use missing add-ons and were hidden.').format(count=missing))
    return True
def settings_menu(section):
    if section=='search':search_settings();return
    if section=='artwork':artwork_settings();return
    dirty=False
    while True:
        if section in ('appearance','playback'):
            options=APPEARANCE if section=='appearance' else PLAYBACK
            labels=[text(title)+'  ['+text('On' if flag(key) else 'Off')+']' for title,key in options]
            if section=='appearance':labels+=[text('Backdrop Dimming')+'  ['+text((setting('orchard.backdropdim') or 'none').title())+']',text('Card Captions')+'  ['+text((setting('orchard.cardcaptions') or 'off').title())+']']
            idx=DIALOG.select(section.title(),labels)
            if idx<0:break
            if idx<len(options):
                title,key=options[idx];set_flag(key,not flag(key));dirty=True
            elif idx==len(options)+1 and section=='appearance':
                values=['Off','Focused','All'];choice=DIALOG.select('Card Captions',values)
                if choice>=0:
                    set_string('orchard.cardcaptions',values[choice].lower())
                    if choice:set_flag('orchard.hidecardtitles',False)
                    dirty=True
            else:
                values=['None','Low','Medium','High'];choice=DIALOG.select('Backdrop Dimming',values)
                if choice>=0:set_string('orchard.backdropdim',values[choice].lower());dirty=True
            xbmc.sleep(100)
        elif section=='performance':
            idx=DIALOG.select('Performance Presets',['Balanced: 10 items per row, animations on','Low memory: 6 items per row, reduced animations'])
            if idx<0:break
            for page in PAGES:
                for row in range(1,9):set_string(row_key(row,page)+'.limit','6' if idx==1 else '10')
            set_flag('orchard.reducedanimations',idx==1);dirty=True;break
        elif section=='maintenance':
            idx=DIALOG.select('Widgets and Maintenance',['Refresh All Widgets','Export All Widget Pages','Import Widget Pages',text('Reset {page} rows').format(page=PAGE_TITLES[current_page()]),'Repository and playback diagnostics','Check for repository updates'])
            if idx<0:break
            if idx==0:dirty=True;break
            if idx==1:export_widgets()
            if idx==2:dirty=import_widgets() or dirty
            if idx==3 and DIALOG.yesno('Reset Page',text('Restore the eight {page} rows to their defaults?').format(page=PAGE_TITLES[current_page()])):
                reset_page(current_page());dirty=True
            if idx==4:
                import pyrus_diagnostics
                pyrus_diagnostics.run()
            if idx==5:xbmc.executebuiltin('UpdateAddonRepos()')
        else:return
    if dirty:
        if section=='maintenance' and idx==0:
            # Queue background refresh; hidden visited hubs refresh on next visit.
            xbmcgui.Window(10000).setProperty('pyrus.refresh.request','true')
            reload_page()
        else:reload_page()

def migrate():
    if flag('orchard.migrated'):return
    old='special://profile/addon_data/skin.orchard/settings.xml'
    if xbmcvfs.exists(old):
        try:
            with xbmcvfs.File(old) as f:doc=ET.fromstring(f.read())
            for e in doc.findall('.//setting'):
                key=e.get('id','');value=e.text or ''
                if re.fullmatch(r'orchard\.row[1-8]\.(path|title|layout|limit)',key) and value:set_string(key,value)
        except (ET.ParseError,OSError):xbmc.log('Pyrus Skin: previous widget settings could not be imported.',xbmc.LOGWARNING)
    set_flag('orchard.migrated',True)

def main():
    if len(sys.argv)<2:return
    command=sys.argv[1]
    if command=='homemenu':home_menu();return
    if command=='quicksetup':quick_setup();return
    if command=='synopsis':
        plot=xbmc.getInfoLabel('ListItem.Plot')
        DIALOG.textviewer('Synopsis',plot or 'No synopsis available.')
        return
    if command=='init':migrate();configure_pov_titles();return
    if command=='addons':launch_addons();return
    if command=='addons_refresh':
        import addons_catalog
        addons_catalog.refresh(rpc)
        return
    if command=='addons_page':
        import addons_catalog
        addons_catalog.move(int(sys.argv[2]))
        xbmc.executebuiltin('SetFocus(50)')
        return
    if command=='views':
        selected=DIALOG.select('View Style',['List','Landscape','Poster'])
        if selected>=0:xbmc.executebuiltin('Container.SetViewMode('+str(50+selected)+')')
        return
    if command=='more':
        if len(sys.argv)>2:more(int(sys.argv[2]))
        return
    if command=='reloadpage':reload_page();return
    if command in ('page','editpage'):
        if len(sys.argv)>2:switch_page(sys.argv[2],editing=command=='editpage')
        return
    if command=='search':search();return
    if command=='openeditor':
        if len(sys.argv)>2 and sys.argv[2] in PAGES:
            set_string('orchard.page',sys.argv[2])
            xbmc.executebuiltin('ActivateWindow(1190)')
        return
    if command=='settings':
        if len(sys.argv)>2:settings_menu(sys.argv[2])
        return
    if command in ('sports','kids'):
        key='orchard.'+command
        choice=DIALOG.select(command.title()+' Source',['Choose Source','Remove Source'])
        if choice==0:save_source(key)
        elif choice==1:
            for s in ('path','title'):xbmc.executebuiltin('Skin.Reset('+key+'.'+s+')')
        return
    if command=='add':
        free=[r for r in range(1,9) if not effective(r,'path')]
        if not free:DIALOG.ok('Page Full','Eight rows per page are available. Edit, hide, or remove an existing row.');return
        save_source(row_key(free[0]));return
    if command not in {str(x) for x in range(1,9)}:return
    r=int(command);key=row_key(r)
    choice=DIALOG.select(text('{page} / Row {row} — {title}').format(page=PAGE_TITLES[current_page()],row=command,title=effective(r,'title')),['Choose Source / Trakt List','Rename','Artwork Style','Item Limit','Move Up','Move Down','Show / Hide Row','Remove Row','Restore Default','Copy Row from Another Page'])
    if choice==0:save_source(key)
    elif choice==1:
        value=DIALOG.input('Row Name',effective(r,'title')).strip()
        if value:set_string(key+'.title',value)
    elif choice==2:
        opts=[('Landscape','landscape'),('Poster','poster'),('Top 10 Posters','ranked')]
        idx=DIALOG.select('Artwork Style',[x[0] for x in opts])
        if idx>=0:set_string(key+'.layout',opts[idx][1])
    elif choice==3:
        opts=['6','10','12','20','24'];idx=DIALOG.select('Maximum Items',opts)
        if idx>=0:set_string(key+'.limit',opts[idx])
    elif choice==4 and r>1:swap_rows(r,r-1)
    elif choice==5 and r<8:swap_rows(r,r+1)
    elif choice==6:set_flag(key+'.disabled',not flag(key+'.disabled'))
    elif choice==7:
        for s in SUFFIXES:xbmc.executebuiltin('Skin.Reset('+key+'.'+s+')')
        set_flag(key+'.disabled',False)
        set_flag(key+'.empty',True)
    elif choice==8:
        for s in (*SUFFIXES,'disabled','empty'):xbmc.executebuiltin('Skin.Reset('+key+'.'+s+')')
    elif choice==9:
        pages=[p for p in PAGES if p!=current_page()]
        idx=DIALOG.select('Copy from Page',[PAGE_TITLES[p] for p in pages])
        if idx<0:return
        page=pages[idx];idx=DIALOG.select('Copy Row',[effective(r,'title',page) for r in range(1,9)])
        if idx<0:return
        for suffix in SUFFIXES:set_string(key+'.'+suffix,effective(idx+1,suffix,page))
        set_flag(key+'.disabled',flag(row_key(idx+1,page)+'.disabled'))
        set_flag(key+'.empty',flag(row_key(idx+1,page)+'.empty'))

if __name__=='__main__':
    try:main()
    except (RuntimeError,ValueError,OSError,KeyError,IndexError,TypeError) as exc:
        xbmc.log('Pyrus Skin editor source request failed: '+type(exc).__name__,xbmc.LOGERROR)
        DIALOG.ok('Pyrus Skin',str(exc) if isinstance(exc,ValueError) else 'The add-on could not return this directory. Open the list directly in its add-on, or use Kodi Favourites.')
