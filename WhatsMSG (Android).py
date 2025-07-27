import subprocess
import time
import threading
import sys
from datetime import datetime

# Ruta a adb.exe (ajusta si no lo tienes en el PATH)
ADB_PATH = "adb"

LOG_FILE = "PyWhatKit_DB.txt"

def input_with_timeout(prompt, timeout):
    """
    Mostrar prompt y esperar input hasta timeout segundos.
    Devuelve la cadena ingresada, o None si no hubo respuesta.
    """
    print(prompt, end=' ', flush=True)
    result = []

    def grab_input():
        line = sys.stdin.readline().strip()
        result.append(line)

    thread = threading.Thread(target=grab_input, daemon=True)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        return None
    return result[0] if result else ''

def format_number(numero):
    """Asegura que el número empiece con '+'."""
    numero = numero.strip()
    if not numero.startswith('+'):
        numero = '+' + numero
    return numero

def parse_time(hora_str):
    """
    Intenta parsear hora en 24h ('HH:MM') o 12h ('HH:MM AM/PM').
    Devuelve (hora, minuto) en int.
    """
    for fmt in ("%H:%M", "%I:%M %p"):
        try:
            t = datetime.strptime(hora_str, fmt)
            return t.hour, t.minute
        except ValueError:
            continue
    raise ValueError("Formato de hora inválido")

def esperar_hora_envio(h, m):
    ahora = datetime.now()
    envio = ahora.replace(hour=h, minute=m, second=0, microsecond=0)
    if envio < ahora:
        raise RuntimeError("La hora ya pasó hoy.")
    segs = (envio - ahora).total_seconds()
    print(f"[⏳] Esperando {int(segs)} segundos hasta las {h:02d}:{m:02d}...")
    time.sleep(segs)

def enviar_whatsapp(numero, mensaje):
    """Usa ADB para enviar mensaje por WhatsApp y luego cierra la app."""
    # Cerrar WhatsApp
    subprocess.run([ADB_PATH, "shell", "am", "force-stop", "com.whatsapp"])
    time.sleep(1)
    # Abrir chat con mensaje
    msg_enc = mensaje.replace(' ', '%20')
    subprocess.run([
        ADB_PATH, "shell", "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", f"https://wa.me/{numero.lstrip('+')}?text={msg_enc}"
    ])
    time.sleep(6)
    # Tap en botón enviar (coordenadas fijas)
    subprocess.run([ADB_PATH, "shell", "input", "tap", "1010", "2155"])
    time.sleep(2)
    # Cerrar WhatsApp
    subprocess.run([ADB_PATH, "shell", "am", "force-stop", "com.whatsapp"])

def log_envio(numero, mensaje):
    now = datetime.now()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("--------------------\n")
        f.write(f"Date: {now.day}/{now.month}/{now.year}\n")
        f.write(f"Time: {now.hour}:{now.minute}\n")
        f.write(f"Phone Number: {numero}\n")
        f.write(f"Message: {mensaje}\n")
        f.write("--------------------\n")

def main():
    while True:
        # Entradas de usuario
        num = input("Número destino (con o sin +): ").strip()
        num = format_number(num)

        msg = input("Mensaje a enviar: ").strip()

        hora_input = input("Hora de envío (24h 'HH:MM' o 12h 'HH:MM AM/PM'): ").strip().upper()
        try:
            h, m = parse_time(hora_input)
        except ValueError as e:
            print("⚠️", e)
            continue

        try:
            esperar_hora_envio(h, m)
        except RuntimeError as e:
            print("⚠️", e)
            continue

        print(f"[📨] Enviando ahora mensaje a {num}...")
        enviar_whatsapp(num, msg)
        log_envio(num, msg)
        print("[✅] Mensaje enviado y registrado en log.")

        # Preguntar si desea otro envío
        ans = input_with_timeout(
            "\n¿Deseas programar otro mensaje? (sí / no):",
            timeout=15
        )
        if ans is None:
            print("\n⏰ Tiempo de respuesta agotado. Cerrando script.")
            break
        if ans.lower().startswith('s'):
            continue
        else:
            print("👋 Cerrando script. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()