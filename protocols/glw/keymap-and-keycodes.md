# `glw` — keymap and key codes

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

## Layout

Each profile has 4 layers; each layer is a 512-byte area with 3 bytes per key matrix index
(128 slots, Jet75-II uses 0–79). Read a layer with `0x08` at offset `512 × (4 × profile + layer)`, write one key
with `0x09` (3 bytes) at `512 × (4 × profile + layer) + 3 × key` (**verified**). Layer 0 is the base layer,
layer 1 the Fn layer, layer 2 the Mac layer (**verified**, **firmware**). The factory keymap (all 4 layers) can be read with
`0x07` at offset `512 × layer` (**verified**).

## Key code `[type, code1, code2]`

| Type | Meaning | code1 | code2 | Evidence |
|---|---|---|---|---|
| `00 00 00` | key disabled | | | **driver** |
| `0x10` | keyboard | modifier bits (`01` LCtrl, `02` LShift, `04` LAlt, `08` LGui, `10` RCtrl, `20` RShift, `40` RAlt, `80` RGui) | HID usage | **verified** |
| `0x10 00 00` | transparent (in upper layers) | | | **verified** |
| `0x30` | consumer (media) | usage low byte | usage high byte | **verified** (Mute) |
| `0x70` | [macro](macros.md) | macro index 0–15 | play mode: `00` while held, `01`–`FE` play n times, `FF` until pressed again | **verified** |
| `0x90` | DKS | slot | 0 | **verified** |
| `0x91` | Toggle | slot | 0 | **verified** |
| `0x92` | Mod-Tap | slot | hold time / 10 ms | **verified** |
| `0x93` | Rapid Strike | slot | partner key index | **verified** |
| `0x94` | Snap Tap (SOCD) | slot | partner key index | **verified** |
| `0x95` | LT (release one → tap the other) | slot | partner key index | **verified** |
| `0xF0` | special | `FF` = Fn / layer, code2 = absolute layer `4 × profile + layer`; `FA` = next [profile](profiles.md); others: [special codes](#special-codes-f0-xx-yy) | | **verified** |
| `F0 F0 F0` | unused slot | | | **verified** |

Combinations are allowed: `10 03 06` = Ctrl+Shift+C (**verified** with Ctrl+Shift+T).
Consumer usages seen in the driver: `E2` Mute, `E9` Vol+, `EA` Vol−, `CD` Play/Pause, `B5` Next, `B6` Previous,
`B7` Stop (**driver**).

Advanced types (`0x90–0x95`) point into per-profile tables — see [advanced-keys.md](advanced-keys.md).
The depth stream always identifies keys by their **factory layer-0 code**, not the user mapping (**verified**).

## Special codes `F0 xx yy`

What the Jet75-II firmware V116 does with each `F0` code (handler `fn_6fea`). Changes to FuncConfig are
saved to flash about 200 ms after the last key press, followed by an `A3` notification
([profiles](profiles.md#notifications)). "Fn layer" = present in the factory Fn layer (layer 1) of the Jet75-II.
Most actions run on key press only.

| Code | Factory key | Action | Evidence |
|---|---|---|---|
| `F0 FF xx` | Fn | momentary layer: absolute layer `xx` = `4 × profile + layer` while held | **verified** |
| `F0 FA 00` | – | next [profile](profiles.md) in the rotation | **verified** |
| `F0 04 00` | Fn+O | Windows mode: base layer = `4 × profile` (FuncConfig byte 1) | **verified** |
| `F0 05 00` | Fn+P | Mac mode: base layer = `4 × profile + 2` | **verified** |
| `F0 02 00` | Fn+LGui | toggle Win-key lock (FuncConfig byte 6 bit 0) | **verified** |
| `F0 32 00` / `F0 33 00` | Fn+A / Fn+S | main light brightness up / down (byte 9, 80 ↔ 100 seen) | **verified** |
| `F0 36 00` / `F0 37 00` | Fn+G / – | main light speed up / down (byte 10, stored as `4 − speed`) | **verified** (up) |
| `F0 2F 00`, `F0 30 00` | Fn+D / – | next main light effect (byte 8; only when brightness > 0) | **verified** (`2F`) |
| `F0 2E 00` | – | main light effect, other direction | **firmware** |
| `F0 3E 00`, `F0 3C 00` / `F0 3D 00` | Fn+F / – | main light colour: next / previous preset (byte 13 = preset index, bytes 14–16 = its RGB) | **verified** (`3E`) |
| `F0 3B 00` | – | main light: direction or similar (driver name "Light Trend") | **firmware** |
| `F0 35 00` | – | main light brightness toggle 0 ↔ 100 (also sets byte 25 to the same value) | **firmware** |
| `F0 2C 00` | – | main light effect off (byte 8 = 0) | **firmware** |
| `F0 A0 00` | Fn+C | next side-light effect (byte 24, cycles 0–3) | **verified** |
| `F0 15 00` / `F0 16 00` | Fn+Z / Fn+X | side-light brightness up / down (byte 25) | **verified** |
| `F0 18 00`, `F0 19 00` / `F0 17 00` | Fn+B / – | side-light speed up / down (byte 26) | **verified** (`18`) |
| `F0 1A 00` / `F0 1B 00` | Fn+V / – | side-light colour: next / previous preset (byte 28 = preset index, bytes 29–31 = its RGB) | **verified** (`1A`) |
| `F0 1C 00` | – | side light on / off (byte 25: 0 ↔ last value, default 100) | **firmware** |
| `F0 03 00` | – | toggles a RAM flag and remaps keys (driver name "WASD Change": WASD ↔ arrows) | **firmware**, meaning **inferred** |
| `F0 2B 00` | – | on-keyboard per-key colour mode: keys stop typing and the stored colours are shown; a second press ends the mode (and presumably saves) | **firmware**, meaning **inferred** |
| `F0 51 00` | – | sends Win+Space | **firmware** |
| `F0 53 00` / `F0 54 00` | – | sends Shift+Win+3 / Shift+Win+4 (macOS screenshots) | **firmware** |
| `F0 57 00` | – | sends Shift+F12 | **firmware** |
| `F0 58 00` | – | sends Win+Q | **firmware** |
| `F0 08 00` | **Fn+Esc** | **held 3 s: factory reset of all profiles** (keyboard blinks white 3 times) | **firmware** — not tested |
| `F0 FE 00` | **Fn+Backspace** | **held 3 s: resets the calibration of all keys** | **firmware** — not tested |
| `F0 07 00` | – | **reboots into the bootloader** (sets FuncConfig byte 0 bit 0) | **firmware** — not tested |
| `F0 01 00`, `F0 52 00` | – | no action in V116 | **firmware** |
| `F0 34 00`, `F0 1E 00`, other codes | – | no action in V116 (the driver's names "Bright", "BackHome" etc. are for other models) | **firmware** |

The driver's key list has names for many more codes (Bluetooth / 2.4 GHz channels, logo and indicator lights,
battery display). They target other models; the Jet75-II firmware ignores them.

**Do not bind `F0 07`, `F0 08` or `F0 FE` to keys that are pressed by accident**, and warn users about
Fn+Esc / Fn+Backspace in tools that show the Fn layer.
