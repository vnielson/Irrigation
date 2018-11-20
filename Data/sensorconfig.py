def get_conn():
    # The raspberry pi has been set up to allow peer authentication locally, and we've created a database
    # and a role with the same name as the linux user we're running this script as. Therefore we can use an
    # empty connection string.
    # See for details: http://initd.org/psycopg/docs/module.html#psycopg2.connect
    return psycopg2.connect(database='irrigationdb')


def getsensordata():
    print('in get sensor data')

    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        destination_overview_query = """
             SELECT
               destination,
               min(pingtime),
               round(avg(pingtime), 2) AS avg,
               max(pingtime)
             FROM
               pings
             WHERE
               recorded_at > now() - INTERVAL '1 hour'
             GROUP BY
               destination;
         """

        cur.execute(destination_overview_query)

        destinations = cur.fetchall()

    sensordata = {'id': 'sensor_100', 'bcmpin': '12'}
    return sensordata
