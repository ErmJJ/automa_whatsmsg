# 📱 WhatsApp Message Scheduler via ADB + Python

Este proyecto permite enviar mensajes programados de WhatsApp desde un dispositivo Android conectado a tu computadora (por USB o red WiFi), utilizando `ADB` y Python. Ideal para automatizar recordatorios, saludos o cualquier comunicación.

---

## 🧰 Requisitos

- **Sistema Operativo:** Windows 10/11
- **Python:** 3.8 o superior
- **ADB (Android Debug Bridge)**
- **Dispositivo Android con depuración USB habilitada**
- **WhatsApp instalado y con sesión activa en el celular**

---

## 🔌 Conexión ADB (USB o WiFi)

### 1. Conexión USB (recomendada para pruebas iniciales)

1. Habilita **Opciones de desarrollador** en el teléfono.
2. Activa **Depuración USB**.
3. Conecta el teléfono por cable USB.
4. Ejecuta:
```bash
adb devices
````

Debe aparecer el ID de tu dispositivo.

---

### 2. Conexión WiFi (requiere USB temporalmente)

1. Conecta el celular por USB.
2. Conecta el celular y tu PC a la **misma red WiFi**.
3. Ejecuta los siguientes comandos:

```bash
adb tcpip 5555
adb shell ip route  # Copia la IP del celular (ej: 192.168.0.12)
adb connect 192.168.0.12:5555 #Ej
adb devices
```

✅ Tu dispositivo ahora está conectado por WiFi.

---

### ❌ Cómo cerrar la conexión

* Para **cerrar sesión WiFi**, ejecuta:

```bash
adb disconnect
```

* Para **cerrar ADB completamente**, ejecuta:

```bash
adb kill-server
```

---

## 🚀 Cómo usar el script

1. Ejecuta el script con Python:

```bash
python enviar_whatsapp.py
```

2. Ingresa los datos que se te solicitarán:
   * Número en formato internacional:`+506xxxxxxxx o 506xxxxxxxx. (Ej.+506 = Costa Rica.)`
   * Mensaje de texto.
   * Hora y minutos para enviar (formato 12 o 24 horas aceptado).

3. El mensaje se enviará automáticamente desde WhatsApp.

4. Se te preguntará si deseas programar otro mensaje o finalizar. (si no marcas una opción el programa finaliza)

---

## 📁 Archivo de Logs

Cada mensaje enviado se guarda en el archivo:

```
PyWhatKit_DB.txt
```

Con el siguiente formato:

```
--------------------
Date: 24/7/2025
Time: 20:09
Phone Number: +506xxxxxxxx
Message: Prueba
--------------------
```

---

## ⚠️ Advertencia de Seguridad

Este proyecto está diseñado únicamente con fines educativos y de automatización personal. **No abuses ni automatices spam.** Utiliza esta herramienta en un entorno controlado.

---

## 📦 Estructura del Proyecto

```
whatsapp_scheduler/
├── WhatsMSG (Android).py
├── WhatsMSG (WEB).py
└── PyWhatKit_DB.txt (Se crea automaticamente)
```


---

### 📝 Licencia

Este proyecto se distribuye bajo la licencia MIT.

---

## ‍💻 Desarrollado por
- Julián Hernández  
Profesional/Estudiante en Ingeniería Informática