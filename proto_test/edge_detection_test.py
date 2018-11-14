import RPi.GPIO as GPIO  # import RPi.GPIO module
from time import sleep  # lets us have a delay
from datetime import datetime

GPIO.cleanup()

id = "id_1"
bcmpin = 12
# set up the pin for input
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
GPIO.setup(bcmpin, GPIO.IN)  # set input pin as an
print("GPIO Pin " + str(bcmpin) + " set as input")
# Set up callback for sensor input (rising edge)

print("Begin gathering sensor data for sensor " + id + "  " + str(bcmpin))

print("self.bcmpin is ", bcmpin)
state = GPIO.input(bcmpin)
print("State is ", state)
# wait for first rising edge detection

# wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
channel = GPIO.wait_for_edge(bcmpin, GPIO.RISING, timeout=5000)

if channel is None:
    print('Timeout occurred')
else:
    print('Edge detected on channel', channel)

# start timer to begin measuring

tstart = datetime.now()
print("Time Start : ", tstart)

sample_count = 20
total_time_measured = 0

# now loop, repeatedly looking for rising edge and timing info
for i in range(1, sample_count):
    channel = GPIO.wait_for_edge(bcmpin, GPIO.RISING, timeout=5000)

    if channel is None:
        print('Timeout occurred, abort')
        break
    else:
        tend = datetime.now()
        time_delta = tend - tstart
        total_seconds = time_delta.total_seconds()
        tstart = datetime.now()
        total_time_measured = total_time_measured + total_seconds
        print("Elapsed Time : ", total_seconds)

# calculate average input period over sample time

period = total_time_measured / sample_count
print("calculated period : ", period)

frequency = 1 / period

print("Frequency is : ", frequency)

GPIO.cleanup()
