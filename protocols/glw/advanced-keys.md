# `glw` — advanced keys

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

An advanced function is bound by writing a special [key code](keymap-and-keycodes.md) into the key's keymap
entry; the code points to a **slot** in a per-profile table (**driver**, **firmware**, **verified**).

| Function | Key code | Table (cmd read/write) | Entry | Slots |
|---|---|---|---|---|
| DKS (Dynamic Keystroke) | `90 slot 00` | DKS (`0xA2`/`0xA3`), 768 B/profile | 24 B | 32 |
| Toggle | `91 slot 00` | TGL (`0xA6`/`0xA7`), 128 B/profile | 3 B: key to toggle | 32 |
| Mod-Tap (hold/tap) | `92 slot time/10ms` | MT (`0xA4`/`0xA5`), 256 B/profile | 6 B: tap key, hold key | 32 shared |
| Rapid Strike (RS) | `93 slot partner` | MT | 6 B: own key, partner key | (2 per pair) |
| Snap Tap (SOCD) | `94 slot partner` | MT + trigger priority | 6 B: own key, partner key | (2 per pair) |
| LT | `95 slot partner` | MT | 6 B: own key, partner key | (2 per pair) |

MT, RS, SOCD and LT **share the 32 MT slots**. A pair uses two slots: key 1 → `{own = key1, other = key2}`,
key 2 → `{own = key2, other = key1}`; each key's code2 holds the partner's matrix index (**driver**, **verified**).
For RS/SOCD/LT the firmware uses only `code1`/`code2` of the entry (modifiers and HID usage), so pairs must
be plain keys (**firmware**). Advanced keys act only on calibrated keys (**firmware**).

Choosing slots: any free slot works; the firmware does not need them contiguous (**firmware**, **verified**).
Find used slots by scanning all four layers of the profile for codes `0x90–0x95`.

## DKS (`0x90`)

Up to four actions on one key depending on depth. Entry (**driver**, **verified**):

| Bytes | Content |
|---|---|
| 0–3 | points in **0.1 mm**: `[press start, bottom, lift from bottom, full lift]` = `[shallow, deep, deep, shallow]`, default `0A 1E 1E 0A` (1.0 / 3.0 mm) |
| 4 + 5n … 6 + 5n | action n key code (n = 0…3) |
| 7 + 5n … 8 + 5n | action n phase mask (little endian, 10 bits) |

Phases: 0 = pressed past the shallow point, 1 = pressed past the deep point, 2 = lifted from the deep point,
3 = lifted past the shallow point. Mask bits: 0–2 belong to an action starting at phase 0, 3–5 to phase 1,
6–7 to phase 2, 9 to phase 3; the number of consecutive bits = how many phases the key stays held
("thermometer" code; one bit = a tap within that phase) (**firmware** `fn_8982`, **driver**).

The driver's editor uses `downStart, downEnd, upStart, upEnd` (0–4/0–3/0–2/0–1) and normalises some
combinations on save — see [known issues](../../known-issues/web-driver.md#dks-settings-silently-altered).

Verified example: one key with W/E/R/T as taps at phases 0/1/2/3 types `wert` on a full press and release,
`wt` when the bottom is not reached.

## Toggle (`0x91`)

Entry = key code to toggle. One press holds it, the next press releases it (**verified**: B held 2.7 s
between two presses).

## Mod-Tap (`0x92`)

Entry = tap key code (3 B) + hold key code (3 B); code2 of the binding = hold threshold in 10 ms
(**verified**: CapsLock → tap Esc, hold LCtrl, 200 ms).

## Rapid Strike (`0x93`)

Two keys; while both are pressed, the **deeper** one is active. A key within 0.20 mm of its max travel
always registers, so two bottomed-out keys are both active (**firmware**, **verified**: deeper key won in
20 of 20 single-key reports). RS output goes through the 6-key buffer and is lost if six keys are already
down (**firmware**).

## Snap Tap / SOCD (`0x94`)

Two keys that cancel each other. Mode in the high nibble of byte 1 of each key's
[trigger entry](key-trigger.md) (**driver**, **firmware**):

| Value | Mode | Key 1 | Key 2 |
|---|---|---|---|
| 0 | last input priority | 0 | 0 |
| 1 | absolute priority key 1 | 1 | 2 |
| 2 | absolute priority key 2 | 2 | 1 |
| 3 | cancel (both pressed → neither) | 3 | 3 |

Firmware meaning per key: 2 = yield to the partner, 3 = cancel, 0/1 = release the partner and press itself
(0 re-presses the partner on release).

> On Jet75-II firmware V116 SOCD output is lost on every host because of the
> [NKRO descriptor bug](../../keyboards/jet75-ii/known-issues.md); with the Linux fix it works
> (**verified**: last-input mode, never both keys down).

## LT (`0x95`)

"Single-key reverse stop": releasing one key of the pair taps the other for ~40–50 ms — a counter-strafe in
one motion (**verified**, both directions).

## Limits

The driver allows at most 40 advanced bindings per profile and 32 slots per table (**driver**).
