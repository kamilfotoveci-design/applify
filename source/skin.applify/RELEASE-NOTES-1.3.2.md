# Applify1.3.2 — Seek alignment, chapters and glass surfaces

Install through Kodi Settings > Add-ons > Install from ZIP file, then restart Kodi. Existing sources/preferences remain in the profile. This package includes1.3.1 complete poster shelves, higher landscape shelves and terminal Down fixes.

Player corrections:
- Fixes the seek dot11px above the bar in1.3.1. The horizontal Kodi slider pins its nib Y to the slider background Y. New14×36 and22×36 transparent PNG canvases center the visible normal/focused dot at y920, matching the y916/h8 track. Checked against source for the exact CoreELEC revision supplied by the user.
- Real native Player.Chapters ranges on both full OSD and pause/seek overlay. Chapter endpoints use contrasting ticks on the same axis as the track. No equal-spacing approximation, provider guesses, JSON-RPC polling or Python service. A source without Kodi-exposed chapter data has no markers.
- Bare white action glyphs32px, with a64px translucent visual focus circle inside a76px remote hit area. The large central skip/play/stop row is removed; pause is a small control next to elapsed time. Seek left/right remains native, and Stop is available through More > Stop playback. Audio, subtitles, video settings, Info and Player Info are preserved.

Shared glass style:
-297 texture references across60 XML consumers, plus shared native includes, adopt consistent transparent plates, fine edges, muted rows and lighter focus surfaces. Main areas include Home navigation, movie/show/file browsing, installed add-ons, details/actions, settings, home editor, native settings/select/keyboard/context dialogs and Player Info. Existing screen layouts and functional controls are retained.
- The large shared plate uses a native1920×1080 PNG with deterministic blue-noise dithering. One decoded shared RGBA plate is approximately7.9MiB; this is an asset-size estimate, not measured device GPU memory. Small button surfaces are nine-sliced. Existing anti-banding cinematic overlays remain.
- Native material surfaces do not reproduce Apple's live background blur/refraction. Third-party Python add-ons with their own windows and hardcoded styling are outside the skin's control. No claim of a complete1:1 Apple UI clone or universal hardware smoothness.

Validation for this release:
- Static XML/package/reference validator:125 XML documents.
-170 native-source/resource/action-preservation/focus/chapter/material checks, including6,006 modeled slider positions across normal, focused and disabled states at1080p/4K scaling. The regression explicitly detects the old11px offset.
- Existing native actions, links, enable conditions and content in the other window/include XML files are compared with1.3.1; formatting whitespace is ignored. Player OSD action changes have their own focus-graph tests including disabled seek/pause controls.
- Unchanged font files and SF Pro license bytes verified against the previous package.
- Retained layout/model regressions rerun for shelves and add-ons; test results below are independent of Kodi execution.
- Offline XML/material player preview inspected. This is not a Kodi screenshot or a physical-box capture.

Target CoreELEC GUI playback, real chapter media, popover/Back history, input, memory and frame rate still require the user's box. No Kodi runtime was available in this environment. Historical intermittent Kodi20.5 software-GL cold-start fixture instability remains unresolved. Original SF Pro license/private-test scope and Kodi21/22 architecture compatibility notes remain in the earlier release documentation.
