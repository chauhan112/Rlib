import datetime
import json
import requests
class BusSchedule:
    b = "100005"
    a = "100600"
    
    def filterRelevantInfos(dic):
        results = []
        for choice in dic['resultList']:
            p = []
            for ele in choice["elementList"]:
                temp = {}
                temp['time'] = ele['start']['scheduledDepartureInUnixEpochMillis']
                temp['time takes'] = ele['durationInS']
                temp['from'] = ele['start']['location']['stopPointName'] + " " + \
                    ele['start']['location']['stopPointIndicator']
                temp['to'] = ele['end']['location']['stopPointName'] + " " + \
                    ele['end']['location']['stopPointIndicator']
                temp['busNr'] = ele['lineName']
                temp['no. of stations'] = ele['haltCount']
                p.append(temp)
            results.append(p)
        return results
    
    def resultDisplayer(resultsArr):
        msg = ''
        for j, choices in enumerate(resultsArr):
            msg += f"choice {j+1}:\n"
            for i, t in enumerate(choices):
                msg += f"""    {i+1}. time: {str(datetime.datetime.fromtimestamp(t['time']/1000))}
               {t['from']} ==> {t['to']}
               busNr: {t['busNr']}
               time takes: {t['time takes'] / 60} min
               no.Of stations: {t['no. of stations']}\n"""
            msg += "\n"
        return msg
    
    def _findRoutes(start, end, time):
        l = f'http://ivu.aseag.de/interfaces/ura/journey?departureTime={time}'\
            f'&startStopId={start}&maxNumResults=10&endStopId={end}'
        return BusSchedule.fetchApiResults(l)
    
    def findRoutes(start, end):
        pass
    
    def ab():
        return BusSchedule._ab(BusSchedule.a,BusSchedule.b)
    
    def ba():
        return BusSchedule._ab(BusSchedule.b, BusSchedule.a)
    
    def _ab(a, b):
        time = BusSchedule.nowTimeStamp()
        k = BusSchedule._findRoutes(a, b, time)
        k = BusSchedule.filterRelevantInfos(k)
        return BusSchedule.resultDisplayer(k)
    
    def fetchApiResults(link):
        r = requests.get(link)
        jsonData = json.loads(r.text)
        return jsonData
    
    def nowTimeStamp():
        date, time = BusSchedule.today()
        date += time[:2]
        return str(int(datetime.datetime.timestamp(datetime.datetime(*date)) *1000))
    
    def today():
        n = datetime.datetime.now()
        return (n.year, n.month, n.day), (n.hour, n.minute, n.second)