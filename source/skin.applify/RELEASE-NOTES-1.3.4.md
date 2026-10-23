# Applify 1.3.4 — Button spacing audit

Install the ZIP over1.3.3 using Kodi > Settings > Add-ons > Install from ZIP file, then restart Kodi. Same add-on ID and user profile; complete editable source included. English UI; target architecture remains Kodi21/22 at1920×1080. Real CoreELEC execution was unavailable.

## Corrected findings

- Floating Home, video-browser and Add-ons navigation:12px between tabs, each tab10px narrower so the full strip keeps its original1000px width. The conservative model includes simultaneous focus/unfocus enlargement. Capsules no longer intersect in that model. Existing glyphs are recentered.
- Native legacy dialogs had negative button gaps, including settings, file selection, add-on information, PVR/group management, playlist tools and playback side-menu controls. Interactive rows now have8px gaps and dimensions adjusted to preserve the existing list pitch where possible. Confirmation rows with touching faces gain12px gaps and280px buttons. Existing control IDs, actions, conditions and remote links are preserved.
- Keyboard:82px key hit areas on a90px pitch, with8px separation in both axes. The complete13-column keyboard and right action menu fit together in a fixed centered geometry. Removes conditional shifts that depended on extra keys and were disabled with reduced animations. Native key IDs/autocomplete integration remain intact.
- Numeric input:92px keys on a100px row pitch; right actions have a gap and fit inside the original dialog. Icons are recentered within resized controls.
- Installed add-on information: eight207px actions with12px gaps fit the1740px action strip. Music-info actions move down48px to clear the information panel. PVR-search edit width is reduced24px to clear its adjacent action.
- Native setting form rows get8px gaps with62px controls where the previous70px rows touched. Default native switch glyph height36px fits the shorter row templates. The Settings/Home editor/context menu and larger Pause/Play/Stop controls remain.
- Fonts, artwork, helper/provider code and media textures are byte-for-byte unchanged from1.3.3. No new service or animation loop. Flat surfaces and corrected dithering from1.3.3 remain.

## What was actually checked

-125 XML files pass the existing structure, references, control IDs and focus-link validator.
- Static include expansion inventories85 window definitions and820 candidate interactive control definitions. This inventory includes conditional alternatives, native templates and invisible event shields; it is not820 independently executed controls.
-588 current checks pass: native behavior comparison across every XML file against1.3.3; negative-gap findings reviewed; conservative safe/focus rectangles in11 principal windows, main navigation spacing, all keyboard key coordinates, and local SF Pro/Inter measurements for literal button labels in those windows.
-11 principal windows: Home, MyVideoNav, home editor, SkinSettings, Settings, VideoOSD, installed Add-ons hub, playback More dialog, video information, keyboard and numeric input. No overlap remains among the modeled visible buttons in these windows after excluding invisible dialog mouse shields and offscreen scrolling content. Native includes/runtime visibility must still be checked in Kodi.
- Retained regressions rerun:115 shelf checks;98 add-on catalog/pagination/focus checks;46 mocked editor/provider tests;459,270 page/style/focus/reduced-mode predicates with52,488 complete poster positions.
- Offline geometry/material previews of navigation, settings, keyboard, numeric input, add-on settings and confirmation controls inspected. They are controlled QA renders, not Kodi screenshots. ZIP CRC and manifest checked after packaging.

## Scope and limits

There is no claim that every dynamic add-on label, localization, overscan setting or transient animation state has been rendered in Kodi. The conservative full inventory retains candidates from invisible mouse shields, mutually exclusive native windows, scrollable content and conditional sidebar transforms. Three dynamically positioned top-bar controls cannot be placed by this static evaluator. Those candidates require runtime review; they are not silently counted as passes. The Weather content shelf's negative gap is a separate non-button composition and is retained.

Physical remote behavior, Kodi-inserted context/settings controls, source-provided long labels, localization, target CoreELEC/ARM frame time, display clipping and stability remain hardware checks. Third-party add-ons that draw their own windows can use their own geometry. Earlier runtime limitations and private-test SF Pro licensing scope remain documented in1.3.3 and earlier releases.

## Reproduce

From the source directory:

    python3 development/validate_skin.py .
    python3 development/test_buttons134.py . /path/to/extracted-1.3.3/skin.applify
    python3 development/test_shelves129.py .
    python3 development/test_addons129.py .
    ORCHARD_TEST_ROOT=. python3 development/test_editor129.py
    python3 development/test_poster131.py .

The audit is a conservative model, not Kodi's GUI engine. On a fresh1.3.3 source, the build steps are fix_spacing134.py followed by finish_spacing134.py, passing the skin directory to each. These build steps are development-only and not intended to run twice on an already-patched source. Pillow/numpy are build/test dependencies only.
