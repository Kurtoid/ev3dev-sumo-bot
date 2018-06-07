#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import sys
import time
from kurtsev3functions import GyroPointTurn, KurtsRobot
if __name__=="__main__":
    r = KurtsRobot.KurtsRobot()
    gpt = GyroPointTurn.GyroPointTurn(r)
    gpt.turn_deg(90)
    r.stop()
