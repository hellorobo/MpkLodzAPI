from flask_restful import Resource
from models.tables import TimeTableModel, LineNameModel, DateModel


class TimeTable(Resource):

    def get(self, lineName, directionName='', stopName=''):
        busStop = LineNameModel.getbusstop(lineName)
        directionName = busStop['directionName']
        stopName = busStop['stopName']
        bustimetable = TimeTableModel().get_bus_table(lineName, directionName, stopName)

        return bustimetable


class LineNameId(Resource):

    def get(self, linename):
        linenameid = LineNameModel().find_id_by_name(linename)

        return linenameid


class Departure(Resource):

    def get(self, lineName):
        busStop = LineNameModel.getbusstop(lineName)
        if busStop:
            directionName = busStop['directionName']
            stopName = busStop['stopName']
            nextDeparture = DateModel().getdeparture(lineName, directionName, stopName)
            httpResponse = 200
        else:
            nextDeparture = {"message": "Error"}
            httpResponse = 404

        return nextDeparture, httpResponse
