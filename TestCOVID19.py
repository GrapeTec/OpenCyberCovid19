from COVID19 import Covid19Model
from Result import ResultModel

R0 = 2.7
T = 5.5
maxT = 14

covid19 = Covid19Model(R0, T, maxT)
covid19.reset(1)
for k in range(1, 90) :
    if (k == 20) :
        R0 = 0.4
    covid19.changeR0(R0)
    covid19.predict()

result = ResultModel(covid19.record)
result.show()