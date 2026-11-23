# `qhw` protocol family

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

**Not researched yet.** Known so far (**driver** only):

- Used by G98 V3 (`0x3837:0x2025`) and K87 V3 (`0x3837:0x2023`), both wireless with the 2.4 GHz receiver
  `0x3837:0x1015`.
- The web driver implements it in a separate SDK class (`QhwSDK`, module 86369 / channel module 53542 in
  the 2026-11 build) with its own packet framing, header parsing and sequence IDs, distinct from `glw`.
  Exposed operations include base info, profiles, key configs, light effects and colours, independent
  macros, GIF/still lighting effects, work mode, sleep time, battery and charging status.
- The driver selects a second "music" HID device for these models.

Help wanted: anyone with a G98 V3 or K87 V3 can start by capturing the official driver's USB traffic.
