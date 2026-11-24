# Jet75-II — open questions

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

- **Macros** — see [macros](../../protocols/glw/macros.md). Still open: where the official driver keeps macro
  names and default delays on this model (custom-data offset beyond the per-profile area, or browser storage);
  untested firmware details (different macro key during playback, modifier left down on early release).
- **Profiles** — see [profiles](../../protocols/glw/profiles.md). Still open: the unidentified byte 4 of `A3`;
  how the official driver decides to bind `F0 FA` (next profile).
- **Fn-layer special codes** in the factory Fn layer: `a0`, `32`, `2f`, `36`, `04`, `16`, `15`, `05`, `18`, `1a`,
  `fe`, `08`, `33`, `3e`, `02` (`F0 xx 00`). The driver has names for them, but what the firmware actually does
  (handler `fn_6fea`) is not documented yet. Known: `fa` next profile, `ff` Fn.
- **Stream bytes 4–5 and 8**: byte 8 behaves like the rapid-trigger accumulator (**inferred**).
- **FuncConfig gaps**: bytes 0, 2–3 (marker `AA BB`), 13, 17–19, 21–22, 28, 39, 43, 52–63.
- **Custom data area** (`0xF1`/`0xF2`): full map of the JSON blobs the driver stores.
- **Calibration** not exercised on hardware (deliberately: it rewrites stored calibration).
- **Firmware update protocol**: packet sequence known from the driver/firmware, never exercised.
- **Earlier firmware**: is the NKRO descriptor correct in V111–V115 (images embedded in the Windows updater)?
- **Report rate** values of the FuncConfig nibble and the `tickRate` nibble.
- **Second image in the Windows updater**: besides the Jet75-II application, every updater version bundles
  an identical second image whose strings say "Ace 60 Pro" — purpose unknown.
