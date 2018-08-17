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



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functionst).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            print ('Color wipe animations.')
            colorWipe(strip, Color(255, 0, 0))  # Red wipe
            colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            colorWipe(strip, Color(0, 0, 255))  # Green wipe
            print ('Theater chase animations.')
            theaterChase(strip, Color(127, 127, 127))  # White theater chase
            theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            print ('Rainbow animations.')
            rainbow(strip)
            rainbowCycle(strip)
            theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

class AnalogDetection(QObject):
    # pwm = 8, AD = 2,3
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
    GPIO_USER_KEY3 = 10 # Fixme: error gpio
    GPIO_USER_KEY2 = 23
    GPIO_USER_KEY1 = 24
    GPIO_USER_KEY0 = 25
    GPIO_USER_LED3 = 4
    GPIO_USER_LED2 = 17
    GPIO_USER_LED1 = 27
    GPIO_USER_LED0 = 22
    ADValueChanged = pyqtSignal(int, int)
    GPIOState = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.count = 0
        self.isRocker = int(Config.value("Rocker"))
        self.rockerCount = 0
        if platform.machine() == "armv7l" and platform.node() == "raspberrypi":
            self.isRaspberryPi = True
        else:
            self.isRaspberryPi = False
        self.selectedUserKey = {}
        self.userKeyLightMethod = {}
    def __del__(self):
        if self.isRaspberryPi:
            GPIO.cleanup()
    @pyqtSlot()
    def init(self):
        if not self.isRaspberryPi: return
        GPIO.setmode(GPIO.BCM)
        # key gpio
        self.keyGpio = {AnalogDetection.GPIO_RAISE: [],
                        AnalogDetection.GPIO_STOP: [],
                        AnalogDetection.GPIO_DROP: [],
                        AnalogDetection.GPIO_ROCKER_DOWN: [],
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
                        AnalogDetection.GPIO_USER_LED0: AnalogDetection.GPIO_USER_KEY0,
                        AnalogDetection.GPIO_USER_LED1: AnalogDetection.GPIO_USER_KEY1,
                        AnalogDetection.GPIO_USER_LED2: AnalogDetection.GPIO_USER_KEY2,
                        AnalogDetection.GPIO_USER_LED3: AnalogDetection.GPIO_USER_KEY3}
        self.rockerKeyBuf = {
                        AnalogDetection.GPIO_ROCKER_RAISE: AnalogDetection.KEY_UP,
                        AnalogDetection.GPIO_ROCKER_DROP: AnalogDetection.KEY_UP,
                        AnalogDetection.GPIO_ROCKER_ENTER: AnalogDetection.KEY_UP
                        }
        GPIO.setwarnings(False)
        for key in self.keyGpio.keys():
            GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # GPIO.add_event_detect(key, GPIO.FALLING, callback=self.keyDetected, bouncetime=200)
        for led in self.ledGpio.keys():
            GPIO.setup(led, GPIO.OUT)
        # AD GPIO2, GPIO3 i2c
        self.ADInit()
        # pwd led
        self.pixel = 0
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

        self.keyTimer = QTimer(self)
        self.keyTimer.timeout.connect(self.onKeyTimerTimeout)
        self.keyTimer.start(10)
        self.perSecondTimer = QTime(self)
        self.perSecondTimer.timeout.connect(self.onPerSecondTimerTimeout)
        self.perSecondTimer.start(1000)

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
                    self.userKeyLightMethod[self.userKeyWithGpio[sKey]] == True:
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
                self.keyDetected(gpio, True)
                self.GPIOState.emit(gpio, True)
            if values == [AnalogDetection.KEY_DOWN, # up
                           AnalogDetection.KEY_UP,
                           AnalogDetection.KEY_UP,
                           AnalogDetection.KEY_UP]:
                self.keyDetected(gpio, False)

    def keyDetected(self, key, state):
        if key in [AnalogDetection.GPIO_DROP,
                    AnalogDetection.GPIO_STOP,
                    AnalogDetection.GPIO_RAISE]:
            for led in self.ledGpio.keys():
                if self.ledGpio[led] != key:
                    GPIO.output(led, GPIO.LOW)
                else:
                    GPIO.output(led, GPIO.HIGH)
        elif key in [AnalogDetection.GPIO_ROCKER_ENTER,
                    AnalogDetection.GPIO_ROCKER_DROP,
                    AnalogDetection.GPIO_ROCKER_RAISE
                    ]:
            self.rockerKeyBuf[key] = state
        elif key in [AnalogDetection.GPIO_USER_KEY0,
                    AnalogDetection.GPIO_USER_KEY1,
                    AnalogDetection.GPIO_USER_KEY2,
                    AnalogDetection.GPIO_USER_KEY3]:
            self.userKeyLightMethod[key] = state

    def onPerSecondTimerTimeout(self):
        if self.isRocker:
            if self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_ENTER] == AnalogDetection.KEY_DOWN:
                if self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_DROP] == AnalogDetection.KEY_DOWN:
                    self.GPIOState.emit(AnalogDetection.GPIO_DROP, True)
                    self.ADValueChanged.emit(0, self.rockerCount % 255)
                elif self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_RAISE] == AnalogDetection.KEY_DOWN:
                    self.GPIOState.emit(AnalogDetection.GPIO_RAISE, True)
                    self.ADValueChanged.emit(0, self.rockerCount % 255)
                else:
                    self.GPIOState.emit(AnalogDetection.GPIO_STOP, True)
            if self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_DROP] == AnalogDetection.KEY_DOWN:
                if self.rockerCount > 0:
                    self.rockerCount -= 1
            elif self.rockerKeyBuf[AnalogDetection.GPIO_ROCKER_RAISE] == AnalogDetection.KEY_DOWN:
                if self.rockerCount < 255:
                    self.rockerCount += 1
            self.ADWrite(self.rockerCount)





