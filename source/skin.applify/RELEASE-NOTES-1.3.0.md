# Applify 1.3.0 — Player material and shelf position

This is an installable native Kodi skin update based on 1.2.9. It is a test release, with no claim of Apple-identical rendering or CoreELEC runtime certification.

Changes:
- Native player title uses a 48px semibold font, with a 24px series/episode line above it. Long titles use native static truncation rather than scrolling.
- Audio, subtitles, video settings and playback options are grouped above the timeline as 76px round controls. Static translucent PNG surfaces, subtle relief, focus shadows and short native fade/slide/zoom animations replace the previous small scattered controls.
- Timeline is 8px tall. Cache, progress and an accessible native seek slider remain functional. Pause/seek and the full OSD share title/timeline coordinates and keep mutually exclusive overlay conditions.
- A native modal Playback popover provides Audio, Subtitles, Video settings, Player Info and Stop. Back closes the popover. Existing native audio/video/subtitle settings dialogs and all diagnostic fields are preserved.
- Reduced Animation mode disables the new transitions. No Python background service, frame capture, real-time blur, repeated JSON-RPC or animated noise was added.
- First landscape shelf/rest position moves from y730 to y670 (60 design pixels) on Watch Now, Movies and TV Shows. Focused poster/later-row viewport stays y460 with height560. Row spacing, See All alignment and native scroll visibility are retained.
- Down on the last populated widget row stays on that row. The same boundary behavior applies to See All. Earlier rows retain their next populated row links. No settings migration is needed.

Installation:
1. Kodi Settings > Add-ons > Install from ZIP file > select this ZIP.
2. Keep Orchard selected; restart Kodi once after the update to load the new fonts, textures and custom dialog.
3. Existing widget sources and skin preferences remain in the user profile. The SSH patch is already included; running it separately is unnecessary.

Validation actually run for this release:
- Static validator: 125 XML files; dependencies, required windows, fonts/textures/includes/variables, control IDs and numeric focus links.
- 130 new resource/layout/focus checks, including native action routes, disabled seek/pause control reachability, menu Back and overlay exclusivity.
- 2,048 modeled Down transitions across all 256 populated/empty row combinations.
- 219 retained layout/material checks and 69,984 modeled steady-state shelf focus positions at the higher position.
- 115 shelf spacing/alignment checks, 98 flat add-on catalog/pagination checks, 46 mocked editor/search/provider/configuration tests.
- 1,159 local native FreeType/font filename checks including 24px and 48px player sizes. SF Pro bytes and license match 1.2.9.
- Offline XML/material preview inspected. This preview uses an analytic background and local font rendering; it is not a screenshot from Kodi.
- ZIP CRC and package structure checks.

Limitations / device checks still required:
- No Kodi executable or connected CoreELEC box was available for this update. Actual playback, target remote focus, modal open/Back history, animations, HDR/DV output and memory/frame rate need testing on the Xiaomi box.
- Apple real-time backdrop blur is not reproduced. The material is a native translucent PNG surface. The underlying native audio/subtitle/video settings dialogs retain their Kodi layouts.
- Player Info preserves the existing supported source/decoder/output information. This release does not infer actual FEL reconstruction or Atmos output from file labels.
- Historical Kodi 20.5 x86 software-GL cold-start instability with eight 300-item Python fixture widgets remains unresolved; this release makes no claim to fix it.
- A following unfocused shelf may be partly visible as a scroll affordance. The selected complete landscape/poster row is the subject of the geometry tests.

Compatibility: declared GUI API 5.17.0/Python3 dependencies remain unchanged for the Kodi21/22 skin architecture. No new mandatory helper dependency. Full Kodi21/22 runtime certification remains pending. User-supplied SF Pro files remain a private font test with their original license.
