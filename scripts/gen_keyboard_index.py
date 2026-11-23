#!/usr/bin/env python3
"""Regenerate keyboards/README.md from data/devices.json.  python3 scripts/gen_keyboard_index.py"""
import json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EDITION = {"(电竞版)": " (Esports edition)", "(超竞版)": " (Ultra edition)"}
DOCUMENTED = {("0x41E4", "0x211A"): "jet75-ii/README.md"}   # (vid, pid) -> page

data = json.load(open(os.path.join(ROOT, "data/devices.json")))
rows = []
for d in data["devices"]:
    name = d.get("fullName") or d.get("name") or d["key"]
    for zh, en in EDITION.items():
        name = name.replace(zh, en)
    boot = (d.get("bootloader") or "").replace("_", ":") or "—"
    rx = ", ".join("%s:%s" % (r["vid"], r["pid"]) for r in d.get("receivers", [])) or "—"
    page = DOCUMENTED.get((d["vid"], d["pid"]))
    status = "[documented, verified](%s)" % page if page else "not researched"
    rows.append("| %s | `%s:%s` | `%s` | `%s` | %s | %s | %s |" % (
        name, d["vid"], d["pid"], d["protocol"], boot, d.get("fwVersion", "—"), rx, status))

out = """# MCHOSE magnetic keyboards

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

Models listed by the official web driver's magnetic-keyboard ("cizhou") section, generated from
[`data/devices.json`](../data/devices.json) by `scripts/gen_keyboard_index.py` (**driver**, build of 2026-11).
"FW" is the newest firmware version the driver offers; "Receivers" are the 2.4 GHz dongle identities of
wireless models. Chinese edition suffixes: 电竞版 = Esports edition, 超竞版 = Ultra edition.

| Model | VID:PID | Protocol | Bootloader | FW | Receivers | Status |
|---|---|---|---|---|---|---|
""" + "\n".join(rows) + """

Notes (**driver**):

- `glw` models share the protocol described in [protocols/glw](../protocols/glw/README.md); per-model data
  (key matrix, switch types, feature flags) differs. `qhw` models use a different protocol
  ([protocols/qhw](../protocols/qhw/README.md)).
- Two vendor IDs are used: `0x41E4` (older models) and `0x3837` (newer models). The bootloader enumerates
  under its own PID, listed in the table.
- To document a new model, copy the structure of [jet75-ii/](jet75-ii/README.md).
"""
open(os.path.join(ROOT, "keyboards/README.md"), "w").write(out)
print("wrote keyboards/README.md with %d models" % len(rows))
