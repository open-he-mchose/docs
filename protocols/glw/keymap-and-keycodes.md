# `glw` — keymap and key codes

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

## Layout

Each profile has 4 layers; each layer is a 512-byte area with 3 bytes per key matrix index
(128 slots, Jet75-II uses 0–79). Read a layer with `0x08` at offset `512 × (4 × profile + layer)`, write one key
with `0x09` (3 bytes) at `512 × (4 × profile + layer) + 3 × key` (**verified**). Layer 0 is the base layer,
layer 1 the Fn layer (**verified**). The factory layer 0 can be read with `0x07` (**verified**).

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
| `0xF0` | special | `FF` = Fn / layer, code2 = layer; `FA` rapid-trigger toggle; `34` brightness; `1E` BackHome | | **driver**, **verified** (Fn) |
| `F0 F0 F0` | unused slot | | | **verified** |

Combinations are allowed: `10 03 06` = Ctrl+Shift+C (**verified** with Ctrl+Shift+T).
Consumer usages seen in the driver: `E2` Mute, `E9` Vol+, `EA` Vol−, `CD` Play/Pause, `B5` Next, `B6` Previous,
`B7` Stop (**driver**).

Advanced types (`0x90–0x95`) point into per-profile tables — see [advanced-keys.md](advanced-keys.md).
The depth stream always identifies keys by their **factory layer-0 code**, not the user mapping (**verified**).
