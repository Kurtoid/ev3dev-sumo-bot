#!/usr/bin/env python3
from ev3dev.auto import LargeMotor, Led, ColorSensor, UltrasonicSensor
import time
import signal
import math

import array
import fcntl
import sys

# from linux/input.h

KEY_UP = 103
KEY_DOWN = 108
KEY_LEFT = 105
KEY_RIGHT = 106
KEY_ENTER = 28
KEY_BACKSPACE = 14

KEY_MAX = 0x2ff


def EVIOCGKEY(length):
    return 2 << (14+8+8) | length << (8+8) | ord('E') << 8 | 0x18

# end of stuff from linux/input.h

BUF_LEN = int((KEY_MAX + 7) / 8)


def test_bit(bit, bytes):
    # bit in bytes is 1 when released and 0 when pressed
    return not bool(bytes[int(bit / 8)] & (1 << (bit % 8)))


def is_enter_pressed():
    buf = array.array('B', [0] * BUF_LEN)
    with open('/dev/input/by-path/platform-gpio-keys.0-event', 'r') as fd:
        ret = fcntl.ioctl(fd, EVIOCGKEY(len(buf)), buf)

    if ret < 0:
        print("ioctl error", ret)
        sys.exit(1)

    # for key in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'ENTER', 'BACKSPACE']:
    #    key_code = globals()['KEY_' + key]
    #    key_state = test_bit(key_code, buf) and "pressed" or "released"
    #    print('%9s : %s' % (key, key_state))
    return test_bit(globals()['KEY_ENTER'], buf)


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

color_sensor = ColorSensor('in3')
color_sensor.mode = 'COL-REFLECT'

sonar_sensor = UltrasonicSensor()
sonar_sensor.mode = 'US-DIST-CM'

lights = Led()
Led.delay_on = 500
Led.delay_off = 1500
lights.trigger = 'none'

time_since_escline = 0
time_since_turn = 0

is_esc_line = False
is_searching = True
lost_target = False
enemy_likes_to_go = 0 # 0 is center, 1 is right, -1 is left


print('ready')
lights.trigger = 'timer'
# input("Press enter to go!")
while not is_enter_pressed():
    pass


def go_forwards():
    MOTOR_POWER = 100
    motor_a.run_forever(duty_cycle_sp=MOTOR_POWER)
    motor_b.run_forever(duty_cycle_sp=MOTOR_POWER)
    motor_c.run_forever(duty_cycle_sp=MOTOR_POWER)
    motor_d.run_forever(duty_cycle_sp=MOTOR_POWER)


def tank_drive(left, right):
    motor_a.run_forever(duty_cycle_sp=right)
    motor_b.run_forever(duty_cycle_sp=left)
    motor_c.run_forever(duty_cycle_sp=left)
    motor_d.run_forever(duty_cycle_sp=right)


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
    if (sonar_sensor.value() / math.pow(10, sonar_sensor.decimals)) < 25:
        is_searching = False
signal.signal(signal.SIGINT, handler)


def proc_charge():
    global lost_target
    global time_since_turn
    go_forwards()
    if (sonar_sensor.value() / math.pow(10, sonar_sensor.decimals)) > 30:
        lost_target = True
        time_since_turn = time.time()


def proc_lost_target():
    global lost_target
    global enemy_likes_to_go
    global is_searching
    if(enemy_likes_to_go==1):
        if(time.time() - time_since_turn) < 1:
            tank_drive(75, -75)
            if (sonar_sensor.value() / math.pow(10, sonar_sensor.decimals)) <30:
                lost_target = False
                enemy_likes_to_go = 1
        elif(time.time() - time_since_turn) < 3:
            tank_drive(-75, 75)
            if (sonar_sensor.value() / math.pow(10, sonar_sensor.decimals)) <30:
                lost_target = False
                enemy_likes_to_go=-1
        else:
            lost_target = False
            enemy_likes_to_go = 0
            is_searching = True
    elif(enemy_likes_to_go==-1):
        if(time.time() - time_since_turn) < 1:
            tank_drive(-75, 75)
            if (sonar_sensor.value() / math.pow(10, sonar_sensor.decimals)) <30:
                lost_target = False
                enemy_likes_to_go = -1
        elif(time.time() - time_since_turn) < 3:
            tank_drive(75, -75)
            if (sonar_sensor.value() / math.pow(10, sonar_sensor.decimals)) <30:
                lost_target = False
                enemy_likes_to_go=1
        else:
            lost_target = False
            enemy_likes_to_go = 0
            is_searching = True
    else:
        if(time.time() - time_since_turn) < 1:
            tank_drive(75, -75)
            if (sonar_sensor.value() / math.pow(10, sonar_sensor.decimals)) <30:
                lost_target = False
                enemy_likes_to_go = 1
        elif(time.time() - time_since_turn) < 3:
            tank_drive(-75, 75)
            if (sonar_sensor.value() / math.pow(10, sonar_sensor.decimals)) <30:
                lost_target = False
                enemy_likes_to_go=-1
        else:
            lost_target = False
            enemy_likes_to_go = 0
            is_searching = True


def main():
    while(True):
        # print(is_enter_pressed())
        if is_esc_line is True:
            proc_esc_line()
        elif is_searching is True:
            proc_search()
        elif lost_target is True:
            proc_lost_target()
        else:
            proc_charge()
        # print(color_sensor.value())
        if is_esc_line is not True:
            if(color_sensor.value() > 40):
                esc_line()
                print('esc line called')
        time.sleep(.001)


if __name__ == "__main__":
    main()
