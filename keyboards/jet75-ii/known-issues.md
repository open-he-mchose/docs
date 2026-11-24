# Jet75-II — known issues

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

## 1. NKRO report declared as Array — Snap Tap, macros and >6 keys are lost (all firmware V111–V116)

**Symptom.** Snap Tap / SOCD does nothing (also with the official driver on Windows). Keyboard keys in
[macros](../../protocols/glw/macros.md) are not typed (only their modifiers arrive). Pressing more than six
keys at once drops the extra keys.

**Cause.** Interface 2, report ID 1 is a 120-bit bitmap (one bit per usage `0x00–0x7C`) but is declared
`Input(Data,Array)` (`81 00`) instead of `Input(Data,Variable)` (`81 02`):

```
05 01 09 06 a1 01 85 01 05 07 19 00 29 7c 15 00 25 01 95 78 75 01 81 00 c0
                                                                      ^^ byte 23 should be 02
```

With "Array" semantics each set bit is read as array index 1, i.e. usage `0x01` (ErrorRollOver), which hosts
discard. The firmware sends SOCD keys and macro keys only through this report, and plain keys only after the
6-key buffer is full (**firmware**).

**Evidence (verified).** Raw reports on interface 2 alternate A/D while SOCD keys are pressed, but Linux
produced **0** key events for them; the maximum number of keys held at once in Linux was **6**. Macro keys likewise appeared in the raw
reports but produced no Linux events; with the fix every test macro typed correctly.

**Workaround on Linux (verified).** A HID-BPF `hid_rdesc_fixup` that flips byte 23 from `0x00` to `0x02`
when the descriptor matches. After loading: SOCD A/D produced **366** events, never both down (last input
wins); up to **19** keys held at once were reported. Nothing is written to the keyboard; unloading or
replugging restores the original descriptor. A udev rule can load it on every plug-in.
Implementation: planned for `open-he-mchose/linux-fixes`.

**Affected versions (firmware).** Every Jet75-II application image known: V111 (build Mar 10 2025) to V116
(Aug 28 2025) all contain the same `81 00` item. Downgrading does not help. The Ace 60 Pro v1.07 image
bundled with the updater has the same descriptor bug.

**Windows / macOS.** No user-side fix known; only a firmware update from MCHOSE can correct the descriptor.

**Side effect to know.** Once fixed, SOCD bindings that were configured earlier (and silently did nothing)
start working — check for forgotten bindings in all profiles.

## 2. RS (Rapid Strike) keys can be lost

RS outputs through the 6-key buffer; if six keys are already down the RS key is dropped (**firmware**).
Not observed in testing (would need seven keys), **inferred** impact.

## 3. Travel curve glitch for switch type 7

One non-monotonic entry in the V116 curve table — see [switches-and-travel.md](switches-and-travel.md#curve-data-glitch).
No effect on type-0 keyboards.

## 4. Depth travel field freezes on release

Not a bug in key handling, but the depth stream's travel field lags — see
[switches-and-travel.md](switches-and-travel.md#lag-and-how-to-avoid-it).

## Official web driver issues

See [known-issues/web-driver.md](../../known-issues/web-driver.md) (DKS settings silently altered,
advanced-key slot renumbering, overlapping Toggle writes).
