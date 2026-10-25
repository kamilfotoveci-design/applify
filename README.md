# Pyrus Skin

**An Apple TV-inspired Kodi skin by kamilwhoo.**

Cinematic artwork, configurable widgets, clean playback controls and detailed Player Info.

## What's new in 1.1.5

- Fixed the Add-on error when opening a widget row in Configure Widgets.
- Corrected the Python name collision still present in the published 1.1.4 ZIP.
- Regression tests exercise the installable ZIP across all 48 page/row menus and key editor operations.
- The repository builder rejects this helper-shadowing error before publishing.
- Existing widgets and settings are preserved. Device confirmation on Kodi 21/22 is still needed.

The 1.1.4 navigation behavior is retained: Left/Right moves focus on the top bar;
OK selects the tab. Pressing OK on the already active tab does not open a library.

The 1.1.3 update also added:

- Added a Power icon beside Settings. It opens Kodi Power Options, including Reboot when Kodi reports that the device supports it.
- Press Right from a widget row's See All control to return to its first card. See All remains reachable from the last card.
- Kept the top navigation centered with the same focus and motion styling.

The 1.1.2 update also added:

- Corrected ranked card numbers in custom hubs.
- Removed older packages that still contained non-English skin catalogs.
- The installable skin now includes only the English language catalog.

The 1.1.1 update also added:

- Three optional custom hubs with eight widget rows each; up to six inline submenu links per hub.
- Native Live TV/Radio destinations: guide, channels, recordings and timers.
- English interface labels, episode titles and ratings supplied by your content add-on.
- Page geometry changes without a full skin reload; hidden tabs cannot capture restored focus.
- Full menu/widget backups and on-demand repository diagnostics.
- Capability-gated Reboot to Android on CoreELEC.
- Existing Player Process Info (PPI): **Media**, **Decoder / Output**, **System**.

Configure the menu in **Kodi Settings → Skin Settings → Top menu and submenus**.
The Settings gear continues to open Kodi Settings directly. Power opens Kodi Power Options. Existing widget settings are retained.

## Install

1. Enable Unknown sources in Kodi Settings → System → Add-ons.
2. File manager → Add source: **https://kamilfotoveci-design.github.io/applify/**
3. Name the source Pyrus.
4. Add-ons → Install from ZIP file → Pyrus → **repository.applify-1.0.2.zip**.
5. Install from repository → **Pyrus Repository → Look and feel → Skin → Pyrus Skin**.

The repository provides updates. The technical IDs `skin.applify` and `repository.applify`
remain unchanged to preserve existing installations.

If the repository cannot connect, restart Kodi once and use **Check for updates**.
One Fire Cube 3 user reported this resolved installation. If it still fails,
report your device, exact Kodi build and a Kodi log captured after the failure.
A permanent root cause for all reported connection failures has not been established.
You can install [the skin ZIP directly](https://kamilfotoveci-design.github.io/applify/skin.applify/skin.applify-1.1.5.zip) after this version is deployed.

## Compatibility and validation

The maintainer has tested earlier versions of the skin on Kodi 22. The 1.1.5 package
passed offline editor regression and static build checks; **device validation of this update is still required**.
Kodi 21/22 builds and hardware can expose different Player Info fields. Missing
HDR, Dolby Vision or decoder details are not proof that a format is unsupported.
PVR requires your own enabled PVR client and backend. The skin does not supply channels.
Ratings depend on the values returned by the selected item's add-on; no API key is bundled.

Pyrus ships only the English skin language catalog. Kodi's own interface and
content titles follow the language and metadata settings in your Kodi installation.
Your custom widget titles are preserved.

See [1.1.5 release notes](RELEASE-1.1.5.txt).

## Screenshots

![Home](screenshots/IMG_4127.png)
![Widgets](screenshots/IMG_4129.png)
![TV Shows](screenshots/IMG_4130.png)
![Collections](screenshots/IMG_4132.png)
![Preview](screenshots/IMG_4135.png)

## Credits and integrity

Pyrus Skin is maintained by **kamilwhoo** and builds on work by the **Estuary contributors**.
Original notices, component licenses and font terms remain inside the package.
This repository does not override those terms. SHA-256 checks detect unexpected
changes against a trusted reference; they are not a digital signature or copy protection.

Independent community project. Not affiliated with Apple or Team Kodi.

## Diagnostics and device reports

Skin Settings → Backup / Refresh / Reset → Repository and playback diagnostics.
The report is saved in `userdata/addon_data/skin.applify/diagnostics.json`.
It checks the index and its hashes over normal verified HTTPS and records selected
Kodi output labels. It does not collect account credentials or media URLs.
Use Check for repository updates to request Kodi's native refresh.

TV-led Dolby Vision/zero-L5 black video and complete p3i T4c compatibility remain
unverified device reports. Compare the same file/settings against Estuary and include
fresh logs. This update does not force HDR/DV options. PVR requires a configured backend.
Full arbitrary menu ordering and unlimited tabs are not provided: the current editor
supports three extra hubs and six child links per hub. The skin is distributed
as an installable Kodi ZIP.
