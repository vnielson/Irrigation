import Data.data_access
import soil_monitor.moisturemeter as MM
import RPi.GPIO as GPIO  # import RPi.GPIO module

def main():
    print("main program for moisture reading")
    sensorinfo = Data.data_access.get_sensors()

    #    print("By Row:")
    #    for row in sensorinfo:
    #        print("Row:", row)

    for row in sensorinfo:
        nxt_sensor = MM.MoistureMeter(row['sensor_id'], row['bcm_pin'])
        print("get kPa for : ", nxt_sensor.id)
        sensor_reading_data = nxt_sensor.get_kpa_value()
        print("Return data: ", sensor_reading_data)
        Data.data_access.save_sensor_reading(nxt_sensor.id, sensor_reading_data)

    # Clean up GPIO
    GPIO.cleanup()


if __name__ == '__main__':
    main()
