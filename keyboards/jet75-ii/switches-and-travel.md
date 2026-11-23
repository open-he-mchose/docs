# Jet75-II — switches, travel and depth

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

## Switch types

The low nibble of byte 0 of each key's [trigger entry](../../protocols/glw/key-trigger.md) selects a switch
type. The web driver offers 10 types for this model (**driver**); the firmware has a table of maximum
travel per type at app address `0x13FEC`, 8 bytes per type (**firmware**):

| Type | Driver key | Max travel |
|---|---|---|
| 0 | `ztDefault` | 3.41 mm |
| 1 | `ztTtcTwBz` | 3.41 mm |
| 2 | `ztTtcTwRgbDj` | 3.41 mm |
| 3 | `ztTtcWcwJr` | 3.41 mm |
| 4 | `ztBx` | 3.41 mm |
| 5 | `ztXl` | 3.41 mm |
| 6 | `ztXm` | 3.41 mm |
| 7 | `ztKailh` | 3.41 mm |
| 8 | `ztLb` | 3.51 mm |
| 9 | `ztKy` | 3.31 mm |

The tested keyboard uses type 0 on all keys (**verified**). The firmware clamps an actuation point above the
type's max travel to 1.50 mm when applying the table (**firmware**, `fn_b530`).

## From Hall sensor to millimetres (firmware V116, `fn_bd6c`)

Per scan and key (**firmware**):

1. Raw ADC sample → adaptive IIR filter (the stronger the change, the faster the filter) → second low-pass
   (accumulator × 8) = **filtered ADC** (stream bytes 16–17). At rest ≈ 12 200–12 800, at the bottom ≈ 6 700–7 200
   on the tested unit (**verified**).
2. If filtered ADC < baseline (rest value, stream bytes 18–19 × 4):
   `norm = (baseline − adc) × 1024 / calibration`, clamped to **1600** (stream bytes 4–5).
3. **Travel** (stream bytes 6–7, 0.01 mm) = index + 1 of the last entry ≤ `norm` in the per-type travel
   curve (app address `0x1403C + type × 800`, `max_travel` 16-bit entries). The curve linearises the
   Hall sensor, whose output changes slowly at the top of the stroke.

### Lag and how to avoid it

The firmware recomputes the travel field only while |raw − smoothed| > 5, so it **freezes when a key
settles** — on fast releases the stream shows 2.5–3.1 mm while the sensor is already back at rest
(**verified**, 36 such packets in a 99 s test). `norm` keeps updating, but stops once the ADC is at or above the
baseline.

Lag-free depth (used by the reference tools, **verified** against captures):

```
if baseline - adc < 20:          depth = 0
elif norm < curve[9]:            depth = 0                 # firmware ignores < 0.10 mm
else: i = number of curve entries <= norm
      depth = (i + (norm - curve[i-1]) / (curve[i] - curve[i-1])) / 100   # mm, interpolated
```

Equal to the firmware field to ±0.01 mm on settled samples, correct where the firmware field is frozen.
The curves can be extracted from a firmware image (curve and max-travel tables above).

### Curve data glitch

In V116 the curve for **type 7** has one non-monotonic entry (index 315: 1398 > 1310) — a firmware data
error (**firmware**). Use a running maximum before searching. Type 0 (this keyboard) is clean.
