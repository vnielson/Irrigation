import RPi.GPIO as GPIO  # import RPi.GPIO module
from time import sleep  # lets us have a delay

GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
GPIO.setup(5, GPIO.OUT)  # set GPIO5 as an output

print("setup complete, start loop")
half_period = 0.25
try:
    while True:
        #        print("set HIGH")
        GPIO.output(5, 1)  # set GPIO24 to 1/GPIO.HIGH/True
        sleep(half_period)  # wait half_period
        #        print("set LOW")
        GPIO.output(5, 0)  # set GPIO24 to 0/GPIO.LOW/False
        sleep(half_period)  # wait half a second

except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    print("Got Control C")
    GPIO.cleanup()  # resets all GPIO ports used by this program
    exit()
