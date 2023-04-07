from City import CovidCityModel
from Result import ResultModel
from datetime import date

city = CovidCityModel("Shanghai", 22000000, 100000, 1000, "alpha")
covid19 = city.startCovid19(date(2020, 1, 1), 0)

n = 2.0
for k in range(1, 45) :        
    record = city.covid19.record 
    currentDate = record.currentDate
    if currentDate >= date(2020, 1, 13) and currentDate <= date(2020, 1, 20) :
        covid19.setInputInfected(n)
        n *= 1.5
    #     city.migrateInfectiousIn(0.1, 0.1)
    if currentDate == date(2020, 1, 20) :
        city.lockdown()
    city.predict()

record = city.covid19.record
result = ResultModel(record)
result.loadHistory("SHANGHAI-2020-01-01.csv")
result.show()
