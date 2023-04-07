# NOTE: 
# All the simulations are made in Chinese cities, so we comments most of the programs in Chinese.
# If you are not familiar with Chinese, and get interested in our program, please email to: xiaowenlei@buaa.edu.cn
# If we get enough requests, we will try to translate the comments into English.

from Country import CovidCountryModel
from Result import ResultModel
from Migration import MigrationModel
from datetime import date

country = CovidCountryModel("China", "alpha") # 病毒信息存在virus文件夹

# 2020年1月1日，在中国武汉首先发现了新冠疫情。
# 这里，我们于2020年1月1日投入了武汉的零号病人
country.startInCity("Wuhan", date(2019, 12, 13), 1)
## 2020年2月3日，火神山医院投入使用，增加1000个床位
## 2020年2月8日，雷神山医院投入使用，增加1600个床位
## 2020年2月5日，武汉市第一批方舱医院投入使用，增加10000个床位
## 2020年2月9日，武汉市的方舱医院全部建成，并形成最大的隔离能力，达到500000张床位（假设）
country.loadHospitalInCity("Wuhan") # 医院信息存在hospital文件夹中
# 以下，进行连续100天的中国疫情模拟
for k in range(1, 120) :
    dt = country.currentDate
    # 此处模拟：在2020年1月10日至2020年1月27期间，从武汉输出到全国各地的人口
    if dt >= date(2020, 1, 10) and dt <= date(2020, 1, 27) :
        migration = MigrationModel(dt)
        for log in migration.logs :
            country.migrateByLog(log, True) # 启用采样，采样感染率信息存在migration文件夹
    # 2020年1月24日，全国宣布进入到一级响应状态
    if dt == date(2020, 1, 24):
        country.lockdown()
    # 每日进行一轮预测，以仿真全国各个城市的疫情结果
    country.predict()

# 获取指定城市的记录
city = "Shanghai"
record = country.getRecord(city)
result = ResultModel(record, city)
# 加载上海的历史数据。
# 请注意：本次模拟直到最后才加载了历史数据，
#        所以我们不是在做数据拟合，而是在模拟疫情传播的真实机理！！！
result.loadHistory(city, 1)
result.show("cumulative")