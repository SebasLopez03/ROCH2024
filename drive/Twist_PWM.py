# vamos a recibir los datos twist para hacer el mapeo y la señal pwm

""""
twist:
    lineal:
        x:byte
        y:0
        z:0
    angular:
        x:0
        y:0
        z:byte

"""
# leer el valor twist.lineal.x desde el topico "drive_mux(sub)"
twist = ...

def map_val_lin(twist):
    # velocidad linear
    # Mapeamos los valores de twist para que esten entre -1.0 y 1.0
    if twist.lineal.x == 127:
        return 0.0
    elif twist.lineal.x < 127:
        return (twist.lineal.x / 127.0) - 1.0
    else:
        return (twist.lineal.x - 128) / 127.0

def map_val_ang(twist):
    # velocidad angular
    # Mapeamos los valores de twist para los motores izquierdo y derecho
    if twist.angular.z == 127:
        left_motor = 0.0
        right_motor = 0.0
    elif twist.angular.z < 127:
        left_motor = -((127 - twist.angular.z) / 127.0)    
        right_motor = ((127 - twist.angular.z) / 127.0)        
    else:
        left_motor = ((twist.angular.z - 128) / 127.0)
        right_motor = -((twist.angular.z - 128) / 127.0)
    return left_motor, right_motor

# Ejemplo de uso
linear_speed = map_val_lin(twist)
left_motor_speed, right_motor_speed = map_val_ang(twist)

print(f"Linear Speed: {linear_speed}")
print(f"Left Motor Speed: {left_motor_speed}")
print(f"Right Motor Speed: {right_motor_speed}")

# enviar al arduino
