import pigpio
import time


def pulse(angle):
    return int(angle/0.09) + 500 

class ServoControl:
    def __init__(self, pi, s):
        self.pi = pi
        self.servo = s

        self.pi.set_mode(servo, pigpio.OUTPUT)

        self.pi.set_servo_pulsewidth(self.servo, pulse(90))

        
    def right(self):
        self.pi.set_servo_pulsewidth(self.servo, pulse(180))
        self.pi.set_servo_pulsewidth(self.servo, 0)

    def center(self):
        self.pi.set_servo_pulsewidth(self.servo, pulse(90))
        self.pi.set_servo_pulsewidth(self.servo, 0)
    
    def left(self):
        self.pi.set_servo_pulsewidth(self.servo, pulse(0))
        self.pi.set_servo_pulsewidth(self.servos, 0)

    def move(self, angle):
        self.pi.set_servo_pulsewidth(self.servo, pulse(angle))

