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
| Earlier firmware versions (V111–V115) | 📋 |

Details: [Jet75-II open questions](keyboards/jet75-ii/open-questions.md).

## 2. Open driver 📋

Repository: `open-he-mchose/driver` (planned).

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

## 3. Cross-platform GUI 📋

A desktop application on top of the driver, built with **Qt 6 (Qt Quick)**, for **Windows and Linux** — an
open alternative to the official web driver. macOS is not planned for now (not a primary target); Qt and
hidapi support it, so it may come later if someone needs it.

- Visual keyboard: select keys, set actuation / rapid trigger, remap.
- Live key-depth view (per-key travel in real time).
- Lighting editor with live preview.
- Advanced-key editor that shows exactly what will be stored (no silent changes).
- Profiles, backup / restore, firmware and device information.

## Alongside

- 📋 `linux-fixes` repository: HID-BPF descriptor fix and udev rules (working locally, to be published).
- 📋 Other MCHOSE magnetic models — needs owners of those keyboards; see
  [keyboards](keyboards/README.md) and open an issue *Add / research a keyboard model*.
- 📋 `qhw` protocol family (G98 V3, K87 V3).
