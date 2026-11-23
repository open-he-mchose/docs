# Official web driver issues

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Found while reading the driver (build of November 2026). They explain some "advanced keys do not behave as
configured" reports. Firmware bugs are listed per model, e.g.
[Jet75-II known issues](../keyboards/jet75-ii/known-issues.md).

## DKS settings silently altered

The DKS editor stores each action as `downStart/downEnd/upStart/upEnd`; its encoder normalises some
combinations before writing (**driver**):

- `downStart = 4` is written as `3/3/2` (continuous hold) — fine;
- `downStart = 3` forces `downEnd = 2`;
- `downEnd = 3` forces `upStart = 2`.

So for example `(3, 1, 0, 0)` is stored and read back as `(3, 0, 0, 0)` (the tap at the bottom disappears) and
`(1, 3, 1, 0)` becomes `(1, 3, 0, 0)`. The UI then shows something different from what the user set. The
encoder also does not mask the first 3-bit field. Tools should reproduce the same encoding (the firmware
expects it) but warn the user when a combination cannot be stored.

## Advanced-key slots renumbered on delete

New bindings get slot `max(used) + 1`; deleting one compacts the table and rewrites the slot number in
every bound key's keymap code (**driver**). If any of these writes fails or another driver instance
interferes, functions end up on the wrong keys. Allocating the lowest free slot without renumbering works
equally well for the firmware (**verified**).

## Overlapping Toggle writes

The Toggle table is written with 6-byte records at a 3-byte stride, so each record overwrites the start of
the next one with zeros; the result is only correct because records are written in order (**driver**).

## Debug bit kept in flash

The driver enables the depth stream by writing FuncConfig (flash) every time the trigger tab opens and
again when it closes — two to four flash writes per visit. The firmware clears the bit at power-up, so a
RAM-only method would have been possible only via `0xA8`, which also recalibrates (**driver**, **firmware**).
