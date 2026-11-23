# MCHOSE Jet75-II (Jet 75, Esports edition)

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

75 % wired magnetic-switch keyboard, 80 keys. Reference model of this documentation: everything in
[protocols/glw](../../protocols/glw/README.md) was verified on this keyboard unless noted.

## Identity

| Item | Value | Evidence |
|---|---|---|
| USB VID:PID | `0x41E4:0x211A`, product string "Jet75-II", manufacturer "MCHOSE" | **verified** |
| Bootloader VID:PID | `0x41E4:0x211B` | **driver**, **firmware** (app checks marker `0x211B41E4`) |
| Web-driver entry | `id: jet75`, `type: 122`, `storageKey: "Jet 75 II"`, protocol `glw` | **driver** |
| MCU | WCH CH32V30x family (QingKe RISC-V, USB High-Speed) | **firmware** (peripheral addresses), **inferred** exact part |
| Firmware tested | V116, build "Aug 28 2025 10:45:06" (reported by command `0x03`) | **verified** |
| Firmware known to driver | newest `116`, minimum supported `108` | **driver** |
| Other images seen | V111–V115 embedded in the Windows "FirmwareUpdateTool" | **firmware** |
| Polling | report-rate field in FuncConfig; High-Speed USB (8 kHz class) | **firmware**, **inferred** rate |
| Keys / layers / profiles | 80 keys (tables sized for 128), 4 layers, 4 on-board profiles | **verified** |
| Switch type | type 0 in all trigger entries (max travel 3.41 mm) | **verified** |
| Precision | actuation and rapid-trigger distances in 0.01 mm | **verified** |

Sibling models with the same name but different hardware IDs: Jet 75 (`0x41E4:0x2118`) and
Jet 75 Ultra edition (`0x3837:0x3008`) — see [keyboards](../README.md). They are not covered here.

## Pages

| Page | Content |
|---|---|
| [usb-interfaces.md](usb-interfaces.md) | The three HID interfaces and their report descriptors |
| [key-matrix.md](key-matrix.md) | Matrix index of every key (needed by all per-key commands), physical layout |
| [switches-and-travel.md](switches-and-travel.md) | Switch types, max travel, travel curves, precise depth calculation |
| [firmware.md](firmware.md) | Firmware V116 internals: memory map, flash regions, command handler, depth pipeline, calibration, advanced-key engine |
| [known-issues.md](known-issues.md) | Bugs: NKRO descriptor (breaks Snap Tap and >6 keys), RS key loss, curve table glitch |
| [verification.md](verification.md) | What was tested on the keyboard, how, and the results |
| [open-questions.md](open-questions.md) | What is still unknown |

## Status

| Area | Status |
|---|---|
| Framing, commands, info | **verified** |
| FuncConfig (performance + lighting) | **verified** (read/write/restore) |
| Per-key trigger settings (sensitivity) | **verified** |
| Keymap / remap, key code types | **verified** for plain keys, media keys, Fn; macros not tested |
| Lighting: effects, stored and live colours | **verified** |
| Depth stream | **verified**, precise lag-free depth implemented |
| Advanced keys MT / DKS / TGL / RS / LT / SOCD | **verified** (SOCD only with the descriptor fix) |
| Calibration (`0xA8`/`0xB1`) | **firmware** only (deliberately not exercised: it rewrites stored calibration) |
| Macros, profile switching, Fn-layer special codes | not researched |
| Firmware update protocol | **driver** / **firmware**, not exercised |
