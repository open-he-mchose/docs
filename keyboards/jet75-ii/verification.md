# Jet75-II — verification log

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Tests run on one Jet75-II, firmware V116, Linux (usbmon / hidraw / evdev), 22 November 2026. Raw captures
are not published (they contain typed text); results are summarised here.

| # | Test | Method | Result |
|---|---|---|---|
| 1 | Packet framing and checksum | USB capture of the official driver, 150 s | all 843 host packets have valid checksums; commands seen: 03, 05/06, 08, 09, 0B, 0C, A0/A1, DD, F1/F2 |
| 2 | Trigger write units | capture: actuation set in the driver | stored values 150/266/148/340 = 1.50…3.40 mm → 0.01 mm units |
| 3 | FuncConfig write | capture | written as two overlapping 56-byte packets (offsets 0 and 8); light effect/brightness/colour bytes as documented |
| 4 | Remap | capture | CapsLock (index 60) written `10 00 29` (Esc) and back `10 00 39` |
| 5 | Depth stream from the driver | capture of the driver's calibration dialog | `0x06` with byte 7 `06→0E`, then `0xA8`; stream only between `0xA8` and `0xA9`; reverse on close |
| 6 | Depth stream with bit 3 only (no `0xA8`) | own tool | stream starts right after the `0x06` write; travel 0…3.41 mm; bit restored |
| 7 | Stream rate | own tool, 99 s, 14 keys, up to 7 moving | packets ≈ 24 ms apart, shared by all keys |
| 8 | Host traffic vs stream | 5 s phases with/without `0xDD` at 10 Hz while keys move | quiet: 72/48/72 packets; with `0xDD`: 0/0/0 |
| 9 | Light index mapping | live colours on indices 71/10/61/11 | exactly W/A/S/D lit |
| 10 | Live colours | 25–30 fps for minutes | stable; keyboard returns to its effect after updates stop |
| 11 | Settings write/restore | trigger, remap, light, per-key colour via own tool, then full restore | each write read back correctly; all 4 profiles byte-identical to the backup after restore |
| 12 | Precise depth | recomputed from `norm` + curve vs firmware field | ±0.01 mm on settled samples; correct where the firmware field is frozen |
| 13 | Mod-Tap | CapsLock: tap Esc / hold LCtrl (200 ms) | taps → Esc, holds → LCtrl, CapsLock never emitted |
| 14 | DKS | key 1: W/E/R/T at the four phases, points 1.0/3.0 mm | `wert` on every full press (17×), `wt` on a partial press |
| 15 | Toggle | key 2 toggles B | B held 2.69 s between the two presses |
| 16 | RS | keys 3/4 with depth logged in parallel | deeper key wins in all 20 single-key reports; both sent when depths are within ~0.2 mm or a key is bottomed out |
| 17 | LT | keys 5/6 | releasing one taps the other for ~40–50 ms, both directions |
| 18 | SOCD without fix | A/D, raw reports + evdev | raw reports alternate A/D; **0** Linux events; max 6 keys at once |
| 19 | SOCD with HID-BPF fix | same | **366** Linux events, never both down; max **19** keys at once |
| 20 | Fix auto-load | replug with udev rule | descriptor fixed again on the new HID device |
