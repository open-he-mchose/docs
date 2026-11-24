# `glw` — FuncConfig (64 bytes per profile)

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Read with `0x05`, write with `0x06`, offset `64 × profile`. Field layout from the driver's serializers
(**driver**); fields marked **verified** were changed and read back on a Jet75-II.

| Byte | Bits | Field | Evidence |
|---|---|---|---|
| 0 | 0 | enter the bootloader on the next start (set by `F0 07` and by the app when the bootloader marker is missing) | **firmware** |
| 1 | | base layer as an absolute layer number: `4 × profile`, + 2 in Mac mode (driver: "macMode"); recomputed by the firmware on every [profile switch](profiles.md#layers-and-funcconfig-byte-1). Bit 0 may be stored set (Fn was held when Fn+O / Fn+P saved it); boot and `0x06` clear it | **verified**, **firmware** |
| 2–3 | | marker `AA BB`. Without it the firmware loads its built-in defaults at boot | **verified**, **firmware** |
| 4 | 0–3 | [report rate](#report-rate). **Changing it for the active profile reboots the keyboard** | **verified**, **firmware** |
| 4 | 4–7 | tickRate — not used by the Jet75-II firmware | **driver**, **firmware** |
| 5 | | deadZone — not used by the Jet75-II firmware (only echoed in `A3`) | **driver**, **firmware** |
| 6 | 0 | lock Win keys (LGui/RGui are dropped, **only on the Windows layers** 0–1, not in Mac mode) | **verified**, **firmware** |
| 6 | 1 | lock Alt+Tab (Tab is dropped while an Alt key is held) | **firmware** |
| 6 | 2 | lock Alt+F4 (F4 is dropped while an Alt key is held) | **firmware** |
| 6 | 3 | lock the Menu / Application key (usage `0x65`); no driver name | **firmware** |
| 7 | 0 | tachyonMode — not used by the Jet75-II firmware | **driver**, **firmware** |
| 7 | 1 | bottom rapid-trigger mode (read by the key scan) | **driver**, **firmware** |
| 7 | 2 | travelCheck ("auto check", automatic recalibration) | **driver**, **firmware** |
| 7 | **3** | **debugMode — enables the [depth stream](depth-stream.md)** | **verified** |
| 7 | 5–7 | debounceLevel (index into an 8-entry firmware table) | **driver**, **firmware** |
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

Bytes the Jet75-II firmware V116 never reads: 5, 17–23 and 32–63 (byte 4 high nibble and byte 7 bit 0 are also
unused). They are driver fields for other models. Keep them unchanged when writing (**firmware**).

## Report rate

The low bits of byte 4 go straight into the `bInterval` of all USB endpoints (the firmware uses bits 0–2),
followed by a USB re-initialisation. On High-Speed USB the interval is `2^(value−1) × 125 µs`
(**firmware**, **verified**: value 2 → `bInterval` 2 in the descriptor).

| Value | Rate | Evidence |
|---|---|---|
| 1 | 8 kHz | **driver**, **firmware** |
| 2 | 4 kHz | **verified** |
| 3 | 2 kHz | **driver**, **firmware** |
| 4 | 1 kHz | **driver**, **firmware** |
| 0 / 5 | 16 kHz / 32 kHz on models with USB 3 support; **do not use on the Jet75-II** (0 is an invalid interval) | **driver** |

The 2.4 GHz report rate of wireless models is a separate field (byte 38, values 0–3 = 1k–8k) (**driver**).

**The report rate is effectively global** (**verified**). On a profile switch the firmware keeps the current
rate and, if the new profile stores a different one, overwrites the new profile's byte 4 with the current
rate (whole byte, so the tickRate nibble is lost) and saves it to flash. Switching from a 4 kHz profile to an
8 kHz profile left the keyboard at 4 kHz and changed the stored value of the other profile to 2.
Writing a different rate into a profile that is **not** active does not reboot the keyboard (**verified**).

## Rules

- Always **read-modify-write** the whole block and verify by reading back (**verified**).
- `0x06` writes flash and reloads the RAM copy of the **active** profile only (**firmware**). It reboots the
  keyboard only if the active profile's report rate changes.
- At power-up the firmware clears bit 3 of byte 7 in RAM, so a debug bit left set in flash does not stream
  after a replug (**firmware**).
