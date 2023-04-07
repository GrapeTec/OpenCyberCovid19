from Migration import MigrationModel
from datetime import date

migration = MigrationModel(date(2020, 1, 10))
for log in migration.logs :
    print(log.cityFrom, log.cityTo, log.number)