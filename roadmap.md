# Roadmap

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Status: ✅ done · 🚧 in progress · 📋 planned. Plans, not promises — the order may change.

## 1. Complete reverse engineering of the Jet75-II 🚧

The reference model: everything the keyboard can do should be documented and verified on hardware.

| Area | Status |
|---|---|
| USB interfaces, packet framing, command set | ✅ |
| Per-key actuation, rapid trigger, dead zones | ✅ |
| Keymap and key codes | ✅ |
| Lighting: effects, stored colours, live per-key colours | ✅ |
| Key-depth stream (how to enable, packet format, lag-free depth) | ✅ |
| Advanced keys: DKS, Mod-Tap, Toggle, Rapid Strike, Snap Tap (SOCD), LT | ✅ |
| NKRO descriptor bug (Snap Tap, >6 keys) and Linux fix | ✅ |
| Macros: storage format, play modes, binding | ✅ |
| Profiles: switching, base-info fields, notifications | ✅ |
| Fn-layer special codes | ✅ |
| Remaining FuncConfig fields, report-rate values | ✅ |
| Calibration (safely) | ✅ guided calibration verified (GUI item 9); reset `0xB1` not exercised |
| Firmware update protocol (documented from analysis; not exercised) | 📋 |
| Earlier firmware versions (V111–V115) | ✅ |

Details: [Jet75-II open questions](keyboards/jet75-ii/open-questions.md).

## 2. Open driver 🚧

Repository: [`open-he-mchose/driver`](https://github.com/open-he-mchose/driver). The `mchosectl` command-line tool
covers what the official driver configures on the Jet75-II, tested on hardware: profiles (switch, rotation, copy),
report rate, lighting (effects, stored and live colours), trigger settings, keymap, macros, advanced keys (DKS,
Toggle, Mod-Tap, RS, SOCD, LT), backup / restore, depth stream. ✅ Released:
[0.3.2](https://github.com/open-he-mchose/driver/releases) for Linux and Windows.

- Library + command-line tool in **C++20** (CMake, HID access through hidapi) for **Linux and Windows**.
  macOS is not planned for now (not a primary target).
- Everything the official driver can configure: actuation and rapid trigger per key, keymap and layers,
  advanced keys, lighting, profiles, macros.
- Live key depth and live per-key lighting.
- Full backup and restore of all profiles; read-back verification after every write; protection against
  flash-wearing write loops.
- Model support described by data ([devices.json](data/devices.json) + per-model files), so new `glw` models
  can be added without code changes.
- Avoids the [official driver issues](known-issues/web-driver.md) (silently altered DKS settings, slot
  renumbering).

## 3. Cross-platform GUI 🚧

`mchose-gui` in the [driver](https://github.com/open-he-mchose/driver) repository: **Qt 6 (Qt Quick)**, **Windows and
Linux**, an open alternative to the official web driver. It uses the system look (platform style and system colours,
no theme of its own). macOS is not planned for now; Qt and hidapi support it.

Released in 0.2.0 (Windows package; confirmed working on Windows by a user): items 1–8 below — visual keyboard,
actuation and rapid trigger, all layers, macros, advanced keys, profiles, per-key colours, Lua effects, other
settings, backup / restore.

Items 10–13 released in 0.3.0 (Linux AppImage, depth graph, virtual gamepad, Russian translation). 0.3.1: one program per user with a background mode (tray where available), the running effect and script parameters restored on connect, start at login. 0.3.2: item 9, switch calibration (hardware-tested on all keys).

Planned, roughly in this order:

| # | Feature | Notes |
|---|---|---|
| 1 ✅ | GUI builds in CI, release 0.2.0 | Done: Windows zip with the Qt DLLs (`windeployqt`), released 0.2.0. Open: Linux AppImage with the udev rule. Qt linked dynamically (LGPL) |
| 2 ✅ | Layers | Edit the Fn and Mac layers, not only layer 0; warn about the reset codes (Fn+Esc factory reset, Fn+Backspace calibration reset) |
| 3 ✅ | Macro editor | List M1–M16, steps (press / release / delay), record from the keyboard, bind to a key with a play mode (once / hold / toggle / N times) |
| 4 ✅ | Advanced-key editor | DKS drawn as the four press phases, Mod-Tap, Toggle, Snap Tap / RS / LT pairs; shows exactly what is stored; `doctor` highlights broken bindings |
| 5 ✅ | Profiles | Rotation of the next-profile key, copy a profile, names |
| 6 ✅ | Per-key colours | Paint selected keys on the keyboard view; preview with live colours before writing to flash |
| 7 ✅ | **Scripted lighting** | See below |
| 8 ✅ | Other settings | Report rate (the keyboard reboots; reconnect automatically), Win / Alt+Tab / Alt+F4 / Menu locks, Windows / Mac mode |
| 9 ✅ | **Switch calibration** | Guided calibration in the GUI and `mchosectl`: start a session (`0xA8`), show every key's calibration status from the depth stream (byte 10: `00` → `01` → `FF`) on the keyboard view, ask the user to press each key down twice, end the session (`0xA9`). Backup before; "reset calibration" (`0xB1`) only behind a confirmation. See [calibration](protocols/glw/calibration.md) |
| 10 ✅ | Linux AppImage | One-file GUI for any distribution, with the udev rule and install instructions |
| 11 ✅ | Depth graph | Travel of a selected key over time with the actuation and rapid-trigger points |
| 12 ✅ | Gamepad input | Analog keys as a virtual gamepad: key depth → stick axes / triggers, keys → buttons, configurable per key. The firmware has no gamepad mode, so the software reads the depth stream and feeds a virtual controller (Linux: `uinput`; Windows: a virtual-controller driver, to be chosen). The firmware pauses the depth stream for ~0.6 s after every host packet, so it cannot run together with live colours (Lua effects, preview): with the gamepad on, the GUI stops the Lua effect and uses the keyboard's own effect or stored colours |
| 13 ✅ | Translations | Russian first (Qt Linguist), language from the system |

### Scripted lighting ✅

Done: `mchosectl light script FILE.lua` and the GUI's Effects tab (editor, parameters, live preview), with six
examples. Design notes:

Custom effects that run on the computer and are shown with **live colours** (RAM only, no flash wear; the keyboard
returns to its own effect a few seconds after the script stops).

- **Language: Lua** (5.4, MIT, embedded in the program): no runtime to install on Windows, small and fast, and
  independent of Qt, so the **same engine and the same scripts** work in the GUI and in `mchosectl light script FILE`.
  It lives in its own module of the driver (`core` stays free of dependencies).
- **Script API (draft):** the script defines `frame(ctx)`, called ~25–30 times per second (the rate tested on the
  keyboard), and sets colours with `ctx.set(key, r, g, b)` or by returning a table of colours. `ctx.t` / `ctx.dt` give
  the time, `ctx.keys` each key's matrix index, name and position in key units (from the model layout) so effects can
  be spatial (waves, ripples), `ctx.pressed` / `ctx.released` the keys since the last frame. Helpers: `hsv()`, `mix()`,
  `rgb()`; optional `init(ctx)` and user parameters (speed, colours) shown as controls in the GUI.
- **Sandbox:** only safe standard libraries (no `io`, `os`, no native modules); a per-frame instruction limit stops
  runaway scripts.
- **Reacting to key presses** uses the operating system's key events (Linux: evdev with the existing udev access
  rule; Windows: raw input), because the keyboard's depth stream pauses while colours are being sent. So effects can
  react to presses and releases, **not to key depth**.
- **Built-in examples:** typing ripple, heat map of key usage, fire, rain, Game of Life, audio level meter (later).
- **Safety:** scripts only produce colours; they cannot write settings to the keyboard. A script that raises an
  error or exceeds the instruction limit is stopped and the keyboard falls back to its stored effect.
- Editor in the GUI with live reload, a gallery of example effects, import / export of `.lua` files.

## Alongside

- ✅ [`linux-fixes`](https://github.com/open-he-mchose/linux-fixes): HID-BPF descriptor fix (Snap Tap, macros, >6 keys)
  and udev rules for Linux.
- 📋 Other MCHOSE magnetic models — needs owners of those keyboards; see
  [keyboards](keyboards/README.md) and open an issue *Add / research a keyboard model*.
- 📋 `qhw` protocol family (G98 V3, K87 V3).
