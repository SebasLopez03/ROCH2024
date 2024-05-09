# Recibe datos desde una Xbee por UART 

import serial
from time import sleep
from serial.tools import list_ports

port = list(list_ports.comports())
for p in port:
    print(p.device)

# Configuración del puerto serie para la XBee
while True:
    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)
        break
    except serial.SerialException:
        print('No se pudo abrir la comunicación con Arduino')
        port = list(list_ports.comports())
        for p in port:
            print(p.device)
        sleep(3)   

while True:
    try:
        xbee = serial.Serial('COM9', 9600, timeout=1) 
        break
    except serial.SerialException:
        print('No se pudo abrir la comunicación con Xbee')
        port = list(list_ports.comports())
        for p in port:
            print(p.device)
        sleep(3)              
# Cambia a puerto correcto y la velocidad de baudios según tus configuraciones

line = ''

try:
    while True:
        try:  # Leer los datos recibidos como bytes
            if xbee.in_waiting > 0:
                line = xbee.readline().decode('utf-8') # Lectura de puerto serial
                print(line)
                arduino.write(line.encode('utf-8')) # Manda linea a Arduino
                
        except UnicodeDecodeError:
            print("Error de decodificación. Recibido un dato no válido.")
            
        except serial.SerialException:
            print('Serial Exception')                  
        
except KeyboardInterrupt:
    xbee.close()  # Cerrar el puerto serial al finalizar
    arduino.close()
    print("Programa detenido por el usuario")
