# `glw` — firmware update (not exercised)

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

> Nothing on this page was tried on hardware. A failed update can leave the keyboard unusable.

Known from the web driver and the firmware (**driver**, **firmware**):

1. Enter the bootloader: raw packet `5F 06 00 52 01 00 00 00 51 00 AA BB` on the configuration interface.
   The keyboard re-enumerates with the bootloader PID listed in [devices.json](../../data/devices.json)
   (Jet75-II: `0x41E4:0x211B`).
2. Erase: `81 07 a0 a1 s0 s1 f` (start and size as little-endian 16-bit values, flag byte).
3. Write: `80 len addr0 addr1 addr2 addr3 data[≤32]` (32-bit little-endian byte offset), repeated.
4. Verify: `82 len addr… data…` with the same chunks.
5. Finish: `83 01 00 00 00`, then `84 01 00 00 00`.

Each raw packet is acknowledged by a reply whose byte 0 is `00` and byte 1 is `00` (byte 1 = `01` means
error). The driver retries twice and uses fixed delays (5 s after erase).

The official update images on the vendor's CDN are raw application images linked at flash `0x5000`
(**firmware**, Jet75-II).
