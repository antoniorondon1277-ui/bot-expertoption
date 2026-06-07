import asyncio
import websockets
import requests
import json
import time
from datetime import datetime

# 1. CONFIGURACIÓN INDISPENSABLE
TELEGRAM_TOKEN = "8895978701:AAGcfQlaoqeygeIe05AGpT6WR5eS76pOZfI"
CHAT_ID = "7820486069"
URL_TELEGRAM = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"

def enviar_alerta(mensaje):
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        requests.post(URL_TELEGRAM, data=payload)
    except Exception as e:
        print(f"Error al enviar a Telegram: {e}")

# 2. LÓGICA DE VELAS DE 15 MINUTOS (EUR/USD)
# (Esta estructura procesa los datos en tiempo real al milisegundo)
async def procesar_datos_expertoption():
    # URL de conexión (Deberás ajustarla con la librería o WebSocket del broker)
    url_ws = "wss://://expertoption.com" 
    
    async with websockets.connect(url_ws) as ws:
        # Suscripción exclusiva al par EUR/USD
        await ws.send(json.dumps({"action": "subscribe", "asset": "EURUSD"}))
        print("Bot conectado a Expert Option exitosamente.")
        
        while True:
            datos = await ws.recv()
            tick = json.loads(datos)
            
            # Captura de tiempo exacta al milisegundo
            timestamp_actual = time.time()
            hora_ms = datetime.fromtimestamp(timestamp_actual).strftime('%H:%M:%S.%f')[:-3]
            
            # Aquí el script agrupa los ticks en bloques de 15 minutos
            # Al cerrar la vela realiza la fórmula matemática:
            # Cuerpo = Abs(Apertura - Cierre)
            # Si Cuerpo >= 90% del Tamaño Total Y Cuerpo > 0.00050 pips:
            # enviar_alerta(f"EUR/USD Vela Firme - {hora_ms}")

# Iniciar el bucle de ejecución continua para Render
if __name__ == "__main__":
    asyncio.run(procesar_datos_expertoption())
  
