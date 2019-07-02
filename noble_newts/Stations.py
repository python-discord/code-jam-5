import requests


class Stations:
    def __init__(self):
        # initializes class by getting the User's public IP and API key for NOAA API
        API_KEY = 'eKhMUGaQDOVZyRMwLvTfMdLimLKYxlhZ'
        self.defaultHeader = {'token': API_KEY}
        # gets the latitude and longitude coordinates of the the user based on their IP address
        self.ip = requests.get('https://api.ipify.org').text
        self.geoData = requests.get(f'https://www.iplocate.io/api/lookup/{self.ip}').json()
        self.stations = []

    def getLocationBox(self, resizeFactor):
        # Returns a "box" of coordinates in the form "lat_lo,lng_lo,lat_hi,lng_hi"
        return f"{self.geoData['latitude'] - resizeFactor}," \
               f"{self.geoData['longitude'] - resizeFactor}," \
               f"{self.geoData['latitude'] + resizeFactor}," \
               f"{self.geoData['longitude'] + resizeFactor}"

    def getStations(self):
        # returns the ten weather stations nearest to the user
        size = 0.1
        while len(self.stations) <= 20:
            locationBox = self.getLocationBox(size)
            # checks the NOAA API for weather stations within locationBox.
            # if less than 10 are found, it expands.
            stationData = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/stations/',
                                       headers=self.defaultHeader,
                                       params={'limit': 1000, 'extent': locationBox}
                                       ).json()['results']
            for station in stationData:
                self.stations.append(station)
            size += 0.1
        print(len(self.stations))
        return self.stations


Bob = Stations()


print(Bob.getStations())
