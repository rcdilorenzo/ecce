import os
import logging
from toolz import curry, dissoc, valfilter

from influxdb import InfluxDBClient
from collections import namedtuple as Struct

LoggerClient = Struct('LoggerClient', ['write_points'])

if os.environ.get('USE_INFLUX'):
    client = InfluxDBClient(
        os.environ['INFLUX_HOST'],
        port=443,
        username=os.environ['INFLUX_USERNAME'],
        password=os.environ['INFLUX_PASSWORD'],
        database=os.environ['INFLUX_DB'],
        path=os.environ['INFLUX_PATH'],
        ssl=True)
else:
    log = curry(lambda msg, data: print(f'INFLUX:[{msg}]: {data}'))
    client = LoggerClient(log('write_points'))


def filter_headers(headers):
    return dissoc(headers, 'connection', 'accept', 'cookie', 'accept-encoding')


def record(event_type, data, request=None):
    tags = {}
    if request is not None and request.headers.get('dnt') is not '1':
        tags = filter_headers(dict(request.headers))

    data = valfilter(lambda v: v is not None and v is not '', data)

    client.write_points([{
        'measurement': event_type,
        'fields': data if len(data) != 0 else dict(empty=True),
        'tags': tags
    }])
