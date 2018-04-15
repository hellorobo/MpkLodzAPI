from flask_restful import Resource
from models.tables import TimeTableModel, LineNameModel



class TimeTable(Resource):
    def get(self):
        url = 'http://www.mpk.lodz.pl/rozklady/tabliczka.jsp'
        direction = '2'
        lineId = '46'
        timetableId = '3704'
        stopNumber = '458'

        table = TimeTableModel().get(url, direction, lineId, timetableId, stopNumber)
        return table.json()


class LineNameId(Resource):

    def get(self, linename):
        linenameid = LineNameModel().find_id_by_name(linename)
        return linenameid


class LineName():
    def __init__(self):
        self.lineNameIddb = {}
