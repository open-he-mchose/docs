# Reverse engineering methods

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

How the documentation was produced, so that others can repeat it for other models. The tools mentioned
here are in [open-he-mchose/re-tools](https://github.com/open-he-mchose/re-tools).

| Page | Content |
|---|---|
| [web-driver.md](web-driver.md) | Getting and reading the official web driver: where the protocol, device table and texts live |
| [firmware-analysis.md](firmware-analysis.md) | Finding and decompiling the firmware: images, load address, WCH QingKe instructions, Ghidra setup |
| [usb-capture.md](usb-capture.md) | Capturing and checking USB traffic on Linux |

Work order that proved efficient: (1) read the web driver to get the command set and data structures,
(2) confirm framing and units with a USB capture of the driver, (3) decompile the firmware to settle what the
driver does not explain (exact semantics, limits, bugs), (4) test each claim with a small tool and read back.
Problems found along the way are collected in [known-issues](../known-issues/README.md).
