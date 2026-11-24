# `glw` — macros

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Sizes and limits are Jet75-II values (firmware V116). Sources: the official web driver (**driver**), static
analysis of the firmware (**firmware**) and tests on a Jet75-II (**verified**, see
[verification log](../../keyboards/jet75-ii/verification.md) tests 21–27).

## Overview

- Macros live in one **macro area**, read with `0x0C` and written with `0x0D` (offset = byte offset in the
  area, up to 56 bytes per packet). Every `0x0D` is a flash write.
- A key plays a macro when its key code is `70 <index> <mode>` ([keymap](keymap-and-keycodes.md)).
- The firmware only uses the 16-entry offset table and the 4-byte action records. Everything else in the
  area is metadata of the official driver.
- Macro names, default delay and the other UI settings are **not** stored in the macro area.

## Macro area

| Property | Jet75-II | Evidence |
|---|---|---|
| Size | 8192 bytes (`0x0D` rejects writes with offset + length > `0x2000`; `0x0C` reads are not bounds-checked) | **firmware** |
| Scope | **one area shared by all profiles** (the driver writes it only through profile 0) | **firmware**, **driver** |
| Factory reset `EE FF` | clears the whole area to zero | **firmware** |
| Number of macros | 16 (driver); the firmware accepts index 0–31, but only 16 offsets exist in the driver's layout | **driver**, **firmware** |

**Area size and scope on other models (driver).** The driver picks them from the base-info flags
"multi profile" and "ordered profiles". If both flags are set, there is one shared area: 4096 bytes for
device types 101/130/131/132 (Ace 60, G87 V2, K87S, K99 V3), 8192 bytes for all other types. Otherwise each
profile has its own 2048-byte area at `2048 × profile`.

## Layout written by the official driver

| Offset | Size | Content | Used by firmware |
|---|---|---|---|
| 0 | 32 | 16 × u16 LE: offset of macro *i*'s first action record, from the start of the area | **yes** |
| 32 | 2 | magic `81 7E` | no |
| 34 | 16 | one "type" byte per macro (the play mode the driver's UI shows; see [Modes](#play-modes)) | no |
| 50 | 2 | `4D 43` ("MC") | no |
| 52 | 2 | u16 LE: offset of the cloud-info block | no |
| 54 | 10 | zero | no |
| 64 | 4 | `00 00 80 00`: one shared **empty macro** (a single end record); every empty slot points here | yes |
| 68 | … | action records of the non-empty macros, one after another | yes |
| cloud-info offset | 16 × 6 | per macro: 0 or a reference to the driver's online macro library (`"MC"` with type bits in bit 7 of both bytes, then a u32 id) | no |

Identical macros share one record list (the driver de-duplicates them). An empty area as written by the
driver is therefore 164 bytes: table, header, the empty macro and 96 zero bytes of cloud info
(**verified**: read back from the keyboard).

## Action record (4 bytes)

| Byte | Meaning |
|---|---|
| 0–1 | **delay after this action**, u16 LE, in **milliseconds** (**verified**: 1000 → 1.016 s, 450 + 50 → 0.518 s cycle) |
| 2 | flags: bits 0–3 = action type, bit 6 = press (`1`) / release (`0`), bit 7 = **last record** of the macro |
| 3 | code (meaning depends on the type) |

| Type | Action | Code | Evidence |
|---|---|---|---|
| 0 | nothing (delay only) | – | **firmware** |
| 1 | modifier | modifier bit mask, same bits as the HID modifier byte (`01` LCtrl, `02` LShift, … `80` RGui) | **verified** (LShift) |
| 2 | keyboard key | HID usage (`04` = A) | **verified** |
| 3 | mouse button | button bit mask (`01` left, `02` right, `04` middle, `08`/`10` side) | **driver** only — the Jet75-II firmware **ignores** type 3 |

Notes:

- The driver encodes a **delay-only step** as type 2, release, code `00`, and never writes a delay below 4 ms
  (a step without a delay gets 4). A delay-only record works as expected (**verified**: 50 + 1000 ms between
  two keys measured 1.07 s).
- A delay of **0** runs the next record in the same tick. A press and release with delay 0 between them never
  reaches the host (**verified**).
- Measured delays were 8–20 ms longer than programmed (**verified**, Linux, evdev time stamps).
- The Jet75-II entry in the driver's model list lacks the `EnableMouseMacro` feature, so the official driver
  does not offer mouse buttons in macros for this model (**driver**). This matches the firmware.

Example from the tests: Shift + B with 20 ms steps:

```
14 00 41 02    20 ms, press,   modifier, LShift
14 00 42 05    20 ms, press,   key, B
14 00 02 05    20 ms, release, key, B
14 00 81 02    20 ms, release, modifier, LShift, last record
```

## Play modes

The third byte of the key code `70 <index> <mode>` selects the mode (**firmware**, **verified**):

| Mode | Behaviour | Official driver label |
|---|---|---|
| `00` | repeat while the key is held; releasing stops at once (keys held by the macro are released immediately) | "until release" |
| `01`–`FE` | play *n* times | `01` = "one time" (the driver only writes 1) |
| `FF` | repeat until the key is pressed again | "until same key down" |

Verified with a 500 ms macro: `03` played exactly 3 times; `00` played while held and stopped on release
(one release cut a 50 ms key press short to 22 ms); `FF` repeated for 3.6 s until the second press.

More details (**firmware**):

- There is one player, so only one macro plays at a time. A macro key pressed while a macro is playing does
  **not** restart it. The player continues the current record list with the new key's mode, and:
  - mode `FF` stops playback;
  - modes `00` and *n* **skip the current delay** (the delay counter is reset to 0); mode *n* also resets
    the remaining count to *n*.

  Tapping a key repeatedly therefore runs its macro faster than programmed (**verified**: tapping produced
  20–60 ms gaps in a macro with 1000 ms delays). Pressing a *different* macro key during playback does not
  switch to the other macro (**inferred** from the code, not tested).
- Releasing a mode-`00` key stops the player and clears the NKRO key bitmap. The modifier byte is not
  cleared there, so a modifier pressed by the macro could stay down when the key is released mid-macro
  (**inferred**, not tested).
- The player runs from the main loop. The delay counter counts down in the 1 ms timer interrupt.

## How the output reaches the host

- **Keyboard keys from a macro are sent only through the NKRO report** (interface 2, report ID 1), which
  firmware V116 declares incorrectly. Without a descriptor fix, hosts drop these keys
  (**verified** on Linux: no events at all). See [known issues](../../keyboards/jet75-ii/known-issues.md).
- Modifiers also go out through the boot keyboard report (interface 0), so they work even without the fix
  (**verified**: LShift arrived, B did not).
- With the Linux HID-BPF fix loaded, all test macros typed correctly (**verified**).
- A macro key held for longer than the host's auto-repeat delay auto-repeats on the host like a real key
  (**verified**: 1000 ms hold → Linux repeat events).

## Writing macros safely

- Write the whole used part of the area (table + records) in ≤ 56-byte chunks, then read it back.
- Keep the driver's layout (magic, `"MC"`, cloud-info block) if the official driver should still show the
  macros. The firmware does not need it.
- Make every macro end with a record that has bit 7 set. Without it the player runs past the macro into
  whatever follows.
- The area is shared by all profiles: changing a macro changes it everywhere it is bound.
