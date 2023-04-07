from Migration import MigrationModel
from datetime import date, timedelta

def updateSampled(dt, rate) :
    migration = MigrationModel(dt)
    migration.setSampledInfo(True, rate)
    migration.saveLogs()

if __name__ == "__main__" :
    dt = date(2020, 1, 10)
    while dt <= date(2020, 1, 27) :
        updateSampled(dt, 0.0002464)
        dt = dt + timedelta(1)