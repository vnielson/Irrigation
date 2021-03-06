from typing import Any, Union

import RPi.GPIO as GPIO  # import RPi.GPIO module
from time import sleep  # lets us have a delay
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt


class MoistureMeter:
    def __init__(self, id, bcmpin):
        self.id = id
        self.bcmpin = int(bcmpin)
        # set up the pin for input
        print("GPIO BCM Value is : ", GPIO.BCM)
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        GPIO.setup(self.bcmpin, GPIO.IN)  # set input pin as an
        print("GPIO Pin " + str(self.bcmpin) + " set as input")

    def compute_kpa(self, frequency):
        # function to calculate the kPA value based on the input frequency.

        print("compute_kpa input frequency is : ", frequency)

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

        sample_count = 500

        per_array = np.zeros(sample_count)

        valid_data = True

        # now loop, repeatedly looking for rising edge and timing info
        for i in range(0, sample_count):
            channel = GPIO.wait_for_edge(self.bcmpin, GPIO.RISING, timeout=5000)

            if channel is None:
                print('Timeout occurred, abort')
                kPa = -1
                valid_data = False
                break
            else:
                tend = datetime.now()
                time_delta = tend - tstart
                # print("Delta for this loop: ",time_delta.total_seconds())
                per_array[i] = time_delta.total_seconds()
                tstart = datetime.now()

        print("per_array: ", per_array)

        if (valid_data):
            # Calculate final kPa data
            total_time_measured = per_array.sum()

            period = total_time_measured / sample_count
            frequency = 1 / period

            # print("calculated period : ", period)
            kPa = self.compute_kpa(frequency)

            # compute some statistics that might help understand how well the system is working
            min_frequency = 1.0 / per_array.max()
            max_frequency = 1.0 / per_array.min()
            mean = 1 / per_array.mean()
            stddev = 1 / per_array.std()

        return_data = {"kPa": kPa, "computed_frequency": frequency, "min_frequency": min_frequency,
                       "max_frequency": max_frequency, "mean": mean, "stddev": stddev}



        return return_data

    def plot_state_data(self):
        print("self.bcmpin is ", self.bcmpin)
        state = GPIO.input(self.bcmpin)
        print("State is ", state)

        # start timer to begin measuring

        # print("Time Start : ", tstart)

        sample_count = 500

        time_array = np.zeros(sample_count)
        state_array = np.zeros(sample_count, dtype=int)

        points = np.arange(-5, 5, 0.01)
        dx, dy = np.meshgrid(points, points)
        z = (np.sin(dx) + np.sin(dy))
        plt.imshow(z)
        plt.colorbar()
        plt.title('plot for sin(x)+sin(y)')
        plt.show()

        valid_data = True

        # now loop, repeatedly looking for rising edge and timing info
        tstart = datetime.now()
        for i in range(0, sample_count):
            state = GPIO.input(self.bcmpin)
            state_array[i] = state
            tend = datetime.now()
            time_delta = tend - tstart
            time_array[i] = time_delta.total_seconds()

        print(time_array)
        print(state_array)
        return
