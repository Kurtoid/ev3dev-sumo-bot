#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import sys
import time
import math
import signal
from kurtsev3functions import GyroPointTurn, KurtsRobot

def signal_handler(signal, frame):
    print('exiting')
    if r != None:
        r.stop()
    sys.exit(1)
r = None

SEARCH_RANGE = 30

STATUS_BEGIN = 0
STATUS_SEARCHING = 1
STATUS_PUSHING = 2
STATUS_AVOID_LINE = 3
STATUS_LOST_TARGET = 4
current_status = STATUS_SEARCHING 
last_status_change_timer = time.time()
enemy_likes_to_go = 0  # 0 is center, 1 is right, -1 is left
def seeing_target(r):
    return (r.sonar_sensor.value()/math.pow(10,r.sonar_sensor.decimals))<SEARCH_RANGE
if __name__=="__main__":
    signal.signal(signal.SIGINT, signal_handler)
    r = KurtsRobot.KurtsRobot()
    while True:
        if(current_status==STATUS_SEARCHING):
            r.turn_left()
            if(seeing_target(r)):
                current_status = STATUS_PUSHING
        elif(current_status == STATUS_PUSHING):
            r.go_forwards(750)
            if(not seeing_target(r)):
                current_status = STATUS_LOST_TARGET
                last_status_change_timer = time.time()
        elif(current_status == STATUS_LOST_TARGET):
            if(enemy_likes_to_go == 0):
                if(time.time() - last_status_change_timer < 1):
                    r.turn_left()
                    if(seeing_target(r)):
                        enemy_likes_to_go=-1
                        current_status = STATUS_PUSHING
                elif(time.time() - last_status_change_timer < 2):
                    r.turn_right()
                    if(seeing_target(r)):
                        enemy_likes_to_go=1
                        current_status = STATUS_PUSHING
                else:
                    current_status = STATUS_SEARCHING
            elif(enemy_likes_to_go == 1):
                r.turn_right()
                if(seeing_target(r)):
                    current_status = STATUS_PUSHING
            elif(enemy_likes_to_go == -1):
                r.turn_left()
                if(seeing_target(r)):
                    current_status = STATUS_PUSHING
        if(r.light_sensor.value()>50):
            current_status = STATUS_AVOID_LINE
            last_status_change_timer = time.time()
        if(current_status == STATUS_AVOID_LINE):
            if(time.time() - last_status_change_timer < 1):
                r.go_back()
            else:
                current_status = STATUS_SEARCHING
        time.sleep(1/15)

