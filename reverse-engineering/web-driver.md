# The official web driver

*AI-generated (Claude, Anthropic); checked on real hardware only where marked **verified**. Report errors via issues.*

MCHOSE configures its keyboards through a WebHID web app ("M HUB"). The magnetic-keyboard part is a
separate Next.js app under the path `/cizhou/` ("cizhou" = 磁轴, magnetic switch), loaded in an iframe.
Notes below refer to the build of November 2026; chunk and module numbers change between builds.

## Getting it

Save the page and its JavaScript chunks for offline reading: the `index.html` of `/cizhou/` lists the
initial chunks; the webpack runtime chunk (`webpack-*.js`) contains the id → hash map for the lazily
loaded ones. Translations are JSON files at `/cizhou/locales/<lang>/common.json`. Do not redistribute the
files — they are the vendor's code.

## Where things are (2026-11 build)

| What | Where |
|---|---|
| Device table (all magnetic models, VID/PID, protocol family, firmware versions, bootloader PID, switch options, feature flags) | module `83050` (chunk `3050-…`); extract with [`scripts/extract_devices.py`](../scripts/extract_devices.py) |
| `glw` channel: packet framing, command numbers, chunking | module `45474` (class with `getInfo`, `getFuncConfig`, `setAllKeyTravel` …) |
| `glw` SDK: struct (de)serialisers (FuncConfig, trigger entry, lighting, DKS) | module `14905` |
| Base transport class (queue, retries, report sending) | module `82398` |
| `qhw` SDK and channel | modules `86369`, `53542` |
| Advanced-key editor (key codes `0x90–0x95`, slot allocation) | chunk `9849-…`; helpers in chunk `3996-…` |
| Depth-stream logic (`DebugAndCalibrationDetector`) and consumer | chunk `3996-…` |
| Per-model layouts (key positions, effect lists) | lazily loaded chunks, e.g. module `98070` for Jet 75 |

The main M HUB bundle (`/assets/main-*.js`, ~7.7 MB) only identifies magnetic models (a `czDeviceName`
list) and hands them over to the `/cizhou/` app.

## Reading tips

- Minified webpack modules can be cut out by brace matching from `NNNNN:function(e,t,i){` and split on
  `;` for reading.
- Search for method names (`openDebug`, `setAllKeyTravel`, `getKeyTrigger`) and i18n keys; the English
  locale explains UI numbers (e.g. key `563` = "Last Input Priority").
- The driver encodes structures in small functions next to each other (decode/encode pairs), which makes
  field layouts easy to read off.
