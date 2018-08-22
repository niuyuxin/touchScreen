#!/usr/bin/env python3

import platform
from PyQt5.QtCore import *
from config import *
if platform.machine() == "armv7l" and platform.node() == "raspberrypi":
    import RPi.GPIO as GPIO
    import PCF8591 as ADC
    import time
    from neopixel import *
    import argparse


# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class AnalogDetection(QObject):
    # pwm = 8, AD = 2,3
    COLOR_R = 0
    COLOR_G = 1
    COLOR_B = 2
    KEY_UP = 1
    KEY_DOWN = 0
    LED_ON  = 1 # GPIO.HIGH
    LED_OFF = 0 # GPIO.LOW
    USER_LED_ON = 0
    USER_LED_OFF = 1
    GPIO_RAISE = 5
    GPIO_STOP = 6
    GPIO_DROP = 13
    GPIO_ROCKER_RAISE = 19
    GPIO_ROCKER_DROP = 26
    GPIO_ROCKER_ENTER = 12
    GPIO_RAISE_LED = 16
    GPIO_STOP_LED = 20
    GPIO_DROP_LED = 21
    GPIO_RUNNING_LED = 11
    GPIO_USER_KEY3 = 10 # Fixme: error gpio
    GPIO_USER_KEY2 = 23
    GPIO_USER_KEY1 = 24
    GPIO_USER_KEY0 = 25
    GPIO_USER_LED3 = 4
    GPIO_USER_LED2 = 17
    GPIO_USER_LED1 = 27
    GPIO_USER_LED0 = 22
    PCF8591_SELECTED = 0
    PCF8591_IDEL = 1
    PCF8591_NOSELECTED = 2
    PCF8591_RUNNING = 3
    ADValueChanged = pyqtSignal(int, int)
    GPIOState = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.count = 0
        self.isRocker = int(Config.value("Rocker"))
        self.rockerCount = 0
        self.pcf8591LedMode = AnalogDetection.PCF8591_NOSELECTED
        self.pcf8591BreathCount = 0
        self.pcf8591BreathDir = 0
        self.pcf8591BreathColor = 0
        if platform.machine() == "armv7l" and platform.node() == "raspberrypi":
            self.isRaspberryPi = True
        else:
            self.isRaspberryPi = False
        self.selectedUserKey = {}
        self.userKeyLightMethod = {}
        self.keyGpio = {AnalogDetection.GPIO_RAISE: [],
                        AnalogDetection.GPIO_STOP: [],
                        AnalogDetection.GPIO_DROP: [],
                        AnalogDetection.GPIO_ROCKER_RAISE: [],
                        AnalogDetection.GPIO_ROCKER_DROP: [],
                        AnalogDetection.GPIO_ROCKER_ENTER: [],
                        AnalogDetection.GPIO_USER_KEY0:[],
                        AnalogDetection.GPIO_USER_KEY1: [],
                        AnalogDetection.GPIO_USER_KEY2: [],
                        AnalogDetection.GPIO_USER_KEY3: []}
        self.userKeyWithGpio = {
                        0:AnalogDetection.GPIO_USER_KEY0,
                        1:AnalogDetection.GPIO_USER_KEY1,
                        2:AnalogDetection.GPIO_USER_KEY2,
                        3:AnalogDetection.GPIO_USER_KEY3}
        self.userKeyWithLed = {
                        0:[AnalogDetection.GPIO_USER_LED0,0],
                        1:[AnalogDetection.GPIO_USER_LED1,0],
                        2:[AnalogDetection.GPIO_USER_LED2,0],
                        3:[AnalogDetection.GPIO_USER_LED3,0]}
        self.ledGpio = {AnalogDetection.GPIO_RAISE_LED: AnalogDetection.GPIO_RAISE,
                        AnalogDetection.GPIO_STOP_LED: AnalogDetection.GPIO_STOP,
                        AnalogDetection.GPIO_DROP_LED: AnalogDetection.GPIO_DROP,
                        AnalogDetection.GPIO_RUNNING_LED: -1,
                        AnalogDetection.GPIO_USER_LED0: AnalogDetection.GPIO_USER_KEY0,
                        AnalogDetection.GPIO_USER_LED1: AnalogDetection.GPIO_USER_KEY1,
                        AnalogDetection.GPIO_USER_LED2: AnalogDetection.GPIO_USER_KEY2,
                        AnalogDetection.GPIO_USER_LED3: AnalogDetection.GPIO_USER_KEY3}
        self.rockerKeyBuf = {
                        AnalogDetection.GPIO_ROCKER_RAISE: AnalogDetection.KEY_UP,
                        AnalogDetection.GPIO_ROCKER_DROP: AnalogDetection.KEY_UP,
                        AnalogDetection.GPIO_ROCKER_ENTER: AnalogDetection.KEY_UP
                        }
    def __del__(self):
        if self.isRaspberryPi:
            for led in self.ledGpio.keys():
                GPIO.output(led, AnalogDetection.LED_OFF)
            GPIO.cleanup()
    @pyqtSlot()
    def init(self):
        if not self.isRaspberryPi: return
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for key in self.keyGpio.keys():
            GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # GPIO.add_event_detect(key, GPIO.FALLING, callback=self.keyDetected, bouncetime=200)
        for led in self.ledGpio.keys():
            GPIO.setup(led, GPIO.OUT)
        GPIO.output(AnalogDetection.GPIO_RUNNING_LED, AnalogDetection.LED_ON)
        # AD GPIO2, GPIO3 i2c
        self.ADInit()
        # pwd led
        self.pixel = 0
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.internetState = 0
        self.keyTimer = QTimer(self)
        self.keyTimer.timeout.connect(self.onKeyTimerTimeout)
        self.keyTimer.start(10)
        self.perSecondTimer = QTimer(self)
        self.perSecondTimer.timeout.connect(self.onPerSecondTimerTimeout)
        self.perSecondTimer.start(1000)
        self.pcf8591LedLights(AnalogDetection.COLOR_R, 255)

    def onKeyTimerTimeout(self):
        if not self.isRocker:
            self.ADRead()
        self.keyRead()
        self.userKeyLedSparking()

    def onUserKeySelected(self, key): # in userkeys.py selected
        self.selectedUserKey = key

    def userKeyLedSparking(self): # per 10ms
        for sKey in self.selectedUserKey.keys():
            if self.selectedUserKey[sKey] < 0:
                GPIO.output(self.userKeyWithLed[sKey][0], AnalogDetection.USER_LED_OFF)
            else:
                if self.userKeyWithGpio[sKey] in self.userKeyLightMethod.keys() and \
                    self.userKeyLightMethod[self.userKeyWithGpio[sKey]] == AnalogDetection.KEY_DOWN:
                    GPIO.output(self.userKeyWithLed[sKey][0], AnalogDetection.USER_LED_ON)
                else:
                    if self.userKeyWithLed[sKey][1] < 195:
                        GPIO.output(self.userKeyWithLed[sKey][0], AnalogDetection.USER_LED_OFF)
                    elif self.userKeyWithLed[sKey][1] >= 195:
                        GPIO.output(self.userKeyWithLed[sKey][0], AnalogDetection.USER_LED_ON)
                    if self.userKeyWithLed[sKey][1] >= 200:
                        self.userKeyWithLed[sKey][1] = 0
                    else:
                        self.userKeyWithLed[sKey][1] += 1
        self.pcf8591Breath()

    def ADInit(self):
        ADC.setup(0x48)
        self.adBuf = []
        self.adValue = 0
    def ADRead(self, port=0):
        temp = ADC.read(port)
        if len(self.adBuf) >= 20:
            self.adBuf.pop(0)
        self.adBuf.append(temp)
        value = 0
        for ad in self.adBuf:
            value += ad
        value = value//len(self.adBuf)
        if self.adValue > value + 2 or self.adValue < value - 2:
            self.adValue = value
            self.ADValueChanged.emit(0, value*100//255)

    def onPcf8591Mode(self, mode):
        if self.internetState == 0:
            return
        self.pcf8591LedMode = mode
        if mode == AnalogDetection.PCF8591_NOSELECTED:
            self.pcf8591LedLights(AnalogDetection.COLOR_B, 0)
        elif mode == AnalogDetection.PCF8591_SELECTED:
            self.pcf8591LedLights(AnalogDetection.COLOR_B, 255)
        # elif mode == AnalogDetection.PCF8591_RUNNING:
        #     for i in range(8):
        #         self.strip.setPixelColor(i, Color(255, 0, 0))
        #         self.strip.show()
    def pcf8591Breath(self):
        if self.internetState == 0:
            return
        if self.pcf8591LedMode == AnalogDetection.PCF8591_IDEL:
            if self.pcf8591BreathDir == 0:
                self.pcf8591BreathCount += 1
                if self.pcf8591BreathCount % 255 >= 254:
                    self.pcf8591BreathDir = 1
            else:
                if self.pcf8591BreathCount > 0:
                    self.pcf8591BreathCount -= 1
                if self.pcf8591BreathCount == 0:
                    self.pcf8591BreathDir = 0
                    self.pcf8591BreathColor = not self.pcf8591BreathColor

            if self.pcf8591BreathColor == 0:
                self.pcf8591LedLights(AnalogDetection.COLOR_B, self.pcf8591BreathCount)
            else:
                self.pcf8591LedLights(AnalogDetection.COLOR_R, self.pcf8591BreathCount)

    def pcf8591LedLights(self, color, value):
        if color == AnalogDetection.COLOR_R:
            for i in range(8):
                self.strip.setPixelColor(i, Color(0, value, 0))
                self.strip.show()
        elif color == AnalogDetection.COLOR_B:
            for i in range(8):
                self.strip.setPixelColor(i, Color(0, 0, value))
                self.strip.show()
        elif color == AnalogDetection.COLOR_G:
            for i in range(8):
                self.strip.setPixelColor(i, Color(value, 0, 0))
                self.strip.show()

    def ADWrite(self, value):
        ADC.write(value)

    def keyRead(self):
        for item in self.keyGpio.items():
            gpio = item[0]
            values = item[1]
            value = GPIO.input(gpio)
            if len(self.keyGpio[gpio]) < 4:
                self.keyGpio[gpio].append(value)
            else:
                self.keyGpio[gpio].pop(0)
                self.keyGpio[gpio].append(value)
            if values == [AnalogDetection.KEY_UP, # down
                           AnalogDetection.KEY_DOWN,
                           AnalogDetection.KEY_DOWN,
                           AnalogDetection.KEY_DOWN]:
                self.keyDetected(gpio, AnalogDetection.KEY_DOWN)
                self.GPIOState.emit(gpio, AnalogDetection.KEY_DOWN)
            if values == [AnalogDetection.KEY_DOWN, # up
                           AnalogDetection.KEY_UP,
                           AnalogDetection.KEY_UP,
                           AnalogDetection.KEY_UP]:
                self.keyDetected(gpio, AnalogDetection.KEY_UP)

    def keyDetected(self, key, state):
        if key in [AnalogDetection.GPIO_DROP,
                    AnalogDetection.GPIO_STOP,
                    AnalogDetection.GPIO_RAISE]:
            self.workingLed(key)
        elif key in [AnalogDetection.GPIO_ROCKER_ENTER,
                    AnalogDetection.GPIO_ROCKER_DROP,
                    AnalogDetection.GPIO_ROCKER_RAISE
                    ]:
            if self.isRocker:
                self.rockerKeyBuf[key] = state
                if self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_ENTER] == AnalogDetection.KEY_DOWN:
                    if self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_DROP] == AnalogDetection.KEY_DOWN:
                        self.GPIOState.emit(AnalogDetection.GPIO_DROP, AnalogDetection.KEY_DOWN)
                        self.ADValueChanged.emit(0, self.rockerCount * 100 // 255)
                    elif self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_RAISE] == AnalogDetection.KEY_DOWN:
                        self.GPIOState.emit(AnalogDetection.GPIO_RAISE, AnalogDetection.KEY_DOWN)
                        self.ADValueChanged.emit(0, self.rockerCount * 100 // 255)
                    else:
                        self.GPIOState.emit(AnalogDetection.GPIO_STOP, AnalogDetection.KEY_DOWN)
        elif key in [AnalogDetection.GPIO_USER_KEY0,
                    AnalogDetection.GPIO_USER_KEY1,
                    AnalogDetection.GPIO_USER_KEY2,
                    AnalogDetection.GPIO_USER_KEY3]:
            self.userKeyLightMethod[key] = state

    def onPerSecondTimerTimeout(self):
        if self.isRocker:
            if self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_DROP] == AnalogDetection.KEY_DOWN:
                if self.rockerCount > 7:
                    self.rockerCount -= 7
                else:
                    self.rockerCount = 0
            elif self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_RAISE] == AnalogDetection.KEY_DOWN:
                if self.rockerCount < 255-8:
                    self.rockerCount += 8
                else:
                    self.rockerCount = 255
            self.ADWrite(self.rockerCount)
    def onWorkingState(self, s):
        if self.internetState == 0:
            return
        if s == -1:
            self.workingLed(AnalogDetection.GPIO_DROP_LED)
        elif s == 1:
            self.workingLed(AnalogDetection.GPIO_RAISE_LED)
        elif s == 0:
            self.workingLed(AnalogDetection.GPIO_STOP)
    def onInternetState(self, s):
        self.internetState = s
        if s == 0:
            self.workingLed(AnalogDetection.GPIO_STOP)
            self.pcf8591LedLights(AnalogDetection.COLOR_R, 255)
        else:
            self.pcf8591LedLights(AnalogDetection.COLOR_R, 0)

    def workingLed(self, key):
        for led in [AnalogDetection.GPIO_RAISE_LED,
                    AnalogDetection.GPIO_STOP_LED,
                    AnalogDetection.GPIO_DROP_LED]:
            if self.ledGpio[led] != key:
                GPIO.output(led, AnalogDetection.LED_OFF)
            else:
                GPIO.output(led, AnalogDetection.LED_ON)



