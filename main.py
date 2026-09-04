import argparse
import time

from colorama import Fore, Style

from config_loader import cargar_config
from http_client import ErrorHTTP, ErrorRed, ErrorServicio, ClienteHTTP
from logging_setup import setup_logging
from services.password_changer import PasswordChanger
from ui.display import (
    imprimir_caja,
    imprimir_error,
    imprimir_exito,
    imprimir_info,
    imprimir_titulo_seccion,
    mostrar_banner,
    panel_cierre,
    panel_titulo,
)
from ui.prompts import panel_input
from validators import ErrorValidacion, validar_codigo, validar_contrasena, validar_dni, validar_email


def _parse_args():
    parser = argparse.ArgumentParser(description="Change Password - EmpleosPeru")
    parser.add_argument("-v", "--verbose", action="store_true", help="Modo verbose (logs de depuracion)")
    return parser.parse_args()


def flujo_completo():
    args = _parse_args()
    config = cargar_config()
    verbose = args.verbose or config.get("verbose", False)
    setup_logging(verbose)

    mostrar_banner()

    imprimir_caja("C A M B I A D O R  D E  C O N T R A S E N A\n Bienvenido al panel automatizado")

    print()
    panel_titulo("Datos del usuario")

    while True:
        try:
            nu_documento = validar_dni(panel_input("Ingrese el DNI"))
            break
        except ErrorValidacion as e:
            imprimir_info(f"Reintente: {e}")

    while True:
        try:
            email = validar_email(panel_input("Correo electronico"))
            break
        except ErrorValidacion as e:
            imprimir_info(f"Reintente: {e}")

    panel_cierre("Datos del usuario")

    cliente = ClienteHTTP(
        timeout=config.get("timeout"),
        max_retries=config.get("max_retries"),
        backoff=config.get("backoff"),
        proxies=config.get("proxies"),
    )
    service = PasswordChanger(cliente=cliente)

    try:
        imprimir_titulo_seccion(1, "VERIFICANDO USUARIO")
        imprimir_info("Enviando peticion de verificacion...")
        identidad = service.verificar_usuario(nu_documento)
        token = identidad["token"]
        celular = identidad["celular"]

        imprimir_exito("Usuario autenticado correctamente")
        imprimir_info(f"Celular registrado: {Fore.WHITE}{celular}")
        imprimir_info("Token de identidad obtenido")
        time.sleep(0.8)

        imprimir_titulo_seccion(2, "ENVIANDO CODIGO DE VERIFICACION")
        imprimir_info(f"Destino: {Fore.WHITE}{email}")
        service.enviar_codigo(token, email)
        imprimir_exito("Codigo de verificacion enviado al correo")
        time.sleep(0.8)

        print()
        panel_titulo("Verificacion de contrasena")

        while True:
            try:
                codigo = validar_codigo(panel_input("Revisa tu correo y escribe el codigo recibido"))
                break
            except ErrorValidacion as e:
                imprimir_info(f"Reintente: {e}")

        while True:
            try:
                nueva_contrasena = validar_contrasena(panel_input("Escribe la nueva contrasena"))
                break
            except ErrorValidacion as e:
                imprimir_info(f"Reintente: {e}")

        panel_cierre("Verificacion de contrasena")

        imprimir_titulo_seccion(3, "CONFIRMANDO NUEVA CONTRASENA")
        imprimir_info("Enviando datos de confirmacion...")
        service.cambiar_contrasena(token, nu_documento, email, codigo, nueva_contrasena, celular)
        imprimir_exito("Contrasena actualizada correctamente")
        time.sleep(0.8)

    except (ErrorServicio, ErrorRed, ErrorHTTP) as e:
        imprimir_error(str(e))

    print()
    imprimir_caja("PROCESO COMPLETADO EXITOSAMENTE\n"
                  f"Contrasena cambiada para el usuario {nu_documento}", Fore.GREEN)
    print(Fore.CYAN + Style.BRIGHT + "\n  Gracias por usar Change Password by SYLAR\n")
    time.sleep(0.5)


if __name__ == "__main__":
    try:
        flujo_completo()
    except KeyboardInterrupt:
        print()
        imprimir_caja("SALIENDO DEL PROGRAMA\n Gracias por usar Change Password by SYLAR", Fore.CYAN)
        print()
    except EOFError:
        print()
        print(Fore.CYAN + Style.BRIGHT + "\n  [!] Sesion finalizada.\n")
        print(Fore.CYAN + Style.BRIGHT + "  Gracias por usar Change Password by SYLAR\n")
