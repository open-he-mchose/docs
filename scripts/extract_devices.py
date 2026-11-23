#!/usr/bin/env python3
"""Extract the MCHOSE Hall-effect keyboard table from the official web driver into data/devices.json.

The magnetic-keyboard part of the web driver (www.mchose.com.cn/cizhou/, a Next.js app) contains a
device table: one object literal per model with `_identity` (VID/PID), protocol family
(`manufacturer`, default "glw"), firmware versions, bootloader PID, HID filters, switch options and
feature flags. This script reads a locally saved copy of that chunk and keeps only plain facts
(identifiers, names, numbers, flags) — no vendor code and no download URLs.

    python3 scripts/extract_devices.py path/to/cizhou/_next/static/chunks/<chunk-with-device-table>.js > data/devices.json

The chunk is the one that contains `ALL_DEVICE_DATA` / `_identity:{vendorId:` (in the 2026-11 build:
`3050-4fde3581e71b2bbc.js`, module 83050).
"""
import json, re, sys


IDENT = re.compile(r'_identity:\{vendorId:(\d+),productId:(\d+),productName:(null|"[^"]*"),key:"([^"]+)"\}')


def enclosing_start(text, pos):
    """Index of the '{' that opens the object literal containing position pos."""
    depth = 0
    for k in range(pos - 1, -1, -1):
        c = text[k]
        if c == "}":
            depth += 1
        elif c == "{":
            if depth == 0:
                return k
            depth -= 1
    raise ValueError("no enclosing object")


def objects(text):
    """Yield (object_text, is_receiver) for every object literal that has an _identity field.
    Objects inside a `spread:[...]` list are the 2.4 GHz receiver identities of the model before them."""
    for m in IDENT.finditer(text):
        s = enclosing_start(text, m.start())
        receiver = text[max(0, s - 8):s].endswith("spread:[")
        depth, quote, k = 0, None, s
        while k < len(text):
            c = text[k]
            if quote:
                if c == "\\":
                    k += 2
                    continue
                if c == quote:
                    quote = None
            elif c in "\"'`":
                quote = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        yield text[s:k + 1], receiver


def top_level(obj):
    """Text of the object with nested {...} / [...] blanked, so field regexes only hit top-level keys."""
    out, depth, quote = [], 0, None
    for i, c in enumerate(obj):
        if quote:
            out.append(c if depth <= 1 else " ")
            if c == quote and obj[i - 1] != "\\":
                quote = None
            continue
        if c in "\"'`":
            quote = c
            out.append(c if depth <= 1 else " ")
            continue
        if c in "{[":
            depth += 1
            out.append(c if depth <= 1 else " ")
            continue
        if c in "}]":
            out.append(c if depth <= 1 else " ")
            depth -= 1
            continue
        out.append(c if depth <= 1 else " ")
    return "".join(out)


def field(text, name, kind):
    pats = {"str": r'(?:[,{]|^)%s:"([^"]*)"', "num": r'(?:[,{]|^)%s:(-?\d+(?:\.\d+)?)', "bool": r'(?:[,{]|^)%s:(!0|!1|true|false)'}
    m = re.search(pats[kind] % re.escape(name), text)
    if not m:
        return None
    v = m.group(1)
    if kind == "num":
        return float(v) if "." in v else int(v)
    if kind == "bool":
        return v in ("!0", "true")
    return v


def parse(obj):
    top = top_level(obj)
    ident = IDENT.search(top) or IDENT.search(obj)
    if not ident:
        return None
    d = {
        "key": ident.group(4),
        "vid": "0x%04X" % int(ident.group(1)),
        "pid": "0x%04X" % int(ident.group(2)),
        "productName": None if ident.group(3) == "null" else ident.group(3).strip('"'),
        "id": field(top, "id", "str"),
        "name": field(top, "name", "str"),
        "fullName": field(top, "fullName", "str"),
        "storageKey": field(top, "storageKey", "str"),
        "protocol": field(top, "manufacturer", "str") or "glw",   # driver default when absent
        "type": field(top, "type", "num"),
        "fwVersion": field(top, "fwVersion", "num"),
        "minFwVersion": field(top, "minFwVersion", "num"),
        "bootloader": field(top, "bootUpdateMode", "str"),
        "wireless": field(top, "isWireless", "bool"),
        "testing": field(top, "isTesting", "bool"),
        "maxKeyCount": field(top, "maxKeyCount", "num"),
        "glbKeyboardKey": field(top, "glbKeyboardKey", "str"),
    }
    filters = re.search(r"hidFilters:\[(.*?)\]", obj)
    if filters:
        d["hidFilters"] = [{"usagePage": int(a), "usage": int(b)} for a, b in re.findall(r"usagePage:(\d+),usage:(\d+)", filters.group(1))]
    prec = re.search(r"precisionConfig:\{([^}]*)\}", obj)
    if prec:
        d["precisionMm"] = sorted(float(k) for k, v in re.findall(r"(\.?\d*\.?\d+):(!0|!1)", prec.group(1)) if v == "!0")
    feats = re.search(r"featSupport:\{(.*?)\}\}?(?:,|$)", obj)
    if feats:
        d["features"] = sorted(set(re.findall(r"([A-Za-z][A-Za-z0-9]+):", feats.group(1))) - {"minFW"})
    return {k: v for k, v in d.items() if v is not None}


def main():
    text = open(sys.argv[1], encoding="utf-8").read()
    devices, seen = [], set()
    for obj, receiver in objects(text):
        d = parse(obj)
        if not d:
            continue
        if receiver:
            if devices:
                r = {"vid": d["vid"], "pid": d["pid"], "productName": d.get("productName")}
                if d.get("bootloader"):
                    r["bootloader"] = d["bootloader"]
                devices[-1].setdefault("receivers", []).append(r)
            continue
        if (d["key"], d.get("productName")) not in seen:
            seen.add((d["key"], d.get("productName")))
            devices.append(d)
    devices.sort(key=lambda d: (d.get("name") or "", d["pid"]))
    json.dump({"source": "MCHOSE web driver (cizhou), device table", "count": len(devices), "devices": devices},
              sys.stdout, indent=1, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
