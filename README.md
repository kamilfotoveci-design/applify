# Applify

**Applify v1.0.0** — an Apple TV-inspired Kodi skin with cinematic artwork,
configurable widgets, SF Pro typography and clean playback controls.

This project also provides an HTTP source for Kodi: add the GitHub Pages URL
in File manager, install **Applify Repository**, then install **Applify**.

## Install in Kodi

1. Open the published GitHub Pages URL shown under **Settings → Pages**.
2. In Kodi, open **Settings → File manager → Add source** and enter that URL.
   Name the source **Applify**.
3. Enable **Settings → System → Add-ons → Unknown sources** if needed.
4. Open **Add-ons → Install from ZIP file → Applify** and select
   `repository.applify-1.0.0.zip`.
5. Open **Install from repository → Applify Repository → Look and feel → Skin → Applify**.
6. Select **Install**, accept the skin switch, then set the skin font to **Default**.

New versions are delivered through Applify Repository according to your Kodi
add-on update settings. Font files are bundled inside the skin ZIP.

## Features

- Cinematic home screens with configurable library and add-on widgets.
- Movie/TV information, search and clean playback controls.
- Bundled SF Pro Display Regular/Semibold and fallback fontsets.
- Dedicated `skin.applify` identity; installs beside the older Orchard skin.

Targets Kodi 21. Kodi 22 compatibility and full CoreELEC runtime have not been
tested in this build environment. Independent project, not affiliated with Apple.
Upstream code and font licenses remain inside the skin package.

## Publish your own source

See **GITHUB-POSTUP-SK.md** for the complete Slovak guide.

Upload `skin.applify-1.0.0.zip`, `build_repository.py`, this README and
`publish.yml` to the repository root. Set **Settings → Pages → Source → GitHub Actions**.
Move `publish.yml` to `.github/workflows/publish.yml` using GitHub's file editor.
The included workflow then builds and deploys the source using the actual Pages
URL; no username or URL substitutions are needed in the repository manifest.

For updates, upload a new `skin.applify-X.Y.Z.zip` whose `addon.xml` version
matches the filename. The builder selects the highest numerical stable version.
