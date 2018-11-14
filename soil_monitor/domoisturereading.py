import Data.sensorconfig
import soil_monitor.moisturemeter as MM
import RPi.GPIO as GPIO  # import RPi.GPIO module

def main():
    print("main program for moisture reading")
    sensorinfo = Data.sensorconfig.getsensordata()

    print("First Sensor name is > ", sensorinfo["id"], " Sensor bcm pin is > ", sensorinfo["bcmpin"])

    sensor_1 = MM.MoistureMeter(sensorinfo["id"], sensorinfo["bcmpin"])
    sensor_kpa = sensor_1.get_kpa_value()

    print("Got kPa of : ", sensor_kpa)

    # Clean up GPIO
    GPIO.cleanup()

if __name__ == '__main__':
    main()
