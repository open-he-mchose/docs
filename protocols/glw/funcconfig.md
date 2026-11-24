# `glw` — FuncConfig (64 bytes per profile)

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Read with `0x05`, write with `0x06`, offset `64 × profile`. Field layout from the driver's serializers
(**driver**); fields marked **verified** were changed and read back on a Jet75-II.

| Byte | Bits | Field | Evidence |
|---|---|---|---|
| 0 | 0 | enter the bootloader on the next start (set by `F0 07` and by the app when the bootloader marker is missing) | **firmware** |
| 1 | | base layer as an absolute layer number: `4 × profile`, + 2 in Mac mode (driver: "macMode"); recomputed by the firmware on every [profile switch](profiles.md#layers-and-funcconfig-byte-1). Bit 0 may be stored set (Fn was held when Fn+O / Fn+P saved it); boot and `0x06` clear it | **verified**, **firmware** |
| 2–3 | | marker `AA BB` (firmware treats the block as valid only with it) | **verified**, **firmware** |
| 4 | 0–3 | reportRate — **changing it reboots the keyboard** | **driver**, **firmware** |
| 4 | 4–7 | tickRate | **driver** |
| 5 | | deadZone | **driver** |
| 6 | 0 / 1 / 2 | lockWin / lockAltTab / lockAltF4 | **verified** (lockWin via Fn+LGui), **driver** |
| 7 | 0 | tachyonMode | **driver** |
| 7 | 1 | bottom rapid-trigger mode | **driver** |
| 7 | 2 | travelCheck ("auto check", automatic recalibration) | **driver**, **firmware** |
| 7 | **3** | **debugMode — enables the [depth stream](depth-stream.md)** | **verified** |
| 7 | 5–7 | debounceLevel | **driver** |
| 8 | | main light effect id ([list](lighting.md#effects)) | **verified** |
| 9 | | main light brightness 0–100 (boot clamps it to 100) | **verified** |
| 10 | | main light speed, stored as `4 − speed` (speed 0–4; boot replaces values > 4 with 2) | **verified**, **firmware** |
| 11 | | main light direction | **driver** |
| 12 | | customColorDisabled | **driver** |
| 13 | | colorIndex: preset colour selected on the keyboard (bytes 14–16 get its RGB) | **verified** |
| 14–16 | | main light colour R, G, B | **verified** |
| 20 | | rtsmart | **driver** |
| 23 | | light scope type index (models with light scopes) | **driver** |
| 24–27 | | side light effect, brightness, `4 − speed`, customColorDisabled | **verified** (24–26 via Fn keys), **driver** |
| 28 | | side light colorIndex (bytes 29–31 get its RGB) | **verified** |
| 29–31 | | side light colour R, G, B | **verified** |
| 32 | 0–6 / 7 | RF battery / charging (wireless models) | **driver** |
| 33–38 | | roller type, work mode, sleep time, sleep mode, RF/BT channel, 2.4 GHz report rate | **driver** |
| 40–42 | | calibration RGB | **driver** |
| 44–51 | | side light 2 block: effect, brightness, `4 − speed`, customColorDisabled, ?, R, G, B | **driver** |

## Rules

- Always **read-modify-write** the whole block and verify by reading back (**verified**).
- `0x06` writes flash and reloads the RAM copy of the **active** profile only (**firmware**).
- At power-up the firmware clears bit 3 of byte 7 in RAM, so a debug bit left set in flash does not stream
  after a replug (**firmware**).
