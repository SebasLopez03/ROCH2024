#!/usr/bin/env python

from datalink import *

SERIAL_PORT = ''

# NOTA: Es importante revisar estos dos valores antes de ejecutar el código
BAUDRATE = 115200
SERIAL_PORT = "/dev/USB0"

if __name__ == '__main__':
    ser = open_serial()
    while True:
        try:
            if ser.in_waiting > 0:
                bytearray_in = ser.readline()
                print(bytearray_in)
                if checksum(bytearray_in):
                    pqt, pqt_type = pqt_interpret(bytearray_in)
                    if pqt:
                        print(pqt)
                    elif pqt == 1:
                        print(f"Unkown package. Header: {bytearray_in[0]}")
                    elif pqt == 2:
                        print('IndexError. Interpret fail.')
                    elif pqt == 3:
                        print('Value error. Interpret fail.')
                    else:
                        pass
            
            if is_pressed('A'):
                data_list = telemetryA_sim()
                print(f"Sending packet of Telemetry A: {data_list}")
                pck, pck_len = pqt_build(101, data_list)
                ser.write(pck)
                print(pck)
                sleep(0.1)
                    
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            break