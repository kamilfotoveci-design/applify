# Current release:1.3.5

See RELEASE-NOTES-1.3.5.md for the fixed player labels, adjacent larger Pause/Stop, matte grey dialogs, Home preservation and actual testing scope. Older notes below retain their historical scope; prior player text-fit assertions are superseded.

# Current release:1.3.4

See RELEASE-NOTES-1.3.4.md for the button-spacing audit, corrections and actual test limits. Earlier entries below retain their original scope.

# Current release 1.3.3

See RELEASE-NOTES-1.3.3.md and development/flat-ui-tests-1.3.3.json. Current changes/tests supersede the historical notes below. Target-box runtime remains unverified.

# Current release:1.3.2

See RELEASE-NOTES-1.3.2.md for current implementation, validation and limits. Earlier sections record prior builds.

# Current release:1.3.1

See RELEASE-NOTES-1.3.1.md for the complete-poster change and current testing scope. This release includes all1.3.0 player changes.

# Current update: 1.3.0

See RELEASE-NOTES-1.3.0.md for current changes, installation, validation and limits. Earlier sections below describe historical releases; their runtime results do not certify this build.

# Feature checklist — 1.2.9

1.2.9: increased heading/card spacing; circular native See All; flat installed-add-on grid with deduplication, twelve-item paging and Refresh. Current verification is static/mocked/model/font-only; live launch/history and target rendering remain unverified. No category tabs.

Current 1.2.8: static overview text, compact caption-optional cards, low first-landscape/raised poster stages and focus-only tab elevation are implemented. Current checks are static/model/native FreeType and mocked menus; any native Kodi results in this table refer to earlier versioned runs in TEST-RESULTS.md. No current CoreELEC runtime certification is claimed.

| Feature | Status / validation |
| --- | --- |
| Watch Now / Movies / TV Shows widget pages | Eight independent rows per page; native tab switching tested |
| Source / Trakt picker | Installed add-ons, favourites, libraries and XSP; live accounts require box testing |
| Rename, limits, artwork, order, visibility, remove/reset | Stateful editor regressions passed |
| Copy between pages | Implemented and regression tested |
| Backup / restore | Native export and complete JSON schema verified; import logic regression tested |
| Settings persistence | Three sources, selected page and appearance state survived actual Kodi restart |
| Appearance / playback settings | Real persistent settings with XML behavior; native appearance menu tested |
| Exclusive playback overlays | Pause/OSD, audio/subtitle and Player Info runtime checks passed |
| Player Info / native debug | Real decoder/audio values, Media/Output/System tabs and debug captures checked |
| HDR / DV / FEL source detail, Atmos codec | Native report fields; physical extended formats still require CoreELEC testing |
| Active output EOTF / display mode / pixel format | Native CoreELEC labels verified from official source; target output unverified |
| Movies / shows / playback / search / system dialogs | Existing native interfaces retained; local library remains accessible from Settings |
| Low-memory preset | Six-item caps and reduced animation; software-rendered x86 audit only |
| Unified navigation / settings / player | Shared six-tab capsule, vertical settings rail and compact OSD; see VISUAL-AUDIT.md |
| Xiaomi/CoreELEC hardware performance | Not yet verified on the target device |

Sources, licenses, tests and remaining limits are included. No Apple logos or reference artwork is bundled. User-supplied SF Pro fonts retain their proprietary license; general redistribution rights are not granted.

1.2.1 adds a runnable Add-ons selector, POV/TMDb title-search routes, More/source pagination access, removed-slot labels and POV artwork/date preferences. Live provider playback and physical image sharpness remain unverified; see README.md and TEST-RESULTS.md.

1.2.2 adds native per-directory List/Landscape/Poster views, direct card-only hero actions, short native transitions and artwork-cache diagnostics/POV metadata refresh. Hardware sharpness and ARM frame pacing remain unverified.

| Native PNG / blue-noise custom UI gradients | Asset/composite checks passed; physical CoreELEC output unverified. See BANDING-FIX.md |

1.2.5: content-width navigation, Inter-derived licensed static typography, inactive focus clearing, raised shelves, scrolling/full synopsis and centered context-menu bounds. Optional keyboard completion remains dependent on its installed provider and target-box runtime verification.
