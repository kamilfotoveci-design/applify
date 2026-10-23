# Current release:1.3.5

See RELEASE-NOTES-1.3.5.md for the fixed player labels, adjacent larger Pause/Stop, matte grey dialogs, Home preservation and actual testing scope. Older notes below retain their historical scope; prior player text-fit assertions are superseded.

# Current release:1.3.4

See RELEASE-NOTES-1.3.4.md for the button-spacing audit, corrections and actual test limits. Earlier entries below retain their original scope.

# Current release 1.3.3

See RELEASE-NOTES-1.3.3.md and development/flat-ui-tests-1.3.3.json. Current changes/tests supersede the historical notes below. Target-box runtime remains unverified.

# Current release:1.3.2

See RELEASE-NOTES-1.3.2.md for current implementation, validation and limits. Earlier sections record prior builds.

# Current release:1.3.1

See RELEASE-NOTES-1.3.1.md for the complete-poster change and current testing scope. This release includes all1.3.0 player changes.

# Current visual update: 1.3.0

See RELEASE-NOTES-1.3.0.md for current changes, installation, validation and limits. Earlier sections below describe historical releases; their runtime results do not certify this build.

# Visual audit — 19 October 2026

## 1.2.9 spacing and directory review

Two user photos show row headings touching focused artwork and a detached rectangular More pill. Heading/font spacing, style-specific row heights and a center-aligned circular See All replace those details. The controlled native-asset preview was inspected. Add-ons is now a flat native tile window, with no category controls; only page navigation and Refresh. There is no current Kodi runtime screenshot or measured ARM frame pacing.

## 1.2.8 current comparison

The user supplied a Severance floating-top-bar reference and a close-up of the current widget/hero text. The new composition follows that reference: title/clearlogo at x84/y250, narrow static synopsis, no Rating text, first landscape header at y730, 302×170 landscape artwork and no default card captions. Other/poster rows use the raised viewport. Controlled synthetic asset/layout previews were inspected; these are not screenshots from Kodi. The app artwork and blur/material renderer differ from Kodi, and pixel identity is not claimed.

Navigation depth is simulated with small PNG shadows, a modest vertical material gradient and native 2px/2% focus motion. There is no real-time backdrop blur, extra Python service or 3D engine. Physical ARM animation smoothness is unverified. SF Pro remains the user-supplied font with its preserved license.

## Reference choice

The supplied screenshots contain multiple Apple TV app generations. The user explicitly selected the floating top capsule, with no Sports or Kids. That remains the reference for the six tabs: Watch Now, Movies, TV Shows, Add-ons, Search and Settings. Apple introduced a sidebar redesign in December 2023; adopting that instead would conflict with the chosen reference.

Official sources inspected:

- https://www.apple.com/newsroom/2023/12/redesigned-apple-tv-app-elevates-the-viewing-experience/
- https://support.apple.com/guide/tvapp/welcome/web
- Apple Support's linked Silo Home image and playback-controls image. The actual images were inspected, rather than relying on page text alone.

No Apple image or branding from these sources is included in the skin.

## Comparison and changes

| Area | Reference | Orchard 1.2.5 / remaining difference |
| --- | --- | --- |
| Home navigation | Floating dark capsule, white active item | Shared capsule on Home and the directory browser. No Sports/Kids. Native remote focus and wraparound. |
| Hero | Full-bleed fanart, left logo/title, readable text | Native scaled fanart, gradient, clearlogo fallback with actions on widget cards. Missing artwork falls back to bundled abstract artwork. |
| Shelves | Horizontal landscape collections near hero bottom | Native horizontal providers inside a vertically scrolling viewport. Focused row stays within safe area; another unfocused row may be partially visible as a scroll cue. |
| Long titles | Readable typography, minimal metadata | 180px wrapping hero/detail title, scrolling focused card labels. Titles longer than two lines scroll when animation is enabled; full title remains in details. |
| Playback | Compact timeline, audio/subtitle icons and minimal action text | Compact OSD with explicit focus links. Additional Kodi Player Info, Video and Stop actions remain available. |
| Settings | Consistent minimalist selection lists | Shared fonts, capsule selection, vertical section rail. Native lower-level Kodi settings dialogs retain Estuary structures. |
| Animations | Apple focus scaling, crossfades and motion | Kodi-native short page fades, content entry, view changes, dialog slide/fades and focus motion; reduced-animation option. No claim to Apple proprietary motion physics or parallax. |
| Rendering | Apple materials, font and platform controls | Licensed Inter-derived custom UI fonts and static translucent textures. No live system blur or SF font. |

## Honest scope

This is an Apple TV-inspired native Kodi implementation, not a pixel-identical port. The full inherited native dialog set has not received a per-pixel audit. The custom homepage, poster/landscape transitions, details, library heading, settings, playback controls and technical overlay were the focused visual-review scope. Physical TV overscan, 4K output, target-device frame pacing, HDR/DV and actual receiver formats still require testing on the user's CoreELEC device.

1.2.5 navigation asset renders were compared against the user-supplied floating-pill reference. Navigation is 1016×76 at x452/y48 with variable-width native buttons and 28px semibold labels. Actual Kodi/TV rendering and animation timing remain unverified for this version.
