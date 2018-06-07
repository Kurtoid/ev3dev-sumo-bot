#! /usr/bin/python3

import curses
import ev3dev.ev3 as ev3
import signal

motor_a = ev3.LargeMotor('outA')
motor_b = ev3.LargeMotor('outB')
motor_c = ev3.LargeMotor('outC')
motor_d = ev3.LargeMotor('outD')
motor_a.polarity = 'inversed'
motor_b.polarity = 'inversed'
motor_c.polarity = 'normal'
motor_d.polarity = 'normal'

motor_a.stop_action = 'brake'
motor_b.stop_action = 'brake'
motor_c.stop_action = 'brake'
motor_d.stop_action = 'brake'
def go_forwards():
    MOTOR_POWER = 100
    motor_a.run_direct(duty_cycle_sp=MOTOR_POWER)
    motor_b.run_direct(duty_cycle_sp=MOTOR_POWER)
    motor_c.run_direct(duty_cycle_sp=MOTOR_POWER)
    motor_d.run_direct(duty_cycle_sp=MOTOR_POWER)


def tank_drive(left, right):
    motor_a.run_direct(duty_cycle_sp=right)
    motor_b.run_direct(duty_cycle_sp=left)
    motor_c.run_direct(duty_cycle_sp=left)
    motor_d.run_direct(duty_cycle_sp=right)


def go_back():
    motor_a.run_direct(duty_cycle_sp=-75)
    motor_b.run_direct(duty_cycle_sp=-75)
    motor_c.run_direct(duty_cycle_sp=-75)
    motor_d.run_direct(duty_cycle_sp=-75)


def turn_right():
    motor_a.run_direct(duty_cycle_sp=-75)
    motor_b.run_direct(duty_cycle_sp=75)
    motor_c.run_direct(duty_cycle_sp=75)
    motor_d.run_direct(duty_cycle_sp=-75)


def turn_left():
    motor_a.run_direct(duty_cycle_sp=75)
    motor_b.run_direct(duty_cycle_sp=-75)
    motor_c.run_direct(duty_cycle_sp=-75)
    motor_d.run_direct(duty_cycle_sp=75)


def stop():
    motor_a.stop()
    motor_b.stop()
    motor_c.stop()
    motor_d.stop()


def endprog():
    stop()
    exit()
def handler(signal, frame):
    print("control c pressed, ending now")
    endprog()
signal.signal(signal.SIGINT, handler)

screen = curses.initscr()
try:
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)
    screen.addstr("Press a key")
    while True:
        event = screen.getch()
        print(event)
        if event == curses.KEY_LEFT:
            print("Left Arrow Key pressed")
            turn_left()

        elif event == curses.KEY_RIGHT:
            print("Right Arrow Key pressed")
            turn_right()
        elif event == curses.KEY_UP:
            go_forwards()
        elif event == curses.KEY_DOWN:
            go_back()
        elif event == curses.KEY_BACKSPACE:
            stop()
        elif event == 120:
            ev3.Sound.tone([
                (392, 350, 100), (392, 350, 100), (392, 350, 100), (311.1, 250, 100),
                (466.2, 25, 100), (392, 350, 100), (311.1, 250, 100), (466.2, 25, 100),
                (392, 700, 100), (587.32, 350, 100), (587.32, 350, 100),
                (587.32, 350, 100), (622.26, 250, 100), (466.2, 25, 100),
                (369.99, 350, 100), (311.1, 250, 100), (466.2, 25, 100), (392, 700, 100),
                (784, 350, 100), (392, 250, 100), (392, 25, 100), (784, 350, 100),
                (739.98, 250, 100), (698.46, 25, 100), (659.26, 25, 100),
                (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200), (554.36, 350, 100),
                (523.25, 250, 100), (493.88, 25, 100), (466.16, 25, 100), (440, 25, 100),
                (466.16, 50, 400), (311.13, 25, 200), (369.99, 350, 100),
                (311.13, 250, 100), (392, 25, 100), (466.16, 350, 100), (392, 250, 100),
                (466.16, 25, 100), (587.32, 700, 100), (784, 350, 100), (392, 250, 100),
                (392, 25, 100), (784, 350, 100), (739.98, 250, 100), (698.46, 25, 100),
                (659.26, 25, 100), (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200),
                (554.36, 350, 100), (523.25, 250, 100), (493.88, 25, 100),
                (466.16, 25, 100), (440, 25, 100), (466.16, 50, 400), (311.13, 25, 200),
                (392, 350, 100), (311.13, 250, 100), (466.16, 25, 100),
                (392.00, 300, 150), (311.13, 250, 100), (466.16, 25, 100), (392, 700)
            ])
        else:
            print(event)
            stop()

finally:
    curses.endwin()
