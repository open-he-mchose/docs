# `glw` — lighting

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Three layers of control:

| What | How | Persistent |
|---|---|---|
| Effect, brightness, speed, colour | [FuncConfig](funcconfig.md) bytes 8–16 (main), 24–31 (side), 44–51 (side 2) | yes (flash) |
| Per-key stored colours (used by the static effect) | `0x0A` / `0x0B`, offset `512 × profile + 3 × key` | yes (flash) |
| Live per-key colours | `0xDD` (main), `0xDF` (side), `0xDC` (side 2), offset `3 × key` | **no** (RAM) |

Light index = key [matrix index](../../keyboards/jet75-ii/key-matrix.md) (**verified** on Jet75-II).

## Effects

Effect id = FuncConfig byte 8 (**driver** names, **verified** ids 0 and 6):

| Id | Name | Id | Name | Id | Name |
|---|---|---|---|---|---|
| 0 | static (per-key colours) | 8 | colorful fountain | 16 | matrix shadows |
| 1 | aurora mapping | 9 | galaxy roaming | 17 | melody piano |
| 2 | shadow steps | 10 | spiral | 18 | flow dance |
| 3 | tranquility | 11 | surge rhythm | 19 | raining |
| 4 | pulsation | 12 | ocean | 20 | stars |
| 5 | flower dance | 13 | ripple dance | 21 | fireworks |
| 6 | tidal rhythm | 14 | ripple | 22 | ripple flow |
| 7 | surging tide | 15 | instant flash | 23 | sword array |
| 255 | off | | | | |

The list of effects offered per model comes from the model's layout file in the driver; Jet75-II offers
0–22 (**driver**).

## Live colours (`0xDD`)

- RGB triplets, 3 bytes per key, starting at `offset = 3 × key`; up to 54 bytes (18 keys) per packet;
  the whole Jet75-II (80 keys = 240 bytes) fits in 5 packets at offsets 0, 54, 108, 162, 216 (**verified**).
- Firmware limit: `offset + size ≤ 0x180` (128 keys); data goes to a RAM buffer; the first packet switches the
  keyboard into live mode and every packet re-arms a timeout. Without new packets the keyboard returns to
  its stored effect within a few seconds (**verified**), so refresh at 10–30 Hz. Nothing is written to flash.
- 25–30 frames per second worked for minutes (**verified**).
- While live colours are sent the depth stream is paused (any host packet pauses it).

### Worked example: live colour packet

Key W (matrix index 71) red, written to hidraw as 65 bytes (**verified**):

```
00 | 55 DD 00 D7 | 03 D5 00 00 | FF 00 00 | 00 … 00 (53 bytes)
```

| Byte | Value | Meaning |
|---|---|---|
| (pre) | `00` | Linux hidraw report ID, stripped by the kernel, not sent over USB |
| 0 | `55` | request flag |
| 1 | `DD` | command: live colours |
| 2 | `00` | XOR key (none) |
| 3 | `D7` | checksum = `(03 + D5 + 00 + 00 + FF + 00 + 00) & FF` |
| 4 | `03` | size: 3 data bytes (one key) |
| 5–6 | `D5 00` | offset = 3 × 71 = 213 = `0x00D5`, low byte first |
| 7 | `00` | reserved |
| 8–10 | `FF 00 00` | R, G, B |
| 11–63 | `00` | padding |

Reply: `AA DD 00 … 03 D5 00 00 …` (command, size and offset echoed).

Shell one-liner (repeat in a loop to keep the key lit):

```sh
{ printf '\x00\x55\xdd\x00\xd7\x03\xd5\x00\x00\xff\x00\x00'; head -c 53 /dev/zero; } > /dev/hidrawN
```

### Why the offset is in bytes

The keyboard does not know about "keys" in this command: it copies `size` bytes into its colour buffer at
position `offset`. Each key occupies 3 bytes, so key `k` starts at byte `3 × k`. Writing to offset 71 instead
of 213 would land in the middle of key 23's slot and colour the wrong keys.
