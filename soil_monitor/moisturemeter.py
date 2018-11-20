from typing import Any, Union

import RPi.GPIO as GPIO  # import RPi.GPIO module
from time import sleep  # lets us have a delay
from datetime import datetime


class MoistureMeter:
    def __init__(self, id, bcmpin):
        self.id = id
        self.bcmpin = int(bcmpin)
        # set up the pin for input
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        GPIO.setup(self.bcmpin, GPIO.IN)  # set input pin as an
        print("GPIO Pin " + str(self.bcmpin) + " set as input")

    def compute_kpa(self, frequency):
        # function to calculate the kPA value based on the input frequency.

        if frequency > 6430:
            kPa = 0
        elif frequency > 4330 and frequency <= 6430:
            kPa = 9 - ((frequency - 4600) * 0.004286)
        elif frequency > 2820 and frequency <= 4330:
            kPa = 15 - ((frequency - 2820) * 0.00291)
        elif frequency > 1110 and frequency <= 2820:
            kPa = 35 - ((frequency - 1110) * 0.01170)
        elif frequency > 770 and frequency <= 1110:
            kPa = 55 - ((frequency - 770) * 0.05884)
        elif frequency > 600 and frequency <= 770:
            kPa = 75 - ((frequency - 600) * 0.1176)
        elif frequency > 485 and frequency <= 600:
            kPa = 100 - ((frequency - 485) * 0.2174)
        elif frequency > 293 and frequency <= 485:
            kPa = 200 - ((frequency - 293) * 0.5208)
        elif frequency <= 293:
            kPa = 200

        return kPa

    def get_kpa_value(self):
        # set up the pin for input
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        GPIO.setup(self.bcmpin, GPIO.IN)  # set input pin as an
        print("GPIO Pin " + str(self.bcmpin) + " set as input")
        # Set up callback for sensor input (rising edge)

        print("Begin gathering sensor data for sensor " + self.id + "  " + str(self.bcmpin))

        print("self.bcmpin is ", self.bcmpin)
        state = GPIO.input(self.bcmpin)
        print("State is ", state)
        # wait for first rising edge detection

        # wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
        channel = GPIO.wait_for_edge(self.bcmpin, GPIO.RISING, timeout=5000)

        if channel is None:
            print('Timeout occurred')
        else:
            print('Edge detected on channel', channel)

        # start timer to begin measuring

        tstart = datetime.now()
        # print("Time Start : ", tstart)

        sample_count = 20
        total_time_measured = 0

        # now loop, repeatedly looking for rising edge and timing info
        for i in range(1, sample_count):
            channel = GPIO.wait_for_edge(self.bcmpin, GPIO.RISING, timeout=5000)

            if channel is None:
                print('Timeout occurred, abort')
                kPa = -1
                break
            else:
                tend = datetime.now()
                time_delta = tend - tstart
                total_seconds = time_delta.total_seconds()
                tstart = datetime.now()
                total_time_measured = total_time_measured + total_seconds
                # print("Elapsed Time : ", total_seconds)
                # calculate average input period over sample time

                period = total_time_measured / sample_count
                # print("calculated period : ", period)

                frequency = 1 / period

                # print("Frequency is : ", frequency)
                kPa = self.compute_kpa(frequency)

                # print("computed kPa is : ",kPa)

        return kPa
