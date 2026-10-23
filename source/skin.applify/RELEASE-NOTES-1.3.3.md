# Applify 1.3.3 — Direct Pause/Stop and flat translucent surfaces

Install this ZIP through Kodi Settings > Add-ons > Install from ZIP file, then restart Kodi. It updates the same skin ID; widgets, provider accounts and profile settings are retained. Full editable source is included. English UI, 1920×1080 native skin coordinates, Kodi 21/22 GUI architecture. This build has not been executed on the target CoreELEC box.

## Playback

- Pause/Play and Stop are separate, prominent 196×64 controls below the timeline, each with a 28px icon and readable text. Pause changes to Play when paused. Native actions are PlayerControl(Play) and PlayerControl(Stop). Stop is directly available without opening More.
- Pause is disabled when Kodi reports that the source cannot pause. Initial focus and directional fallback go to Stop in that case. Audio, subtitles, video settings, Info, Player Info, seek and Back remain native.
- Padded seek-dot textures and native Player.Chapters ranges from 1.3.2 are unchanged. Markers appear only when the source exposes chapters to Kodi. No guessed HDR/DV/FEL/Atmos status is added; technical Player Info retains its existing Kodi data.

## Global banding correction and settings

- Shared panel, button, focus, row and navigation faces now use constant RGBA interiors, with antialiased rounded edges. A flat PNG background replaces the bundled JPEG/ambient gradient. Narrow inherited overlay/keyboard fades now use a uniform translucent scrim. This removes the decorative gradient responsible for stripes on these surfaces.
- Found and corrected a genuine 1.3.2 dithering error: the stored blue-noise rank tile was already normalized to 0..1, but was divided by 4096 again. Its variation was practically eliminated. Native-width cinematic PNG fades now use the correctly normalized noise in alpha and RGB; endpoint transparency is preserved. This release supersedes the earlier material/dithering assertions.
- Large shared panel asset shrinks from 1920×1080 RGBA to a nine-sliced 128×128 RGBA resource: approximately 7.9 MiB to 64 KiB of raw texture data for this asset. This is an asset calculation, not a device-memory measurement. No new background service, refresh loop or runtime noise generation.
- Settings uses one left native grouplist. CoreELEC Settings appears there when installed/enabled. Duplicate right-hand Return to Home is removed; Watch Now remains in the left menu. Existing actions remain intact. The menu fits its viewport with or without CoreELEC Settings.

## Validation actually performed for 1.3.3

- Static validator: 125 XML documents; includes, font and texture references, custom control IDs, focus links, widget/page conditions and dependency/package structure.
- 1,495 focused static/pixel/font/focus-model checks: uniform face/composite statistics, effective noise variation and clear/opaque endpoints, optional CoreELEC menu navigation, retained actions, native Pause/Stop, label fit, safe geometry and unchanged chapter/seek resources.
- Retained regressions rerun: 115 shelf-spacing/native-control checks; 98 installed-add-on catalog/pagination/focus checks; 46 mocked editor/provider tests; 1,159 filename/native FreeType glyph checks. SF Pro/font-license bytes compared with 1.3.2.
- Offline material/layout rendering of Settings and the playback controls inspected. This is a controlled renderer, not a Kodi screenshot. ZIP CRC, single top-level add-on directory, version and manifest checked after packaging.

## Still requires real hardware

Kodi/CoreELEC runtime, physical remote behavior, actual playback/pause/stop and chapter media, HDR/DV compositing, real-output banding, GPU frame time, memory, restart behavior and long-running stability. No SSH access or current target runtime was available here. Flat UI faces cannot remove banding already present in source artwork/video, display processing or the output pipeline. No claim of pixel-identical Apple blur/refraction or universal crash-free performance.

The earlier unresolved Kodi 20.5 software-GL stress-fixture cold-start limitation remains historical and unresolved. Older test records retain their original scope, not current runtime certification. Third-party add-ons with self-drawn windows may retain their own styling. Existing SF Pro user-supplied/private-test license scope remains unchanged.

## Reproducing current checks

From the source directory:

    python3 development/validate_skin.py .
    python3 development/test_flat133.py . /path/to/extracted-1.3.2/skin.applify
    python3 development/test_shelves129.py .
    python3 development/test_addons129.py .
    ORCHARD_TEST_ROOT=. python3 development/test_editor129.py
    python3 development/test_player_fonts130.py .

The flat133 regression uses the previous 1.3.2 source for action/asset byte comparisons; supply its directory as the second argument. Pillow/numpy and system FreeType are development-only requirements. Kodi does not execute the test renderer or texture builder.
