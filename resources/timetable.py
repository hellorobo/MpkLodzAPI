from flask_restful import Resource
from models.tables import TimeTableModel, LineNameModel



class TimeTable(Resource):
    def get(self, lineName):
        url = 'http://www.mpk.lodz.pl/rozklady/tabliczka.jsp'
        direction = '2'
        # lineId = '46'
        timetableId = '3704'
        stopNumber = '458'

        table = TimeTableModel().get(url, direction, lineName, timetableId, stopNumber)
        return table


class LineNameId(Resource):

    def get(self, linename):
        linenameid = LineNameModel().find_id_by_name(linename)
        return linenameid
