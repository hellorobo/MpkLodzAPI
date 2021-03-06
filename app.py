from flask import Flask
from flask_restful import Api
from resources.timetable import TimeTable, LineNameId, Departure


app = Flask(__name__)
api = Api(app)

api.add_resource(TimeTable, '/timetable/<string:lineName>')
api.add_resource(LineNameId, '/lineid/<string:linename>')
api.add_resource(Departure, '/departure/<string:lineName>')

if __name__ == '__main__':
    app.run(port=5002)
