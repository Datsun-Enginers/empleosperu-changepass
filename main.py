import time

from colorama import Fore, Style

from services.password_changer import ErrorServicio, PasswordChanger
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


def flujo_completo():
    mostrar_banner()

    imprimir_caja("C A M B I A D O R  D E  C O N T R A S E N A\n Bienvenido al panel automatizado")

    print()
    panel_titulo("Datos del usuario")

    nu_documento = panel_input("Ingrese el DNI")
    email = panel_input("Correo electronico")

    panel_cierre("Datos del usuario")

    service = PasswordChanger()

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

        codigo = panel_input("Revisa tu correo y escribe el codigo recibido")
        nueva_contrasena = panel_input("Escribe la nueva contrasena")

        panel_cierre("Verificacion de contrasena")

        imprimir_titulo_seccion(3, "CONFIRMANDO NUEVA CONTRASENA")
        imprimir_info("Enviando datos de confirmacion...")
        service.cambiar_contrasena(token, nu_documento, email, codigo, nueva_contrasena, celular)
        imprimir_exito("Contrasena actualizada correctamente")
        time.sleep(0.8)

    except ErrorServicio as e:
        imprimir_error(str(e))

    print()
    imprimir_caja("PROCESO COMPLETADO EXITOSAMENTE\n"
                  f"Contrasena cambiada para el usuario {nu_documento}", Fore.GREEN)
    print(Fore.CYAN + Style.BRIGHT + "\n  Gracias por usar Change Password by SYLAR\n")
    time.sleep(0.5)


if __name__ == "__main__":
    flujo_completo()
