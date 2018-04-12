from flask import Flask
from flask_restful import Api
from resources.timetable import TimeTable, LineNameId


app = Flask(__name__)
api = Api(app)

api.add_resource(TimeTable, '/timetable')
api.add_resource(LineNameId, '/lineid/<string:linename>')

if __name__ == '__main__':
    app.run(port=5002, debug=True)
