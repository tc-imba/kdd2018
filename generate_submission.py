import json
import csv
import pandas
import numpy
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
import datetime

beijing_stations = json.load(open('beijing.json'))
london_stations = json.load(open('london.json'))

beijing_data = {}
for station in beijing_stations:
    beijing_data[station] = []

reader = csv.reader(open('beijing_recent_aq.csv'))
for row in reader:
    if beijing_data.__contains__(row[1]):
        arr = [x and float(x) or 0 for x in row[3:6]]
        beijing_data[row[1]].append([row[2]] + arr)

data = list(zip(*beijing_data['aotizhongxin_aq']))
time_format = '%Y-%m-%d %H:%M:%S'
end_datetime = datetime.datetime.strptime(data[0][-1], time_format)
predict_start = end_datetime #+ datetime.timedelta(hours=1)
predict_end = datetime.datetime.combine(end_datetime.date(), datetime.time.min) \
              + datetime.timedelta(hours=47)

# print(list(data[1]))
d = pandas.Series(list(data[1]))
d.index = pandas.Index(sm.tsa.datetools.dates_from_str(data[0]))
d = d.diff(1)
d = d.fillna(0)
d = d.asfreq('H', method='backfill')

print(d)

# fig = plt.figure(figsize=(12, 8))
# d.plot()
# fig.show()

# fig = plt.figure(figsize=(12, 8))
# diff1 = d.diff(1)
# diff1.plot()
# fig.show()

# print(diff1)
arma = sm.tsa.ARMA(d, (24, 0)).fit()
predict = arma.predict(predict_start, predict_end, dynamic=True)
fig, ax = plt.subplots(figsize=(12, 8))
ax = d.plot(ax=ax)
predict.plot(ax=ax)
fig.show()
print(predict)

writer = csv.writer(open('submission.csv', 'w'))
writer.writerow(['test_id', 'PM2.5', 'PM10', 'O3'])

for station in beijing_stations:
    for i in range(48):
        writer.writerow([station + '#' + str(i), 0, 0, 0])

for station in london_stations:
    for i in range(48):
        writer.writerow([station + '#' + str(i), 0, 0, 0])
