from flask_restful import Resource
from models.tables import TimeTableModel, LineNameModel, DateModel


class TimeTable(Resource):
    def get(self, lineName, directionName='', stopName=''):

        directionName = 'pl. Wolności'
        stopName = 'Radogoszcz Zachód'

        lineId = LineNameModel().find_id_by_name(lineName)['lineId']
        print(f'lineId is -> {lineId}')
        routeTable = LineNameModel().find_routeTable_by_id(lineId)
        direction = routeTable[lineId][directionName][stopName]['direction']
        timetableId = routeTable[lineId][directionName][stopName]['timeTableId']
        stopNumber = routeTable[lineId][directionName][stopName]['stopNumber']

        url = 'http://www.mpk.lodz.pl/rozklady/tabliczka.jsp'
        table = TimeTableModel().get(url, direction, lineName, timetableId, stopNumber)

        return table


class LineNameId(Resource):

    def get(self, linename):
        linenameid = LineNameModel().find_id_by_name(linename)
        return linenameid


class Departure(Resource):
    def get(self, lineName):
        direction = 'pl. Wolności'
        stopName = 'Radogoszcz Zachód'
        dt = DateModel().getnow()
        table = TimeTable().get(lineName, direction, stopName)
        day = DateModel().datetype(dt)
        print(day)
        tableDay = table[lineName][day]

        return tableDay
