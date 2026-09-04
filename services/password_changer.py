import requests

from config import BASE_URL, HEADERS_BASE, ID_DOCUMENTO


class ErrorServicio(Exception):
    pass


class PasswordChanger:
    def __init__(self):
        self.session = requests.Session()

    def verificar_usuario(self, nu_documento):
        url = f"{BASE_URL}/usermanagement/usuario/resetpassword/verificar"
        params = {"id-documento": ID_DOCUMENTO, "nu-documento": nu_documento}
        headers = {**HEADERS_BASE}

        resp = self.session.get(url, params=params, headers=headers)
        data = resp.json()

        if not data.get("succes"):
            raise ErrorServicio(data.get("description"))

        return {
            "token": data["data"]["token"]["token"],
            "celular": data["data"]["sNumeroCelular"],
        }

    def enviar_codigo(self, token, email):
        url = f"{BASE_URL}/usermanagement/email/enviar"
        headers = {**HEADERS_BASE, "X-Validate-Identity": token, "Content-Type": "application/json"}
        body = {"nInMotivo": 10140202, "sEmailTo": email}

        resp = self.session.post(url, json=body, headers=headers)
        data = resp.json()

        if not data.get("succes"):
            raise ErrorServicio(data.get("description"))

        return data

    def cambiar_contrasena(self, token, nu_documento, email, codigo, nueva_contrasena, numero_celular):
        url = f"{BASE_URL}/usermanagement/usuario/resetpassword/confirmar"
        headers = {**HEADERS_BASE, "X-Validate-Identity": token, "Content-Type": "application/json"}
        body = {
            "bIndicadorEmail": False,
            "nInDocIdentidad": ID_DOCUMENTO,
            "sCodigoCelular": "",
            "sCodigoEmail": codigo,
            "sNuDocIdentidad": nu_documento,
            "sNumeroCelular": numero_celular,
            "sEmail": email,
            "sPassword": nueva_contrasena,
            "sRePassword": nueva_contrasena,
            "nInGenero": 10080201,
        }

        resp = self.session.post(url, json=body, headers=headers)
        data = resp.json()

        if not data.get("succes"):
            raise ErrorServicio(data.get("description"))

        return data
