# Contributing

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Corrections, confirmations and new models are very welcome.

## Reporting

- **Mistake or contradiction:** open an issue with the page, the statement and what you observed.
- **Confirmation on another model or firmware:** say which model (name, VID/PID from `lsusb`),
  firmware version (`0x03` info command or the official driver) and what you tested.
- **New model:** start a directory under `keyboards/` modelled on [`jet75-ii/`](keyboards/jet75-ii/README.md).

## Rules

1. **Label evidence** on every non-trivial fact: **verified**, **firmware**, **driver** or **inferred**
   (see the [README](README.md#evidence-labels)). Say what hardware/firmware a **verified** claim was checked on.
2. **No vendor material:** do not commit firmware images, updaters, the web driver's JavaScript,
   decompiled vendor code or download links to them. Describe behaviour in your own words; short
   identifiers (module numbers, function names, addresses, constants) are fine.
3. **No personal data in captures:** raw USB captures and key logs contain everything typed during the
   recording. Only commit trimmed, anonymised packet excerpts.
4. **Keep protocol and model apart:** shared behaviour goes to `protocols/<family>/`, model-specific
   values (key matrix, switch tables, quirks) to `keyboards/<model>/`.
