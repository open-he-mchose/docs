# `glw` — commands

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Offsets are byte offsets inside each command's region; "p" = profile 0–3, "l" = layer 0–3, "k" = key
[matrix index](../../keyboards/jet75-ii/key-matrix.md). Sizes and limits are Jet75-II values (**firmware**, V116).

| Cmd | Dir | Offset | Size | Meaning | Flash write | Evidence |
|---|---|---|---|---|---|---|
| `0x01` / `0x02` | W | 0 | 0 | set / clear a host flag (purpose unknown) | no | **firmware** |
| `0x03` | R | 0 | 56 | info: version (LE u16), build date string | – | **verified** |
| `0x04` / `0x0E` | R / W | 0 | 56 | base info (active profile, profile count/order); `0x0E` reloads the profile | yes | **driver**, **firmware** |
| `0x05` / `0x06` | R / W | 64·p | 64 | [FuncConfig](funcconfig.md); `0x06` reloads the active profile, reboots if the report rate changes | yes | **verified** |
| `0x07` | R | 3·k (layer 0 at offset 0) | 3/key | factory keymap (constant table) | – | **verified** (layer 0) |
| `0x08` / `0x09` | R / W | 512·(4p+l) + 3·k | 3/key | user [keymap](keymap-and-keycodes.md) | yes | **verified** |
| `0x0A` / `0x0B` | R / W | 512·p + 3·k | 3/key | stored per-key colours | yes | **verified** |
| `0x0C` / `0x0D` | R / W | byte offset in the macro area (shared by all profiles) | ≤ 0x2000 | [macros](macros.md) | yes | **verified** |
| `0xA0` / `0xA1` | R / W | 1024·p + 8·k | 8/key | [trigger settings](key-trigger.md); applied immediately | yes | **verified** |
| `0xA2` / `0xA3` | R / W | 768·p + 24·slot | 24 | [DKS](advanced-keys.md) table | yes | **verified** |
| `0xA4` / `0xA5` | R / W | 256·p + 6·slot | 6 | [MT / RS / SOCD / LT](advanced-keys.md) table | yes | **verified** |
| `0xA6` / `0xA7` | R / W | 128·p + 3·slot | 3 | [Toggle](advanced-keys.md) table | yes | **verified** |
| `0xA8` | W | 0 | 1 (`00`) | start a [calibration](calibration.md) session (also enables the depth stream) | later, by main loop | **verified** (driver traffic), **firmware** |
| `0xA9` | W | 0 | 1 (`00`) | end the calibration session | no | **verified** (driver traffic) |
| `0xB0` | R | 0 | 12 | chip unique ID | – | **firmware** |
| `0xB1` | W | 0 | 1 (`00`) | reset calibration of all keys | yes | **firmware** |
| `0xDC` / `0xDD` / `0xDF` | W | 3·k | ≤ 54 | [live colours](lighting.md) for side light 2 / main / side light, RAM only | **no** | **verified** (`0xDD`) |
| `0xDE` | R | 3·k | ≤ 0x180 | current (rendered) colours | – | **firmware** |
| `0xEE` | W | 0 | 1 | factory reset (`FF` = all, else profile) | yes | **driver**, **firmware** |
| `0xF1` / `0xF2` | R / W | 1024·p + off | | custom data area: profile names @336, feature support @616, custom param @280, light store @728, light effect JSON @840/896 | yes | **driver** |

Bootloader packets (header `0x5F` and raw `0x80–0x84`) are described in [firmware-update.md](firmware-update.md).

## Unsolicited input reports

| First bytes | Meaning | Evidence |
|---|---|---|
| `A0 …` | depth stream packet ([depth-stream](depth-stream.md)) | **verified** |
| `A1 xx` | profile switched to `xx` | **driver** |
| `A4 xx` | profile about to switch | **driver** |
| `A2` or `FA FB FF` | reset | **driver** |
| `A3 …` | FuncConfig changed on the keyboard | **driver** |
| `AA FA …` | light change | **driver** |
| `FA FB 07 bb 01/00` | charging / not charging, battery level `bb` (wireless models) | **driver** |
| `FA FB 06 01/00` | start / stop communication | **driver** |
| `AA 04/05/06/F1/F2 …` | chunk-update notifications for base info, FuncConfig, custom data | **driver** |
