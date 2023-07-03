from collections import defaultdict

from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["settings.toml", ".secrets.toml"],
    envvar_prefix=False,
)
ENVIRON_TYPE = settings.get("environ_type", "dev")
SETTINGS = settings.get(ENVIRON_TYPE) or defaultdict(lambda: "missing data")
print(ENVIRON_TYPE)
print(SETTINGS)


# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
