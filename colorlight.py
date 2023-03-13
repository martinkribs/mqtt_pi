import config
import RPi.GPIO as GPIO
# import VPi.GPIO as GPIO


class Led:
    # Color values
    RED = 0
    GREEN = 0
    BLUE = 0
    IS_ON = False
    BRIGHT = config.FREQ

    def __init__(self):

        GPIO.setwarnings(False)

        # choose BCM or BOARD numbering schemes. I use BCM
        GPIO.setmode(GPIO.BCM)

        # set color ports as outputs
        GPIO.setup(config.PORT_RED, GPIO.OUT)
        GPIO.setup(config.PORT_GREEN, GPIO.OUT)
        GPIO.setup(config.PORT_BLUE, GPIO.OUT)

        # create objects for PWM on color output ports
        self.RED_PWM = GPIO.PWM(config.PORT_RED, self.BRIGHT)
        self.GREEN_PWM = GPIO.PWM(config.PORT_GREEN, self.BRIGHT)
        self.BLUE_PWM = GPIO.PWM(config.PORT_BLUE, self.BRIGHT)

    # cleanup PWM and GPIO environment
    def __del__(self):
        print('cleaning up')
        self.RED_PWM.stop()
        self.GREEN_PWM.stop()
        self.BLUE_PWM.stop()
        GPIO.cleanup()

    def get_status(self):
        return self.IS_ON

    def get_color(self):
        return self.RED, self.GREEN, self.BLUE

    def get_brightness(self):
        return self.BRIGHT

    def set_status(self, switch):
        self.IS_ON = switch
        # switch lights off (color = [0, 0, 0]), but keep actual color in mind
        if switch:
            self.change(self.RED, self.GREEN, self.BLUE)
        elif not switch:
            self.change(0, 0, 0)
        else:
            print('switch is not boolean')

    def set_color(self, red_in, green_in, blue_in):
        # update internal color values
        self.RED = red_in
        self.GREEN = green_in
        self.BLUE = blue_in
        if self.RED == 0 and self.GREEN == 0 and self.BLUE == 0:
            self.IS_ON = False
        else:
            self.IS_ON = True
        self.change(red_in, green_in, blue_in)
        return True

    def set_brightness(self, brightness_in):
        self.BRIGHT = brightness_in
        return True

        # method to start the pwm

    def start(self):
        self.RED_PWM.start(0)
        self.GREEN_PWM.start(0)
        self.BLUE_PWM.start(0)
        self.set_color(0, 0, 0)

    def change(self, red_in, green_in, blue_in):
        # keep self values, just modify output values
        # change pwm duty cycles
        # calculate from 0..255 to 0..100%
        self.RED_PWM.ChangeDutyCycle(red_in * 100.0 / 255.0)
        self.GREEN_PWM.ChangeDutyCycle(green_in * 100.0 / 255.0)
        self.BLUE_PWM.ChangeDutyCycle(blue_in * 100.0 / 255.0)
