from flask import Flask
from flask_restful import Api, Resource
from cachelib import SimpleCache

from resources.main import Main
from resources.daily_illini import DailyIllini
from resources.purdue_exponent import PurdueExponent
from resources.yale_daily import YaleDaily

app = Flask(__name__)
api = Api(app)
cache = SimpleCache(app)

# Define routes
api.add_resource(Main, '/')

'''News'''
api.add_resource(DailyIllini, '/DailyIllini')
api.add_resource(PurdueExponent, '/PurdueExponent')
api.add_resource(YaleDaily, '/YaleDaily')

if __name__ == '__main__':
    app.run()
