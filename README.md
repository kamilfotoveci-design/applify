<p align="center"><img src="icon.png" alt="Pyrus Skin pear icon" width="120"></p>

# Pyrus Skin

**An Apple TV-inspired Kodi skin by kamilwhoo.** Cinematic artwork, configurable widgets and detailed Player Info, with a clean interface designed for the TV.

**Current version: 1.0.1 · Tested by the maintainer on Kodi 22.**

Previously named **Applify**. Existing installations receive Pyrus Skin through the same repository and keep their skin settings.

## Features

- **Your own home screen:** separate Watch Now, Movies and TV Shows widget collections, configurable sources, artwork and row order.
- **Cinematic presentation:** artwork-led browsing, search and readable typography.
- **Clean controls:** circular playback focus, larger switches, consistent dark settings, dialogs and information actions.
- **Detailed Player Info:** Media, Decoder / Output and System tabs show the data available from Kodi, including video/audio codecs, dimensions, frame rate, stream/live bitrates, audio channels and sample rate, decoder information and available HDR / Dolby Vision details.
- **Repository updates:** install once, then receive future versions through Kodi's add-on manager.
- **Personalization:** appearance and playback options, reduced animations and widget backup/import.

Player Info availability depends on the Kodi build, device, playback path and media. A source Dolby Vision profile describes the file; it does not by itself confirm the active output mode.

## Install in Kodi

1. Open **Settings → File manager → Add source**.
2. Enter this source URL:

   ```text
   https://kamilfotoveci-design.github.io/applify/
   ```

3. Name the source **Pyrus**.
4. Open **Add-ons → Install from ZIP file → Pyrus**. Enable **Unknown sources** if Kodi prompts you.
5. Select **repository.applify-1.0.1.zip**.
6. Open **Install from repository → Pyrus Repository → Look and feel → Skin → Pyrus Skin**.
7. Install and confirm the skin switch.

The source URL and ZIP identifiers retain the old Applify name so existing installations can update. The displayed skin name is **Pyrus Skin**, by **kamilwhoo**.

## Already using Applify?

Keep your existing source and repository. Check for add-on updates, install the available repository / skin update and restart Kodi if the old interface remains cached. Keep automatic updates enabled if you want future versions automatically.

## Compatibility and feedback

The maintainer has tested the skin on **Kodi 22**. This is a community project; other versions and hardware combinations are not covered by that test.

For feedback, [open an issue](https://github.com/kamilfotoveci-design/applify/issues) with your Kodi version/build, device, a screenshot and reproduction steps. For Player Info issues, include the affected format and whether you use passthrough.

## Screenshots

Real captures supplied by the maintainer. These show the existing home interface; the new 1.0.1 dialog refresh is described in the release notes.

![Watch Now — Next Episodes](screenshots/01-watch-now-silo.jpg)

![Home widgets — Next Episodes](screenshots/02-next-episodes.jpg)

![Latest TV Shows](screenshots/03-tv-shows.jpg)

![Trending — poster widgets](screenshots/04-trending.jpg)

## Release notes

See [1.0.1 release notes](RELEASE-v1.0.1.md).

## Credits and licenses

Pyrus Skin is maintained by **kamilwhoo** and builds on work by the Estuary contributors. Original notices and licenses are retained inside the skin package. Font files have their own licenses; see `fonts/` in the package, including the SF Pro license. This repository does not change those terms.

Independent project. Not affiliated with Apple or Team Kodi.
