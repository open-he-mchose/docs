# Protocol families

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

The official web driver talks to MCHOSE magnetic keyboards through WebHID and has two device SDKs,
selected per model by a `manufacturer` field (**driver**):

| Family | Models | Status |
|---|---|---|
| [`glw`](glw/README.md) | 30 of 32 magnetic models (default when the field is absent) | documented; **verified** on Jet75-II |
| [`qhw`](qhw/README.md) | G98 V3, K87 V3 (wireless, 2.4 GHz receiver `0x3837:0x1015`) | not researched |

Which family a model uses is listed in [`data/devices.json`](../data/devices.json) (`protocol`).
