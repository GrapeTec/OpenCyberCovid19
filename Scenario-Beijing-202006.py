from City import CovidCityModel
from Result import ResultModel
from Virus import Covid19DataBase
from Trace import TraceModel
from datetime import date

name = "Beijing"
virusDB = Covid19DataBase("beta")
virusInfo = virusDB.getVirusInfo(name)

city = CovidCityModel(name, virusInfo, 22000000, 100000, 1000)
covid19 = city.startCovid19(date(2020, 5, 30), 1) # 1. 什么时候开始？
# print(city.virusInfo.R0, city.virusInfo.ldR0)

trace = TraceModel()
traceRate, detectRate = trace.getRates(name, "COVID-19", "beta")
# print(traceRate, detectRate)

record = city.covid19.record
for k in range(1, 100) :
    currentDate = record.currentDate
    if currentDate == date(2020, 6, 13) : # 什么时候发现，并启动什么措施？参数是什么？
        city.lockdown()
        city.startTraceDetection(traceRate, detectRate)
    city.predict()

result = ResultModel(record, name)
result.loadHistory("Beijing", 2)
result.show()