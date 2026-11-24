# Jet75-II — key matrix

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

The keyboard addresses keys by **matrix index** 0–79, not by physical position. The same index is
used by every per-key structure: keymap (3 bytes/key), trigger settings (8 bytes/key), stored and live
colours (3 bytes/key) and the depth stream. Slots 80–127 exist in the tables but are unused and contain
`f0 f0 f0` in the keymap.

- Table read from the keyboard's **factory** layer-0 keymap with command `0x07` (**verified**, V116).
- **Light index = key index** (**verified**: live colours at indices 71/10/61/11 lit exactly W/A/S/D).
- Key codes are `[type, code1, code2]`; `10 00 xx` = plain key with HID usage `xx`, `10 mm 00` = modifier
  bit `mm`, `f0 ff 01` = Fn — see [key codes](../../protocols/glw/keymap-and-keycodes.md).

| Index | Key | Default code | | Index | Key | Default code |
|---|---|---|---|---|---|---|
| 0 | Q | `10 00 14` | | 40 | \` | `10 00 35` |
| 1 | E | `10 00 08` | | 41 | 3 | `10 00 20` |
| 2 | Y | `10 00 1c` | | 42 | T | `10 00 17` |
| 3 | - | `10 00 2d` | | 43 | I | `10 00 0c` |
| 4 | Enter | `10 00 28` | | 44 | Backspace | `10 00 2a` |
| 5 | F6 | `10 00 3f` | | 45 | F8 | `10 00 41` |
| 6 | C | `10 00 06` | | 46 | LCtrl | `10 01 00` |
| 7 | . | `10 00 37` | | 47 | J | `10 00 0d` |
| 8 | Left | `10 00 50` | | 48 | L | `10 00 0f` |
| 9 | Delete | `10 00 4c` | | 49 | F12 | `10 00 45` |
| 10 | A | `10 00 04` | | 50 | Esc | `10 00 29` |
| 11 | D | `10 00 07` | | 51 | 2 | `10 00 1f` |
| 12 | G | `10 00 0a` | | 52 | 5 | `10 00 22` |
| 13 | O | `10 00 12` | | 53 | 8 | `10 00 25` |
| 14 | PgUp | `10 00 4b` | | 54 | = | `10 00 2e` |
| 15 | F5 | `10 00 3e` | | 55 | F3 | `10 00 3c` |
| 16 | X | `10 00 1b` | | 56 | LAlt | `10 04 00` |
| 17 | , | `10 00 36` | | 57 | M | `10 00 10` |
| 18 | Up | `10 00 52` | | 58 | / | `10 00 38` |
| 19 | Home | `10 00 4a` | | 59 | F11 | `10 00 44` |
| 20 | Z | `10 00 1d` | | 60 | CapsLock | `10 00 39` |
| 21 | R | `10 00 15` | | 61 | S | `10 00 16` |
| 22 | H | `10 00 0b` | | 62 | F | `10 00 09` |
| 23 | P | `10 00 13` | | 63 | U | `10 00 18` |
| 24 | PgDn | `10 00 4e` | | 64 | ] | `10 00 30` |
| 25 | F4 | `10 00 3d` | | 65 | F1 | `10 00 3a` |
| 26 | B | `10 00 05` | | 66 | LShift | `10 02 00` |
| 27 | K | `10 00 0e` | | 67 | N | `10 00 11` |
| 28 | RShift | `10 20 00` | | 68 | ; | `10 00 33` |
| 29 | Down | `10 00 51` | | 69 | F9 | `10 00 42` |
| 30 | 1 | `10 00 1e` | | 70 | Tab | `10 00 2b` |
| 31 | 4 | `10 00 21` | | 71 | W | `10 00 1a` |
| 32 | 7 | `10 00 24` | | 72 | 6 | `10 00 23` |
| 33 | 0 | `10 00 27` | | 73 | 9 | `10 00 26` |
| 34 | \ | `10 00 31` | | 74 | [ | `10 00 2f` |
| 35 | F7 | `10 00 40` | | 75 | F2 | `10 00 3b` |
| 36 | V | `10 00 19` | | 76 | LGui | `10 08 00` |
| 37 | Fn | `f0 ff 01` | | 77 | Space | `10 00 2c` |
| 38 | RCtrl | `10 10 00` | | 78 | ' | `10 00 34` |
| 39 | Right | `10 00 4f` | | 79 | F10 | `10 00 43` |

## Physical layout (75 %, 80 keys)

Key set from the keymap (**verified**); the right-hand column checked on the physical board (**verified**: Delete
top right, below it Home, PgUp, PgDn); key widths **inferred**:

| Row | Keys |
|---|---|
| 1 | Esc, F1–F12, Delete |
| 2 | `` ` `` 1 2 3 4 5 6 7 8 9 0 - = Backspace Home |
| 3 | Tab Q W E R T Y U I O P [ ] \ PgUp |
| 4 | CapsLock A S D F G H J K L ; ' Enter PgDn |
| 5 | LShift Z X C V B N M , . / RShift ↑ |
| 6 | LCtrl LGui LAlt Space Fn RCtrl ← ↓ → |

There is no End/Insert/RAlt/PrtSc key on the physical board; `Delete`'s Fn layer maps to Insert.
