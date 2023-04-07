from COVID19 import SaturedCovid19Model
from Result import ResultModel

covid19 = SaturedCovid19Model()
covid19.reset(1)
covid19.setMaxSickbeds(3000)
for k in range(1, 60) :
    if (k == 40) :
        covid19.changeR0(0.6)
    covid19.predict()

result = ResultModel(covid19.record)
result.show()