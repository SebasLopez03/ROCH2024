# El código pretende recibir 8 bytes a partir de la Xbee de tal manera que se puedan usar para controlar el rover

import serial
from serial.tools import list_ports
from serial import SerialException
from time import sleep

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
        xbee = open_serial('Xbee')
        report = []
        while True:
            if xbee.in_waiting > 0:
                read = xbee.readline(1)
                decode = int.from_bytes(read, "big")
                report.append(decode)
            if len(report) == 8:
                print(report)
                report.clear()
                
    except KeyboardInterrupt:
        print("\n   ---Interrupción de teclado---")
