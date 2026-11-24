# `glw` protocol family

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Configuration protocol of most MCHOSE magnetic keyboards (30 models, see [keyboards](../../keyboards/README.md)).
Reconstructed from the official web driver (**driver**), the Jet75-II firmware V116 (**firmware**) and USB
captures / tests on a Jet75-II (**verified**). Offsets, sizes and limits below are Jet75-II values;
other models may differ in table sizes, key count and supported features.

## Transport

- A vendor HID interface with 64-byte input and output reports and **no report ID**
  (Usage Page `0x0001`, Usage `0x0000`) — on Jet75-II interface 1 (**verified**).
- The host writes a request, the keyboard answers with one input report. The keyboard also sends
  unsolicited input reports (depth stream, notifications) on the same interface.
- On Linux: hidraw, prefix writes with report ID `00` (65 bytes). In a browser: WebHID
  `sendReport(0, data)` / `inputreport` events.

## Pages

| Page | Content |
|---|---|
| [framing.md](framing.md) | Packet layout, checksum, XOR key, replies and errors |
| [commands.md](commands.md) | All commands with offsets, sizes and flash behaviour |
| [funcconfig.md](funcconfig.md) | 64-byte per-profile settings block (performance, lighting, debug bit) |
| [key-trigger.md](key-trigger.md) | 8-byte per-key trigger entry: actuation, rapid trigger, dead zones, mode |
| [keymap-and-keycodes.md](keymap-and-keycodes.md) | Keymap layout and the 3-byte key code format |
| [lighting.md](lighting.md) | Effects, stored per-key colours, live colours (with a byte-by-byte example) |
| [depth-stream.md](depth-stream.md) | Key-depth streaming: how to enable it and the packet format |
| [advanced-keys.md](advanced-keys.md) | DKS, Mod-Tap, Toggle, Rapid Strike, Snap Tap (SOCD), LT |
| [macros.md](macros.md) | Macro area layout, 4-byte action records, play modes, how macro keys reach the host |
| [calibration.md](calibration.md) | Calibration commands and why to avoid them in tools |
| [firmware-update.md](firmware-update.md) | Bootloader packets (not exercised) |

## Things every implementation should know

- **Every settings write is a flash write** (except live colours and calibration start/stop) — avoid
  writing in loops.
- **Any host packet pauses the depth stream** for ~0.6 s — you cannot poll or animate lighting while
  reading depth.
- **Read-modify-write** shared blocks (FuncConfig) and verify by reading back.
- Changing the report-rate nibble of FuncConfig **reboots** the keyboard.
- Only one program should use the interface at a time (replies would be stolen).
