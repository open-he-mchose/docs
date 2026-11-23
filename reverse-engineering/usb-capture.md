# Capturing USB traffic on Linux

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

1. Load `usbmon` (`modprobe usbmon`) and give your user read access to `/dev/usbmonN`
   (e.g. a udev rule `SUBSYSTEM=="usbmon", GROUP="plugdev", MODE="0640"`).
2. Find the keyboard's bus with `lsusb` and capture that bus with Wireshark/`dumpcap -i usbmonN`.
3. Use the official driver in Chrome/Chromium (WebHID) and change one setting at a time; note the time.
4. Filter the configuration interface's endpoints (Jet75-II: OUT `0x04`, IN `0x82`) and export the
   64-byte payloads; check the checksum of every request (see [framing](../protocols/glw/framing.md)).

Alternatively read the vendor interface directly: a raw-report logger on the keyboard's other `hidraw` nodes
next to Linux key events (`/dev/input/event*`) shows what the keyboard sends versus what the OS makes of it —
this is how the NKRO descriptor bug was proven.

**Privacy:** captures contain every key typed during the recording (input reports). Never publish raw
captures; publish trimmed packet excerpts only.

Close the official driver tab before using your own tools: two programs on the same interface steal each
other's replies.
