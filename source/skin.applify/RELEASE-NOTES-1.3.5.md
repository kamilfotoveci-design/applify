# Applify 1.3.5 — Fixed player labels, larger controls and matte grey dialogs

Install through Kodi Settings > Add-ons > Install from ZIP file, then restart Kodi. This updates the same skin ID and retains profile settings/widgets/providers. Source and development checks are included. Kodi21/22 architecture,1920×1080 skin coordinates; current target-box execution remains unavailable.

## Final user-directed scope

Home is preserved from1.3.4: Home.xml and Orchard_Variables.xml are byte-identical, and all original Orchard UI texture bytes are retained under their original names. Font assets and all provider/helper code are unchanged. The player-specific font entry alone grows from24px to26px; Home uses its existing font entries. Neutral matte variants are scoped under media/orchard/matte135 and referenced by other windows. No Home shelf position, navigation, artwork or animation change is introduced here.

The playback UI returns toward the earlier simple layout: native seek-back icon, Pause/Play, Stop and seek-forward icon form one centered cluster. Pause and Stop have matching196×72px hit areas and16px separation. Arrows have88×72px hit areas and40px icons. Top audio/subtitle/video/More actions grow from76px to88px hit areas with40px icons; the player text is26px. Info and Player Info now have icons, and Player Info has extra label room. Focus/Back and unavailable-pause/seek fallbacks remain native and are modeled in tests. Seek-back/forward use Kodi StepBack/StepForward with the user's configured Kodi skip behavior; they do not invent seek intervals.

## Pause text root cause and correction

The previous width check was wrong. CoreELEC GUIButtonControl enables scrolling whenever a button has focus. CGUILabel's usable text width is width minus TWO horizontal insets. The196px button with72px inset therefore provided only52px for Pause. This explains the moving/cut first letter in the supplied photograph, and supersedes the earlier text-fit claim.

Native actionable button labels are retained with transparent text for Kodi semantics; their visible names use separate native label controls with fixed bounds, zero text inset and explicit scroll=false. Pause/Play, Stop, Info and Player Info each have enabled/focused/disabled visible states and real image icons. The visible Pause/Play label changes with Player.Paused and does not become a scrolling button label. Font tests cover SF Pro and Inter at1080p and4K scaling.

Source reference: CoreELEC/xbmc revision cfc215086edfe8b96de48530c5cdff1d2d78e92a, xbmc/guilib/GUIButtonControl.cpp, GUILabel.cpp, GUILabelControl.cpp and GUIControlFactory.cpp. URLs and source hashes are recorded in development/native-button-source-1.3.5.json. The build is informed by actual source inspection; this is not target-box runtime verification.

## Matte grey materials and modal correction

Non-Home panel/button/navigation variants use neutral grey RGB. Main dialog plates are opaque charcoal; button faces have constant fills and no shiny rim. Raised navigation shadows are removed for those variants. Named style palettes and cool-grey literal tints outside Home are neutralized; semantic error red remains. These are flat native textures, not live blur or refraction. Original coloured video/artwork/add-on logos are not recoloured.

Remaining native-width cinematic fade variants retain EXACT alpha/dither fields from1.3.4 and use neutral RGB. No JPEG conversion or new fullscreen noise layer/service is added. Flat faces have no decorative gradient to band. Home retains its existing corrected dithering and original artwork/materials as requested. This cannot remove banding in a source video, artwork, display processing or the output pipeline.

DialogConfirm, used for messages including Playback failed, now has matching430px group/plate height, a real footer and72px actions ending34px above the plate bottom. One, two and three visible buttons all fit inside the plate. Native dialog/action IDs remain intact.

The screenshot's Playback failed message is not enough to diagnose its media failure. Home widgets still use native target=videos activation; this release does not change resolver/provider/account/network code or claim that this playback failure is fixed. A Kodi log from the actual failure is required to locate that cause.

## Tests actually run

-125 XML files pass structural/reference/dependency/custom-ID/focus validation.
-824 current checks pass: reproduces the old symmetric-inset overflow; measures all visible labels in both fontsets; checks native action/state preservation, fixed label settings, icons, neutral palette/assets, unchanged dither alpha, modal1/2/3-button containment, Home preservation and remote reachability with pause and seek independently enabled/disabled.
- Conservative expanded geometry audit reports no modeled OSD or confirmation-button overlap/screen overflow after excluding invisible modal event shields. The two arrow buttons are included.
-115 retained shelf checks,98 installed-add-on catalog/focus checks,46 mocked editor/provider tests and1,159 native FreeType/filename-gate checks pass.
- Offline player/settings material preview inspected. It is a QA renderer, not Kodi or a physical-box screenshot. ZIP CRC, manifest version and one top-level add-on directory verified after packaging.

Still requires CoreELEC hardware: actual focus/label rendering, action callbacks, Kodi-inserted modal content, playback and chapters, HDR/DV/output banding, GPU timing, memory, skin/restart lifecycle and long-running stability. No universal bug-free,1:1 Apple or device-performance guarantee. Previous unresolved software-GL stress-fixture limitations and private-test SF Pro license scope remain in earlier notes.

## Reproduce current checks

    python3 development/validate_skin.py .
    python3 development/test_labels135.py . /path/to/extracted-1.3.4/skin.applify
    python3 development/test_shelves129.py .
    python3 development/test_addons129.py .
    ORCHARD_TEST_ROOT=. python3 development/test_editor129.py
    python3 development/test_player_fonts130.py .

Development-only build stages on a fresh1.3.4 source: build_labels135.py SKIN, finish_scope135.py SKIN BASELINE134, then refine_player135.py SKIN. Do not rerun the stages on already-patched source. Pillow/numpy/FreeType are development dependencies only; Kodi does not execute them.
