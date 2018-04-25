import json
import csv
import pandas
import numpy
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

beijing_stations = json.load(open('beijing.json'))
london_stations = json.load(open('london.json'))

beijing_data = {}
for station in beijing_stations:
    beijing_data[station] = []

reader = csv.reader(open('beijing_17_18_aq.csv'))
for row in reader:
    if beijing_data.__contains__(row[0]):
        arr = [x and float(x) or 0 for x in row[2:-1]]
        beijing_data[row[0]].append([row[1]] + arr)

data = list(zip(*beijing_data['aotizhongxin_aq']))
# print(list(data[1]))
d = pandas.Series(list(data[1]))
d.index = pandas.Index(sm.tsa.datetools.dates_from_str(data[0]))

fig = plt.figure(figsize=(12, 8))
d.plot()
fig.show()

fig = plt.figure(figsize=(12, 8))
diff1 = d.diff(1)
diff1.plot()
fig.show()

arma = sm.tsa.ARMA(diff1, (1, 0)).fit()


writer = csv.writer(open('submission.csv', 'w'))
writer.writerow(['test_id', 'PM2.5', 'PM10', 'O3'])

for station in beijing_stations:
    for i in range(48):
        writer.writerow([station + '#' + str(i), 0, 0, 0])

for station in london_stations:
    for i in range(48):
        writer.writerow([station + '#' + str(i), 0, 0, 0])
