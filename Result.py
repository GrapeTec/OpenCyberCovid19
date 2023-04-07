import matplotlib.pyplot as plt
import csv
from datetime import date, datetime

class DatePoint :
    def __init__(self, date, confirmed, cured = 0, dead = 0):
        self.date = date
        self.confirmed = confirmed
        self.cured = cured
        self.dead = dead

class ResultModel :
    def __init__(self, record, city):
        self.city = city
        self.record = record
        self.hasHistory = False
        self.historyDateList = []
        self.historyCummulativeConfirmedList = []
        self.historyNewConfirmedList = []
        self.historyCummulativeCuredList = []
        self.historyNewCuredList = []
        self.historyCummulativeDeadList = []
        self.historyNewDeadList = []

    def clearHistory(self) :
        self.historyDateList = []
        self.historyCummulativeConfirmedList = []
        self.historyNewConfirmedList = []
        self.historyCummulativeCuredList = []
        self.historyNewCuredList = []
        self.historyCummulativeDeadList = []
        self.historyNewDeadList = []

    def loadHistory(self, city, round) :
        csvFile = city.upper() + "-" + str(round) + ".csv"
        self.clearHistory()
        historyList = []
        filePath = "history/" + csvFile
        with open(filePath, encoding="utf8") as f:
            reader = csv.reader(f)
            next(reader)
            for i, line in enumerate(reader, 1):
                historyDate = datetime.strptime(line[0], "%Y-%m-%d").date()
                confirmed = int(line[1])
                cured = int(line[2])
                dead = int(line[3])
                datePoint = DatePoint(historyDate, confirmed, cured, dead)
                historyList.append(datePoint)
        dateStart = historyList[0].date
        dateEnd = historyList[-1].date

        days = self.record.currentDays
        lastConfirmed = 0
        lastCured = 0
        lastDead = 0
        for day in range(0, days + 1) :
            date = self.record.getDate(day)
            if date >= dateStart and date <= dateEnd :
                self.historyDateList.append(date)
                dist = date - dateStart
                confirmed = historyList[dist.days].confirmed
                cured = historyList[dist.days].cured
                dead = historyList[dist.days].dead
                self.historyCummulativeConfirmedList.append(confirmed)
                self.historyNewConfirmedList.append(confirmed - lastConfirmed)
                self.historyCummulativeCuredList.append(cured)
                self.historyNewCuredList.append(cured - lastCured)
                self.historyCummulativeDeadList.append(dead)
                self.historyNewDeadList.append(dead - lastDead)
                lastConfirmed = confirmed
                lastCured = cured
                lastDead = dead

        self.hasHistory = True
        
    
    def show(self, type = "cumulative", infectedCurve = True, confirmedCurve = True, curedCurve = False, deadCurve = False) :
        record = self.record
        dateList = []
        days = record.currentDays
        for day in range(0, days + 1) :
            date = record.getDate(day)
            dateList.append(date) 
        
        plt.xlim((record.zeroDate, record.currentDate))

        simHead = ""
        if self.hasHistory :
            simHead = "Simulated "

        if infectedCurve :
            if type == "cumulative" :
                plt.plot(dateList, record.cumulativeInfectedList, label = simHead + "Cumulative Infected Cases", linewidth = 2, linestyle=':', color = 'g')
            elif type == "new" :
                plt.plot(dateList, record.newInfectedList, label = simHead + "New Infected Cases", linewidth = 2, linestyle=':', color = 'g')
        
        if confirmedCurve :
            if type == "cumulative" :
                plt.plot(dateList, record.cumulativeConfirmedList, label = simHead + "Cumulative Confirmed Cases", linewidth = 2, color = 'r')
            elif type == "new" :
                plt.plot(dateList, record.newConfirmedList, label = simHead + "New Confirmed Cases", linewidth = 2, color = 'r')

        if curedCurve :
            if type == "cumulative" :
                plt.plot(dateList, record.cumulativeCuredList, label = simHead + "Cumulative Cured Cases", linewidth = 2, color = 'b')
            elif type == "new" :
                plt.plot(dateList, record.newCuredList, label = simHead + "New Cured Cases", linewidth = 2, color = 'b')

        if deadCurve :
            if type == "cumulative" :
                plt.plot(dateList, record.cumulativeDeadList, label = simHead + "Cumulative Dead Cases", linewidth = 2, color = 'k')
            elif type == "new" :
                plt.plot(dateList, record.newDeadList, label = simHead + "New Dead Cases", linewidth = 2, color = 'k')

        if self.hasHistory :
            if type == "cumulative" :
                plt.plot(self.historyDateList, self.historyCummulativeConfirmedList, \
                    label = "History Cumulative Confirmed Cases", linewidth = 4, linestyle=':', color = 'r')
            elif type == "new" :
                plt.plot(self.historyDateList, self.historyNewConfirmedList, \
                    label = "History New Confirmed Cases", linewidth = 4, linestyle=':', color = 'r')

        title = self.city + " [" + str(record.zeroDate) + " ~ " \
            + str(record.currentDate) + "]"
        plt.title(title)
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
    
    def showDynamics(self) :
        record = self.record
        dateList = []
        days = record.currentDays
        for day in range(0, days + 1) :
            date = record.getDate(day)
            dateList.append(date) 
        plt.plot(dateList, self.record.C0List, label = "C0", linewidth = 2, linestyle=':', color = 'r')
        plt.plot(dateList, self.record.R0List, label = "R0", linewidth = 2, linestyle=':', color = 'g')
        
        plt.title(self.city)
        plt.legend()
        plt.grid()
        plt.show()