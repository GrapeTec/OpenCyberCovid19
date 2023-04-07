from SARS import SarsModel
from Result import ResultModel
from datetime import date

sars = SarsModel()
sars.reset(1)
for k in range(1, 180) :
    if sars.record.currentDate == date(2003, 3, 6) :
        sars.changeR0(1.6) # 2003-3-6 发现第1例非典病人，北京启动封城
    elif sars.record.currentDate == date(2003, 5, 1) :
        sars.changeR0(0.5) # 2003-5-1 小汤山医院开始接受病人
    sars.predict()

result = ResultModel(sars.record, "Beijing")
result.show("cumulative")
