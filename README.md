# bdh-app-vacation-mode

Black Diamond Hub app: Vacation / home mode switching via Home Assistant and the bdl_modes AppDaemon app. Moved out of
[BlackDiamondHub](https://github.com/blackdiamondlodge/BlackDiamondHub) and
installed into the hub through the `blackdiamondhub.plugins` entry point
(see [bdh-sdk](https://github.com/blackdiamondlodge/bdh-sdk)).

Page: `/vacation_mode/`.

## Container (hub API 2)

Since 2.0.0 the app runs in its own container and talks to Home Assistant through the hub
broker (`bdh_sdk.ha`), not with the hub's HA token.

- Permissions are exactly what the built-in steps in `steps.py` use. The steps are fixed in
  code, not user-configurable, so each service is granted by name:
  `ha.call:switch.turn_on|turn_off`, `ha.call:input_boolean.turn_on|turn_off`,
  `ha.call:number.set_value`, `ha.call:climate.set_temperature|set_preset_mode|set_hvac_mode`.
  Reads: `input_boolean.home_away_mode_enabled` (the away flag),
  `sensor.hvac_load_shift_metrics_outdoor_avg_day` (heating/cooling season) and
  `switch.*`, `number.*`, `climate.*` (checking each target reached its new state). A test
  checks the grants cover every step for both seasons.
- `network: lan`: the bdl_modes AppDaemon endpoint is on the LAN (`192.168.10.217:5050`).
- `lifecycle: always`, `memory_mb: 96`: a run takes minutes in a background thread and must
  not be stopped as idle part-way through.

Settings (Settings page, or seed them):

| Key | Type | Was (hub env) |
| --- | --- | --- |
| `modes_url` | string | `BDL_MODES_URL` |
| `modes_api_key` | secret | `BDL_MODES_API_KEY` |
| `preheat` | bool | `BDL_MODES_PREHEAT` |

`modes_api_key` is read with `bdh_sdk.secrets.get` (the vault's legacy-plain migration
moves an existing value into the secret store), falling back to the old setting. In the
container, settings come from the hub through the broker; `BDL_MODES_*` and
`BDH_VACATION_MODE_*` environment variables on the hub are not visible to the app. Nothing
is stored in the database, so no data migration is needed.

CI's `image` job (from bdh-sdk's `app-ci.yml`) locks the dependencies against the hub's app
runtime, builds the app's image and smoke-tests it the way the supervisor runs it.

## Development

CI (`.github/workflows/ci.yml`) uses the reusable `app-ci.yml` from
bdh-sdk. It builds the wheel, installs it next to the hub, then runs
`hub_smoke`, the app tests and the selenium tests.

To release, bump `version` in `pyproject.toml`. When that lands on
`main`, `release.yml` tags it and publishes the wheel, and the release
notes include the hashed line for the hub's `sites/<site>/apps.txt`.
