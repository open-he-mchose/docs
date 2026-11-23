# open-he-mchose / docs

Documentation of MCHOSE Hall-effect (magnetic switch) keyboards: USB protocols, per-model details,
firmware internals and known bugs — the groundwork for open drivers.

**Read it as a website: https://open-he-mchose.github.io/** (search, navigation, dark mode).

> **⚠️ AI-generated content.** The reverse engineering, documentation and code in this organization
> were produced almost entirely by an AI assistant (Claude, by Anthropic). The maintainer directed the
> work and tested the results on real hardware, but did not write the analysis or code by hand. Facts
> are marked by how they were confirmed (hardware test, firmware analysis, or inference from the
> vendor's web driver). Verify before relying on anything here, and please report mistakes.

**Unofficial community project. Not affiliated with or endorsed by MCHOSE.** No vendor firmware,
software or code is distributed here — only descriptions written from observation and analysis.

## Contents

| Section | What it covers |
|---|---|
| [keyboards/](keyboards/README.md) | All MCHOSE magnetic models known to the official driver, one directory per documented model |
| [keyboards/jet75-ii/](keyboards/jet75-ii/README.md) | **Jet75-II** (the reference model, fully documented and tested) |
| [protocols/](protocols/README.md) | Protocol families: [`glw`](protocols/glw/README.md) (30 models) and [`qhw`](protocols/qhw/README.md) (2 models, not yet researched) |
| [known-issues/](known-issues/README.md) | Bugs: per-model firmware issues and problems of the official web driver |
| [reverse-engineering/](reverse-engineering/README.md) | How the information was obtained: web driver, firmware analysis, USB captures — methods to repeat for other models |
| [data/devices.json](data/devices.json) | Machine-readable model table (VID/PID, protocol, bootloader, firmware version, receivers) |
| [scripts/](https://github.com/open-he-mchose/docs/tree/main/scripts) | Maintenance of this repository: regenerate `devices.json` and the model table |

Tools for researching new models (Ghidra language for the WCH MCU, firmware → ELF, web-driver and USB
helpers) live in [open-he-mchose/re-tools](https://github.com/open-he-mchose/re-tools).

## Evidence labels

Every non-trivial statement carries one of these labels:

| Label | Meaning |
|---|---|
| **verified** | Tested on a real keyboard (USB capture, or a tool exercising the device and reading back) |
| **firmware** | Taken from static analysis of the vendor firmware image (decompiled with Ghidra) |
| **driver** | Taken from the official web driver's JavaScript |
| **inferred** | Reasoned from the above, not confirmed |

Unless stated otherwise, **verified** facts were checked on a Jet75-II (VID `0x41E4`, PID `0x211A`)
running firmware **V116** in November 2026. Other `glw` models very likely share the protocol, but
model-specific values (key matrix, switch tables, features) differ and are untested.

## Quick facts (Jet75-II)

- Vendor configuration channel: HID interface 1, 64-byte reports without report ID, framing
  `55 cmd xor sum | size off_lo off_hi 00 | data…`, reply `AA …` — [framing](protocols/glw/framing.md).
- Key depth streaming exists and needs a single bit — [depth stream](protocols/glw/depth-stream.md).
- Every settings write goes to flash; live colours (`0xDD`) are RAM-only — [commands](protocols/glw/commands.md).
- **Firmware bug:** the NKRO report is declared `Input(Array)`, so Snap Tap/SOCD output and keys beyond 6
  are dropped by every host — [known issues](keyboards/jet75-ii/known-issues.md).

## License

Documentation: [CC BY-SA 4.0](https://github.com/open-he-mchose/docs/blob/main/LICENSE). Scripts in `scripts/`: MIT (see file headers).
Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
