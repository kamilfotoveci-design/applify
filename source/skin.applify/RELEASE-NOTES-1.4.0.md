# Applify 1.4.0 — clean UI polish

- Refined backward/forward 15-second icons: single open-ring stroke, one arrow tip, cleaner numerals, antialiasing and transparent backgrounds.
- Reflowed `DialogSubtitles.xml` into three non-overlapping areas: Services, subtitle results, and actions, with fixed margins, uniform surfaces, and controlled file-title length.
- Improved `DialogSettings.xml` and `DialogAddonSettings.xml` spacing to isolate category, content and action panels.
- Playback commands, focus relationships, native subtitle results IDs and player actions are preserved.

Verification: XML syntax and static geometry checks. Visual runtime check required on actual Kodi/CoreELEC, particularly modal dialogs from third-party subtitle addons.
