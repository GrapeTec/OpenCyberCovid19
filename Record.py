from datetime import date, timedelta

class RecordModel:
    def __init__(self, year = 2000, month = 1, day = 1) :
        self.newInfectedList = [0]
        self.cumulativeInfectedList = [0]
        self.newConfirmedList = [0]
        self.cumulativeConfirmedList = [0]
        self.newQuarantinedList = [0]
        self.cumulativeQuarantinedList = [0]
        self.newRecoveredList = [0]
        self.cumulativeRecoveredList = [0]
        self.newDeadList = [0]
        self.cumulativeDeadList = [0]
        self.infectiousList = [0]
        self.currentDays = 0
        self.zeroDate =  date(year, month, day)
        self.currentDate = date(year, month, day)
        self.currentInfected = 0
        self.currentConfirmed = 0
        self.currentQuarantined = 0
        self.currentInfectious = 0
        self.currentIncubatoryCarriers = 0
        self.currentRecovered = 0
        self.currentDead = 0
        self.currentQuarantinedRecovered = 0
        self.currentQuarantinedDead = 0
        self.currentExposedRecovered = 0
        self.currentExposedDead = 0
        self.R0List = [0]
        self.C0List = [0]
        
    def __init__(self, dt) :
        self.newInfectedList = [0]
        self.cumulativeInfectedList = [0]
        self.newConfirmedList = [0]
        self.cumulativeConfirmedList = [0]
        self.newQuarantinedList = [0]
        self.cumulativeQuarantinedList = [0]
        self.newRecoveredList = [0]
        self.cumulativeRecoveredList = [0]
        self.newDeadList = [0]
        self.cumulativeDeadList = [0]
        self.infectiousList = [0]
        self.currentDays = 0
        self.zeroDate =  date(dt.year, dt.month, dt.day)
        self.currentDate = date(dt.year, dt.month, dt.day)
        self.currentInfected = 0
        self.currentConfirmed = 0
        self.currentQuarantined = 0
        self.currentInfectious = 0
        self.currentIncubatoryCarriers = 0
        self.currentRecovered = 0
        self.currentDead = 0
        self.currentQuarantinedRecovered = 0
        self.currentQuarantinedDead = 0
        self.currentExposedRecovered = 0
        self.currentExposedDead = 0
        self.R0List = [0]
        self.C0List = [0]
    
    def reportEpidemics(self, newInfected, newConfirmed, newQuarantined, newRecovered = 0, newDead = 0, newExposedRecovered = 0, newExposedDead = 0) :
        self.currentDays += 1 # 当前天数
        self.currentDate += timedelta(days = 1) # 当前日期
        self.currentInfected += newInfected # 感染过的人数 = 每日累加（新增感染人数：新增感染的一定处于潜伏期）
        self.currentConfirmed += newConfirmed # 确诊过的人数 = 每日累加（新增确诊人数）
        # 当前被隔离的人数 = 每日累加（新增隔离人数 - 新增被隔离治愈人数 - 新增被隔离死亡人数）
        # 此处假设：被隔离的一定是确诊后的！！！
        self.currentQuarantined += newQuarantined - (newRecovered - newExposedRecovered) - (newDead - newExposedDead)
        # 有传染性的人数（社会面感染）= 每日累加（新增感染人数 - 新增社会面自愈人数 - 新增社会面死亡人数 - 新增隔离人数）
        self.currentInfectious += newInfected - newExposedRecovered - newExposedDead - newQuarantined
        self.currentIncubatoryCarriers += newInfected - newConfirmed
        self.currentRecovered += newRecovered # 每日累加（新增治愈人数）
        self.currentDead += newDead # 每日累加（新增死亡人数）
        self.currentQuarantinedRecovered += (newRecovered - newExposedRecovered) # 每日累加（新增被隔离治愈人数）
        self.currentQuarantinedDead += (newDead - newExposedDead) # 每日累加（新增被隔离死亡人数）
        self.currentExposedRecovered += newExposedRecovered # 每日累加（新增社会面自愈人数）
        self.currentExposedDead += newExposedDead # 每日累加（新增社会面死亡人数）

        self.newInfectedList.append(newInfected)
        self.cumulativeInfectedList.append(self.currentInfected)

        self.newConfirmedList.append(newConfirmed)
        self.cumulativeConfirmedList.append(self.currentConfirmed)

        self.newQuarantinedList.append(newQuarantined)
        self.cumulativeQuarantinedList.append(self.currentQuarantined)

        self.newRecoveredList.append(newRecovered)
        self.cumulativeRecoveredList.append(self.currentRecovered)

        self.newDeadList.append(newDead)
        self.cumulativeDeadList.append(self.currentDead)

        self.infectiousList.append(self.currentInfectious)

    def reset(self) :
        self.newInfectedList = [0]
        self.cumulativeInfectedList = [0]
        self.newConfirmedList = [0]
        self.cumulativeConfirmedList = [0]
        self.newQuarantinedList = [0]
        self.cumulativeQuarantinedList = [0]
        self.newRecoveredList = [0]
        self.cumulativeRecoveredList = [0]
        self.newDeadList = [0]
        self.cumulativeDeadList = [0]
        self.infectiousList = [0]
        self.currentDate = self.zeroDate
        self.currentDays = 0
        self.currentInfected = 0
        self.currentConfirmed = 0
        self.currentQuarantined = 0
        self.currentRecovered = 0
        self.currentDead = 0
        self.currentQuarantinedRecovered = 0
        self.currentQuarantinedDead = 0
        self.currentExposedRecovered = 0
        self.currentExposedDead = 0
    
    def getDate(self, day) :
        dayDate = self.zeroDate + timedelta(day)
        return dayDate

    def reportDynamics(self, R0, C0 = 0.0) :
        self.R0List.append(R0)
        self.C0List.append(C0)