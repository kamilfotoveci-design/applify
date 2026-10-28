"""Refresh retained native directories without changing their URLs or clearing cards.

Kodi DirectoryProvider::UpdateSort schedules an asynchronous directory job when
sortorder changes. With sortby=none, provider order is unchanged. Existing items
remain present until the job completes. The source add-on still owns its cache.
"""
import time
import uuid
import xbmc
import xbmcgui

PAGES = ('home', 'movies', 'tv', 'custom1', 'custom2', 'custom3')
INTERVAL = 60.0
COOLDOWN = 15.0
OWNER = 'pyrus.refresh.owner'


class RefreshState:
    def __init__(self):
        self.last = {}
        self.dirty = set()
        self.away = False
        self.page = None
        self.since = 0.0

    def tick(self, now, page, visited, ready, busy=False, manual=False):
        for p in visited:
            self.last.setdefault(p, now)
        if not ready:
            self.away = True
            self.page = None
            return None
        if self.away:
            self.dirty.update(visited)
            self.away = False
        if page != self.page:
            self.page, self.since = page, now
        if manual:
            self.dirty.update(visited)
        if page not in visited or busy:
            return None
        age = now - self.last[page]
        # Wait only before background refresh, never before displaying the hub.
        if not manual and (now-self.since < 1.0 or age < COOLDOWN):
            return None
        if manual or page in self.dirty or age >= INTERVAL:
            self.last[page] = now
            self.dirty.discard(page)
            return page
        return None


def run():
    home = xbmcgui.Window(10000)
    token = uuid.uuid4().hex
    home.setProperty(OWNER, token)
    monitor = xbmc.Monitor()
    state = RefreshState()
    try:
        while not monitor.abortRequested() and home.getProperty(OWNER) == token:
            if xbmc.getSkinDir() != 'skin.applify':
                break
            page = home.getProperty('pyrus.hub')
            visited = {p for p in PAGES if home.getProperty('pyrus.visited.'+p)}
            ready = xbmc.getCondVisibility('Window.IsActive(Home) + !System.HasActiveModalDialog + !Player.HasMedia')
            offset = PAGES.index(page)*10000 if page in PAGES else 0
            busy = any(xbmc.getCondVisibility('Container(%d).IsUpdating' % (offset+5100+r)) for r in range(1,9)) if page in PAGES else False
            manual = bool(home.getProperty('pyrus.refresh.request'))
            if manual and ready and not busy and page in visited:
                home.clearProperty('pyrus.refresh.request')
            refresh = state.tick(time.monotonic(), page, visited, ready, busy, manual)
            if refresh:
                key = 'pyrus.refresh.order.'+refresh
                home.setProperty(key, 'descending' if home.getProperty(key) != 'descending' else 'ascending')
            if monitor.waitForAbort(0.5):
                break
    finally:
        if home.getProperty(OWNER) == token:
            home.clearProperty(OWNER)


if __name__ == '__main__':
    run()
