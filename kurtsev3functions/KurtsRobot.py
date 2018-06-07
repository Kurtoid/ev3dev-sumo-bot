#! /usr/bin/python3

import ev3dev.ev3 as ev3
class KurtsRobot(object):
    def __init__(self):
        self.motor_a = ev3.LargeMotor('outA')
        self.motor_b = ev3.LargeMotor('outB')
        self.motor_c = ev3.LargeMotor('outC')
        self.motor_d = ev3.LargeMotor('outD')
        self.motor_a.polarity = 'inversed'
        self.motor_b.polarity = 'inversed'
        self.motor_c.polarity = 'normal'
        self.motor_d.polarity = 'normal'

        self.motor_a.stop_action = 'brake'
        self.motor_b.stop_action = 'brake'
        self.motor_c.stop_action = 'brake'
        self.motor_d.stop_action = 'brake'

        self.sonar_sensor = ev3.UltrasonicSensor()
        self.sonar_sensor.mode = self.sonar_sensor.MODE_US_DIST_CM

        self.gyro_sensor = ev3.GyroSensor()
        self.gyro_sensor.mode = self.gyro_sensor.MODE_GYRO_ANG

        self.light_sensor = ev3.ColorSensor()
        self.light_sensor.mode = self.light_sensor.MODE_COL_REFLECT

    def go_forwards(self, speed):
        self.motor_a.speed_sp = speed
        self.motor_b.speed_sp = speed
        self.motor_c.speed_sp = speed
        self.motor_d.speed_sp = speed

        self.motor_a.run_forever()
        self.motor_b.run_forever()
        self.motor_c.run_forever()
        self.motor_d.run_forever()


    def tank_drive(self, left, right):
        self.motor_a.speed_sp = right
        self.motor_b.speed_sp = left
        self.motor_c.speed_sp = left
        self.motor_d.speed_sp = right

        self.motor_a.run_forever()
        self.motor_b.run_forever()
        self.motor_c.run_forever()
        self.motor_d.run_forever()


    def go_back(self):
        self.motor_a.run_direct(duty_cycle_sp=-75)
        self.motor_b.run_direct(duty_cycle_sp=-75)
        self.motor_c.run_direct(duty_cycle_sp=-75)
        self.motor_d.run_direct(duty_cycle_sp=-75)


    def turn_right(self):
        self.motor_a.run_direct(duty_cycle_sp=-75)
        self.motor_b.run_direct(duty_cycle_sp=75)
        self.motor_c.run_direct(duty_cycle_sp=75)
        self.motor_d.run_direct(duty_cycle_sp=-75)


    def turn_left(self):
        self.motor_a.run_direct(duty_cycle_sp=75)
        self.motor_b.run_direct(duty_cycle_sp=-75)
        self.motor_c.run_direct(duty_cycle_sp=-75)
        self.motor_d.run_direct(duty_cycle_sp=75)


    def stop(self):
        self.motor_a.stop()
        self.motor_b.stop()
        self.motor_c.stop()
        self.motor_d.stop()
