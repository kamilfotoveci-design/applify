# Current release:1.3.5

See RELEASE-NOTES-1.3.5.md for the fixed player labels, adjacent larger Pause/Stop, matte grey dialogs, Home preservation and actual testing scope. Older notes below retain their historical scope; prior player text-fit assertions are superseded.

# Current release:1.3.5

See RELEASE-NOTES-1.3.5.md for the fixed player labels, adjacent larger Pause/Stop, matte grey dialogs, Home preservation and actual testing scope. Older notes below retain their historical scope; prior player text-fit assertions are superseded.

# Current release 1.3.3

See RELEASE-NOTES-1.3.3.md and development/flat-ui-tests-1.3.3.json. Current changes/tests supersede the historical notes below. Target-box runtime remains unverified.

# UI gradient banding correction — 1.2.4

The supplied reference crops illustrate contour banding; they are not native captures from the current test box. Physical improvement has not been measured here.

## Changes

- Build-time void-and-cluster blue-noise masks, two independent 64×64 rank fields. All 4096 ranks occur once. The measured low/high spatial-frequency power ratio is below 0.0001 for the saved diagnostic mask; this is not white noise relabelled as blue noise.
- Very low amplitude monochrome RGB dither and independent alpha dither. RGB channels preserve the original neutral/blue ink relationship, avoiding colored speckles. Zero and full-opacity edges remain exact. There is no animated noise.
- Home: one 1920×1080 RGBA gradient replaces the intersecting 1100×1080 left and 1920×640 bottom gradients. Their analytic alpha is composed before quantization.
- Details: one 1920×1080 RGBA gradient replaces the left/bottom combination.
- Playback OSD: 1920×500; seek/pause: 1920×400; full-screen info: 1920×600; browser: 1920×830. These match their controls at the 1920×1080 skin design resolution.
- Ambient background: regenerated analytically as 1920×1080 RGB PNG, including missing-art fallbacks. A JPEG-to-PNG conversion alone would retain existing compression artifacts.
- Uniform optional dimming layers remain uniform; they contain no gradient to dither. Their setting is retained. No source fanart is altered.
- No shader, unsupported Kodi API, Python background service or additional noise overlay is introduced. Dither is baked into existing PNG loads. A full-size RGBA texture is approximately 7.9 MiB decoded; Kodi can keep windows/assets cached. The background uses more memory than the former half-resolution JPEG. This is not a hardware frame-rate benchmark.

## Verification

53 targeted checks passed: mask uniqueness/spectrum; native PNG sizes/modes; unbiased and bounded alpha quantization; exact transparent/opaque edges; absence of chroma noise; one custom gradient per screen; no JPEG fallback references; controlled synthetic alpha compositing. Native-resolution synthetic before/after composites were visually inspected. Static XML/resources validation and the existing shelf geometry model also pass.

No Kodi executable is available in the current execution environment. Previous Kodi 20.5 navigation/playback checks are historical and are not relabelled as tests of these new textures. CoreELEC 21/22, the Xiaomi ARM device, actual TV output and overscan still require testing. The inherited lower-level Estuary dialog set is outside this targeted gradient replacement. No 4K texture set is bundled: 4K output can scale the 1080p design, including its grain. This patch cannot guarantee zero contouring from an 8-bit compositor/output chain or from source fanart.

## Install and check

Install the ZIP using Add-ons → Install from zip file, then restart Kodi. Compare Home and the video OSD on the same artwork/scene and display settings. No blanket thumbnail-cache deletion or HDMI changes are required. If stripes remain, a native Kodi screenshot plus a TV photo of the same frame will help distinguish composed pixels from downstream display processing.

## Rebuild and references

`development/upgrade_banding.py` requires NumPy, SciPy and Pillow at build time only. It generates the seven PNGs and merges the two custom overlay pairs. Full source and test JSON are included.

- https://www.momentsingraphics.de/BlueNoise.html — blue-noise properties and void-and-cluster method.
- https://kodi.wiki/view/Texture_Attributes — Kodi native texture behavior.
