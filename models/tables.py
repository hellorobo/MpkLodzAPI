from datetime import datetime
from bs4 import BeautifulSoup
import requests


class TimeTableModel():

    a1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    a2 = ' (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    agent = {'User-Agent': a1 + a2}

    def __init__(self):
        pass

    def get(self, url, direction, lineId, timetableId, stopNumber):
        dt = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        self.curl = f'{url}?direction={direction}&lineId={lineId}&timetableId={timetableId}&stopNumber={stopNumber}&date={dt}'

        resp = requests.get(self.curl, headers=self.agent)
        soup = BeautifulSoup(resp.text, 'html.parser')

        dTab = soup.find("div", {"id": "dTab"})
        dDayTypeNames = {dtname.get_text(): dtname.get('id').replace('_name', '') for dtname in dTab.find('div', {'id': 'dDayTypeNames'}).find_all('a')}
        dDayTypes = dTab.find("div", {"id": "dDayTypes"})

        dDayTables = {}
        for dName, tName in dDayTypeNames.items():
            dDayTables[dName] = dDayTypes.find("div", {"id": "table_{}".format(tName)}).find('table')
        bustimetable = {f'{lineId}': ''}
        daytimetable = {}
        timetable = {}

        for dName, tName in dDayTables.items():
            for row in tName.find_all('tr'):
                hour = row.find('th').get_text()
                minute = []
                for cell in row.find_all('a'):
                    minute.append(cell.get_text())
                timetable.update({f'{hour}': minute})
            daytimetable.update({dName: timetable})
        bustimetable.update({f'{lineId}': daytimetable})

        return self


class LineNameModel():
    def __init__():
        pass

    def find_id_by_name(self, lineName):
        if lineName in lineNameIddb:
            lineId = lineNameIddb[f'{lineName}']
            return {"lineName": lineName, "lineId": lineId}
        else:
            return {'Message': None}
