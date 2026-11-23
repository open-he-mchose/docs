# Firmware analysis

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

## Images

- The Windows "FirmwareUpdateTool" for Jet75-II (MFC, 32-bit) embeds two raw images as PE resources of type
  `BIN`: the keyboard application (changes per version) and a second image labelled "Ace 60 Pro"
  (identical in every version).
- The web driver's device table points to an update image per model on the vendor CDN; for Jet75-II it
  is the V116 application, identical in layout to the embedded ones.
- Images are **not encrypted** (entropy ≈ 4.7–4.9, readable strings such as "MCHOSE", "Jet75-II",
  build date).

## Architecture and load address

- First word `jal`, followed by `nop`s → RISC-V. Peripheral constants (USB HS `0x40023400`, PFIC
  `0xE000E000`) → WCH CH32V30x family (QingKe core).
- The application is linked at flash **`0x5000`**. Found by testing candidate bases against the command jump
  table (`lui/addi` → `0x13840`, 243 words): only base `0x5000` puts all 243 targets inside the image; the
  vector-table words (`0x5308`, `0x999A` …) agree.
- Initialised data (`.data`) is copied to RAM `0x20000000`; global pointer `0x20000A68`.

## WCH QingKe "XW" instructions

The QingKe core has extra 16-bit byte/halfword loads and stores in encodings that stock RISC-V tools read as
floating-point (`c.fld`, `c.fsd`, `c.fldsp`, `c.fsdsp`) or reserved (Q0 funct3 = 100) instructions. Without
handling them, decompilation breaks ("bad instruction data"). Encodings inferred from code context
(e.g. three byte loads at offsets 4/5/6 of the packet buffer = size and offset of the protocol header):

| Encoding | Instruction | Offset bits |
|---|---|---|
| Q0, funct3 = 001 | `lbu rd', off(rs1')` | b12 = off[0], b6–5 = off[2:1], b11–10 = off[4:3] |
| Q0, funct3 = 101 | `sb rs2', off(rs1')` | same |
| Q2, funct3 = 001 | `lhu rd', off(rs1')` | b6–5 = off[2:1], b12–10 = off[5:3] |
| Q2, funct3 = 101 | `sh rs2', off(rs1')` | same |
| Q0, funct3 = 100, b12–11 = 0 | `lbu/sb/lhu/sh rd', off(sp)` | b6 = store, b5 = halfword, b10–7 = off (×2 for halfwords) |

A Ghidra language with these instructions is in [re-tools/ghidra](https://github.com/open-he-mchose/re-tools/tree/main/ghidra).

## Making Ghidra find the code

A raw image gives Ghidra only the entry point. Wrap it into an ELF (load address `0x5000`, RAM segment
`0x20000000`, `.riscv.attributes` declaring rv32imac, soft-float ABI) and add a function symbol for every
direct call target (`jal ra` / `c.jal`, found with `objdump -b binary -m riscv:rv32`) and every vector-table
entry. With that, ~290 functions decompile (`firmware/make_elf.py` in
[re-tools](https://github.com/open-he-mchose/re-tools) does this; the PE resources of a Windows updater can be
extracted with `firmware/extract_pe_resources.py`).

## Useful anchors (Jet75-II V116)

- Packet handler: the function comparing byte 0 with `0x55`/`0x5F` and writing `0xAA`; the command switch uses
  a jump table at `0x13840`.
- Descriptors: USB device descriptor (`12 01 00 02 …`) and the report descriptors lie together in read-only data
  (V115 image: file offset `0xE188`; search for `05 01 09 06 a1 01`).
- Tables: max travel per switch type `0x13FEC` (8 bytes per type), travel curves `0x1403C` (800 bytes per type).

Function-level details: [keyboards/jet75-ii/firmware.md](../keyboards/jet75-ii/firmware.md).
