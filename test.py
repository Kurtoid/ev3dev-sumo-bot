#!/usr/bin/env python3
from ev3dev.auto import LargeMotor, Led, ColorSensor, UltrasonicSensor
import time
import signal
import math

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

color_sensor = ColorSensor()
color_sensor.mode = 'COL-REFLECT'

sonar_sensor = UltrasonicSensor()
sonar_sensor.mode = 'US-DIST-CM'

lights = Led()
Led.delay_on = 500
Led.delay_off = 1500
lights.trigger = 'none'

time_since_escline = 0

is_esc_line = False
is_searching = False


print('ready')
lights.trigger = 'timer'
input("Press enter to go!")


def go_forwards():
    motor_a.run_forever(duty_cycle_sp=75)
    motor_b.run_forever(duty_cycle_sp=75)
    motor_c.run_forever(duty_cycle_sp=75)
    motor_d.run_forever(duty_cycle_sp=75)


def go_back():
    motor_a.run_forever(duty_cycle_sp=-75)
    motor_b.run_forever(duty_cycle_sp=-75)
    motor_c.run_forever(duty_cycle_sp=-75)
    motor_d.run_forever(duty_cycle_sp=-75)


def turn_right():
    motor_a.run_forever(duty_cycle_sp=75)
    motor_b.run_forever(duty_cycle_sp=-75)
    motor_c.run_forever(duty_cycle_sp=-75)
    motor_d.run_forever(duty_cycle_sp=75)


def stop():
    motor_a.stop()
    motor_b.stop()
    motor_c.stop()
    motor_d.stop()


def endprog():
    lights.trigger = 'none'
    stop()
    exit()


def is_backing_up():
    if(motor_a.duty_cycle_sp > 0 and motor_b.duty_cycle_sp > 0 and
       motor_c.duty_cycle_sp > 0 and motor_d.duty_cycle_sp > 0):
        return True
    else:
        return False


def is_going_fwds():
    if(motor_a.duty_cycle_sp < 0 and motor_b.duty_cycle_sp < 0 and
       motor_c.duty_cycle_sp < 0 and motor_d.duty_cycle_sp < 0):
        return True
    else:
        return False


def handler(signal, frame):
    print("control c pressed, ending now")
    endprog()


def esc_line():
    global time_since_escline
    global is_esc_line
    time_since_escline = time.time()
    is_esc_line = True
    go_back()


def proc_esc_line():
    global is_esc_line
    global is_searching
    if time.time()-time_since_escline > 1:
        print('time is done')
        is_esc_line = False
        is_searching = True
        return
    else:
        go_back()


def proc_search():
    global is_searching
    turn_right()
    if (sonar_sensor.value() / math.pow(10, sonar_sensor.decimals)) < 15:
        is_searching = False
signal.signal(signal.SIGINT, handler)


def main():
    while(True):
        if is_esc_line is True:
            proc_esc_line()
        elif is_searching is True:
            proc_search()
        else:
            go_forwards()
        print(color_sensor.value())
        if is_esc_line is not True:
            if(color_sensor.value() > 40):
                esc_line()
                print('esc line called')
        time.sleep(.001)


if __name__ == "__main__":
    main()
