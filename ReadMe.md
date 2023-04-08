# NOTE: 
All the simulations are made in Chinese cities, so we comments most of the programs in Chinese. If you are not familiar with Chinese, and get interested in our program, please email to: xiaowenlei@buaa.edu.cn. If we get enough requests, we will try to translate the comments into English.
# Authors
Wenlei Xiao (Associate Professor, Beihang University, xiaowenlei@buaa.edu.cn);
Qiang Liu  (Professor, Beihang University, qliusmea@buaa.edu.cn);
Liuquan Wang (PhD candidate, Beihang University);
Ji Huan (Professor, Beihang University);
Pengpeng Sun (PhD candidate, Beihang University);
Chenxin Zang (PhD candidate, Beihang University);
Sanying Zhu (PhD candidate, Beihang University);
Liansheng Gao (Associate Professor, Beihang University)

# 程序说明
## City.py : 城市模块，包含CityModel，用于模拟城市疫情
## Country.py : 国家模块，包含CountryModel，用于模拟国家疫情
## COVID19.py : COVID-19模块，包含COVID-19疫情机理模型Covid19Model和SaturedCovid19Model
## Delay.py : 延迟模块，包含DelayModel，提供延迟环节
## Hospital.py : 医院模块，模拟医院床位的饱和情况
## Incubation.py : 潜伏期模块，模拟病毒的潜伏期
## Migration.py : 迁移模块，模拟城市之间的人口迁移
## Quarantine.py : 隔离模块，模拟隔离疑似感染者的行为
## Record.py : 记录模块，记录仿真过程数据
## Result.py : 结果模块，展示仿真结果
## SARS.py : SARS疫情模型
## SEIR.py : SEIR疫情模型
## Trace.py : 追踪模块，模拟密接追踪的行为
## Virus.py : 病毒模块，病毒的基础数据结构

# Test
## TestCity.py : 城市模拟的测试程序
## TestCOVID19.py : COVID-19模型的测试程序
## TestMigration.py : 迁移模型的测试程序
## TestSARS.py : SARS的测试程序
## TestSaturedCOVID19.py : 饱和COVID-19模型的测试程序
## TestSEIR.py : SEIR模型的测试程序

# Scenario
## Scenario-Wuhan-202001.py : 这是模拟2020年1月武汉疫情的脚本，在脚本之中修改想模拟的城市名（例如：Beijing），直接运行，观察结果即可。

# Data
## city : 城市人口数据
## history : 疫情的历史数据
## hospital : 医院床位数据
## migration : 城市间的迁移人口数据
## trace : 密接追踪参数
## virus：各种病毒的基本参数