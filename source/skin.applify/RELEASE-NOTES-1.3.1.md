# Applify 1.3.1 — Complete poster shelf

Includes the full 1.3.0 player/material, timeline, 60px landscape lift and terminal Down fixes. See RELEASE-NOTES-1.3.0.md for installation and base validation.

Poster and ranked portrait shelf groups now reserve the complete 560px native vertical viewport. A focused poster row aligns at y460, ending at y1020. Its heading, card, outline, caption/progress and See All control have room inside the viewport. The next poster row begins outside that viewport, instead of appearing as an additional clipped shelf. Navigation still uses the next populated row; Down at the last row remains on that row.

When the first configured visible row uses posters, both the shelf and hero are raised while navigation remains in the top bar. This avoids leaving the initial poster row low at y670 before focus enters it. Landscape first rows remain y670,60px above1.2.9. Watch Now, Movies and TV Shows all use the same logic; reduced-motion endpoints match normal mode.

This is native XML/container geometry, without an extra provider or background service. The new page/style/focus predicate tests and poster geometry checks are models, not a run of Kodi's actual scroll/animation engine. Physical remote navigation, transitions and the new player popover still require CoreELEC testing. During native scrolling transitions, moving content can cross the viewport edge; complete active rows are the steady-state layout target. Unfocused landscape previews may remain partly visible.

Compatibility, font license and historical unresolved test-fixture cold-start limitations are unchanged from1.3.0. This is not a claim of Apple-identical blur/rendering or crash-free behavior on untested hardware.
