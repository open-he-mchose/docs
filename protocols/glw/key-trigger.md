# `glw` — per-key trigger settings (8 bytes per key)

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Read with `0xA0`, write with `0xA1`, offset `1024 × profile + 8 × key`. A single 8-byte entry can be written
and takes effect immediately (**verified**). Distances are stored as `value − 1` in 0.01 mm on Jet75-II
(the driver's "precision" setting for the model, **verified**).

| Byte | Bits | Field | Evidence |
|---|---|---|---|
| 0 | 4–7 | `0xA` marker (entries without it are replaced by defaults) | **firmware** |
| 0 | 0–3 | switch type (selects max travel and travel curve, see the [model page](../../keyboards/jet75-ii/switches-and-travel.md)) | **verified** |
| 1 | 0–3 | keyMode: 0 = rapid trigger off, 1 = rapid trigger, 2 = continuous rapid trigger; > 2 is forced to 1 | **driver**, **verified**, **firmware** |
| 1 | 4–7 | priority — used by [SOCD](advanced-keys.md#snap-tap--socd-0x94) | **driver**, **verified** |
| 2, 3 bit 0 | | actuation − 1 (9 bits) | **verified** |
| 3 | 3–4 / 1–2 | press / release precision | **driver** |
| 4, 5 bit 0 | | rapid-trigger press distance − 1 (9 bits) | **verified** |
| 5 | 1–7 | press dead zone | **driver** |
| 6, 7 bit 0 | | rapid-trigger release distance − 1 (9 bits) | **verified** |
| 7 | 1–7 | release dead zone | **driver** |

Example (**verified**): `A0 01 95 00 1D 00 1D 00` = switch type 0, rapid trigger on, actuation 1.50 mm
(0x95 + 1 = 150), press/release sensitivity 0.30 mm.

The firmware clamps an actuation beyond the switch type's max travel to 1.50 mm (**firmware**). With rapid
trigger on, a key is reported released after moving up by the release distance from its deepest point
(**verified**: state flips ≈ 0.3 mm above the bottom with 0.30 mm).
