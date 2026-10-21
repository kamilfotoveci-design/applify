# Pyrus Skin 1.0.1 — validation report

- Parsed all 125 skin XML files and both Python scripts.
- Compared native control IDs and click actions across all 110 window/include XML files against installed 1.0.0: none removed or changed. Added the native edit template to category settings.
- Updated common material references in 59 files; shared components carry the changes into other dialogs.
- Resolved new texture references and validated all three font sets. All seven font binaries are unchanged and load through FreeType. Both primary faces contain Slovak glyphs.
- Checked circular action alignment at every declared width; eight information actions fit the 1920×1080 layout.
- Confirmed the supplied icon is byte-for-byte unchanged in the skin package.
- Built the repository locally and fetched all metadata, ZIP, icon and screenshot paths over HTTP. Index and archive MD5 values match.
- Verified all four supplied screenshots publish and remain byte-for-byte unchanged. Also tested support for a future additional screenshot using an isolated fixture.
- Inspected layout proofs generated from current XML positions, fonts and assets. These are not Kodi screenshots.

The maintainer confirms testing the skin on Kodi 22. There is no Kodi runtime in this build environment. The new 1.0.1 visual changes require an on-device pass before public announcement. The GitHub repository has not been written or deployed by this local build.
