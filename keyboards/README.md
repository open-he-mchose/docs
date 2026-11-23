# MCHOSE magnetic keyboards

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Models listed by the official web driver's magnetic-keyboard ("cizhou") section, generated from
[`data/devices.json`](../data/devices.json) by `scripts/gen_keyboard_index.py` (**driver**, build of 2026-11).
"FW" is the newest firmware version the driver offers; "Receivers" are the 2.4 GHz dongle identities of
wireless models. Chinese edition suffixes: 电竞版 = Esports edition, 超竞版 = Ultra edition.

| Model | VID:PID | Protocol | Bootloader | FW | Receivers | Status |
|---|---|---|---|---|---|---|
| Ace 60 | `0x41E4:0x2101` | `glw` | `0x41E4:0x2102` | 120 | 0x19F5:0xFC30 | not researched |
| Ace 60 Pro | `0x41E4:0x2103` | `glw` | `0x41E4:0x2104` | 118 | 0x19F5:0xFC31 | not researched |
| Ace 60 Pro ISO FR | `0x3837:0x3040` | `glw` | `0x3837:0x3041` | 100 | — | not researched |
| Ace 60 Pro Nordic | `0x3837:0x3002` | `glw` | `0x3837:0x3022` | 107 | — | not researched |
| Ace 60X (Esports edition) | `0x41E4:0x2112` | `glw` | `0x41E4:0x2113` | 104 | — | not researched |
| Ace 60X | `0x41E4:0x2126` | `glw` | `0x41E4:0x2127` | 105 | — | not researched |
| Ace 68 | `0x41E4:0x2114` | `glw` | `0x41E4:0x2115` | 109 | — | not researched |
| Ace 68 Pro | `0x41E4:0x2116` | `glw` | `0x41E4:0x2117` | 121 | — | not researched |
| Ace 68 (Ultra edition) | `0x3837:0x3003` | `glw` | `0x3837:0x302A` | 113 | — | not researched |
| Ace 68 Air (Esports edition) | `0x41E4:0x2120` | `glw` | `0x41E4:0x2121` | 117 | — | not researched |
| Ace 68 Air (Ultra edition) | `0x41E4:0x2132` | `glw` | `0x41E4:0x2133` | 116 | — | not researched |
| Ace 68 Air 2 | `0x3837:0x300A` | `glw` | `0x3837:0x300B` | 114 | — | not researched |
| Ace 68 GT | `0x3837:0x3007` | `glw` | `0x3837:0x3009` | 113 | — | not researched |
| Ace 68 Turbo(16K) | `0x3837:0x3026` | `glw` | `0x3837:0x3027` | 122 | — | not researched |
| Ace 68 Turbo(8K) | `0x3837:0x3028` | `glw` | `0x3837:0x3029` | 106 | — | not researched |
| Ace 68 V2 (Ultra edition) | `0x3837:0x3024` | `glw` | `0x3837:0x3025` | 107 | — | not researched |
| Ace 75(16K) | `0x3837:0x301D` | `glw` | `0x3837:0x301F` | 100 | — | not researched |
| Ace 75 | `0x3837:0x303C` | `glw` | `0x3837:0x303D` | 114 | — | not researched |
| G75 V2(8K) | `0x3837:0x2021` | `glw` | `0x3837:0x2022` | 114 | 0x3837:0x3033 | not researched |
| G87 V2(8K) | `0x3837:0x2015` | `glw` | `0x3837:0x2019` | 119 | 0x3837:0x3033 | not researched |
| G98 V3 | `0x3837:0x2025` | `qhw` | `—` | 100 | 0x3837:0x1015 | not researched |
| GT 75 | `0x3837:0x302D` | `glw` | `0x3837:0x302F` | 100 | — | not researched |
| God 60 | `0x3837:0x3020` | `glw` | `0x3837:0x301A` | 100 | — | not researched |
| Jet 75 | `0x41E4:0x2118` | `glw` | `0x41E4:0x2119` | 109 | — | not researched |
| Jet 75 (Esports edition) | `0x41E4:0x211A` | `glw` | `0x41E4:0x211B` | 116 | — | [documented, verified](jet75-ii/README.md) |
| Jet 75 (Ultra edition) | `0x3837:0x3008` | `glw` | `0x3837:0x302B` | 100 | — | not researched |
| K87 V3 | `0x3837:0x2023` | `qhw` | `0x3837:0x2024` | 0 | 0x3837:0x1015 | not researched |
| K87S | `0x3837:0x200E` | `glw` | `0x3837:0x200F` | 142 | 0x3837:0x3033 | not researched |
| K99 V3 | `0x3837:0x2020` | `glw` | `0x3837:0x201F` | 128 | 0x3837:0x3033 | not researched |
| Mix 87 | `0x41E4:0x2122` | `glw` | `0x41E4:0x2123` | 112 | — | not researched |
| Mix 87 (Ultra edition) | `0x3837:0x300D` | `glw` | `0x3837:0x302C` | 122 | — | not researched |
| ZERO 75X | `0x41E4:0x211C` | `glw` | `0x41E4:0x211D` | 114 | — | not researched |

Notes (**driver**):

- `glw` models share the protocol described in [protocols/glw](../protocols/glw/README.md); per-model data
  (key matrix, switch types, feature flags) differs. `qhw` models use a different protocol
  ([protocols/qhw](../protocols/qhw/README.md)).
- Two vendor IDs are used: `0x41E4` (older models) and `0x3837` (newer models). The bootloader enumerates
  under its own PID, listed in the table.
- To document a new model, copy the structure of [jet75-ii/](jet75-ii/README.md).
