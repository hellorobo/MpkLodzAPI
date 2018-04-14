from flask_restful import Resource
from models.tables import TimeTableModel, LineNameModel
import requests
from bs4 import BeautifulSoup


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
    def __init__(self):
        pass

    def get(self, linename):
        linenameid = self.lines.find_id_by_name(linename)
        return linenameid


class LineName():
    def __init__(self):
        self.lineNameIddb = {}

    def getLineNameIds(self):
        url = 'http://www.mpk.lodz.pl/rozklady/linie.jsp'
        print(f'getting line IDs from {url}')
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        dWrkspc = soup.find('div', {'id': "dWrkspc"})
        dLineTypes = dWrkspc.find_all('div', class_="dLines")
        for lineType in dLineTypes:
            tData = lineType.find('table').find('td')
            for dataRow in tData.find_all('a'):
                lineName = dataRow.get_text()
                lineId = dataRow.get('href').partition('?')[2].partition('&')[0].partition('=')[2]
                self.lineNameIddb.update({lineName: lineId})
