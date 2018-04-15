from datetime import datetime
from bs4 import BeautifulSoup
import requests

w1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
w2 = ' (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'

l1 = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
l2 = '(KHTML, like Gecko) Ubuntu Chromium/62.0.3202.89 Chrome/62.0.3202.89 Safari/537.36'

agent = {'User-Agent': l1 + l2}


def getLineNameIds(url):
    print(f'getting line IDs from {url}')
    resp = requests.get(url, headers=agent)
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

    def __init__(self):
        pass

    def get(self, url, direction, lineName, timetableId, stopNumber):
        lineId = lineNameIdDB[f'{lineName}']
        dt = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        curl = f'{url}?direction={direction}&lineId={lineId}&timetableId={timetableId}&stopNumber={stopNumber}&date={dt}'

        resp = requests.get(curl, headers=agent)
        soup = BeautifulSoup(resp.text, 'html.parser')

        dTab = soup.find("div", {"id": "dTab"})
        dDayTypeNames = {dtname.get_text(): dtname.get('id').replace('_name', '') for dtname in dTab.find('div', {'id': 'dDayTypeNames'}).find_all('a')}
        dDayTypes = dTab.find("div", {"id": "dDayTypes"})

        dDayTables = {}
        for dName, tName in dDayTypeNames.items():
            dDayTables[dName] = dDayTypes.find("div", {"id": "table_{}".format(tName)}).find('table')
        bustimetable = {f'{lineName}': ''}
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
        bustimetable.update({f'{lineName}': daytimetable})

        return bustimetable


class LineNameModel():

    def find_id_by_name(self, lineName):
        if lineName in lineNameIdDB:
            lineId = lineNameIdDB['{}'.format(lineName)]
            return {"lineName": lineName, "lineId": lineId}
        else:
            return {'Message': None}, 404
