import pigpio
import time

pi = pigpio.pi()

class MotorControl:
    def __init__(self, in1, in2, in3, in4, enA, enB, pi):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.enA = enA
        self.enB = enB
        self.pi = pi

        pi.set_mode(in1, pigpio.OUTPUT)
        pi.set_mode(in2, pigpio.OUTPUT)
        pi.set_mode(in3, pigpio.OUTPUT)
        pi.set_mode(in4, pigpio.OUTPUT)
        pi.set_mode(enA, pigpio.OUTPUT)
        pi.set_mode(enB, pigpio.OUTPUT)


    def forward(self):
        self.pi.set_bank_1((1 << self.in1) |  (1 << self.in3))
        self.pi.clear_bank_1((1 << self.in2) | (1 << self.in4))

        self.pi.set_PWM_dutycycle(self.enA, 255)
        self.pi.set_PWM_dutycycle(self.enB, 255)

  

    def backward(self):
        self.pi.clear_bank_1((1 << self.in1) |  (1 << self.in3))
        self.pi.set_bank_1((1 << self.in2) | (1 << self.in4))

        self.pi.set_PWM_dutycycle(self.enA, 255)
        self.pi.set_PWM_dutycycle(self.enB, 255)


    def right(self):
        self.pi.set_bank_1((1 << self.in1) |  (1 << self.in4))
        self.pi.clear_bank_1((1 << self.in2) | (1 << self.in3))

        self.pi.set_PWM_dutycycle(self.enA, 255)
        self.pi.set_PWM_dutycycle(self.enB, 255)

        time.sleep(1.5)

    def left(self):
        self.pi.set_bank_1((1 << self.in2) |  (1 << self.in3))
        self.pi.clear_bank_1((1 << self.in1) | (1 << self.in4))

        self.pi.set_PWM_dutycycle(self.enA, 255)
        self.pi.set_PWM_dutycycle(self.enB, 255)

        time.sleep(1.5)


    def spin(self):
        self.right()
        self.right()


    def run(self, m1, m2, threshold):
        """
        Runs both motor with speed m1 and m2 having a threshold value.
        The threshold value prevents humming of motor at lower duty_cycle/Speed.
        """

        if m1 == 0 and m2 == 0:
            self.pi.clear_bank_1((1 << self.in1) | (1 << self.in2) | (1 << self.in3) | (1 << self.in4))
        else: 
            if m1 > 0:
                self.pi.write(self.in1, 1)
                self.pi.write(self.in2, 0)
            elif m1 < 0:
                self.pi.write(self.in2, 1)
                self.pi.write(self.in1, 0)

            if m2 > 0:
                self.pi.write(self.in3, 1)
                self.pi.write(self.in4, 0)
            elif m2 < 0:
                self.pi.write(self.in3, 1)
                self.pi.write(self.in4, 0)

        speed1 = (255-threshold) * (abs(m1)/50) + threshold if abs(m1) > 0 else 0    #threshold - 255
        speed2 = (255-threshold) * (abs(m2)/50) + threshold if abs(m2) > 0 else 0

        self.pi.set_PWM_dutycycle(self.enA, speed1)    
        self.pi.set_PWM_dutycycle(self.enB, speed2)     


    def stop(self):
        self.pi.clear_bank_1((1 << self.in1) | (1 << self.in2) | (1 << self.in3) | (1 << self.in4))
        self.pi.set_PWM_dutycycle(self.enA, 0)    
        self.pi.set_PWM_dutycycle(self.enB, 0)

