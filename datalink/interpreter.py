import struct

def add_checksum(bytearray_):
    checksum = sum(bytearray_)
    bytearray.extend((checksum // 256, checksum % 256))
    return checksum

def checksum(bytearray_):
    received_sum = [0, 0]
    received_sum[0] = bytearray_[-2]
    received_sum[1] = bytearray_[-1]
    
    calculated_sum = [sum(bytearray_[:-2]) // 256, sum(bytearray_[:-2]) % 256]
    
    if received_sum == calculated_sum:
        return True
    else:
        return False

def interpret(bytearray_):
    header = bytearray_[0]
    if header == 101:
        # Mediciones desde RoboClaw del chasis
        voltage_chasis = struct.unpack('f', bytearray_[1:5])[0]
        corriente_chasis = struct.unpack('f', bytearray_[5:9])[0]
        error_chasis = bytearray_[9]
        
        # Mediciones desde RoboClaw para brazo
        voltage_brazo = struct.unpack('f', bytearray_[10:14])[0]
        corriente_brazo = struct.unpack('f', bytearray_[14:18])[0]
        error_brazo = bytearray_[18]
        
        temperatura_chasis = bytearray_[19]
        
        telemetriaA = {'VC':voltage_chasis, 'CC':corriente_chasis, 'EC':error_chasis, 
                       'VB':voltage_brazo, 'VB':corriente_brazo, 'EB':error_brazo,
                       'TC': temperatura_chasis}
        return telemetriaA, 'A'
    
    elif header == 102:
        # GPS
        gps_latitud = struct.unpack('f', bytearray_[1:5])[0]
        gps_altitud = struct.unpack('f', bytearray_[5:9])[0]
        
        # IMU
        orientacion = struct.unpack('>H', bytearray_[9:11])[0]
        
        telemetriaB = {'GPS_X': gps_latitud, 'GPS_Y':gps_altitud, 'Orientacion': orientacion}
        return telemetriaB, 'B'
    
    else:
        print('Interpretación fallida')
        return {}, False
