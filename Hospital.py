import csv
from datetime import datetime

class HospitalModel :
    def __init__(self, city) :
        self.dateList = []
        self.sickbedsList = []
        self.eventList = []
        self.days = 0
        self.loadData(city + ".csv")

    def loadData(self, csvFile) :
        filePath = "hospital/" + csvFile
        with open(filePath, encoding="utf8") as f:
            reader = csv.reader(f)
            next(reader)
            for i, line in enumerate(reader, 1):
                date = datetime.strptime(line[0], "%Y-%m-%d").date()
                sickbeds = int(line[1])
                event = line[2]
                self.dateList.append(date)
                self.sickbedsList.append(sickbeds)
                self.eventList.append(event)
                self.days += 1

    def getSickbeds(self, date) :
        dist = date - self.dateList[0]
        days = dist.days
        if days < 0 :
            return self.sickbedsList[0]
        elif days >= self.days :
            return self.sickbedsList[-1]
        else :
            return self.sickbedsList[days]