from Record import RecordModel

class SeirModel :
    def __init__(self, N, dt) :
        self.r1 = 21 # 每个感染者每天接触的平均人数
        self.r2 = 21 # 每个潜伏着每天接触的平均人数
        self.beta1 = 0.048 # 易感者被感染者感染的概率
        self.beta2 = 0.048 # 易感者被潜伏者感染的概率
        self.alpha = 0.13 # 潜伏者转化为感染者的概率（潜伏期的倒数）
        self.gamma = 0.066 # 康复概率
        self.N = N # 总人数
        self.E = [0] # 潜伏者人数
        self.I = [1] # 感染者人数
        self.S = [N - self.I[0]] # 易感者人数
        self.R = [0] # 康复者人数
        self.record = RecordModel(dt)
    
    def setParameters(self, r1, r2, beta1, beta2, alpha, gamma) :
        self.r1 = r1
        self.r2 = r2
        self.beta1 = beta1
        self.beta2 = beta2
        self.alpha = alpha
        self.gamma = gamma

    def predict(self) :
        Si = self.S[-1]
        Ii = self.I[-1]
        Ei = self.E[-1]
        Ri = self.R[-1]
        self.S.append(Si - self.r1 * self.beta1 * Si * Ii / self.N - self.r2 * self.beta2 * Si * Ei / self.N)
        self.E.append(Ei + self.r1 * self.beta1 * Si * Ii / self.N - self.alpha * Ei + self.r2 * self.beta2 * Si * Ei / self.N)
        self.I.append(Ii + self.alpha * Ei - self.gamma * Ii)
        self.R.append(Ri + self.gamma * Ii)
        newInfected = (self.r1 * self.beta1 * Ii + self.r2 * self.beta2 * Ei) * Si / self.N
        newConfirmed = self.alpha * Ei
        newQuarantined = 0
        newRecovered = self.gamma * Ii
        self.record.reportEpidemics(newInfected, newConfirmed, newQuarantined, newRecovered)

class QSeirModel :
    def __init__(self, N, dt) :
        self.r = 21 # 每个潜伏着每天接触的平均人数
        self.beta = 0.048 # 易感者被潜伏者感染的概率
        self.alpha = 0.13 # 潜伏者转化为感染者的概率（潜伏期的倒数）
        self.gamma = 0.066 # 康复概率
        self.N = N # 总人数
        self.E = [0] # 潜伏者人数
        self.I = [1] # 感染者人数
        self.S = [N - self.I[0]] # 易感者人数
        self.R = [0] # 康复者人数
        self.record = RecordModel(dt)
    
    def setParameters(self, r, beta, alpha, gamma) :
        self.r = r
        self.beta = beta
        self.alpha = alpha
        self.gamma = gamma

    def predict(self) :
        Si = self.S[-1]
        Ii = self.I[-1]
        Ei = self.E[-1]
        Ri = self.R[-1]
        self.S.append(Si - self.r * self.beta * Si * Ei / self.N)
        self.E.append(Ei + self.r * self.beta * Si * Ii / self.N - self.alpha * Ei)
        self.I.append(Ii + self.alpha * Ei - self.gamma * Ii)
        self.R.append(Ri + self.gamma * Ii)
        
        newInfected = self.r * self.beta * Si * Ei / self.N
        newConfirmed = self.alpha * Ei
        newQuarantined = self.alpha * Ei
        newRecovered = self.gamma * Ii
        self.record.reportEpidemics(newInfected, newConfirmed, newQuarantined, newRecovered)