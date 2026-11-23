# `glw` — calibration

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

| Command | Effect | Evidence |
|---|---|---|
| `0xA8` | start a calibration session: also enables the depth stream (RAM debug bit) and sends two full sweeps | **verified** (driver traffic), **firmware** |
| `0xA9` | end the session (does **not** clear the stream bit — the driver clears it with a `0x06` write) | **verified**, **firmware** |
| `0xB1` | reset the calibration of all keys to the default bottom value and save it | **firmware** |

During a session (**firmware**, Jet75-II V116): every key that gets pressed has its stored bottom value reset;
after two stable deep presses its calibration status (depth-stream byte 10) goes `00` → `01` → `FF` and the new
bottom value is stored; the main loop then writes the calibration tables to flash.

**Why tools should avoid it:** a partial but steady press during a session can be stored as the new
"bottom", which distorts all travel values of that key afterwards. Use the FuncConfig bit to stream depth
instead ([depth-stream.md](depth-stream.md)). The test campaign deliberately never sent `0xA8`/`0xB1`
from its own tools.

With FuncConfig byte 7 bit 2 (travelCheck) set, the firmware also adjusts calibration automatically during
normal use (**firmware**).
