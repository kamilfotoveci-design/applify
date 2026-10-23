# Applify 1.3.7 — centered player controls

## Changes

Play/Pause, Stop, Info and Player Info now center the icon and actual label width as a single unit inside each button. A native horizontal grouplist with centered alignment and an auto-width non-scrolling label replaces the previous fixed left offsets. Changing Play to Pause recalculates the content width without moving or resizing the button itself. A one-pixel optical lift aligns the caption with the icon, accounting for the broad SF Pro font cell.

The visible player captions use a new regular26px font role in all three bundled fontsets. All previous font roles and font files remain unchanged. Primary transport icons use clean vector-derived PNGs. Play/Pause and Stop retain196×72px remote targets and their16px gap. Idle capsules use a subdued, flat translucent charcoal fill; focus uses matte white with dark content. No glossy edge, gradient or blur effect was added.

The native Play/Pause, Stop, seek, Back, information and audio/subtitle/video actions and focus links are unchanged. The seek slider and chapter controls are unchanged. Home, widget setup and source settings are byte-identical to1.3.6. No new dependency, background service, polling or provider request is introduced.

This is Apple TV inspired styling with the user's requested named Pause/Stop controls; it is not an exact Apple player replica.

## Installation

Install this ZIP over Applify using Kodi Settings > Add-ons > Install from ZIP file, then restart Kodi. Existing rows and settings are retained. SF Pro remains bundled/default; no separate font installation is needed. Kodi21/22 dependency declarations are retained; runtime compatibility still needs checking on the actual Kodi build.

## Verification actually performed

-125 XML files pass the existing structure/include/texture/font/custom focus/provider wiring validator.
-1,432 assertions pass: native interactive actions preserved across XML, existing font roles retained, centered icon/text geometry and safe widths across Default/Arial/Inter fontsets and1080p/4K scale/focus factors, non-scrolling labels, old asset/source/Home preservation and uniform neutral button faces. These are model/static/byte checks, not1,432 live functional tests.
-1,162 Kodi filename-gate and native FreeType glyph checks pass locally.
- A controlled preview rendered with the actual font and button/icon PNGs was visually inspected for idle, focused Play and focused Pause. The preview is not a Kodi screenshot.
- The final ZIP is checked for CRC integrity, safe single-root structure and exact packaged-source bytes.

The native auto-width/group alignment implementation was checked against CoreELEC source revision cfc215086edfe8b96de48530c5cdff1d2d78e92a. Documentation: https://kodi.wiki/view/Label_control and https://kodi.wiki/view/Group_List_Control . Source hashes and detailed results are in development/centering-tests-1.3.7.json.

## Target-device checks still required

Kodi/CoreELEC has not been executed in this environment. Verify the new centering and font weight on the TV, paused/playing transitions, focused/idle/disabled states, mouse/remote focus and actual audio/subtitle/play/stop actions. Timing of the first autosized-label frame and ARM frame pacing require a Kodi runtime. Hardware scaling, calibration and HDR output can alter the visible result. Earlier provider/playback limitations and the unresolved Playback failed report still apply; see1.3.6 notes. Earlier test reports keep their original scope and are not a claim that all historical suites were rerun against1.3.7.
