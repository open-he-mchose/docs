# Jet75-II — USB interfaces

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

The keyboard exposes three HID interfaces (**verified**, descriptors read from Linux sysfs; identical to
the descriptors stored in the firmware image, **firmware**).

| Interface | Purpose | Reports |
|---|---|---|
| 0 | Boot keyboard (6-key rollover) | 8-byte report: modifiers, reserved, 6 key codes; LED output report |
| 1 | **Vendor configuration channel** | 64-byte input + 64-byte output, **no report ID**; Usage Page `0x0001`, Usage `0x0000` |
| 2 | NKRO keyboard, mouse, consumer, system, wireless-radio | Report IDs 1–5 (below) |

Endpoints of the config channel: OUT `0x04`, IN `0x82` (**verified**, USB capture).

## Interface 1 — configuration

```
05 01 09 00 a1 01 15 00 26 ff 00 19 00 29 08 95 40 75 08 81 02 19 01 29 08 95 40 75 08 91 02 c0
```

On Linux, find it as the `hidraw` node whose `report_descriptor` starts with `05 01 09 00`. Writes to
hidraw must be prefixed with report ID `00` (65 bytes); reads return 64 bytes.
All of [protocols/glw](../../protocols/glw/README.md) happens here.

## Interface 2 — NKRO and extra collections

| Report ID | Collection | Layout |
|---|---|---|
| 1 | Keyboard (NKRO) | 120 one-bit fields, usages `0x00–0x7C` — **declared `Input(Data,Array)` instead of `Variable`**, see [known issues](known-issues.md) |
| 2 | Mouse | 5 buttons, X/Y/wheel (relative), AC Pan |
| 3 | Consumer control | one 16-bit usage `0x001–0x2A0` |
| 4 | System control | one 16-bit usage `0x01–0xB7` |
| 5 | Wireless radio button | 1 bit |

How keys are routed (**firmware**): a pressed key goes into the 6-key buffer of interface 0; only when all
six slots are full does it go into the NKRO bitmap (report ID 1). Snap Tap/SOCD keys go **only** to the
NKRO bitmap.

## Interface 0 — boot keyboard

Standard boot keyboard: modifier byte, reserved byte, 6 key codes (`Input(Data,Array)`, usages 0–0x91),
plus the 3 LED output bits.
