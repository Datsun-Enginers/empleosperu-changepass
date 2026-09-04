from config import BASE_URL, HEADERS_BASE, ID_DOCUMENTO
from http_client import ClienteHTTP, ErrorServicio


class PasswordChanger:
    def __init__(self, cliente=None):
        self.cliente = cliente or ClienteHTTP()

    def verificar_usuario(self, nu_documento):
        url = f"{BASE_URL}/usermanagement/usuario/resetpassword/verificar"
        params = {"id-documento": ID_DOCUMENTO, "nu-documento": nu_documento}
        headers = {**HEADERS_BASE}

        resp = self.cliente.get(url, params=params, headers=headers)
        data = self.cliente.verificar_codigo_http(resp)

        return {
            "token": data["data"]["token"]["token"],
            "celular": data["data"]["sNumeroCelular"],
        }

    def enviar_codigo(self, token, email):
        url = f"{BASE_URL}/usermanagement/email/enviar"
        headers = {**HEADERS_BASE, "X-Validate-Identity": token, "Content-Type": "application/json"}
        body = {"nInMotivo": 10140202, "sEmailTo": email}

        resp = self.cliente.post(url, json=body, headers=headers)
        return self.cliente.verificar_codigo_http(resp)

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

        resp = self.cliente.post(url, json=body, headers=headers)
        return self.cliente.verificar_codigo_http(resp)
