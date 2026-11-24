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
| Calibration (safely) | 📋 |
| Firmware update protocol (documented from analysis; not exercised) | 📋 |
| Earlier firmware versions (V111–V115) | ✅ |

Details: [Jet75-II open questions](keyboards/jet75-ii/open-questions.md).

## 2. Open driver 🚧

Repository: [`open-he-mchose/driver`](https://github.com/open-he-mchose/driver). The `mchosectl` command-line tool
covers what the official driver configures on the Jet75-II, tested on hardware: profiles (switch, rotation, copy),
report rate, lighting (effects, stored and live colours), trigger settings, keymap, macros, advanced keys (DKS,
Toggle, Mod-Tap, RS, SOCD, LT), backup / restore, depth stream. ✅ Released:
[mchosectl 0.1.0](https://github.com/open-he-mchose/driver/releases) for Linux and Windows.

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

Done (first version): visual keyboard with click / drag selection; actuation and rapid trigger; remapping without
typing (key picker, factory default, disable, media keys); lighting effect / brightness / speed / colour; live key
depth; backup / restore (same files as `mchosectl`); profile switching; automatic backup before the first change.

Planned, roughly in this order:

| # | Feature | Notes |
|---|---|---|
| 1 | GUI builds in CI, release 0.2.0 | Windows: zip with the Qt DLLs (`windeployqt`); Linux: AppImage with the udev rule. Qt linked dynamically (LGPL) |
| 2 | Layers | Edit the Fn and Mac layers, not only layer 0; warn about the reset codes (Fn+Esc factory reset, Fn+Backspace calibration reset) |
| 3 | Macro editor | List M1–M16, steps (press / release / delay), record from the keyboard, bind to a key with a play mode (once / hold / toggle / N times) |
| 4 | Advanced-key editor | DKS drawn as the four press phases, Mod-Tap, Toggle, Snap Tap / RS / LT pairs; shows exactly what is stored; `doctor` highlights broken bindings |
| 5 | Profiles | Rotation of the next-profile key, copy a profile, names |
| 6 | Per-key colours | Paint selected keys on the keyboard view; preview with live colours before writing to flash |
| 7 | **Scripted lighting** | See below |
| 8 | Other settings | Report rate (the keyboard reboots; reconnect automatically), Win / Alt+Tab / Alt+F4 / Menu locks, Windows / Mac mode |
| 9 | Depth graph | Travel of a selected key over time with the actuation and rapid-trigger points |
| 10 | Translations | Russian first (Qt Linguist), language from the system |

### Scripted lighting (planned)

Custom effects that run on the computer and are shown with **live colours** (RAM only, no flash wear; the keyboard
returns to its own effect a few seconds after the script stops).

- **Language: JavaScript** (Qt's built-in engine in the GUI), so no extra runtime is needed on Windows. The same
  script API is meant for `mchosectl light script FILE` later (with a small embedded engine such as QuickJS),
  keeping `core` free of script dependencies.
- **Script API (draft):** the script defines `frame(t, dt, keys, input)` and returns one colour per key, called
  ~25–30 times per second (the rate tested on the keyboard). `keys` gives each key's matrix index, name and
  position in key units (from the model layout) so effects can be spatial (waves, ripples); `input` holds the keys
  pressed since the last frame. Helpers: `hsv()`, `mix()`, `rgb()`; optional `init()` and user parameters
  (speed, colours) shown as controls in the GUI.
- **Reacting to key presses** uses the operating system's key events (Linux: evdev with the existing udev access
  rule; Windows: raw input), because the keyboard's depth stream pauses while colours are being sent. So effects can
  react to presses and releases, **not to key depth**.
- **Built-in examples:** typing ripple, heat map of key usage, fire, rain, Game of Life, audio level meter (later).
- **Safety:** scripts only produce colours; they cannot write settings to the keyboard. A script that throws or
  takes too long is stopped and the keyboard falls back to its stored effect.
- Editor in the GUI with live reload, a gallery of example effects, import / export of `.js` files.

## Alongside

- ✅ [`linux-fixes`](https://github.com/open-he-mchose/linux-fixes): HID-BPF descriptor fix (Snap Tap, macros, >6 keys)
  and udev rules for Linux.
- 📋 Other MCHOSE magnetic models — needs owners of those keyboards; see
  [keyboards](keyboards/README.md) and open an issue *Add / research a keyboard model*.
- 📋 `qhw` protocol family (G98 V3, K87 V3).
