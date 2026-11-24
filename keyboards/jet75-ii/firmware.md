# Jet75-II — firmware V116 internals

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

All facts on this page are **firmware** (static analysis of the official V116 application image, build
"Aug 28 2025 10:45:06" — the same build the keyboard reports) unless labelled otherwise. Function names
are Ghidra's auto names in an ELF built with base `0x5000`; see [reverse-engineering/firmware-analysis.md](../../reverse-engineering/firmware-analysis.md).

## Platform

- WCH CH32V30x family, QingKe RISC-V (RV32IMAC + WCH "XW" compressed byte/half load/store).
  Peripherals seen: RCC `0x40021000`, USB High-Speed `0x40023400`, PFIC `0xE000E000`, TIM2 `0x40000000`,
  TIM3 `0x40000400`; chip UID read from `0x1FFFF7E8`.
- Application linked at flash **`0x5000`**; a bootloader occupies the flash below. The app checks the
  bootloader marker `0x211B41E4` at `0x08004C00` (the bootloader's VID/PID).
- Global pointer `gp = 0x20000A68`.

## Flash regions used by commands (application addresses)

| Region | Content | Command |
|---|---|---|
| `0x17784` | factory keymap (constant) | `0x07` read |
| `0x20100` + 64·profile | FuncConfig | `0x05` / `0x06` |
| `0x20200` | base info (active profile, profile order) | `0x04` / `0x0E` |
| `0x20300` + 256·profile | MT table (also RS/SOCD/LT pairs), 6 B × 32 | `0xA4` / `0xA5` |
| `0x20700` + 128·profile | TGL table, 3 B × 32 | `0xA6` / `0xA7` |
| `0x20900`, `0x20A00`, `0x20B00` | calibration tables | saved by the main loop |
| `0x20D00` | custom data area (profile names, JSON blobs) | `0xF1` / `0xF2` |
| `0x21D00` + 768·profile | DKS table, 24 B × 32 | `0xA2` / `0xA3` |
| `0x22900` | macros | `0x0C` / `0x0D` |
| `0x24900` | stored per-key colours | `0x0A` / `0x0B` |
| `0x25100` | user keymaps (512 B per layer, 4 layers per profile) | `0x08` / `0x09` |
| `0x27100` + 1024·profile | per-key trigger settings | `0xA0` / `0xA1` |

Writes go through a flash routine (`fn_11e5e`, address ORed with `0x08000000`). Every write command except
`0xDD`, `0xA8`, `0xA9` erases and rewrites flash.

## Main functions

| Function | Role |
|---|---|
| `fn_5f84` | packet handler: XOR, checksum, command switch (jump table `0x13840`, 243 entries) |
| `fn_5ed8` | FuncConfig write + reload of the active profile's RAM copy; reboots if the report rate changes |
| `fn_94b4` | boot: loads base info, FuncConfig, calibration; **clears the debug (stream) bit in RAM** |
| `fn_b530` | applies the trigger table: forces `keyMode > 2` to 1, clamps actuation > max travel to 1.50 mm |
| `fn_bd6c` | per-key scan: filtering, normalised depth, travel curve, key state, advanced-key dispatch |
| `fn_ba30` | calibration / auto-recalibration |
| `fn_b8ee` / `fn_b76e` | depth-stream scheduler / packet builder |
| `fn_7c88` | key action executor (plain keys, media, macros, TGL, MT, RS, SOCD, LT) |
| `fn_8c3e` | deferred actions (tap/hold timers, toggles) |
| `fn_7814` | macro key handler: start / stop / repeat count by play mode ([macros](../../protocols/glw/macros.md)) |
| `fn_78d8` | macro player (main loop): reads 4-byte records, NKRO bitmap and modifier byte |
| `fn_8982` | DKS engine |
| `fn_761a` | plain key output (6-key buffer first, NKRO bitmap on overflow) |
| `fn_7a60` | report sender (boot report, NKRO report ID 1, consumer, system, config replies) |
| `fn_7bb8` | TIM3 tick ISR (tick counter, runs the packet handler and sender) |
| `fn_1239e` | main-loop deferred flash saver (calibration, base info) |

## Depth stream

See [protocols/glw/depth-stream.md](../../protocols/glw/depth-stream.md) for the packet. Internals:
`fn_b8ee` runs from the main loop and sends only while **bit 3 of byte 7 of the RAM copy of FuncConfig**
(`0x200053D7`) is set; after every host packet it waits ~25 periods; then sends at most one key per 10 TIM3
ticks — changed keys only, or two full sweeps of all 80 keys right after `0xA8`.

## Calibration

`0xA8` (if not active): TIM2 period 149 → 299, sets the RAM debug bit, calibrating = 1, full-sweep counter = 2,
fills the per-key "recalibrate" array (`0x200038D0`, 80 bytes) with `0xFF`, snapshots baselines (`fn_b9c8`).
While active, any key that is pressed gets its stored bottom value reset to `0x73A`; after two stable deep
presses its status goes 0 → 1 → `0xFF`, the new bottom value is stored, and the main loop writes the
calibration tables to flash. `0xA9` ends the session (TIM2 back to 149) but does not clear the debug bit.
`0xB1` resets the calibration of all keys to `0x73A` and saves it. Advanced keys and DKS only act on keys
whose calibration status is `0xFF`.

## Advanced keys

Bindings and tables: [protocols/glw/advanced-keys.md](../../protocols/glw/advanced-keys.md). Engine details:

- On key press, for key types `0x93–0x95` the scan fills a 14-byte runtime record per slot
  (`gp + 0x514 + 14·slot`, 32 records): own index, partner index (from `code2`), depths, priority
  (trigger byte 1 high nibble).
- **SOCD** (`0x94`) writes the chosen key only into the NKRO bitmap → affected by the descriptor bug.
- **RS** (`0x93`) writes into the 6-key buffer → silently lost when 6 keys are already down. A key within
  `0x14` (0.20 mm) of max travel always registers.
- SOCD/RS/LT read only `code1`/`code2` of their MT entry (the type byte is ignored), so only plain keys
  work in pairs.
- DKS (`fn_8982`) compares travel in 0.1 mm with the four points and executes the per-phase mask.

## Commands not used by the driver UI

`0x01`/`0x02` set/clear a host flag; `0xB0` returns the 12-byte chip UID; `0xEE` factory reset with a scope byte.
