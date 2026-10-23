# Applify 1.3.6 — Home widget setup / internal test build

This is an installable native Kodi skin, with editable XML/Python source and all default fonts in this ZIP. It is an internal test release; the static and mocked checks below do not certify every Kodi window or device.

## Quick setup from Home

Open the gear in the top navigation. Choose **Add widget**, **Customize this page**, or **Kodi settings**.

Add widget asks for the content source, widget name and artwork style. It uses the first free or removed slot on the current Watch Now, Movies or TV Shows page. Up to eight rows per page are available. The wizard saves all four row settings together after the last prompt; cancelling a prompt leaves the row untouched. A successful add refreshes the skin once so poster geometry is rebuilt. The empty-home Configure Widgets button opens the same wizard directly.

Sources include the Kodi library, smart playlists, Kodi Favourites and directories exposed by enabled installed video add-ons. For POV/Umbrella/Trakt: enter that installed add-on, browse its real folders to the desired watchlist/collection/list and choose **Use This List**. Alternatively favourite a complete add-on list first and select it under Kodi Favourites. The skin does not invent provider routes or credentials. Configure accounts in the provider. A source without any returned content remains empty.

Customize this page opens the full existing row editor: choose/change sources, rename, change artwork/item limit, move, hide, remove, restore or copy rows. Apply changes when finished. Settings are stored through Kodi's native skin settings; restart persistence still needs a target-device check. A full page offers the editor rather than overwriting an existing row.

## Audit fixes and preserved appearance

- List and Poster video views no longer intercept Back to focus the top bar. Kodi handles parent/back navigation consistently with Landscape.
- The editor's Add-ons shortcut now uses the same flat installed-add-on hub as Home.
- Sorting, Play, Resume and Trailer SendClick IDs were checked against the specified CoreELEC source revision. These are native Kodi hooks, not unimplemented decorative controls.
- The Home layout, colors, artwork, animations and widget geometry are unchanged. Only the gear and empty-state actions changed.
- Player controls, adjacent Pause/Stop, fixed non-scrolling labels, chapter/seek geometry and neutral matte materials are byte-identical to delivered 1.3.5. No new glossy surfaces or gradients were introduced.
- SF Pro Regular and Semibold are bundled and used by the first/default Font.xml fontset. New installs require no separate font installation. Existing user font preferences are respected; choose Default under Kodi Interface > Skin > Fonts if a different fontset was previously selected. Font filenames keep the .ttf suffix accepted by Kodi's font manager; the actual outlines are unchanged.
- No service, polling loop or new dependency was added. Quick setup runs only on explicit selection. Provider directory loading speed still depends on the provider.

## Installation

Copy the ZIP to your CoreELEC storage or accessible network share. In Kodi open Settings > Add-ons > Install from ZIP file and select it. Enable unknown sources if Kodi asks. Select Applify under Interface > Skin if needed, then restart Kodi. Installing over the same skin ID retains existing skin settings; no manual uninstall is required.

The package retains xbmc.gui 5.17.0 and Python 3.0.0 requirements. It targets Kodi 21 Omega / Kodi 22 Piers skin APIs; source hook checks used CoreELEC revision cfc215086edfe8b96de48530c5cdff1d2d78e92a. Actual installation and behavior of this build on either release require runtime testing. Optional providers and AutoCompletion are not bundled.

## Checks actually executed for 1.3.6

| Check | Result and scope |
| --- | --- |
| XML/package structure, includes, textures, font references, custom focus IDs and provider wiring | Passed across 125 XML files; static |
| Quick setup | 13 unittest methods passed, with subcases for all three pages, cancellation, full slots, missing/failing provider, removed-slot reuse and exact preservation; mocked |
| Existing editor/search/provider regressions | 46 unittest methods passed; mocked |
| Native font filename gate and FreeType glyph loading | 1,159 checks passed locally |
| Shelf spacing | 115 model/static checks passed |
| Flat add-on catalog, paging and focus/actions | 98 mocked/static checks passed |
| Poster layouts | 459,270 predicates and 52,488 complete-poster positions passed in the offline model |
| Native hooks | Five sorting/playback/info hooks matched the CoreELEC C++ control IDs; static |
| Fonts, player, artwork/material assets, variables and Home | Actual byte comparisons against delivered 1.3.5 passed, allowing only the two new Home actions |
| ZIP | Full archive CRC, safe single root, manifest and source-byte checks performed during packaging |

The broad button inventory covered 85 windows / 822 interactive candidates. Its conservative expansion reports 538 potential overlaps, 345 potential offscreen cases and three unresolved dynamic positions; these include conditional alternatives and scrollable controls and have not all been classified at runtime. It is an inventory, not evidence that every screen has no overlap. The inherited provider-dependent MyWeather negative gap was retained. Detailed results are in development/audit-results-1.3.6.json; earlier release reports retain their original scope.

## Remaining hardware checks / limits

Kodi was not run in this environment. Before sharing more widely, verify a fresh install and upgrade; the Home gear on all three pages; source selection/cancellation; poster/landscape rows; remove/reorder and restart persistence; real POV/Umbrella lists and search; play/resume/seek/chapters/stop/audio/subtitles; information/context/settings dialogs; and remote Back through add-on folders. Measure memory, frame pacing and playback on the actual ARM box.

The earlier Playback failed message still needs a Kodi log to identify the cause. A screenshot cannot establish whether it came from skin activation, the provider, URL resolution or the player. Artwork sharpness depends on the original image and Kodi cache; this build does not manufacture 4K details. Dolby Vision Level 5 / FEL, HDR or Atmos reporting depends on the player/platform exposing that information; skin code cannot guarantee compositor visibility or infer unsupported output modes. Dithered textures reduce skin-gradient banding but cannot guarantee the TV/output chain will never band.

Do not interpret these checks as a bug-free guarantee or a completed Apple 1:1 visual audit.
