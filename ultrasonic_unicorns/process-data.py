import requests
import json
req = requests.get('https://weather-1283198235129847.s3.amazonaws.com/weatherExtremesJSON.json')

with open("weather.json", "wb") as weather:
    weather.write(req.content)
jdata = json.loads(open('weather.json').read())

# grab all useful records
for record in jdata['records']:
    state = record['state']
    # rename record element to type of record
    type = record['element']
    value = str(record['value']) + record['units']
    date = record['date']
    location = record['location']
    # we should ultimately only return on record but here is everything for now
    message = "On {}  an {} of {} was recorded in {}, {} ".format(date,  type, value, location, state)
    print(message)

# returns a random state record.
def return_record(state):
    pass
