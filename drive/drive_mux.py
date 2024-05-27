import rospy
import time

from geometry_msgs.msg import Twist

def __init__(self):
        rospy.Subscriber("Twist_PWM", Twist, callback=self.joystick)
        self.block_duration = 0
        self.joystick_time = time.time()
        
def joystick(self, twist):
        self.joystick_time = time.time()
        self.block_duration = rospy.get_param('~block_duration', 5) #Para baja latencia comentar para evitar rospy.get_param
        self.pub.publish(twist)
