#!/usr/bin/env python3
from ev3dev import ev3
class GyroPointTurn(object):
    def turn_deg(self, degrees):
        print(self.sensor.value())
        old_ang = self.sensor.value()
        while(abs(old_ang-self.sensor.value())<degrees):
            self.robot.turn_left()

    def __init__(self, robot):
        self.sensor = ev3.GyroSensor()
        self.sensor.mode = self.sensor.MODE_GYRO_ANG
        self.robot = robot

if __name__=="__main__":
    g = GyroPointTurn()
    g.turn_deg(90)
