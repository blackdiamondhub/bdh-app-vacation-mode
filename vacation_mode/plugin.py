from bdh_sdk import OWNER_ONLY, PluginSpec, Setting, Tile
from bdh_sdk.plugins import BOOL, LIFECYCLE_ALWAYS, NETWORK_LAN, SECRET

spec = PluginSpec(
    id="vacation_mode",
    app="vacation_mode",
    urls="vacation_mode.urls",
    tiles=(
        Tile(
            title="Vacation Mode",
            url_name="vacation_mode",
            icon="vacation_mode/hub/icon.svg",
            section="more",
            subtitle="Away & arrival",
            order=30,
            modes=OWNER_ONLY,
        ),
    ),
    settings=(
        Setting("modes_url", "bdl_modes URL",
                help="The bdl_modes AppDaemon endpoint, e.g. http://192.168.10.217:5050/api/appdaemon/"
                     "bdl_modes. Empty uses the built-in Home Assistant steps instead."),
        Setting("modes_api_key", "bdl_modes API key", type=SECRET),
        Setting("preheat", "Pre-heat before arrival", type=BOOL, default=False),
    ),
    api_version=2,
    # Exactly the services and entities the built-in steps (steps.py) use: the
    # steps are fixed in code, not user-configurable. Reads cover the away flag,
    # the season sensor, and checking each switch/number/climate reached its target.
    permissions=(
        "ha.read:input_boolean.home_away_mode_enabled",
        "ha.read:sensor.hvac_load_shift_metrics_outdoor_avg_day",
        "ha.read:switch.*",
        "ha.read:number.*",
        "ha.read:climate.*",
        "ha.call:switch.turn_on",
        "ha.call:switch.turn_off",
        "ha.call:input_boolean.turn_on",
        "ha.call:input_boolean.turn_off",
        "ha.call:number.set_value",
        "ha.call:climate.set_temperature",
        "ha.call:climate.set_preset_mode",
        "ha.call:climate.set_hvac_mode",
    ),
    # The bdl_modes AppDaemon endpoint is on the LAN (192.168.10.217:5050).
    network=NETWORK_LAN,
    # A run takes minutes in a background thread; it must not be stopped as idle mid-run.
    lifecycle=LIFECYCLE_ALWAYS,
    memory_mb=96,
)
