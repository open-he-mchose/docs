# `glw` — calibration

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

| Command | Effect | Evidence |
|---|---|---|
| `0xA8` | start a calibration session: also enables the depth stream (RAM debug bit) and sends two full sweeps | **verified** (driver traffic; own tools, 2026-11-25), **firmware** |
| `0xA9` | end the session (does **not** clear the stream bit — the driver clears it with a `0x06` write) | **verified**, **firmware** |
| `0xB1` | reset the calibration of all keys to the default bottom value and save it | **firmware** |

All three take one data byte `00` at offset 0 and get a normal `AA` reply (**verified** for `0xA8`/`0xA9`).

During a session (**firmware**, Jet75-II V116): every key that gets pressed has its stored bottom value reset;
after two stable deep presses its calibration status (depth-stream byte 10) goes `00` → `01` → `FF` and the new
bottom value is stored; the main loop then writes the calibration tables to flash.

**Verified 2026-11-25** with the open driver's guided calibration (`mchose-gui`, Jet75-II V116): all 80 keys
calibrated by pressing each fully down twice; statuses went `00` → `01` → `FF` as above, and travel was correct
afterwards. `0xB1` was not used.

**Risk:** a partial but steady press during a session can be stored as the new "bottom", which distorts all
travel values of that key afterwards. So:

- start a session only for calibration, never just to stream depth — use the FuncConfig bit for that
  ([depth-stream.md](depth-stream.md));
- ask for full presses held at the bottom for a moment, and show the per-key status (byte 10 of the
  stream) so the user sees which keys are done;
- end the session without the keyboard (mouse, a timeout), otherwise the key used to end it is half-way;
- after `0xA9` write FuncConfig with the debug bit as it was before the session, even if `0x05` already
  shows it clear (`0xA8` set it in RAM).

How the open driver does it: [driver README](https://github.com/open-he-mchose/driver#calibration).

With FuncConfig byte 7 bit 2 (travelCheck) set, the firmware also adjusts calibration automatically during
normal use (**firmware**).
