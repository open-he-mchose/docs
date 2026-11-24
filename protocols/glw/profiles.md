# `glw` — profiles

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Jet75-II values (firmware V116). Sources: the official web driver (**driver**), static analysis of the firmware
(**firmware**) and tests on a Jet75-II (**verified**, see [verification log](../../keyboards/jet75-ii/verification.md)
tests 28–31).

## What a profile contains

The keyboard has 4 profiles (0–3). Each profile has its own:

- [FuncConfig](funcconfig.md) (performance and lighting settings);
- 4 keymap layers ([keymap](keymap-and-keycodes.md));
- per-key trigger settings, stored per-key colours, DKS / MT / Toggle tables;
- part of the custom data area used by the official driver (`0xF1`/`0xF2`: profile names, lighting JSON).

**Shared by all profiles:** the [macro area](macros.md) and the calibration tables.

## Base info (`0x04` read / `0x0E` write)

The firmware stores and uses 6 bytes (flash `0x20200`) (**firmware**, **verified**):

| Byte | Meaning |
|---|---|
| 0 | active position: index into the order list (not the profile number) |
| 1 | length: number of profiles in the rotation, 1–4 |
| 2–5 | order: the profile numbers 0–3, a permutation; positions `0 … length−1` are in the rotation |
| 6–7 | `AA BB` marker |
| 8–55 | filler (`A2` on the test keyboard) |

The active profile is `order[active position]`. At boot the firmware uses position 0 if the stored position is
not below `length`, and profile 0 if the order entry is not below 4 (**firmware**).

Example from the test keyboard: `00 02 00 01 02 03 AA BB`. Position 0, two profiles in the rotation, natural
order, so profile 0 is active and Fn+Enter toggles between profiles 0 and 1 (**verified**).

**Driver interpretation (driver).** If bytes 2–5 are a permutation of 0–3, the driver treats the model as
supporting ordered profiles. If the position and length are in range, it treats it as supporting several profiles.
The driver writes the whole 56-byte block back with the new position, length and order. It refuses a length
outside 1–4, a position outside `0 … length−1` and an order that is not a permutation. If the stored position
is out of range, it "repairs" the block by activating `order[0]`.

## Switching the profile

| Way | How | Evidence |
|---|---|---|
| Host | write the new position with `0x0E` (a 1-byte write at offset 0 is enough). Nothing happens if the active profile stays the same | **verified** |
| Keyboard | key code `F0 FA 00` = **next profile**: position = (position + 1) mod length | **verified** (Fn+Enter) |

`F0 FA 00` is not in the factory keymap. On the test keyboard it was bound to Fn+Enter in profiles 0 and 1,
presumably by the official driver. The driver's key list labels code `FA` "RT", but the firmware and the test
show that it switches the profile.

### What the firmware does on a switch (**firmware**)

1. Releases all keys (clears the 6-key buffer, the NKRO bitmap and the modifiers).
2. Loads the new profile's FuncConfig into RAM and resets the current layer to the profile's base layer
   (FuncConfig byte 1, see [below](#layers-and-funcconfig-byte-1)).
3. Re-applies the trigger table and updates the lighting.
4. Sends the [`A1` notification](#notifications).
5. As soon as no key has been pressed for 200 ms, it saves base info **and the new profile's FuncConfig** to
   flash and sends `A3`.

**Every profile switch costs two flash writes**, even from a key press. Avoid switching profiles in a loop.

## Layers and FuncConfig byte 1

- Keymap layers are addressed by an **absolute layer number** `4 × profile + layer` (0–15): the same
  number gives the offset of `0x08`/`0x09` (`512 ×` number).
- FuncConfig byte 1 holds the profile's **base layer** as an absolute number: `4 × profile`, plus 2 when the
  profile is in Mac mode (layer 2 is the Mac layer). On every switch the firmware recomputes it this way
  (**firmware**). The test keyboard had 0 / 4 / 8 / 12 in profiles 0–3 (**verified**).
- The Fn key `F0 FF xx` also uses absolute numbers. On the test keyboard, layer 0 of profile *p* had
  `F0 FF (4p+1)` and layer 2 had `F0 FF (4p+3)` (**verified**). A tool that copies a keymap to another
  profile must rewrite these codes.

## Notifications

Input reports the keyboard sends on the configuration interface without a request:

| Report | When | Layout | Evidence |
|---|---|---|---|
| `A1` | right after a profile switch (host or key) | `A1`, FuncConfig[1], profile, position, `FF FF FF FF`, FuncConfig[8] (light effect), FuncConfig[13], position, zeros | **verified** |
| `A3` | when the firmware saves a changed FuncConfig: after a profile switch, or after settings changed on the keyboard (lighting keys and similar) | `A3`, position, FuncConfig[1], current absolute layer, ?, FuncConfig[5…], … | **verified** (after switches), **firmware** |
| `A2` | after a factory reset | `A2`, current layer, selected FuncConfig bytes | **firmware** |
| `A4` | "profile about to switch" in the driver | not sent by Jet75-II V116 (no code builds it) | **driver**, **firmware** |

Bytes past the documented fields are left over from earlier notifications (one buffer is shared by all
notification types). Ignore them.

Measured timing: the host switch's reply, `A1` 1 ms later, `A3` 41 ms later. After Fn+Enter, `A3` came about
300 ms after `A1`, because the firmware waits until no key has been pressed for 200 ms (**verified**).

The official web driver reacts to `A1`/`A3`: it re-reads base info, FuncConfig, profile names and the lighting
JSON (**verified**: these requests showed up while the driver page was open).

## Notes for tools

- Read base info, change only bytes 0–5, keep the `AA BB` marker, write back and read back.
- After a switch, wait for `A1` (or poll `0x04`) before writing profile-specific settings. Commands that say
  "active profile" (for example the RAM reload of `0x06`) depend on it.
- If another program (for example the official driver in a browser) has the interface open, it sees all the
  replies and notifications too. Run only one configuration program at a time.
