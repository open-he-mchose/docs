# Jet75-II — verification log

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Tests run on one Jet75-II, firmware V116, Linux (usbmon / hidraw / evdev), 22 November 2026 (tests 1–20)
and 24 November 2026 (tests 21–33). Raw captures
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
| 21 | Macro area read | `0x0C`, 8192 bytes | driver layout as documented: 16 offsets → 64, `81 7E`, `"MC"`, cloud-info offset 68; 164 bytes used, rest zero |
| 22 | Macros without fix | 3 macros on F10–F12 (`70 i 01`), raw reports + evdev | macro keys appear only in the interface-2 NKRO report; **0** Linux key events for them; LShift (boot report) arrived |
| 23 | Delay unit | macro: A press, 1000 ms, A release | 1.004–1.016 s → 1 ms units |
| 24 | Macros with fix | same macros, HID-BPF fix loaded | `a`, Shift+`B`, `c` … 1.07 s … `d`; a press + release with delay 0 never appeared |
| 25 | Mode `03` | 500 ms macro (A 50 ms + 450 ms) | exactly 3 plays, 0.518 s apart |
| 26 | Mode `00` | same, key held ~2 s | played while held, stopped on release (one 50 ms press cut to 22 ms) |
| 27 | Mode `FF` | same, press – wait 3.6 s – press | repeated until the second press; settings restored, all 4 profiles and the macro area byte-identical to the backup |
| 28 | Profile key | Fn+Enter (`F0 FA 00`) twice, config-interface reports logged | profile 0 → 1 → 0; `A1` at once, `A3` ~0.3 s later; base info position stored (`01`, then `00`) |
| 29 | Host switch | `0x0E`, 1 byte at offset 0: `01`, then `00` | reply, `A1` 1 ms later, `A3` 41 ms later; `0x04` reads back the new position |
| 30 | Notification layout | compared `A1`/`A3` with FuncConfig of profiles 0 and 1 | `A1`: FuncConfig[1], profile, position, `FF`×4, FuncConfig[8], FuncConfig[13], position; `A3` carries FuncConfig[5…] |
| 31 | Layer numbering | read all keymaps and FuncConfig byte 1 | FuncConfig[1] = 0/4/8/12; Fn key = `F0 FF (4p+1)` in layer 0 and `F0 FF (4p+3)` in layer 2; factory keymap readable for all 4 layers via `0x07` |
| 32 | Fn-layer codes | each factory Fn combination pressed once (except Fn+Esc, Fn+Backspace), FuncConfig polled every 0.4 s, `A3` logged | brightness ±, speed, next effect, colour preset (main and side fields), Win lock toggled twice, Mac/Win mode via FuncConfig byte 1; one `A3` per change; brightness+ at maximum changes nothing but still sends `A3`; settings restored, all profiles identical to the backup |
| 33 | FuncConfig byte 1 bit 0 | after Fn+P / Fn+O | stored as `03` / `01` (Fn held); firmware clears bit 0 at boot and on `0x06` |
