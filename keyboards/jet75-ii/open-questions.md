# Jet75-II — open questions

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

- **Macros** — see [macros](../../protocols/glw/macros.md). Still open: where the official driver keeps macro
  names and default delays on this model (custom-data offset beyond the per-profile area, or browser storage);
  untested firmware details (different macro key during playback, modifier left down on early release).
- **Profiles** — see [profiles](../../protocols/glw/profiles.md). Still open: the unidentified byte 4 of `A3`;
  how the official driver decides to bind `F0 FA` (next profile).
- **Special codes** — see [keymap](../../protocols/glw/keymap-and-keycodes.md#special-codes-f0-xx-yy). Still open: the
  exact behaviour of `F0 03` (WASD swap), `F0 2B` (per-key colour mode) and `F0 3B`; whether the Jet75-II has a
  visible side light at all (its FuncConfig fields change).
- **Stream bytes 4–5 and 8**: byte 8 behaves like the rapid-trigger accumulator (**inferred**).
- **FuncConfig**: meaning of the other bits of byte 0 (`50` on all profiles; the bootloader may read them);
  the firmware's debounce table values; what "bottom rapid-trigger mode" changes exactly. The remaining
  undocumented bytes are not read by the Jet75-II firmware.
- **Custom data area** (`0xF1`/`0xF2`): full map of the JSON blobs the driver stores.
- **Calibration reset** (`0xB1`) not exercised on hardware (the session commands `0xA8`/`0xA9` are verified).
- **Firmware update protocol**: packet sequence known from the driver/firmware, never exercised.
- **Updater image selection**: confirm by decompiling the updater that the bundled Ace 60 Pro image is never
  flashed to a Jet75-II.
