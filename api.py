from flask import Flask
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
from IPython import embed
import urllib2
import re

app = Flask(__name__)
api = Api(app)

data = {}

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Dining(Resource):
  def get(self):
    return {"yo": "ayy"}

class Weather(Resource):
  global data
  webpage = urllib2.urlopen('https://www.atmos.illinois.edu/weather/')
  soup = BeautifulSoup(webpage, "html.parser")
  location = str(soup.find_all('font')[3])
  match = re.compile(r'<b>(.*?)<br>(.*?)<\/br>')
  data['weather_station_location'] = match.search(location).group(1) + " " + match.search(location).group(2)

  time = str(soup.find_all('font')[5]) #convert to unix
  match = re.compile(r'(^([0-1]\d:[0-5]\d)(AM|PM)?$)')
  data['last_recorded_time'] = match.search(time)
  weather_data = str(soup.find_all('font')[6])

  match = re.compile(r'.*?>\\n(.*?)\\n')
  #data['weather_condition'] = match.search(weather_data)
  match = re.compile(r'Temperature:.*?([0-9]+)')
  data['temperature'] = match.search(weather_data).group(1)
  match = re.compile(r'Dew Point:.*?([0-9]+)')
  data['dew_point'] = match.search(weather_data).group(1)
  match = re.compile(r'Rel. Humidity:.*?([0-9]+%)')
  data['relative_humidity'] = match.search(weather_data).group(1)
  match = re.compile(r'Winds:(.*?)\\n')
  #data['winds'] = match.search(weather_data)
  match = re.compile(r'Visibility:.*?([0-9]+.*?)\\n')
  #data['visibility'] = match.search(weather_data)
  match = re.compile(r'Pressure:.*?(([0-9]+(\.[0-9][0-9]?)?).*?)\\n(.*?)\\n')
  #data['pressure'] = match.search(weather_data)
  embed()

  data['latestRadarImage'] = "https://www.atmos.illinois.edu/weather/tree/prods/current/nicerad/nicerad_N.gif"
  data['stormTotalPrecipImage'] = "https://www.atmos.illinois.edu/weather/tree/prods/current/niceradilxpretx/niceradilxpretx_N.gif"
  data['surfaceTempImage'] = "https://www.atmos.illinois.edu/weather/tree/prods/current/sfctmp/sfctmp_N.gif"
  data['surfaceDewPointTempImage'] = "https://www.atmos.illinois.edu/weather/tree/prods/current/sfctdp/sfctdp_N.gif"
  data['seaLevelPressure'] = "https://www.atmos.illinois.edu/weather/tree/prods/current/sfcslp/sfcslp_N.gif"
  data['mdwSufaceObservations'] = "https://www.atmos.illinois.edu/weather/tree/prods/current/sfcslp/sfcslp_N.gif"
  data['irImage'] = "https://www.atmos.illinois.edu/weather/tree/prods/current/satconusenhir/satconusenhir_N.gif"
  data['irImage2'] = "https://www.atmos.illinois.edu/weather/tree/prods/current/satnoamir/satnoamir_N.gif"
  def get(self):
    return data


api.add_resource(HelloWorld, '/')
api.add_resource(Dining, '/dining')
api.add_resource(Weather, '/weather')

if __name__ == '__main__':
    app.run(debug=True)
