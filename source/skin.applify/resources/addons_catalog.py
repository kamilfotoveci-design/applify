"""On-demand deduplicated installed add-on catalog for a native skin window.

No service or Python GUI loop. The script exits after filling twelve native
slots. Kodi owns focus, icon loading, launch actions and return navigation.
"""
import json, math, re
import xbmcgui

PREFIX='orchard.addons.'
PAGE_SIZE=12
KINDS=('video','audio','image','executable')
def collect(rpc):
    found={}
    for kind in KINDS:
        for addon in rpc('Addons.GetAddons',{'type':'xbmc.addon.'+kind,'enabled':True,'properties':['name','thumbnail']}).get('addons',[]):
            addonid=addon.get('addonid','')
            if not re.fullmatch(r'[A-Za-z0-9_.-]+',addonid):
                continue
            entry={'id':addonid,'name':addon.get('name') or addonid,'icon':addon.get('thumbnail') or 'DefaultAddon.png'}
            if addonid not in found or found[addonid]['icon']=='DefaultAddon.png':found[addonid]=entry
    return sorted(found.values(),key=lambda a:(a['name'].casefold(),a['id']))

def apply_page(window,catalog,page):
    total=len(catalog);pages=max(1,math.ceil(total/PAGE_SIZE));page=max(0,min(int(page),pages-1))
    batch=catalog[page*PAGE_SIZE:(page+1)*PAGE_SIZE]
    for index in range(PAGE_SIZE):
        data=batch[index] if index<len(batch) else {'id':'','name':'','icon':''}
        for key,value in data.items():window.setProperty(PREFIX+'slot%d.'%(index+1)+key,value)
    for key,value in {'count':total,'visiblecount':len(batch),'page':page,'pages':pages,'hasnext':int(page+1<pages),'page_label':'%d of %d'%(page+1,pages)}.items():
        window.setProperty(PREFIX+key,str(value))

def refresh(rpc,reset=False):
    # Resolve the entire catalog before mutating visible state, so errors leave
    # a previously loaded catalog intact rather than a half-filled page.
    catalog=collect(rpc);window=xbmcgui.Window(10000)
    page=0 if reset else int(window.getProperty(PREFIX+'page') or 0)
    window.setProperty(PREFIX+'catalog',json.dumps(catalog,ensure_ascii=False))
    apply_page(window,catalog,page)

def move(delta):
    window=xbmcgui.Window(10000)
    raw=window.getProperty(PREFIX+'catalog')
    catalog=json.loads(raw) if raw else []
    apply_page(window,catalog,int(window.getProperty(PREFIX+'page') or 0)+int(delta))
