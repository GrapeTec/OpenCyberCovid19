from SEIR import SeirModel, QSeirModel
from Result import ResultModel
from datetime import date

# ##########################################################
# # def TestSeir() :
# seir = SeirModel(96400000, date(2020, 1, 1))
# # r1 = 21 # 每个感染者每天接触的平均人数
# # r2 = 21 # 每个潜伏着每天接触的平均人数
# # beta1 = 0.048 # 易感者被感染者感染的概率
# # beta2 = 0.048 # 易感者被潜伏者感染的概率
# # alpha = 0.13 # 潜伏者转化为感染者的概率（潜伏期的倒数）
# # gamma = 0.066 # 康复概率
# seir.setParameters(r1 = 10, r2 = 10, beta1 = 0.048, beta2 = 0.048, alpha = 0.13, gamma = 0.066)

# for i in range(0, 100) :
#     if i == 10 :
#         seir.setParameters(r1 = 3, r2 = 3, beta1 = 0.048, beta2 = 0.048, alpha = 0.13, gamma = 0.066)
#     seir.predict()

# result = ResultModel(seir.record, "Shanghai")
# result.loadHistory("Shanghai", 1)
# result.show()

##########################################################
# def TestQSeir() :
seir = QSeirModel(96400000, date(2020, 1, 16))
seir.setParameters(r = 17, beta = 0.049, alpha = 0.18, gamma = 0.066)
# r1 : 每个感染者每天接触的平均人数
# beta1 : 易感者被感染者感染的概率
# beta2 : 易感者被潜伏者感染的概率;
# alpha : 潜伏者转化为感染者的概率（潜伏期的倒数）
# gamma : 康复概率

for i in range(0, 120) :
    if i == 20 :
        seir.setParameters(r = 0.2, beta = 0.049, alpha = 0.18, gamma = 0.066)
    seir.predict()

result = ResultModel(seir.record, "Shanghai")
result.loadHistory("Shanghai", 1)
result.show()