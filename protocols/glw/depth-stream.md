# `glw` — key-depth stream

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

The keyboard can report how deep every magnetic key is pressed, on the configuration interface.

## Enabling

The stream runs while **bit 3 of FuncConfig byte 7 ("debugMode") is set in the keyboard's RAM copy**
(**firmware**, **verified**). Two ways to set it:

1. Read FuncConfig (`0x05`), set the bit, write it back (`0x06`) — what the official driver does
   (**verified**). Costs two 64-byte flash writes on enable and two on disable.
2. `0xA8` — sets the bit in RAM only, **but starts a calibration session** that can rewrite stored
   calibration ([calibration.md](calibration.md)). Do not use it just to stream.

The official driver enables it only on its trigger-settings tab with the calibration dialog open, sends
`0xA8` too, and clears both when leaving (**driver**, **verified**). After a power cycle the bit is cleared in
RAM even if it was left set in flash (**firmware**).

## Timing

- After **any host packet** the stream pauses for ~25 scheduler periods (~0.6 s) (**firmware**, **verified**:
  sending live colours at 10 Hz gave 0 stream packets).
- Then at most **one packet per ~24 ms for the whole keyboard**, only for keys whose travel changed
  (values < 0.10 mm count as 0); after `0xA8`, two full sweeps of all keys first (**firmware**, **verified**).
  With several keys moving each key is updated less often. Not host-configurable (fixed by a firmware timer).

## Packet (64-byte input report)

| Byte | Content | Evidence |
|---|---|---|
| 0 | `0xA0` | **verified** |
| 1–3 | key, as its factory layer-0 code `[type, code1, code2]` (e.g. `10 00 04` = A, `10 08 00` = LGui, `F0 FF 01` = Fn) | **verified** |
| 4–5 | normalised depth 0…1600, big endian (input to the travel curve) | **firmware**, **verified** |
| 6–7 | **travel in 0.01 mm, big endian**; < 10 → 0; ≥ max − 5 → max. Freezes on fast releases, see below | **verified** |
| 8 | rapid-trigger accumulator (0…29 with 0.30 mm settings), `0xDD` when idle | **inferred** |
| 9 | key state: `01` pressed, `FF` released | **verified** |
| 10 | calibration status: `FF` calibrated, `00`/`01` in progress | **verified** |
| 11–13 | stored bottom calibration value ÷ 4 as decimal digits (thousands, hundreds, tens) | **firmware** |
| 14–15 | max travel of the key's switch type, big endian (`01 55` = 3.41 mm) | **verified** |
| 16–17 | filtered Hall ADC value, big endian | **verified** |
| 18–19 | rest (baseline) ADC ÷ 4, big endian | **verified** |
| 20–21 | peak noise (max raw − smoothed difference) | **firmware** |
| 22–23 | counter while held deeper than 3.00 mm | **firmware** |

## Precise, lag-free depth

The travel field (bytes 6–7) is only refreshed while the sensor value changes quickly, so it can stay at
2.5–3.1 mm after the key is already released. Compute depth from bytes 4–5 with the model's travel curve and
treat "ADC within 20 of the rest value" as 0 — algorithm on the
[Jet75-II switches page](../../keyboards/jet75-ii/switches-and-travel.md#lag-and-how-to-avoid-it) (**verified**).

## Consequences for software

- A depth visualiser works well; precise timing does not (24 ms per packet for the whole board).
- Depth-reactive lighting is impossible over this interface: writing colours stops the stream.
- Do not poll the keyboard while streaming.
