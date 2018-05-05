from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import holidays

w1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
w2 = ' (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'

l1 = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
l2 = '(KHTML, like Gecko) Ubuntu Chromium/62.0.3202.89 Chrome/62.0.3202.89 Safari/537.36'

agent = {'User-Agent': l1 + l2}

holiday = holidays.PL(years=datetime.now().year)

busStop = {
    "73": {
        "directionName": "pl. Wolności",
        "stopName": "Radogoszcz Zachód",
        "walkTime": 5
    },
    "99": {
        "directionName": "Retkinia",
        "stopName": "Radogoszcz Zachód",
        "walkTime": 5
    },
    "89": {
        "directionName": "cm. Szczecińska",
        "stopName": "Radogoszcz Zachód",
        "walkTime": 5
    }
}


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
            timetable = {}
        bustimetable.update({f'{lineName}': daytimetable})

        return bustimetable

    def get_bus_table(self, lineName, directionName, stopName):

        lineId = LineNameModel().find_id_by_name(lineName)['lineId']
        routeTable = LineNameModel().find_routeTable_by_id(lineId)
        busStop = routeTable[lineId][directionName][stopName]
        direction = busStop['direction']
        timetableId = busStop['timeTableId']
        stopNumber = busStop['stopNumber']

        url = 'http://www.mpk.lodz.pl/rozklady/tabliczka.jsp'
        table = TimeTableModel().get(url, direction, lineName, timetableId, stopNumber)

        return table


class LineNameModel():

    @classmethod
    def getbusstop(cls, lineName):
        try:
            stop = busStop[lineName]
        except KeyError:
            return None

        return stop

    def find_id_by_name(self, lineName):
        if lineName in lineNameIdDB:
            lineId = lineNameIdDB['{}'.format(lineName)]
            return {"lineId": lineId}
        else:
            return {'Message': None}, 404

    def find_routeTable_by_id(self, lineId):

        dateTime = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        urlRoot = 'http://www.mpk.lodz.pl/rozklady/trasa.jsp'
        urlTail = f'?lineId={lineId}&date={dateTime}'
        url = urlRoot + urlTail

        # print(f'find_routeTable_by_id url ==> {url}')

        resp = requests.get(url, headers=agent)
        soup = BeautifulSoup(resp.content, 'lxml')

        dRoute = soup.find('div', {'id': "dRoute"})

        routeTableDB = {f'{lineId}': {}}
        dStreetStop = {}
        dDirectionTable = {}

        tData = dRoute.find('table').findAll('tr', recursive=False)
        tDirectionTables = tData[1]
        for Table in tDirectionTables.findAll('td', recursive=False):
            tDirection = Table.find('div', {'class': 'headSign'}).contents[0]  # route direction
            Rows = Table.find('table').findAll('tr', recursive=False)
            for Row in Rows[1:]:  # skipping table header
                Cells = Row.findAll('td', recursive=False)

                sStreet = Cells[0].get_text().strip()
                sStop = Cells[2].get_text().strip()
                sStreetStop = (f'{sStreet} {sStop}').lstrip()

                sDirection = Cells[2].find('a').get('href').partition('?')[2].split('&')[0].partition('=')[2]
                sTimeTableId = Cells[2].find('a').get('href').partition('?')[2].split('&')[2].partition('=')[2]
                sNumber = Cells[2].find('a').get('href').partition('?')[2].split('&')[3].partition('=')[2]

                dStreetStop.update({sStreetStop: {'direction': sDirection, 'stopNumber': sNumber, 'timeTableId': sTimeTableId}})
            dDirectionTable.update({tDirection: dStreetStop})
            dStreetStop = {}
        routeTableDB.update({lineId: dDirectionTable})

        return routeTableDB


class DateModel():

    @staticmethod
    def getnowpluswalk(walk):
        time = datetime.now() + timedelta(minutes=walk)
        return time

    @classmethod
    def daytype(cls, date):
        weekday = date.weekday()
        if (date in holiday) or (weekday == 6):
            return 'NIEDZIELA'
        if weekday in range(0, 5):
            return 'ROBOCZY'
        if weekday == 5:
            return 'SOBOTY'

        return None

    def getdeparture(self, lineName, directionName, stopName, myTime):

        table = TimeTableModel().get_bus_table(lineName, directionName, stopName)
        # now = self.getnow()
        day = self.daytype(myTime)

        tableDay = table[lineName][day]
        hours = [th for th in tableDay.keys() if int(th) >= myTime.hour]
        # TODO: handle no key error!
        # TODO: make sure that list is ordered

        for hour in hours:
            for minute in tableDay[hour]:

                # deal with minutes with 'x'
                remark = 'None'
                if len(minute) > 2:
                    minute = minute.strip('x')
                    remark = 'x'

                tblTime = datetime.strptime(f'{hour}:{minute}:00', '%X')
                if tblTime.time() >= myTime.time():
                    return {
                        "lineName": lineName,
                        "time": str(tblTime.time()),
                        "note": remark
                    }
        return None
