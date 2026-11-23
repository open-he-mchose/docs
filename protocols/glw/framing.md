# `glw` — packet framing

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

## Request (host → keyboard), 64 bytes

| Byte | Field | Notes |
|---|---|---|
| 0 | flag `0x55` | `0x5F` selects raw bootloader-style packets; anything else is ignored (**firmware**) |
| 1 | command | see [commands](commands.md) |
| 2 | XOR key | `0` = none. If non-zero, the firmware XORs bytes 3…(size+7) with it, and the reply too (**firmware**). The driver always sends 0 |
| 3 | checksum | `(bytes 4 … size+7) summed, & 0xFF` (**verified**) |
| 4 | size | read: bytes requested; write: bytes of data; ≤ 56 (`0x38`) |
| 5–6 | offset | little endian (low byte first) — a byte offset into the command's memory region |
| 7 | `0` | reserved, included in the checksum |
| 8–63 | data | writes only; zero padding to 64 bytes |

Two bytes are used for the offset because regions are larger than 255 bytes; the keyboard's RISC-V CPU
reads them directly as one little-endian 16-bit value (**firmware**).

Reads send no data: the checksum then covers `size, off_lo, off_hi, 0`.

## Reply (keyboard → host), 64 bytes

| Byte | Field |
|---|---|
| 0 | `0xAA` = OK, `0xAB` = error |
| 1 | same command |
| 2–3 | XOR key, checksum (same rules) |
| 4–6 | size and offset echoed |
| 8… | data (reads) |

Match a reply by `AA`, command and offset; skip other input reports that arrive in between
(depth stream `A0 …`, notifications). On error the payload is ASCII `cserr` (bad checksum) or
`unknw` (unknown command) (**firmware**).

## Chunking

Transfers larger than 56 bytes are split into chunks with increasing offsets (**driver**, **verified**).
The driver writes the 64-byte FuncConfig as two overlapping packets: offset 0 size 56, then offset 8 size 56
(**verified**).

## Example

Read firmware info (command `0x03`, 56 bytes): `55 03 00 38 38 00 00 00` + zeros
(checksum `0x38` = size 56). Reply: `AA 03 00 8D 16 00 00 00 | 16 01 "Aug 28 2025,10:45:06"` — the
firmware sets the reply size to the real length (0x16 = 22 bytes); data = version `0x0116` (little endian)
followed by the build date (**verified**). A write example is in [lighting.md](lighting.md#worked-example-live-colour-packet).
