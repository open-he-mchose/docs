# Jet75-II — open questions

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

- **Macros** — see [macros](../../protocols/glw/macros.md). Still open: where the official driver keeps macro
  names and default delays on this model (custom-data offset beyond the per-profile area, or browser storage);
  untested firmware details (different macro key during playback, modifier left down on early release).
- **Profiles**: switching via base info (`0x0E`), meaning of all base-info bytes, the unsolicited
  `0xA1`/`0xA4` notifications.
- **Fn-layer special codes** seen in layer 1: `f0 a0 00`, `f0 32 00` and others besides the known
  `f0 fa 00` (rapid-trigger toggle), `f0 34 00` (brightness), `f0 1e 00` (BackHome).
- **Stream bytes 4–5 and 8**: byte 8 behaves like the rapid-trigger accumulator (**inferred**).
- **FuncConfig gaps**: bytes 0, 2–3 (marker `AA BB`), 13, 17–19, 21–22, 28, 39, 43, 52–63.
- **Custom data area** (`0xF1`/`0xF2`): full map of the JSON blobs the driver stores.
- **Calibration** not exercised on hardware (deliberately: it rewrites stored calibration).
- **Firmware update protocol**: packet sequence known from the driver/firmware, never exercised.
- **Earlier firmware**: is the NKRO descriptor correct in V111–V115 (images embedded in the Windows updater)?
- **Report rate** values of the FuncConfig nibble and the `tickRate` nibble.
- **Second image in the Windows updater**: besides the Jet75-II application, every updater version bundles
  an identical second image whose strings say "Ace 60 Pro" — purpose unknown.
