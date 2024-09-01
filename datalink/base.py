#!/usr/bin/env python

from datalink import *

if __name__ == '__main__':
    while True:
        ser = open_serial_window()
        if ser:
            try:
                control_window_1(ser)
                break
            except SerialException:
                pass
        else:
            break