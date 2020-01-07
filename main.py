import motor
import servo
import sonicrange
import pigpio
import time


pi = pigpio.pi()

# PINS CONFIGURATION
in1 = 1
in2 = 1
in3 = 1
in4 = 1
enA = 1
enB = 1

trig = 1
echo = 1

sv = 1

ir_obs = 1

# SETTINGS
CLEARANCE = 0
STEP = 1

# HARDWARE INITIALIZATION
wheels = motor.MotorControl(in1, in2, in3, in4, enA, enB, pi)
pan = servo.ServoControl(pi, sv)
ranger = sonicrange.sonicrange(pi, trig, echo)

# IR SENSOR SETUP
pi.set_mode(ir_obs, pigpio.INPUT)
pi.set_pull_up_down(ir_obs, pigpio.PUD_UP)





def left_is_clear():
    pan.left()
    return True if ranger.read() >= CLEARANCE else False

def right_is_clear():
    pan.right() 
    return True if ranger.read() >= CLEARANCE else False

def front_obstacle():
    return True if pi.read(ir_obs) == 0 else True



def left_mode():
    while True:
        pan.left()
        wheels.forward()

        #time.sleep(STEP)
        while True:
            if left_is_clear():
                wheels.stop()
                wheels.left()
                break

            if front_obstacle():
                wheels.stop()
                if right_is_clear():
                    wheels.right()
                    break
                else:
                    wheels.spin()
                    break
            time.sleep(STEP)

def right_mode():
    while True:
        pan.right()
        wheels.forward()

        #time.sleep(STEP)
        while True:
            if left_is_clear():
                wheels.stop()
                wheels.left()
                break

            if front_obstacle():
                wheels.stop()
                if right_is_clear():
                    wheels.right()
                    break
                else:
                    wheels.spin()
                    break
            time.sleep(STEP)

try:
    left_mode()
finally:
    pi.stop()



