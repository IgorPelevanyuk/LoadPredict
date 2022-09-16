from ResourceUsage import ResourceUsage
#from influxdb_client import InfluxDBClient, BucketRetentionRules, Point, WritePrecision, WriteOptions
from influxdb import InfluxDBClient
from influxdb_client import Point, WritePrecision

import datetime
import random

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Accounting(object, metaclass=Singleton):

    def __init__(self):
        self.data = []
        self.inner_data = []
        self.time = 0
        self.set_time(0)
        self.write_data = self.write_data_influx18
        self.is_database_created = False

        self.url = "http://localhost:8086"
        self.host = "localhost"
        self.port = 8086
        self.user = "user"
        self.password = "password"

    def create_database(self):

        self.database = "test_" + str(random.randint(0, 999999))

        client = InfluxDBClient(self.host, self.port, self.user, self.password, self.database)
        client.create_database(self.database)

        print(self.database)

        self.is_database_created = True

    def set_time(self, time):
        #self.time = datetime.datetime.now() - datetime.timedelta(hours=4) + datetime.timedelta(seconds = time)
        self.time = datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds = time)

    def add_data(self, data_type, element, value):
        self.data.append([data_type, element, value, self.time])

    def write_data(self):
        pass

    def list_databases(self):
        client = InfluxDBClient(self.host, self.port, self.user, self.password)
        response = client.get_list_database()
        result = [x['name'] for x in response]
        return result

    def drop_databases(self, databases):
        client = InfluxDBClient(self.host, self.port, self.user, self.password)
        for db in databases:
            client.drop_database(db)

    def write_data_influx18(self):
        if not self.is_database_created:
            self.create_database()
        client = InfluxDBClient(self.host, self.port, self.user, self.password, self.database)
        for elem in self.data:
            record = {
                "measurement": elem[0],
                "tags": {
                    "element": elem[1],
                },
                "time": elem[3],
                "fields": {"value": 1.0*elem[2]},
            }
            self.inner_data.append(record)
        client.write_points(self.inner_data)
        self.inner_data = []
        self.data = []
