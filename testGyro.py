#!/usr/bin/env python3
from ev3dev.auto import *

gyro = GyroSensor()

gyro.mode='GYRO-ANG'

motor_a = LargeMotor('outA')
motor_b = LargeMotor('outB')
motor_c = LargeMotor('outC')
motor_d = LargeMotor('outD')
motor_c.polarity = 'inversed'
motor_d.polarity = 'inversed'

motor_a.stop_action = 'brake'
motor_b.stop_action = 'brake'
motor_c.stop_action = 'brake'
motor_d.stop_action = 'brake'


def go_forwards():
    MOTOR_POWER=100
    motor_a.run_forever(duty_cycle_sp=MOTOR_POWER)
    motor_b.run_forever(duty_cycle_sp=MOTOR_POWER)
    motor_c.run_forever(duty_cycle_sp=MOTOR_POWER)
    motor_d.run_forever(duty_cycle_sp=MOTOR_POWER)


def go_back():
    motor_a.run_forever(duty_cycle_sp=-75)
    motor_b.run_forever(duty_cycle_sp=-75)
    motor_c.run_forever(duty_cycle_sp=-75)
    motor_d.run_forever(duty_cycle_sp=-75)

def stop():
    motor_a.stop()
    motor_b.stop()
    motor_c.stop()
    motor_d.stop()

while True:
    print(gyro.value())
    if(gyro.value()>5):
        go_back()
    elif(gyro.value()<-5):
        go_forwards()
    else:
        stop()
