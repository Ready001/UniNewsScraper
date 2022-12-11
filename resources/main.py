from flask_restful import Resource

class Main(Resource):
    def get(self):
        return {"News site": "url", 
        "Daily Illini": "/DailyIllini", 
        "Purdue Exponent": "/PurdueExponent",
        "Yale Daily News": "/YaleDaily"
        }
