import config
# import RPi.GPIO as GPIO
# import VPi.GPIO as GPIO


class Led:
    RED = config.PORT_RED  # GPIO port for red
    GREEN: int = config.PORT_GREEN  # GPIO port for green
    BLUE = config.PORT_BLUE  # GPIO port for blue
    FREQ = config.FREQ  # Frequency for PWM
    IS_ON = False

    def __init__(self):

        GPIO.setwarnings(False)

        # choose BCM or BOARD numbering schemes. I use BCM
        GPIO.setmode(GPIO.BCM)

        # set color ports as outputs
        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.setup(self.GREEN, GPIO.OUT)
        GPIO.setup(self.BLUE, GPIO.OUT)

    # cleanup PWM and GPIO environment
    def __del__(self):
        print('cleaning up')
        GPIO.cleanup()

    # method to start the pwm
    def start(self):
        self.set_color(0, 0, 0)

    def set_color(self, red_in, green_in, blue_in):
        # update internal color values
        self.RED = red_in
        self.GREEN = green_in
        self.BLUE = blue_in
        if self.RED == 0 and self.GREEN == 0 and self.BLUE == 0:
            self.IS_ON = False
        else:
            self.IS_ON = True
        self.change_color(red_in, green_in, blue_in)
        return True

    def set_on(self, switch):
        self.IS_ON = switch
        # switch lights off (color = [0, 0, 0]), but keep actual color in mind
        if switch:
            self.change_color(self.RED, self.GREEN, self.BLUE)
        elif not switch:
            self.change_color(0, 0, 0)
        else:
            print('switch is not boolean')

    def is_on(self):
        return self.IS_ON

    def change_color(self, red_in, green_in, blue_in):
        self._red_pwm.ChangeDutyCycle(red_in * 100.0 / 255.0)
        self._green_pwm.ChangeDutyCycle(green_in * 100.0 / 255.0)
        self._blue_pwm.ChangeDutyCycle(blue_in * 100.0 / 255.0)

    def print_color(self):
        print("r g b :", self.RED, self.GREEN, self.BLUE)

    def get_color(self):
        print(self.RED, self.GREEN, self.BLUE)
        return [self.RED, self.GREEN, self.BLUE]
