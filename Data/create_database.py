from sqlalchemy import (create_engine, Table, Column, Integer, Float,
                        String, MetaData, DateTime, inspect, select)


def drop_all_tables(eng):
    print("in drop")

    inspector = inspect(eng)

    for table_name in inspector.get_table_names():
        print("Next Table is: ", table_name)
        eng.DropTable(table_name)

    # print("Drop crop_data")
    # eng.drop('crop_data')
    # print("Drop sensor_readings")
    # eng.drop('sensor_readings')
    # print("Drop sensors")
    # eng.drop('sensors')


def create_tables(eng):
    print("in create")
    connection = eng.connect()
    metadata = MetaData()

    sensors = Table('sensors', metadata,
                    Column('sensor_id', String(255)),
                    Column('configuration', String(255)),
                    Column('crop', String(255)),
                    Column('bcm_pin', int)
                    )
    sensor_readings = Table('sensor_readings', metadata,
                            Column('recorded_at', DateTime(True), default=datetime.datetime.utcnow),
                            Column('sensor_id', String(255)),
                            Column('kpa_value', Float(2)),
                            Column('min_frequency', Float(2)),
                            Column('max_frequency', Float(2))
                            )
    crop_data = Table('crop_data', metadata,
                      Column('crop', String(255)),
                      Column('soil_type', String(255), nullable=False),
                      Column('ideal_kpa', Integer(), default=100.0),
                      Column('saturated_kpa', Integer(), default=100.0),
                      Column('saturated_kpa', Integer(), default=100.0)
                      )

    metadata.create_all(eng)  # Creates the table

# if __name__ == '__main__':
#   engine = create_engine('postgres:///irrigationdb')

#  drop_all_tables(engine)
    # create_tables(engine)
