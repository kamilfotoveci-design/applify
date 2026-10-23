"""Pyrus home hubs. No service, arbitrary built-ins, or network requests."""
import sys
import xbmc
import xbmcgui
import widget_setup as widgets
from pyrus_l10n import text, LocalizedDialog
DIALOG = LocalizedDialog()
HOME = xbmcgui.Window(10000)
PAGES = ('home', 'movies', 'tv', 'custom1', 'custom2', 'custom3')
NAV = {'home':9101, 'movies':9102, 'tv':9103, 'addons':9104,
       'custom1':9111, 'custom2':9112, 'custom3':9113, 'livetv':9114}
NAMES = {'home':'Watch Now','movies':'Movies','tv':'TV Shows','addons':'Add-ons',
         'custom1':'Custom Hub 1','custom2':'Custom Hub 2','custom3':'Custom Hub 3','livetv':'Live TV'}

def title(page):
    return widgets.setting('pyrus.hub.'+page+'.label') or text(NAMES[page])

def hub_visible(page):
    if page not in NAV:return False
    if page.startswith('custom'):return widgets.flag('pyrus.hub.'+page+'.enabled')
    if page=='livetv':return widgets.flag('pyrus.showlivetv') or xbmc.getCondVisibility('PVR.HasTVChannels')
    return True

def apply_geometry(page):
    # Kodi exposes XML groups, lists and buttons through Window.getControl.
    # GroupList recalculates its child heights each frame. Keep one provider
    # container per row, preserving list focus and avoiding ReloadSkin.
    controls=[]
    for row in range(1,9):
        poster=widgets.effective(row,'layout',page) in ('poster','ranked')
        controls.append((HOME.getControl(5000+row),HOME.getControl(5100+row),
                         HOME.getControl(5200+row),poster))
    HOME.setProperty('pyrus.nav.transition','true')
    try:
        for group,items,more,poster in controls:
            group.setHeight(560 if poster else 276)
            items.setHeight(378 if poster else 200)
            more.setPosition(1660,206 if poster else 117)
    finally:HOME.clearProperty('pyrus.nav.transition')

def restore_focus():
    value=HOME.getProperty('pyrus.nav.restore')
    first_load=not HOME.getProperty('pyrus.nav.initialized')
    page=HOME.getProperty('pyrus.hub') or widgets.current_page()
    if page in PAGES:page=widgets.current_page()
    if value.isdecimal():page=next((p for p,c in NAV.items() if c==int(value)),page)
    if not hub_visible(page):
        page='home';widgets.set_string('orchard.page',page);value=str(NAV[page])
    if page in PAGES:apply_geometry(page)
    HOME.setProperty('pyrus.hub',page)
    HOME.setProperty('pyrus.nav.initialized','true')
    HOME.clearProperty('pyrus.nav.restore')
    if first_load or value:
        xbmc.executebuiltin('SetFocus(%d)'%NAV[page])

def go_back():
    if (HOME.getProperty('pyrus.hub') or widgets.current_page())=='home':
        xbmc.executebuiltin('ActivateWindow(ShutdownMenu)');return
    HOME.clearProperty('pyrus.nav.restore')
    preview('home',9101,require_focus=False)
    xbmc.executebuiltin('SetFocus(9101)')

def preview(page, control, require_focus=True):
    if not hub_visible(page) or NAV[page] != control:return
    if not HOME.getProperty('pyrus.nav.initialized'):return
    if HOME.getProperty('pyrus.nav.restore') and HOME.getProperty('pyrus.nav.restore')!=str(control):return
    # Ignore scripts left behind while the user quickly crosses the top menu.
    if require_focus:
        focused='Window.IsActive(Home) + Control.HasFocus(%d)'%control
        if not xbmc.getCondVisibility(focused):return
        # The highlight responds immediately; skip provider requests for tabs
        # crossed rapidly on the way to the intended destination.
        if xbmc.Monitor().waitForAbort(0.08):return
        if not xbmc.getCondVisibility(focused):return
    if page in ('addons','livetv'):
        if HOME.getProperty('pyrus.hub') == page:return
        HOME.setProperty('pyrus.hub',page)
        if page=='addons':
            import addons_catalog
            addons_catalog.refresh(widgets.rpc)
        return
    old = widgets.current_page()
    if old == page:
        HOME.setProperty('pyrus.hub',page);return
    apply_geometry(page)
    HOME.setProperty('pyrus.hub',page)
    widgets.set_string('orchard.page',page)
    HOME.setProperty('orchard.hero.row','1')

def open_hub(page):
    if page not in NAV:return
    path=widgets.setting('pyrus.hub.'+page+'.path')
    if path:
        open_target(path);return
    if page=='addons':
        xbmc.executebuiltin('ActivateWindow(Videos,"addons://sources/video/",return)');return
    if page=='livetv':xbmc.executebuiltin('ActivateWindow(TVGuide)');return
    if page in ('movies','tv'):
        widgets.open_videos('videodb://'+('movies' if page=='movies' else 'tvshows')+'/titles/');return
    # A configured widget's full directory wins over the local fallback. Empty
    # or disabled first slots do not prevent a later row being the hub root.
    for row in range(1,9):
        path=widgets.effective(row,'path',page)
        if path and not widgets.flag(widgets.row_key(row,page)+'.disabled'):
            widgets.open_videos(path);return
    if page in ('movies','tv'):
        widgets.open_videos('videodb://'+('movies' if page=='movies' else 'tvshows')+'/titles/')
    else:
        widgets.set_string('orchard.page',page)
        xbmc.executebuiltin('ActivateWindow(1190)')

PVR_DESTINATIONS={'guide':'TVGuide','channels':'TVChannels','radio':'RadioChannels','recordings':'TVRecordings'}
def open_target(path):
    from urllib.parse import urlparse
    if path.startswith('addon://'):
        import addons_catalog
        addon=urlparse(path).netloc
        if path!='addon://'+addon or addon not in {a['id'] for a in addons_catalog.collect(widgets.rpc)}:
            raise ValueError(text('The add-on is not installed or enabled.'))
        xbmc.executebuiltin('RunAddon('+addon+')');return
    if path.startswith('pyrus://'):
        dest=path[len('pyrus://'):]
        if dest not in PVR_DESTINATIONS:raise ValueError(text('Invalid source path.'))
        xbmc.executebuiltin('ActivateWindow('+PVR_DESTINATIONS[dest]+')');return
    widgets.validate_path(path,widgets.available_addons())
    widgets.open_videos(path)

def target():
    mode=DIALOG.select('Opening destination',['Video collection','Installed add-on','TV guide','TV channels','Radio channels','Recordings'])
    if mode<0:return None
    if mode==0:
        result=widgets.choose_source()
        if not result:return None
        path,label=result
    elif mode==1:
        import addons_catalog
        addons=addons_catalog.collect(widgets.rpc)
        if not addons:
            DIALOG.ok('Add-ons','No enabled runnable add-ons are installed.');return None
        idx=DIALOG.select('Installed add-on',[a['name'] for a in addons])
        if idx<0:return None
        path,label='addon://'+addons[idx]['id'],addons[idx]['name']
    else:
        key,label=[('guide','TV guide'),('channels','TV channels'),('radio','Radio channels'),('recordings','Recordings')][mode-2]
        path='pyrus://'+key
    label=DIALOG.input('Menu name',label).strip()
    if not label:return None
    if len(label)>60:raise ValueError(text('Use a name of up to 60 characters.'))
    return path,label

def select_hub(page):
    """Change the active top-level tab only when OK confirms it.

    Left/Right merely move focus. Confirming an already active tab is a
    deliberate no-op: never open a video library or configured destination.
    """
    if page not in NAV or not hub_visible(page):return
    active=HOME.getProperty('pyrus.hub') or widgets.current_page()
    if active != page:
        preview(page,NAV[page],require_focus=False)

def move_down(page):
    # Moving down without OK enters the CURRENT page, not the unconfirmed tab.
    # Never switch hubs from directional focus movement.
    if page not in NAV:return
    active=HOME.getProperty('pyrus.hub') or widgets.current_page()
    page=active if active in NAV and hub_visible(active) else 'home'
    for i in range(1,7):
        if widgets.setting('pyrus.hub.'+page+'.sub'+str(i)+'.path'):
            xbmc.executebuiltin('SetFocus(%d)'%(8400+i));return
    enter_content(page)

def enter_content(page):
    if page=='addons':
        xbmc.executebuiltin('SetFocus(50)' if xbmc.getCondVisibility('Integer.IsGreater(Window(Home).Property(orchard.addons.visiblecount),0)') else 'SetFocus(8201)');return
    if page=='livetv':xbmc.executebuiltin('SetFocus(8301)');return
    for row in range(1,9):
        if xbmc.getCondVisibility('Integer.IsGreater(Container(%d).NumItems,0)'%(5100+row)):
            xbmc.executebuiltin('SetFocus(%d)'%(5100+row));return
    xbmc.executebuiltin('SetFocus(7200)')

def open_submenu(index):
    page=HOME.getProperty('pyrus.hub')
    if page not in NAV or index not in range(1,7):return
    path=widgets.setting('pyrus.hub.'+page+'.sub'+str(index)+'.path')
    if path:
        open_target(path)

def submenu(page):
    choices=[]
    for i in range(1,7):
        key='pyrus.hub.'+page+'.sub'+str(i)
        path=widgets.setting(key+'.path')
        if path:choices.append((widgets.setting(key+'.label') or text('Open'),path))
    if not choices:
        if DIALOG.yesno('Submenu','No submenu items yet. Open the menu editor?'):edit_hub(page)
        return
    idx=DIALOG.select(title(page),[x[0] for x in choices])
    if idx>=0:
        open_target(choices[idx][1])

def edit_submenu(page):
    while True:
        labels=[widgets.setting('pyrus.hub.'+page+'.sub'+str(i)+'.label') or text('Empty Slot') for i in range(1,7)]
        i=DIALOG.select('Submenu',labels)
        if i<0:return
        key='pyrus.hub.'+page+'.sub'+str(i+1)
        action=DIALOG.select(labels[i],['Choose Source','Remove'])
        if action==0:
            item=target()
            if item:
                widgets.set_string(key+'.path',item[0]);widgets.set_string(key+'.label',item[1])
        elif action==1:
            for s in ('path','label'):xbmc.executebuiltin('Skin.Reset('+key+'.'+s+')')

def edit_hub(page):
    while True:
        options=['Rename','Set opening destination','Reset opening destination','Edit submenu']
        if page in PAGES:options+=['Edit widget rows','Continue Watching first']
        if page.startswith('custom'):options+=['Show / Hide Hub']
        idx=DIALOG.select(title(page),options)
        if idx<0:return
        key='pyrus.hub.'+page
        if idx==0:
            name=DIALOG.input('Menu name',title(page)).strip()
            if name and len(name)<=60:
                widgets.set_string(key+'.label',name)
                if page.startswith('custom'):widgets.set_flag(key+'.enabled',True)
        elif idx==1:
            item=target()
            if item:
                widgets.set_string(key+'.path',item[0])
                if page.startswith('custom'):widgets.set_flag(key+'.enabled',True)
        elif idx==2:xbmc.executebuiltin('Skin.Reset('+key+'.path)')
        elif idx==3:edit_submenu(page)
        elif idx==4 and page in PAGES:
            widgets.set_string('orchard.page',page)
            if page.startswith('custom'):widgets.set_flag(key+'.enabled',True)
            xbmc.executebuiltin('ActivateWindow(1190)');return
        elif idx==5 and page in PAGES:
            widgets.set_string('orchard.page',page)
            selected=DIALOG.select('Continue Watching first',[widgets.effective(r,'title',page) for r in range(1,9)])
            if selected<0:continue
            # Stable move: all intervening rows retain their relative order.
            for row in range(selected+1,1,-1):widgets.swap_rows(row,row-1)
            widgets.reload_page();return
        elif page.startswith('custom'):
            widgets.set_flag(key+'.enabled',not widgets.flag(key+'.enabled'))
            if not hub_visible(page) and (HOME.getProperty('pyrus.hub')==page or widgets.current_page()==page):
                HOME.setProperty('pyrus.hub','home');widgets.set_string('orchard.page','home')
                HOME.setProperty('pyrus.nav.restore','9101')

def configure():
    while True:
        keys=list(NAV)
        idx=DIALOG.select('Top menu and submenus',[title(p)+('  · '+text('On' if widgets.flag('pyrus.hub.'+p+'.enabled') else 'Off') if p.startswith('custom') else '') for p in keys]+['Show / Hide Live TV','Back'])
        if idx<0 or idx==len(keys)+1:return
        if idx==len(keys):widgets.set_flag('pyrus.showlivetv',not widgets.flag('pyrus.showlivetv'))
        else:edit_hub(keys[idx])

def pvr_menu():
    options=['TV guide','TV channels','Recordings','Timers','Radio guide','Radio channels','PVR settings']
    destinations=['TVGuide','TVChannels','TVRecordings','TVTimers','RadioGuide','RadioChannels','PVRSettings']
    idx=DIALOG.select('Live TV and Radio',options)
    if idx>=0:xbmc.executebuiltin('ActivateWindow('+destinations[idx]+')')

def main():
    args=sys.argv[1:]
    if not args:return
    if args[0]=='restore':restore_focus()
    elif args[0]=='configure':configure()
    elif args[0]=='back':go_back()
    elif args[0]=='down' and len(args)==2:move_down(args[1])
    elif args[0]=='content' and len(args)==2:enter_content(args[1])
    elif args[0]=='subopen' and len(args)==2:open_submenu(int(args[1]))
    elif args[0]=='pvr':pvr_menu()
    elif args[0]=='preview' and len(args)==3:preview(args[1],int(args[2]))
    elif args[0]=='select' and len(args)==2:select_hub(args[1])
    elif args[0]=='submenu' and len(args)==2 and args[1] in NAV:submenu(args[1])

if __name__=='__main__':
    try:main()
    except (RuntimeError,ValueError,OSError,KeyError,TypeError) as exc:
        xbmc.log('Pyrus home menu: '+type(exc).__name__,xbmc.LOGERROR)
        DIALOG.ok('Pyrus Skin',str(exc) if isinstance(exc,ValueError) else 'Unable to open this source. Check that its add-on is enabled.')
