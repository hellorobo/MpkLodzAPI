from datetime import datetime
from bs4 import BeautifulSoup
import requests

def getLineNameIds(url):
    print('getting line IDs from {}'.format(url))
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    dWrkspc = soup.find('div', {'id': "dWrkspc"})
    dLineTypes = dWrkspc.find_all('div', class_="dLines")
    lineNameId = {}
    for lineType in dLineTypes:
        tData = lineType.find('table').find('td')
        for dataRow in tData.find_all('a'):
            lineName = dataRow.get_text()
            lineId = dataRow.get('href').partition('?')[2].partition('&')[0].partition('=')[2]
            lineNameId.update({lineName: lineId})

    return lineNameId

lineNameIdDB = getLineNameIds('http://www.mpk.lodz.pl/rozklady/linie.jsp')

class TimeTableModel():
    pass
'''
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
'''

class LineNameModel():

    def find_id_by_name(self, lineName):
        if lineName in lineNameIdDB:
            lineId = lineNameIdDB['{}'.format(lineName)]
            return {"lineName": lineName, "lineId": lineId}
        else:
            return {'Message': None}, 404
