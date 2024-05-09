# Toma el input de 8 bits del joystick y lo manda a través de UART a una Xbee en modo transparente
# Sebastián López Tena 13/03/2024 bastianlopezt@gmail.com

import hid
from time import sleep
from keyboard import is_pressed
from keyboard import read_key
import serial
from serial import SerialException
from serial.tools import list_ports

def open_serial(dev_):
    while True:
        # Abrir comunicación serial con un dispositivo. Se espera hasta que se logre conectar
        try:
            # Se enlistan los puertos disponibles
            print('Puertos disponibles: ')
            port = list(list_ports.comports())
            for p in port:
                print(p.device)
            
            puerto = input(f'Escriba el puerto para {dev_}: ')
            dev = serial.Serial(puerto, 9600, timeout=1)
            break
        
        except SerialException:
            print('No se pudo abrir el puerto serial')
            print("\n")
            sleep(2)         
    return dev
    

if __name__ == '__main__':
    try:
        while True: 
            # Se enlistan los dispositivos conectados disponibles con sus ID
            for device in hid.enumerate():
                print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")  
            
            # Se crea una instancia de hid.device para leer los inputs de los dispositivos
            joystick = hid.device()
            # Se abre comunicación con joystick especificamente usando su ID
            joystick.open(0x12bd, 0xa02f)
            # Si el dispositivo no está listo, solo se regresará None cuando se quiera leer 
            joystick.set_nonblocking(True)
            
            xbee = open_serial('Xbee')
            
            while True:
                report = joystick.read(8)
                if report:
                    print(report)
                    xbee.write(report)
                if is_pressed('SHIFT') and read_key() == 'Q':
                    xbee.close()
                    break
            
    except KeyboardInterrupt:
        print('\n   --- Programa interrumpido por el usuario. ---')
