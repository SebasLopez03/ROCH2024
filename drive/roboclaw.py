import hid
import serial
from serial import SerialException
from serial.tools import list_ports
from keyboard import is_pressed, read_key
from time import sleep

# Constante que representa la posición neutra del joystick
standard = 127.0

# Función que mapea los valores del joystick a velocidades lineales
def map_val_lin(lineal):
    if lineal == standard:
        return 0.0
    elif lineal < standard:
        return (standard - lineal)
    else:
        return (standard + 1) - lineal

# Función que mapea los valores del joystick a velocidades angulares
def map_val_ang(angular):
    if angular == standard:
        return 0.0, 0.0
    elif angular < standard:
        # Girando a la izquierda
        left_motor = -(standard - angular)
        right_motor = standard - angular
    else:
        # Girando a la derecha
        left_motor = angular - (standard + 1)
        right_motor = -(angular - (standard + 1))
    return left_motor, right_motor

# Función para abrir el puerto serial
def open_serial(dev_):
    while True:
        try:
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
            # Se abre comunicación con el joystick usando su ID
            joystick.open(0x12bd, 0xa02f)
            joystick.set_nonblocking(True)
            
            # Abrir comunicación con Arduino
            arduino = open_serial('Arduino')
            
            while True:
                report = joystick.read(8)
                if report:
                    lineal = report[1]
                    angular = report[2]

                    # Mapeo de valores
                    vel_lineal = map_val_lin(lineal)
                    vel_left_motor, vel_right_motor = map_val_ang(angular)

                    # Enviar datos al Arduino
                    data = f"{vel_lineal},{vel_left_motor},{vel_right_motor}\n"
                    arduino.write(bytes(data, 'utf-8'))
                    print(f"Enviado: {data.strip()}")
                
                if is_pressed('SHIFT') and read_key() == 'Q':
                    arduino.close()
                    break
    except KeyboardInterrupt:
        print('\n   --- Programa interrumpido por el usuario. ---')

## ? porque muere el arduino. ?