from colorama import Fore, Style

from config import ANCHO_PANEL


def panel_input(etiqueta):
    print(Fore.CYAN + Style.BRIGHT + "  │" + Fore.GREEN + f"  {etiqueta}")
    print(Fore.CYAN + Style.BRIGHT + "  │" + " " * (ANCHO_PANEL - 3))
    valor = input(Fore.YELLOW + "  │     → " + Style.RESET_ALL).strip()
    return valor
