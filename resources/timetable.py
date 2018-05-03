from flask_restful import Resource
from models.tables import TimeTableModel, LineNameModel, DateModel


class TimeTable(Resource):

    def get(self, lineName, directionName='', stopName=''):
        directionName = 'pl. Wolności'
        stopName = 'Radogoszcz Zachód'
        bustimetable = TimeTableModel().get_bus_table(lineName, directionName, stopName)
        return bustimetable


class LineNameId(Resource):

    def get(self, linename):
        linenameid = LineNameModel().find_id_by_name(linename)
        return linenameid


class Departure(Resource):

    def get(self, lineName):
        directionName = 'pl. Wolności'
        stopName = 'Radogoszcz Zachód'
        dt = DateModel().getnow()
        table = TimeTableModel().get_bus_table(lineName, directionName, stopName)
        day = DateModel().daytype(dt)
        print(day)
        tableDay = table[lineName][day]

        return tableDay
