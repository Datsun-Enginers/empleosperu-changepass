import time

import requests

from logging_setup import get_logger


class ErrorRed(Exception):
    pass


class ErrorHTTP(ErrorRed):
    def __init__(self, status_code, descripcion=""):
        self.status_code = status_code
        super().__init__(f"Error HTTP {status_code}: {descripcion}")


class ErrorServicio(Exception):
    def __init__(self, mensaje="", codigo=None):
        self.codigo = codigo
        super().__init__(mensaje)


def _leer_json(resp):
    try:
        return resp.json()
    except (requests.exceptions.JSONDecodeError, ValueError) as e:
        raise ErrorServicio(f"Respuesta no valida (no es JSON): {e}")


class ClienteHTTP:
    def __init__(self, timeout=30, max_retries=3, backoff=1.0, proxies=None, session=None):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff
        self.proxies = proxies or {}
        self.session = session or requests.Session()
        self.log = get_logger()

    def _ejecutar(self, metodo, url, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("proxies", self.proxies)
        ultimo_error = None

        for intento in range(1, self.max_retries + 1):
            try:
                self.log.debug("[%s] %s (intento %d/%d)", metodo.__name__.upper(), url, intento, self.max_retries)
                resp = metodo(url, **kwargs)
                return resp
            except requests.exceptions.Timeout as e:
                ultimo_error = e
                self.log.warning("Timeout en %s (intento %d)", url, intento)
            except requests.exceptions.ConnectionError as e:
                ultimo_error = e
                self.log.warning("Error de conexion en %s (intento %d)", url, intento)
            except requests.exceptions.RequestException as e:
                raise ErrorRed(f"Fallo de red en {url}: {e}") from e

            if intento < self.max_retries:
                time.sleep(self.backoff * intento)

        raise ErrorRed(f"Fallo tras {self.max_retries} intentos en {url}: {ultimo_error}")

    def get(self, url, **kwargs):
        return self._ejecutar(self.session.get, url, **kwargs)

    def post(self, url, **kwargs):
        return self._ejecutar(self.session.post, url, **kwargs)

    def verificar_codigo_http(self, resp):
        if resp.status_code != 200:
            raise ErrorHTTP(resp.status_code, resp.text[:200])
        data = _leer_json(resp)
        if not data.get("succes"):
            raise ErrorServicio(data.get("description", "Operacion fallida"), data.get("code"))
        return data
