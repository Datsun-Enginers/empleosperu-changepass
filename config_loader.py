import json
import os
import sys

DEFAULT_CONFIG = {
    "timeout": 30,
    "max_retries": 3,
    "backoff": 1.0,
    "verbose": False,
    "proxies": {},
}


def _config_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "appsettings.json")


def cargar_config():
    config = dict(DEFAULT_CONFIG)
    ruta = _config_path()
    if os.path.exists(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                usuario = json.load(f)
            config.update(usuario)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[warn] No se pudo leer la configuracion: {e}", file=sys.stderr)
    return config
