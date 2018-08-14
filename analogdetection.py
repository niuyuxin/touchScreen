#!/usr/bin/env python3

import platform
from PyQt5.QtCore import *
if platform.machine() == "armv7l" and platform.node() == "raspberrypi":
    import RPi.GPIO as GPIO


class AnalogDetection(QObject):
    GPIO_RAISE = 5
    GPIO_STOP = 6
    GPIO_DROP = 7
    GPIO_RAISE_LED = 3
    GPIO_STOP_LED = 4
    GPIO_DROP_LED = 5
    SPEED_ANALOG_IN = 6
    GPIO_PWM = 7
    GPIO_USER_KEY0 = 18
    GPIO_USER_KEY1 = 23
    GPIO_USER_KEY2 = 24
    GPIO_USER_KEY3 = 25

    def __init__(self, parent=None):
        super().__init__(parent)
        if platform.machine() == "armv7l" and platform.node() == "raspberrypi":
            self.isRaspberryPi = True
        else:
            self.isRaspberryPi = False

    @pyqtSlot()
    def init(self):
        if not self.isRaspberryPi: return
        self.keyGpio = {AnalogDetection.GPIO_RAISE:[],
                          AnalogDetection.GPIO_STOP:[],
                          AnalogDetection.GPIO_DROP:[],
                          AnalogDetection.GPIO_USER_KEY0:[],
                          AnalogDetection.GPIO_USER_KEY1: [],
                          AnalogDetection.GPIO_USER_KEY2: [],
                          AnalogDetection.GPIO_USER_KEY3: []}
        for key in self.keyGpio.keys():
            GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(key, GPIO.FALLING, callback=self.keyDetected, bouncetime=30)
        # self.keyTimer = QTimer(self)
        # self.keyTimer.timeout.connect(self.onKeyTimerTimeout)
        # self.keyTimer.start(10)

    def onKeyTimerTimeout(self):
        pass

    def keyDetected(self, key):
        print(key, "Pressed")


