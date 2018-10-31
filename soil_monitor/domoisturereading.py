import Data.sensorconfig

def main():
    print("main program for moisture reading")
    sensorinfo = Data.sensorconfig.getsensordata()

    print ("First Sensor name is > ",sensorinfo["id"], " Sensor port is > ",sensorinfo["port"])

if __name__ == '__main__':
    main()
