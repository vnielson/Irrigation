from sqlalchemy import (create_engine, Table, Column, Integer,
                        String, MetaData)

from sqlalchemy import (create_engine, Table, Column, Integer,
                        String, MetaData, inspect, select)


def get_sensors():
    engine = create_engine('postgres:///irrigationdb')

    with engine.connect() as con:
        meta = MetaData(engine)
        sensors = Table('sensors', meta, autoload=True)

        stm = select([sensors])
        rs = con.execute(stm)
    return rs


def save_sensor_reading(sensor_id, kpa_value):
    print("save data: ", sensor_id, kpa_value)

    engine = create_engine('postgres:///irrigationdb')

    with engine.connect() as con:
        meta = MetaData(engine)
        sensor_readings = Table('sensor_readings', meta, autoload=True)

        ins1 = sensor_readings.insert().values(sensor_id=sensor_id, kpa_value=kpa_value)
        con.execute(ins1)
