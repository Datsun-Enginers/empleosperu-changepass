import requests
import json
import sys
import time

BASE_URL = "https://www.empleosperu.gob.pe"
HEADERS_BASE = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Ch-Ua": '"Chromium";v="149", "Not)A;Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/portal-mtpe/",
}


ID_DOCUMENTO = 10080399


def paso1_verificar(session, nu_documento):
    print("[*] Paso 1: Verificando usuario y obteniendo token...")
    url = f"{BASE_URL}/usermanagement/usuario/resetpassword/verificar"
    params = {"id-documento": ID_DOCUMENTO, "nu-documento": nu_documento}
    headers = {**HEADERS_BASE}

    resp = session.get(url, params=params, headers=headers)
    data = resp.json()

    if not data.get("succes"):
        print(f"[!] Error: {data.get('description')}")
        sys.exit(1)

    token = data["data"]["token"]["token"]
    existe = data["data"]["bExiste"]
    celular = data["data"]["sNumeroCelular"]

    print(f"[+] Usuario encontrado: {existe}")
    print(f"[+] Celular: {celular}")
    print(f"[+] Token obtenido correctamente")
    return token, celular


def paso2_enviar_codigo(session, token, email):
    print(f"\n[*] Paso 2: Enviando codigo de verificacion a {email}...")
    url = f"{BASE_URL}/usermanagement/email/enviar"
    headers = {**HEADERS_BASE, "X-Validate-Identity": token, "Content-Type": "application/json"}
    body = {"nInMotivo": 10140202, "sEmailTo": email}

    resp = session.post(url, json=body, headers=headers)
    data = resp.json()

    if not data.get("succes"):
        print(f"[!] Error: {data.get('description')}")
        sys.exit(1)

    print(f"[+] Codigo enviado al correo correctamente")
    return data


def paso3_cambiar_contrasena(session, token, nu_documento, email, codigo, nueva_contrasena, numero_celular):
    print(f"\n[*] Paso 3: Cambiando contrasena...")
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

    resp = session.post(url, json=body, headers=headers)
    data = resp.json()

    if not data.get("succes"):
        print(f"[!] Error: {data.get('description')}")
        sys.exit(1)

    print(f"[+] Contrasena cambiada correctamente!")
    return data


def main():
    print("=" * 50)
    print("   CAMBIADOR DE CONTRASENA - EmpleosPeru")
    print("=" * 50)

    nu_documento = input("\nNumero de Documento (DNI): ").strip()
    email = input("Correo electronico: ").strip()

    session = requests.Session()

    token, celular = paso1_verificar(session, nu_documento)

    paso2_enviar_codigo(session, token, email)

    print("\n[!] Revisa tu correo para obtener el codigo de verificacion.")
    codigo = input("Ingresa el codigo recibido: ").strip()
    nueva_contrasena = input("Nueva contrasena: ").strip()

    print(f"\n[!] Confirmando cambio de contrasena...")
    paso3_cambiar_contrasena(session, token, nu_documento, email, codigo, nueva_contrasena, celular)

    print("\n" + "=" * 50)
    print("   PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 50)


if __name__ == "__main__":
    main()
