#!/usr/bin/env python3

import platform
from PyQt5.QtCore import *
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
    # Intialize the library (must be called once before other functions).
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
    GPIO_RAISE = 5
    GPIO_STOP = 6
    GPIO_DROP = 13
    GPIO_RAISE_LED = 16
    GPIO_STOP_LED = 20
    GPIO_DROP_LED = 21
    SPEED_ANALOG_IN = 6
    GPIO_PWM = 7
    GPIO_USER_KEY0 = 17
    GPIO_USER_KEY1 = 23
    GPIO_USER_KEY2 = 24
    GPIO_USER_KEY3 = 25
    ADValueChanged = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super().__init__(parent)
        if platform.machine() == "armv7l" and platform.node() == "raspberrypi":
            self.isRaspberryPi = True
        else:
            self.isRaspberryPi = False

    @pyqtSlot()
    def init(self):
        if not self.isRaspberryPi: return
        # key gpio
        self.keyGpio = {AnalogDetection.GPIO_RAISE:[],
                          AnalogDetection.GPIO_STOP:[],
                          AnalogDetection.GPIO_DROP:[],
                          AnalogDetection.GPIO_USER_KEY0:[],
                          AnalogDetection.GPIO_USER_KEY1: [],
                          AnalogDetection.GPIO_USER_KEY2: [],
                          AnalogDetection.GPIO_USER_KEY3: []}
        self.ledGpio = {AnalogDetection.GPIO_RAISE_LED:AnalogDetection.GPIO_RAISE,
                        AnalogDetection.GPIO_STOP_LED:AnalogDetection.GPIO_STOP,
                        AnalogDetection.GPIO_DROP_LED:AnalogDetection.GPIO_DROP}
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for key in self.keyGpio.keys():
            GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(key, GPIO.FALLING, callback=self.keyDetected, bouncetime=200)
        for led in self.ledGpio.keys():
            GPIO.setup(led, GPIO.OUT)
        # AD
        ADC.setup(0x48)
        self.adBuf = []
        self.adValue = 0
        # pwd led
        self.pixel = 0
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

        self.keyTimer = QTimer(self)
        self.keyTimer.timeout.connect(self.onKeyTimerTimeout)
        self.keyTimer.start(10)

    def onKeyTimerTimeout(self):
        temp = ADC.read(0)
        if len(self.adBuf) >= 20:
            self.adBuf.pop(0)
        self.adBuf.append(temp)
        value = 0
        for ad in self.adBuf:
            value += ad
        value = value//len(self.adBuf)
        if self.adValue > value + 3 or self.adValue < value - 3:
            self.adValue = value
            self.ADValueChanged.emit(0, value*100//255)
        if self.pixel < 16:
            self.pixel += 1
        else:
            self.pixel = 0
        self.strip.setPixelColor(self.pixel, Color(value, 0, 0))
        self.strip.show()
    def keyDetected(self, key):
        print(key, "Pressed")
        if key in [AnalogDetection.GPIO_DROP, AnalogDetection.GPIO_STOP, AnalogDetection.GPIO_RAISE]:
            for led in self.ledGpio.keys():
                if self.ledGpio[led] != key:
                    GPIO.output(led, GPIO.LOW)
                else:
                    GPIO.output(led, GPIO.HIGH)

