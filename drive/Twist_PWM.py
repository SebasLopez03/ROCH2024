# recibimos la señal del joystick con valores entre 0 y 255
# 127 es la posicion neutra, 0 hacia adelante y 255 hacia atras

# Constante que representa la posición neutra del joystick
standard = 127.0

# Función que mapea los valores del joystick a velocidades lineales
# Mapeamos los valores del joystick entre 0 y 10 para asignanrlo al TWIST
def map_val_lin(lineal):
    if lineal == standard:
        return 0.0
    elif lineal < standard:
        return 10 - ((lineal / standard) * 10)                  
    else:
        return ((lineal - standard) * 10 ) / (standard + 1)

# Función que mapea los valores del joystick a velocidades angulares
# Mapeamos los valores del joystick para los motores izquierdo y derecho
def map_val_ang(angular):
    if angular == standard:
        left_motor = 0.0
        right_motor = 0.0
    elif angular < standard:
        #considerando que en este caso el giro es a la izquierda
        left_motor = -((10 - ((angular / standard) * 10)))
        right_motor = (10 - ((angular / standard) * 10))       ### Revisar bytes ###
    else:
        left_motor = ((angular - standard) * 10 ) / (standard + 1)
        right_motor = -(((angular - standard) * 10 ) / (standard + 1))
    return left_motor, right_motor

#generar el PWM de 0 a 255
def twist_to_pwm(linear, angular):
    pwm_linear = map_value(int(abs(linear)), 0, 10, 0, 255)
    left_pwm, right_pwm = map_val_ang(angular)

    left_pwm = map_value(int(abs(left_pwm)), 0, 10, 0, 255)
    right_pwm = map_value(int(abs(right_pwm)), 0, 10, 0, 255)

#pasamos los valores de [0,10] a [0,255]
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def main():
    # Data proviene del joystick como una cadena de 8 bytes
    data = read_joystick_data()
    lineal = data[1]
    angular = data[2]

    twist = Twist()
    twist.linear.x = map_val_lin(lineal)
    twist.angular.z = map_val_ang(angular)

def read_joystick_data():
    #obtenemos los datos del joystick
    return bytearray(8)
