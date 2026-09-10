import os
import sys

from colorama import init, Fore, Style

from config import ANCHO_PANEL

init(autoreset=True)

if sys.platform == "win32":
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleOutputCP(65001)
    kernel32.SetConsoleCP(65001)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BANNER = r"""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║      ██████ ██   ██  █████  ███    ██  ██████  ███████         ║
║     ██      ██   ██ ██   ██ ████   ██ ██       ██              ║
║     ██      ███████ ███████ ██ ██  ██ ██   ███ ███████         ║
║     ██      ██   ██ ██   ██ ██  ██ ██ ██    ██      ██         ║
║      ██████ ██   ██ ██   ██ ██   ████  ██████  ███████         ║
║                                                                ║
║           P A S S W O R D   C H A N G E R                      ║
║         EmpleosPeru  |  by  SYLAR  |  Ciberseguridad           ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_banner():
    limpiar_pantalla()
    print(Fore.MAGENTA + Style.BRIGHT + BANNER)
    print(
        Fore.CYAN
        + Style.BRIGHT
        + "  [!] Herramienta de automatizacion de cambio de contrasena\n"
    )


def calcular_ancho_display(texto):
    ancho = 0
    i = 0
    while i < len(texto):
        if texto[i] == '\x1b':
            while i < len(texto) and texto[i] != 'm':
                i += 1
            i += 1
            continue
        ancho += 1
        i += 1
    return ancho


def imprimir_caja(contenido, color=Fore.WHITE):
    lineas = str(contenido).split("\n")
    ancho = max([calcular_ancho_display(l) for l in lineas] + [0]) + 4
    print(color + Style.BRIGHT + "┌" + "─" * (ancho - 2) + "┐")
    for linea in lineas:
        ancho_linea = calcular_ancho_display(linea)
        espacios = max((ancho - 4 - ancho_linea) // 2, 0)
        print(color + "│" + " " * espacios + linea + " " * (ancho - 4 - ancho_linea - espacios) + "│")
    print(color + Style.BRIGHT + "└" + "─" * (ancho - 2) + "┘")


def imprimir_titulo_seccion(numero, titulo):
    ancho = len(titulo) + 6
    print(Fore.YELLOW + Style.BRIGHT + f"  ▸ {numero} • {titulo}")
    print(Style.DIM + "  " + Fore.YELLOW + "─" * ancho)


def imprimir_exito(msg):
    print(Fore.GREEN + Style.BRIGHT + f"     [✓] {msg}")


def imprimir_error(msg):
    print(Fore.RED + Style.BRIGHT + f"\n  [!] ERROR: {msg}")
    sys.exit(1)


def imprimir_info(msg):
    print(Fore.CYAN + Style.BRIGHT + f"     [i] {msg}")


def imprimir_advertencia(msg):
    print(Fore.YELLOW + Style.BRIGHT + f"     [!] {msg}")


def panel_titulo(titulo):
    relleno = ANCHO_PANEL - len(titulo) - 6
    print(
        Fore.MAGENTA + Style.BRIGHT + "  ┌─ "
        + titulo
        + " " + "─" * relleno + "┐"
    )


def panel_cierre(titulo):
    print(Fore.MAGENTA + Style.BRIGHT + "  └" + "─" * (ANCHO_PANEL - 4) + "┘")
