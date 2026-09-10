import re


class ErrorValidacion(Exception):
    pass


REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
REGEX_MAYUSCULA = re.compile(r"[A-Z]")
REGEX_MINUSCULA = re.compile(r"[a-z]")
REGEX_DIGITO = re.compile(r"\d")
REGEX_ESPECIAL = re.compile(r"[^A-Za-z0-9]")


def validar_dni(dni):
    dni = str(dni).strip()
    if not dni.isdigit() or len(dni) != 8:
        raise ErrorValidacion("El DNI debe tener 8 digitos numericos")
    return dni


def validar_email(email):
    email = str(email).strip()
    if not REGEX_EMAIL.match(email):
        raise ErrorValidacion("El correo electronico no tiene un formato valido")
    return email


def validar_codigo(codigo):
    codigo = str(codigo).strip()
    if not codigo:
        raise ErrorValidacion("El codigo de verificacion no puede estar vacio")
    return codigo


def validar_contrasena(contrasena, min_longitud=8):
    contrasena = str(contrasena)
    if len(contrasena) < min_longitud:
        raise ErrorValidacion(f"La contrasena debe tener al menos {min_longitud} caracteres")
    if not REGEX_MAYUSCULA.search(contrasena):
        raise ErrorValidacion("La contrasena debe tener al menos una mayuscula")
    if not REGEX_MINUSCULA.search(contrasena):
        raise ErrorValidacion("La contrasena debe tener al menos una minuscula")
    if not REGEX_DIGITO.search(contrasena):
        raise ErrorValidacion("La contrasena debe tener al menos un digito")
    if not REGEX_ESPECIAL.search(contrasena):
        raise ErrorValidacion("La contrasena debe tener al menos un caracter especial")
    return contrasena
