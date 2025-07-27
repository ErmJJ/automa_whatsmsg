# msgwa.py
import sys
import pywhatkit as kit

def enviar_mensaje(numero: str, mensaje: str, hora: int, minuto: int, wait_time: int = 20):
    """
    Envía un mensaje de WhatsApp programado.

    Parámetros:
      numero     – Número de destino, con o sin '+' al inicio.
      mensaje    – Texto a enviar.
      hora       – Hora en formato 24h (0–23).
      minuto     – Minuto (0–59).
      wait_time  – Segundos para esperar a que cargue WhatsApp Web.
    """
    # Asegurar el '+' al inicio
    destino = numero if numero.startswith('+') else f'+{numero}'
    try:
        kit.sendwhatmsg(destino, mensaje, hora, minuto, wait_time=wait_time)
        print(f"[✔] Mensaje programado para las {hora:02d}:{minuto:02d} → {destino}")
    except Exception as e:
        print(f"[✖] Error al programar el mensaje: {e}")

def main():
    # 1) Pedir datos al usuario
    numero  = input("Número de destino (ej. 50680008000 o +50680008000): ").strip()
    mensaje = input("Mensaje a enviar: ").strip()
    try:
        hora   = int(input("Hora de envío (0–23): ").strip())
        minuto = int(input("Minuto de envío (0–59): ").strip())
    except ValueError:
        print("[✖] Hora o minuto inválido. Deben ser números enteros.")
        sys.exit(1)

    # 2) Validar rangos básicos
    if not (0 <= hora <= 23 and 0 <= minuto <= 59):
        print("[✖] La hora o el minuto están fuera de rango.")
        sys.exit(1)

    # 3) Programar el envío
    enviar_mensaje(numero, mensaje, hora, minuto)

if __name__ == "__main__":
    main()
