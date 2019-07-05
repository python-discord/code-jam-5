import requests
import json
import random
req = requests.get('https://weather-1283198235129847.s3.amazonaws.com/weatherExtremesJSON.json')


def parseData(state):
    jdata = json.loads(open('weather.json').read())
    records = []
    # grab all useful records
    state = state.lower()
    for record in jdata['records']:
        if state != record['state'].lower():
            continue
        stateData = record['state']
        # rename record element to type of record
        type = record['element']
        value = str(record['value']) + ' ' + record['units']
        date = record['date']
        location = record['location']
        # we should ultimately only return one record but here is everything for now
        message = "On {}  an {} of {} was recorded in {}, {} ".format(
            date, type, value, location, stateData
        )
        records.append(message)

    return(records)


def return_record(state):
    """
    returns a random state record.
    :param state:
    :return:
    """

    return random.choice(parseData(state))


print(return_record(state="California"))
