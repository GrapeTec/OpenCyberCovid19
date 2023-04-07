from Incubation import IncubationModel
from Record import RecordModel
from Quarantine import QuarantineModel, SaturedQuarantineModel
from Delay import DelayModel
from datetime import date

###模型说明
## 2019年12月27日，中国武汉的医生张继先最早将3例不明原因肺炎的病例，上报给了地方公共卫生管理部门。之后，在全世界范围爆发了新冠疫情。
## 新冠疫情的爆发初期，中国主要存在两种模型
## 第一种称之为标准COVID-19模型(Covid19Model)，主要用于仿真疫情防控形势良好，未发生医疗资源挤兑的城市，如上海、北京等
## 第二种称之为饱和COVID-19模型(SaturedCovid19Model)，主要用于仿真疫情防控形势严峻，发生了医疗资源挤兑的城市，如武汉等


################################################################
## 标准COVID-19模型
# 初始化参数
# - R0 : 再生传播系数
# - T1 : 平均潜伏期（泊松分布的期望）
# - maxT1 : 最长潜伏期
# - T2 : 发病后的治疗周期
# - deathRate : 死亡率
# - Y-M-D : 起始日期（年-月-日）
# 成员函数
# - reset(n) : 模型复位，重设为n个初始感染者
# - changeR0(R0) : 修改模型中当前的R0
# - predict() : 预测一天的数据，结果存在record里面
###############################################################
class Covid19Model:
    def __init__(self,
                 R0 = 2.7,
                 T1 = 5.5,
                 maxT1 = 14,
                 T2 = 14,
                 deathRate = 0.06,
                 dt = date(2020, 1, 1)):
        self.C0 = R0 / T1
        self.incubation = IncubationModel(T1, maxT1)
        self.quarantine = QuarantineModel(T2, deathRate)
        self.record = RecordModel(dt)

    def reset(self, n):
        self.incubation.addInfected(n)
        self.record.reset()
        self.quarantine.reset()

    def changeR0(self, R0):
        T1 = self.incubation.T
        self.C0 = R0 / T1

    def predict(self):
        infectious = self.incubation.getInfectious()
        symOnset = self.incubation.getSymOnset()
        newInfected = infectious * self.C0
        newCured, newDead = self.quarantine.addPatients(symOnset)
        self.record.report(newInfected, symOnset, symOnset, newCured, newDead)
        self.incubation.addInfected(newInfected)
        self.incubation.overnight()


###############################################################
## 饱和COVID-19模型
# 初始化参数
# - R0 : 再生传播系数
# - T1 : 平均潜伏期（泊松分布的期望）
# - maxT1 : 最长潜伏期
# - T2 : 发病后的治疗周期
# - deathRate1 : 收治死亡率
# - deathRate2 : 未收治死亡率
# - maxSickbeds : 最大隔离床位数
# - Y-M-D : 起始日期（年-月-日）
# 成员函数
# - reset(n) : 模型复位，重设为n个初始感染者
# - changeR0(R0) : 修改模型中当前的R0
# - setMaxSickbeds(maxSickbeds) : 设置最大隔离床位数
# - predict() : 预测一天的数据，结果存在record里面
###############################################################
class SaturedCovid19Model:
    def __init__(self,
                 R0 = 2.7,
                 T1 = 5.5,
                 maxT1 = 14,
                 T2 = 14,
                 deathRate1 = 0.03,
                 deathRate2 = 0.06,
                 maxSickbeds = 1000,
                 dt = date(2020, 1, 1)):
        self.R0 = R0
        self.C0 = R0 / T1
        self.incubation = IncubationModel(T1, maxT1, "incubation")
        self.quarantine = SaturedQuarantineModel(T2, deathRate1, deathRate2,
                                                 maxSickbeds)
        self.record = RecordModel(dt)
        self.infectDelay = DelayModel()
        self.inputInfected = 0
        self.mixedDetection = False
        self.detectionDays = 0
        self.traceDetection = False
        self.traceRate = 0.0
        self.detectRate = 0.0

    def reset(self, n=0):
        self.record.reset()
        self.quarantine.reset()
        self.addInfected(n)

    def addInfected(self, infected) :
        self.incubation.addInfected(infected)
        self.inputInfected = infected

    def addIncubatoryCarriers(self, incubatoryCarriers) :
        self.incubation.addIncubatoryCarriers(incubatoryCarriers)
        infected = 0
        for carriers in incubatoryCarriers :
            infected += carriers
        self.inputInfected = infected

    def getInputInfected(self):
        infected = self.inputInfected
        self.inputInfected = 0
        return infected

    def changeR0(self, R0):
        self.R0 = R0
        self.C0 = R0 / self.incubation.T

    def setMaxSickbeds(self, maxSickbeds):
        self.quarantine.setMaxSickbeds(maxSickbeds)

    def startMixedDetection(self, days) :
        self.mixedDetection = True
        self.detectionDays = days
    
    def stopMixDetection(self) :
        self.mixedDetection = False
        self.detectionDays = 0

    def startTraceDetection(self, traceRate, detectRate) :
        self.traceDetection = True
        self.traceRate = traceRate
        self.detectRate = detectRate

    def stopTraceDetection(self) :
        self.traceDetection = False
        self.traceRate = 0.0
        self.detectRate = 0.0

    # def detectIncubatoryCarriers(self, rate) :
    #     return self.incubation.reduceInfectious(rate)

    def predict(self):
        symOnset = self.incubation.getSymOnset()
        infectious = self.incubation.getInfectious() + \
                     self.quarantine.getInfectious()

        infectRate = self.C0
        if self.traceDetection :
            infectRate *= (1.0 - self.traceRate)

        # if infectious < 0.5 :
        #     infectious = 0.0
        infected = infectious * infectRate
        infected = self.infectDelay.push(infected)

        newInfected = infected + self.getInputInfected()
        newConfirmed = symOnset
        newExposedCured = self.quarantine.getExposedCured()
        newExposedDead = self.quarantine.getExposedDead()
        newQuarantine, newCured, newDead = self.quarantine.addPatients(symOnset)

        if self.traceDetection :
            removedInfected = self.incubation.reduceInfectious(self.detectRate)
            newConfirmed += removedInfected
            newQuarantine += removedInfected

        self.record.reportDynamics(self.R0, self.C0)
        self.record.reportEpidemics(newInfected, newConfirmed, newQuarantine, newCured,
                           newDead, newExposedCured, newExposedDead)

        self.incubation.overnight()
        self.incubation.addInfected(infected)